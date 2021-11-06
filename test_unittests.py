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
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass
    
    def test_login_page_status(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=True
            )
            self.assertIn(b'Success', response.data)
    
    def test_incorrect_login(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/',
                data=dict(username="Sam", password="Michael", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=True
            )
            self.assertIn(b'Incorrect username/password!', response.data)

    def test_login_with_no_credentials(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/livinggreen/',
                data=dict(username="", password=""),
                follow_redirects=True
            )
            self.assertTrue(b'Please fill out this field.', response.data)

    def test_register_status(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the register page loads correctly
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/register', content_type='html/text')
        self.assertTrue(b'Register' in response.data)

    #Change username/email/password everytime you run tests
    def test_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='zaidz', email='doshiaarsh111@gmail.com',
            password='12345', cpassword='12345'
            ), follow_redirects=True)
            self.assertIn(b'You have successfully registered!', response.data)
    
    def test_incorrect_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/register', data=dict(
            username='John', email='johnrealdoshi.com',
            password='John', cpassword='John'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address!', response.data)    

    def test_other(self):
        tester = app.test_client(self)
        response = tester.get('a', content_type='html/text')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'Not Found' in response.data)

    def test_activate_status(self):
        tester = app.test_client(self)
        response = tester.get('/livinggreen/activate/<string:email>/<string:code>', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_activate_loads(self): #fix this
        tester = app.test_client(self)
        response = tester.get('/livinggreen/activate/<string:email>/<string:code>', content_type='html/text')
        self.assertFalse(b'activate' in response.data)

    def test_home_status(self):
        tester = app.test_client(self)
        # first need to login before testing home page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_home_loads(self):
        tester = app.test_client(self)
        # first need to login before testing home page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/home', content_type='html/text')
        self.assertTrue(b'home' in response.data)

    def test_profile_status(self):
        tester = app.test_client(self)
        # first need to login before testing profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_profile_loads(self):
        tester = app.test_client(self)
        # first need to login before testing profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile', content_type='html/text')
        self.assertTrue(b'profile' in response.data)
        
    def test_edit_profile_status(self):
        tester = app.test_client(self)
        # first need to login before testing edit profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile/edit', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_loads(self):
        tester = app.test_client(self)
        # first need to login before testing edit profile page
        tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
        response = tester.get('/livinggreen/profile/edit', content_type='html/text')
        self.assertTrue(b'Edit Profile' in response.data)

    def test_invalid_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='Doshi', email='Doshilivinggreen.com',
            password='doshi', 
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address!', response.data) 
            #self.assertTrue(b'Edit Profile' in response.data)
            #self.assertFalse(b'Updated!' in response.data)

    
    def test_valid_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='Doshi', email='aarshdoshi11@gmail.com',
            password='doshi', 
            ), follow_redirects=True)
            #self.assertIn(b'Invalid email address!', response.data) 
            self.assertTrue(b'Updated!' in response.data)

    def test_invalid_uername_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='test', email='aarshdoshi11@gmail.com',
            password='doshi', 
            ), follow_redirects=True)
            self.assertTrue(b'Username must be between 5 and 20 characters long!' in response.data)

    def test_invalid_password_edit_profile(self):
        with app.test_client(self):
            tester = app.test_client(self)
            # first need to login before testing edit profile page
            tester.post( 
                '/livinggreen/',
                data=dict(username="Doshi", password="doshi", token="da7c2a09cf8983a1ddea90f94c1a5ce86165b4cc"),
                follow_redirects=False
            )
            response = tester.post('/livinggreen/profile/edit', data=dict(
            username='Doshi', email='aarshdoshi11@gmail.com',
            password='test', 
            ), follow_redirects=True)
            self.assertTrue(b'Password must be between 5 and 20 characters long!' in response.data) 

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
    
    def test_forget_password(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/forgotpassword', data=dict(email='aarshdoshi11@gmail.com'), follow_redirects=True)
            self.assertIn(b'Reset password link has been sent to your email!', response.data)

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
    
    #Change url based on the frontend
    def test_reset_password(self):
        with app.test_client(self):
            response = app.test_client(self).post('/livinggreen/resetpassword/aarshdoshi11%40gmail.com/f3393def-6b6a-4234-8c4d-72971d7d0280', data=dict(npassword='Doshi', cpassword='Doshi'), follow_redirects=True)
            self.assertIn(b'Your password has been reset, you can now', response.data)

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