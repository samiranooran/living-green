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
app.config['MYSQL_PASSWORD'] = '8288'
app.config['MYSQL_DB'] = 'pythonlogin'

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

# http://localhost:5000/livinggreen/ - this will be the login page, we need to use both GET and POST requests
@app.route('/livinggreen/', methods=['GET', 'POST'])
def login():
	# Redirect user to home page if logged-in
	if loggedin():
		return redirect(url_for('home'))
	# Output message if something goes wrong...
	msg = ''
	# Check if "username" and "password" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'token' in request.form:
		# Create variables for easy access
		username = request.form['username']
		password = request.form['password']
		token = request.form['token']
		# Retrieve the hashed password
		hash = password + app.secret_key
		hash = hashlib.sha1(hash.encode())
		password = hash.hexdigest();
		# Check if account exists using MySQL
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
		# Fetch one record and return result
		account = cursor.fetchone()
		# If account exists in accounts table in out database
		if account:
			if account_activation_required and account['activation_code'] != 'activated' and account['activation_code'] != '':
				return gettext('Please activate your account to login!')
			if csrf_protection and str(token) != str(session['token']):
				return gettext('Invalid token!')
			# Create session data, we can access this data in other routes
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			
			if 'rememberme' in request.form:
				# Create hash to store as cookie
				hash = account['username'] + request.form['password'] + app.secret_key
				hash = hashlib.sha1(hash.encode())
				hash = hash.hexdigest();
				# the cookie expires in 90 days
				expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
				resp = make_response('Success', 200)
				resp.set_cookie('rememberme', hash, expires=expire_date)
				# Update rememberme in accounts table to the cookie hash
				cursor.execute('UPDATE accounts SET rememberme = %s WHERE id = %s', (hash, account['id'],))
				mysql.connection.commit()
				return resp
			return 'Success'
		else:
			# Account doesnt exist or username/password incorrect
			return gettext('Incorrect username/password!')
	# Generate random token that will prevent CSRF attacks
	token = uuid.uuid4()
	session['token'] = token
	# Show the login form with message (if any)
	return render_template('index.html', msg=msg, token=token)

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
		elif not re.match(r'^[A-Za-z0-9_-]*$', username):
			return gettext('Username must contain letters, numbers, underscores and dashes only')
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

# http://localhost:5000/livinggreen/activate/<email>/<code> - this page will activate a users account if the correct activation code and email are provided
@app.route('/livinggreen/activate/<string:email>/<string:code>', methods=['GET'])
def activate(email, code):
	msg = gettext('Account doesn\'t exist with that email or the activation code is incorrect!')
	# Check if the email and code provided exist in the accounts table
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT * FROM accounts WHERE email = %s AND activation_code = %s', (email, code,))
	account = cursor.fetchone()
	if account:
		# account exists, update the activation code to "activated"
		cursor.execute('UPDATE accounts SET activation_code = "activated" WHERE email = %s AND activation_code = %s', (email, code,))
		mysql.connection.commit()
		# automatically log the user in and redirect to the home page
		session['loggedin'] = True
		session['id'] = account['id']
		session['username'] = account['username']
		
		return redirect(url_for('home'))
	return render_template('activate.html', msg=msg)

# http://localhost:5000/livinggreen/home - this will be the home page, only accessible for loggedin users
@app.route('/livinggreen/home')
def home():
	# Check if user is loggedin
	if loggedin():
		# User is loggedin show them the home page
		#if request.method == 'POST' and 'email' in request.form:
		#	email = request.form['email']
		#	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		#	cursor.execute('SELECT * FROM users WHERE emailid = %s', (email,))
		#	val = cursor.fetchone()
		# We need all the account info for the user so we can display it on the profile page
		#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		#if request.method == 'POST':
		#	global value
		#	email = request.form['email']
		#	cursor.execute('SELECT * FROM users WHERE emailid = %s', (email,))
		#	value = cursor.fetchone()
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
		account = cursor.fetchone()

		cursor.execute('SELECT * FROM users WHERE emailid = %s', (account['email'],))
		val = cursor.fetchone()
		return render_template('home.html', val=val, account=account)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

# http://localhost:5000/livinggreen/profile - this will be the profile page, only accessible for loggedin users
@app.route('/livinggreen/profile')
def profile():
	# Check if user is loggedin
	if loggedin():
		# We need all the account info for the user so we can display it on the profile page
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
		account = cursor.fetchone()
		# Show the profile page with account info
		return render_template('profile.html', account=account)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))

# http://localhost:5000/livinggreen/profile/edit - user can edit their existing details
@app.route('/livinggreen/profile/edit', methods=['GET', 'POST'])
def edit_profile():
	# Check if user is loggedin
	if loggedin():
		# We need all the account info for the user so we can display it on the profile page
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# Output message
		msg = ''
		# Check if "username", "password" and "email" POST requests exist (user submitted form)
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
			# Create variables for easy access
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			# Retrieve account by the username
			cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
			account = cursor.fetchone()
			# validation check
			if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = gettext('Invalid email address!')
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = gettext('Username must contain only characters and numbers!')
			elif not username or not email:
				msg = gettext('Please fill out the form!')
			elif session['username'] != username and account:
				msg = gettext('Username already exists!')
			elif len(username) < 5 or len(username) > 20:
				return gettext('Username must be between 5 and 20 characters long!')
			elif len(password) < 5 or len(password) > 20:
				return gettext('Password must be between 5 and 20 characters long!')
			else:
				cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
				account = cursor.fetchone()
				current_password = account['password']
				if password:
					# Hash the password
					hash = password + app.secret_key
					hash = hashlib.sha1(hash.encode())
					current_password = hash.hexdigest();
				# update account with the new details
				cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s WHERE id = %s', (username, current_password, email, session['id'],))
				mysql.connection.commit()
				msg = gettext('Updated!')
		cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
		account = cursor.fetchone()
		# Show the profile page with account info
		return render_template('profile-edit.html', account=account, msg=msg)
	return redirect(url_for('login'))

# http://localhost:5000/livinggreen/forgotpassword - user can use this page if they have forgotten their password
@app.route('/livinggreen/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
	msg = ''
	if request.method == 'POST' and 'email' in request.form:
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
		account = cursor.fetchone()
		if account:
			# Generate unique ID
			reset_code = uuid.uuid4()
			# Update the reset column in the accounts table to reflect the generated ID
			cursor.execute('UPDATE accounts SET reset = %s WHERE email = %s', (reset_code, email,))
			mysql.connection.commit()
			# Change your_email@gmail.com
			email_info = Message('Password Reset', sender = app.config['MAIL_USERNAME'], recipients = [email])
			# Generate reset password link
			reset_link = app.config['DOMAIN'] + url_for('resetpassword', email = email, code = str(reset_code))
			# change the email body below
			email_info.body = 'Please click the following link to reset your password: ' + str(reset_link)
			email_info.html = '<p>Please click the following link to reset your password: <a href="' + str(reset_link) + '">' + str(reset_link) + '</a></p>'
			mail.send(email_info)
			msg = gettext('Reset password link has been sent to your email!')
		else:
			msg = gettext('An account with that email does not exist!')
	return render_template('forgotpassword.html', msg=msg)

# http://localhost:5000/livinggreen/resetpassword/EMAIL/CODE - proceed to reset the user's password
@app.route('/livinggreen/resetpassword/<string:email>/<string:code>', methods=['GET', 'POST'])
def resetpassword(email, code):
	msg = ''
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# Retrieve the account with the email and reset code provided from the GET request
	cursor.execute('SELECT * FROM accounts WHERE email = %s AND reset = %s', (email, code,))
	account = cursor.fetchone()
	# If account exists
	if account:
		# Check if the new password fields were submitted
		if request.method == 'POST' and 'npassword' in request.form and 'cpassword' in request.form:
			npassword = request.form['npassword']
			cpassword = request.form['cpassword']
			# Password fields must match
			if npassword == cpassword and npassword != "":
				# Hash new password
				hash = npassword + app.secret_key
				hash = hashlib.sha1(hash.encode())
				npassword = hash.hexdigest();
				# Update the user's password
				cursor.execute('UPDATE accounts SET password = %s, reset = "" WHERE email = %s', (npassword, email,))
				mysql.connection.commit()
				msg = gettext('Your password has been reset, you can now <a href="') + url_for('login') + '">login</a>!'
			else:
				msg = gettext('Passwords must match and must not be empty!')
		return render_template('resetpassword.html', msg=msg, email=email, code=code)
	return gettext('Invalid email and/or code!')

# http://localhost:5000/livinggreen/logout - this will be the logout page
@app.route('/livinggreen/logout')
def logout():
	# Remove session data, this will log the user out
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	
	# Remove cookie data "remember me"
	resp = make_response(redirect(url_for('login')))
	resp.set_cookie('rememberme', expires=0)
	return resp

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


if __name__ == '__main__':
	app.debug = True
	app.run()
