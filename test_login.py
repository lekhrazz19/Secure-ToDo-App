import unittest
from app import app, db, User

class TestLogin(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Create a test user
            user = User(username='testuser')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)
        self.assertIn(b'Welcome, testuser', response.data) # Check base.html update

    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        
        self.assertIn(b'Login unsuccessful', response.data)
        self.assertNotIn(b'Welcome, testuser', response.data)

    def test_logout(self):
        # Login first
        self.app.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        
        # Then logout
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out', response.data)
        self.assertIn(b'Login', response.data) # Should be back on login page (or hav login link)

if __name__ == '__main__':
    unittest.main()
