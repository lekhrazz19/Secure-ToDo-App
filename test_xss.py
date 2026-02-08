import unittest
from app import app, db, User, Todo

class TestXSSProtection(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            user = User(username='hacker')
            user.set_password('pass123')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        self.app.post('/login', data=dict(
            username='hacker',
            password='pass123'
        ), follow_redirects=True)

    def test_xss_injection_attempt(self):
        self.login()
        # Attempt to inject a script
        malicious_script = "<script>alert('XSS')</script>"
        response = self.app.post('/todos', data=dict(
            title=malicious_script,
            description='Harmless description'
        ), follow_redirects=True)
        
        # Check if the script is present but ESCAPED in the response
        # It should NOT be present as raw HTML.
        # Jinja2 converts '<' to '&lt;', etc.
        
        response_text = response.data.decode('utf-8')
        
        # We expect the TEXT to be there (so the user sees what they typed)
        # But we expect the BROWSER to treat it as text, not code.
        # In the raw HTML verify it is escaped.
        self.assertIn("&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;", response_text)
        self.assertNotIn("<script>alert('XSS')</script>", response_text)
        print("\n[SUCCESS] XSS Attempt Blocked: Script tag was escaped.")

if __name__ == '__main__':
    unittest.main()
