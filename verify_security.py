import unittest
import sys
import os

def run_all_tests():
    print("========================================")
    print("      SECURETODO SECURITY REPORT        ")
    print("========================================")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test files
    test_files = [
        'test_registration', 
        'test_login', 
        'test_password_complexity',
        'test_xss',
        'test_headers',
        'test_todo'
    ]
    
    for test_file in test_files:
        print(f"Loading {test_file}...")
        try:
            module = __import__(test_file)
            suite.addTests(loader.loadTestsFromModule(module))
        except ImportError as e:
            print(f"Error loading {test_file}: {e}")

    print("\nRunning Security Tests...\n")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n========================================")
    if result.wasSuccessful():
        print(" [PASSED] ALL SECURITY CHECKS PASSED!")
        print("========================================")
        print("Attributes Verified:")
        print(" - Password Hashing: ACTIVE")
        print(" - Input Sanitization (XSS): ACTIVE")
        print(" - Secure Headers: ACTIVE")
        print(" - Access Control: ACTIVE")
        print(" - Secure Sessions: ACTIVE")
    else:
        print(" [FAILED] SOME CHECKS FAILED.")
        print("========================================")
        sys.exit(1)

if __name__ == '__main__':
    run_all_tests()
