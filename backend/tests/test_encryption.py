import unittest
import os
import sys

# Add backend directory to path to allow direct imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import encrypt_data, decrypt_data
from agents.security import SecurityAgent

class TestVibeCodeSecurity(unittest.TestCase):
    
    def setUp(self):
        self.passphrase = "master_secret_123"
        self.wrong_passphrase = "wrong_secret_456"
        self.test_data = "Student Profile: Moniii | Grade: College Junior | Notes: Passed DSA!"
        self.security_agent = SecurityAgent()

    def test_cryptographic_encryption_decryption(self):
        """Verify that AES-256-GCM encrypts and decrypts correctly with the correct key."""
        # Encrypt
        encrypted = encrypt_data(self.passphrase, self.test_data)
        self.assertNotEqual(self.test_data, encrypted)
        self.assertTrue(len(encrypted) > 28) # must contain salt + nonce + payload
        
        # Decrypt with correct key
        decrypted = decrypt_data(self.passphrase, encrypted)
        self.assertEqual(self.test_data, decrypted)

    def test_cryptographic_decryption_failure(self):
        """Verify that AES-256-GCM raises a ValueError when decrypted with an incorrect key."""
        encrypted = encrypt_data(self.passphrase, self.test_data)
        
        # Try to decrypt with wrong key, must fail with ValueError
        with self.assertRaises(ValueError):
            decrypt_data(self.wrong_passphrase, encrypted)

    def test_pii_sanitization_and_restoration(self):
        """Verify that the Security Agent redacts PII and restores it correctly."""
        raw_prompt = "Hi, my name is Moniii (id: 9876543) working on Homework #2. Email: moni@college.edu"
        
        # Sanitize
        sanitized, mapping = self.security_agent.sanitize(raw_prompt)
        
        # Assert that sensitive data is removed
        self.assertNotIn("Moniii", sanitized)
        self.assertNotIn("9876543", sanitized)
        self.assertNotIn("moni@college.edu", sanitized)
        self.assertNotIn("Homework #2", sanitized)
        
        # Assert that placeholders are injected
        self.assertIn("[REDACTED_STUDENT_", sanitized)
        self.assertIn("[REDACTED_ID_", sanitized)
        self.assertIn("[REDACTED_EMAIL_", sanitized)
        self.assertIn("[REDACTED_ASSIGNMENT_", sanitized)
        
        # Simulate LLM response containing placeholders
        simulated_response = "Hello [REDACTED_STUDENT_4], I have checked your [REDACTED_ASSIGNMENT_3]..."
        
        # Restore PII
        restored = self.security_agent.restore(simulated_response, mapping)
        
        # Assert that PII is restored accurately
        self.assertIn("Moniii", restored)
        self.assertIn("Homework #2", restored)
        self.assertNotIn("[REDACTED_STUDENT_", restored)

if __name__ == "__main__":
    unittest.main()
