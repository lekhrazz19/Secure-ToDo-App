import unittest
from app import app, db, User

class TestRegistrationValues(unittest.TestCase):
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

    def test_print_registration_response(self):
        print("\n--- DEBUGGING REGISTRATION RESPONSE ---")
        response = self.app.post('/register', data=dict(
            username='debuguser',
            password='Password123',
            confirm_password='Password123'
        ), follow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        print("Response Data (excerpt):")
        print(response.data.decode('utf-8'))
        print("---------------------------------------")

if __name__ == '__main__':
    unittest.main()
