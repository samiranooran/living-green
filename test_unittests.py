import unittest   # The test framework
from flask_login import current_user

from main import app
class BasicTestCase(unittest.TestCase):
    def test_login_page_status(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login/', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/login/',
                data=dict(username="par", password="par"),
                follow_redirects=True
            )
            self.assertIn(b'You have successfully logged in', response.data)
    
    def test_incorrect_login(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/login/',
                data=dict(username="par", password="Michael"),
                follow_redirects=True
            )
            self.assertIn(b'Incorrect password!', response.data)


    def test_login_with_no_credentials(self):
        with app.test_client(self):
            response = app.test_client(self).post(
                '/login/',
                data=dict(username="", password=""),
                follow_redirects=True
            )
            self.assertTrue(b'Please fill out this field.', response.data)



    def test_register_status(self):
        tester = app.test_client(self)
        response = tester.get('/register/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the register page loads correctly
    def test_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/register/', content_type='html/text')
        self.assertTrue(b'Register' in response.data)

    #Change username/email/password everytime you run tests
    def test_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/register/', data=dict(
            username='feiz', email='feiz@realpython.com',
            password='1234'
            ), follow_redirects=True)
            self.assertIn(b'You have successfully registered!', response.data)
    
    def test_incorrect_user_registeration(self):
        with app.test_client(self):
            response = app.test_client(self).post('/register/', data=dict(
            username='John', email='johnrealpython.com',
            password='John'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address!', response.data)    
    


    def test_other(self):
        tester = app.test_client(self)
        response = tester.get('a', content_type='html/text')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b'Not Found' in response.data)

if __name__ == '__main__':
    unittest.main()