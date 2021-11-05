from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb.cursors, re, uuid, hashlib, datetime, os
from flask_babel import Babel, gettext
import smtplib

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
babel = Babel(app)

# add to you main app code
@babel.localeselector
def get_locale():
    if 'language' in session:
        return session['language']
    return 'en'

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# App Settings
app.config['threaded'] = True

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'living_green'

# Enter your email server details below, the following details uses the gmail smtp server (requires gmail account)
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'livingwithtree2021@gmail.com'
app.config['MAIL_PASSWORD'] = '1234!@#$'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Enter your domain name below
app.config['DOMAIN'] = 'http://localhost:5000/'

# Intialize MySQL
mysql = MySQL(app)

# Intialize Mail
mail = Mail(app)

# Enable account activation?
account_activation_required = False

# Enable CSRF Protection?
csrf_protection = False

@app.route("/change-language")
def change_language():
    session['language'] = request.args.get('ln')
    back = request.referrer if request.referrer else '/'
    return redirect(back)

@app.route("/")
def index():
    return redirect('/livinggreen/')




@app.route('/login/', methods=['GET', 'POST'])
def login():
    # if you're logged in you should not be able to see the login page
    if 'loggedin' in session:
        return gettext('You are already logged in')
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
        # Fetch one record and return result
        if result > 0:
            account = cursor.fetchone()
            password1 = account['password']
            if bcrypt.check_password_hash(password1, password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return gettext('You have successfully logged in')
            else:
                msg = gettext('Incorrect password!')
        else:
            msg = gettext('Incorrect Username!')
    return render_template('login.html', msg=msg)

# http://localhost:5000/livinggreen/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/livinggreen/register', methods=['GET', 'POST'])
def register():
	# Redirect user to home page if logged-in
	if loggedin():
		return redirect(url_for('home'))
	# Output message if something goes wrong...
	msg = ''
	# Check if "username", "password" and "email" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'cpassword' in request.form and 'email' in request.form:
		# Create variables for easy access
		username = request.form['username']
		password = request.form['password']
		cpassword = request.form['cpassword']
		email = request.form['email']
		# Hash the password
		hash = password + app.secret_key
		hash = hashlib.sha1(hash.encode())
		hashed_password = hash.hexdigest();
		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
		account = cursor.fetchone()
		# If account exists show error and validation checks
		if account:
			return gettext('Account already exists!')
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			return gettext('Invalid email address!')
		elif not re.match(r'[A-Za-z0-9]+', username):
			return gettext('Username must contain only characters and numbers!')
		elif not username or not password or not cpassword or not email:
			return gettext('Please fill out the form!')
		elif password != cpassword:
			return gettext('Passwords do not match!')
		elif len(username) < 5 or len(username) > 20:
			return gettext('Username must be between 5 and 20 characters long!')
		elif len(password) < 5 or len(password) > 20:
			return gettext('Password must be between 5 and 20 characters long!')
		elif account_activation_required:
			# Account activation enabled
			# Generate a random unique id for activation code
			activation_code = uuid.uuid4()
			cursor.execute('INSERT INTO accounts (username, password, email, activation_code) VALUES (%s, %s, %s, %s)', (username, hashed_password, email, activation_code,))
			mysql.connection.commit()
			# Create new message
			email_info = Message('Account Activation Required', sender = app.config['MAIL_USERNAME'], recipients = [email])
			# Activate Link URL
			activate_link = app.config['DOMAIN'] + url_for('activate', email=email, code=str(activation_code))
			# Define and render the activation email template
			email_info.body = render_template('activation-email-template.html', link=activate_link)
			email_info.html = render_template('activation-email-template.html', link=activate_link)
			# send activation email to user
			mail.send(email_info)
			return gettext('Please check your email to activate your account!')
		else:
			# Account doesnt exists and the form data is valid, now insert new account into accounts table
			cursor.execute('INSERT INTO accounts (username, password, email, activation_code) VALUES (%s, %s, %s, "activated")', (username, hashed_password, email,))
			mysql.connection.commit()
			return gettext('You have successfully registered!')
	elif request.method == 'POST':
		# Form is empty... (no POST data)
		return gettext('Please fill out the form!')
	# Show registration form with message (if any)
	return render_template('register.html', msg=msg)


# Check if logged in function, update session if cookie for "remember me" exists
def loggedin():
	if 'loggedin' in session:
		return True
	elif 'rememberme' in request.cookies:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# check if remembered, cookie has to match the "rememberme" field
		cursor.execute('SELECT * FROM accounts WHERE rememberme = %s', (request.cookies['rememberme'],))
		account = cursor.fetchone()
		if account:
			# update session variables
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			
			return True
	# account not logged in return false
	return False

