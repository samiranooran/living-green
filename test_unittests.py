from typing import Reversible
import unittest   # The test framework
#from flask_login import current_user

from main import app
class BasicTestCase(unittest.TestCase):

    def setUp(self):
        # Setup run before every test method.
        tester = app.test_client(self)
        tester.post(
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass
    
    #test01
    def test_register_status(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test02
    # Ensure that the register page loads correctly
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/register', content_type='html/text')
        self.assertTrue(b'Register' in response.data)

    #test03
    #Change username/email/password everytime you run tests
    def test_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='zaidzaid', email='livingwithtree2021@gmail.com',
            password='123456', cpassword='123456'
            ), follow_redirects=True)
            self.assertIn(b'You have successfully registered!', response.data)

    #test04
    def test_duplicate_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='zaidz', email='livingwithtree2021@gmail.com',
            password='12345', cpassword='12345'
            ), follow_redirects=True)
            self.assertIn(b'Account already exists!', response.data)
    
    #test05
    def test_incorrect_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='John', email='johnrealpython.com',
            password='John', cpassword='John'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address!', response.data) 

    #test06
    def test__registeration_username_Check(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='Pardis!@', email='livingwithtree2021@gmail.com',
            password='12345', cpassword='12345'
            ), follow_redirects=True)
            self.assertIn(b'Username must contain letters, numbers, underscores and dashes only', response.data)   

    #test07
    def test_register_with_no_credentials(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/register',
                data=dict(username="", password="", cpassword="", email='livingwithtree2021@gmail.com'),
                follow_redirects=True
            )
            self.assertTrue(b'Please fill out the form!', response.data)

    #test08
    def test_notmatch_password_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='PardisF', email='livingwithtree.2021@gmail.com',
            password='12345', cpassword='123456'
            ), follow_redirects=True)
            self.assertIn(b'Passwords do not match!', response.data)

    #test09
    def test_login_page_status(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #test10
    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    #test11
    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=True
            )
            self.assertIn(b'Success', response.data)
    
    #test12
    def test_incorrect_login(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/',
                data=dict(username="Sam", password="Michael", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=True
            )
            self.assertIn(b'Incorrect username/password!', response.data)

    #test13
    def test_login_with_no_credentials(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/',
                data=dict(username="", password=""),
                follow_redirects=True
            )
            self.assertTrue(b'Please fill out this field.', response.data)

    #test14
    def test_other(self):
        tester = app.test_client(self)
        response = tester.get('a', content_type='html/text')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'Not Found' in response.data)

    #test15
    def test_activate_status(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/activate/<string:email>/<string:code>', content_type='html/text')
        self.assertEqual(response.status_code, 500)

    #test16
    def test_activate_loads(self): 
        tester = app.test_client(self)
        response = tester.get('/livinggreen/activate/<string:email>/<string:code>', content_type='html/text')
        self.assertFalse(b'activate' in response.data)

    #test17
    def test_home_status(self):
        tester = app.test_client(self)
        # first need to login before testing home page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test18
    def test_home_loads(self):
        tester = app.test_client(self)
        # first need to login before testing home page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertTrue(b'home' in response.data)

    #test19
    def test_home_chart(self):
        tester = app.test_client(self)
        # first need to login before testing home page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertTrue(b'Your waste details are below:' in response.data)

    #test20
    def test_home_chart_details(self):
        tester = app.test_client(self)
        # first need to login before testing home page charts
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=True
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertFalse(b'Recyclables:	20 tons' in response.data) ### need to fix

    #test21
    def test_home_email_details(self):
        tester = app.test_client(self)
        # first need to login before testing home page charts
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=True
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertTrue(b'Email:' in response.data) 

    #test22
    def test_grabage_amount(self):
        tester = app.test_client(self)
        # first need to login before testing home page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertIn(b'Recyclables:	20 tons', response.data) ### need to fix

    #test23
    def test_progressbar_load(self):
        tester = app.test_client(self)
        # first need to login before testing profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertTrue(b'progress' in response.data)

    #test24
    def test_profile_status(self):
        tester = app.test_client(self)
        # first need to login before testing profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test25
    def test_profile_loads(self):
        tester = app.test_client(self)
        # first need to login before testing profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile', content_type='html/text')
        self.assertTrue(b'profile' in response.data)
        
    #test26
    def test_edit_profile_status(self):
        tester = app.test_client(self)
        # first need to login before testing edit profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile/edit', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test27
    def test_edit_profile_loads(self):
        tester = app.test_client(self)
        # first need to login before testing edit profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile/edit', content_type='html/text')
        self.assertTrue(b'Edit Profile' in response.data)

    #test28
    def test_invalid_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='test01', email='livingwithtree2021gamil.com',
            password='test01', 
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address!', response.data) 

    #test29
    def test_no_credentials_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username="", email='livingwithtree2021@gmail.com',
            password="", 
            ), follow_redirects=True)
            self.assertIn(b'Username must contain only characters and numbers!', response.data)
            

    #test30
    def test_valid_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='test03', email='livingwithtree2021@gmail.com',
            password='test03', 
            ), follow_redirects=True)
            # need to make sure after each valid edit profile goes back to the default username and password
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='test01', email='livingwithtree2021@gmail.com',
            password='test01', 
            ), follow_redirects=True)
            self.assertTrue(b'Updated!' in response.data)

    #test31
    def test_invalid_uername_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='test', email='livingwithtree2021@gmail.com',
            password='test01', 
            ), follow_redirects=True)
            self.assertTrue(b'Username must be between 5 and 20 characters long!' in response.data)

    #test32
    def test_invalid_password_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="test01", password="test01", token="9a10f5bd76ee98061b8b107492219a4c5fb5b469"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='test01', email='livingwithtree2021@gmail.com',
            password='test', 
            ), follow_redirects=True)
            self.assertTrue(b'Password must be between 5 and 20 characters long!' in response.data) 

    #test33
    def test_forget_password_status(self):
        tester = app.test_client(self)
        # first need to login before testing forget password page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/forgotpassword', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #test34
    def test_forget_password_loads(self):
        tester = app.test_client(self)
        # first need to login before testing forget password page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/forgotpassword', content_type='html/text')
        self.assertTrue(b'Forgot Password' in response.data)
    
    #test35
    def test_forget_password(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/forgotpassword', data=dict(email='livingwithtree2021@gmail.com'), follow_redirects=True)
            self.assertIn(b'Reset password link has been sent to your email!', response.data)

    #test36
    def test_reset_password_status(self):
        tester = app.test_client(self)
        # first need to login before testing reset password page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/resetpassword/<string:email>/<string:code>', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    
    #test37
    #Change url based on the frontend
    def test_reset_password_loads(self):
        tester = app.test_client(self)
        # first need to login before testing reset password page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/resetpassword/aarshdoshi11%40gmail.com/f1a6c219-1963-4593-b9d3-a2a42e0a0215', content_type='html/text')
        self.assertIn(b'Submit', response.data)
    
    #test38
    #Change url based on the frontend
    def test_reset_password(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/resetpassword/aarshdoshi11%40gmail.com/f3393def-6b6a-4234-8c4d-72971d7d0280', data=dict(npassword='Doshi', cpassword='Doshi'), follow_redirects=True)
            self.assertIn(b'Your password has been reset, you can now', response.data)

    #test39
    def test_logout_status(self):
        tester = app.test_client(self)
        # first need to login before testing logout page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/logout', content_type='html/text')
        self.assertEqual(response.status_code, 302) 

    #test40
    def test_logout_loads(self):
        tester = app.test_client(self)
        # first need to login before testing logout page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
            #when logging out, application redirects to login page, so follow redirect = true, and test for Login title
        response = tester.get('/livinggreen/logout', content_type='html/text',follow_redirects=True )
        self.assertTrue(b'Login' in response.data)

if __name__ == '__main__':
    unittest.main()