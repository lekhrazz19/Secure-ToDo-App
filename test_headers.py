import unittest
from app import app

class TestSecurityHeaders(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_headers_present(self):
        response = self.app.get('/')
        headers = response.headers
        
        self.assertEqual(headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')
        print("[SUCCESS] Security headers are present.")

if __name__ == '__main__':
    unittest.main()
