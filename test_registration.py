import unittest
from app import app, db, User

class TestRegistration(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for tests
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing headers if needed (not using WTF here yet)
        
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration_page_loads(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create an Account', response.data)

    def test_valid_registration(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            password='Password123',
            confirm_password='Password123'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful! Please login.', response.data)
        
        # Check if user is in DB
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password('Password123'))

    def test_password_mismatch(self):
        response = self.app.post('/register', data=dict(
            username='user2',
            password='password123',
            confirm_password='mismatching'
        ), follow_redirects=True)
        
        self.assertIn(b'Passwords do not match', response.data)
        
        with app.app_context():
            user = User.query.filter_by(username='user2').first()
            self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
