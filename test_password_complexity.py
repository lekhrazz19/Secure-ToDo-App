import unittest
from app import app, db, User

class TestPasswordComplexity(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_short_password(self):
        # Too short (< 8 chars)
        response = self.app.post('/register', data=dict(
            username='user_short',
            email='short@example.com',
            password='Pass1',
            confirm_password='Pass1'
        ), follow_redirects=True)
        self.assertIn(b'Password must be at least 8 characters long', response.data)

    def test_no_number(self):
        # No number
        response = self.app.post('/register', data=dict(
            username='user_nonumber',
            email='nonumber@example.com',
            password='PasswordNoNumber',
            confirm_password='PasswordNoNumber'
        ), follow_redirects=True)
        self.assertIn(b'Password must contain at least one number', response.data)

    def test_no_uppercase(self):
        # No uppercase
        response = self.app.post('/register', data=dict(
            username='user_noupper',
            email='noupper@example.com',
            password='password123',
            confirm_password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Password must contain at least one uppercase letter', response.data)

    def test_strong_password(self):
        # Strong password
        response = self.app.post('/register', data=dict(
            username='user_strong',
            email='strong@example.com',
            password='StrongPassword123',
            confirm_password='StrongPassword123'
        ), follow_redirects=True)
        self.assertIn(b'Registration successful', response.data)

if __name__ == '__main__':
    unittest.main()
