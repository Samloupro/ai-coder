import unittest
from bs4 import BeautifulSoup
from utils.email_extractor import (
    validate_and_normalize_email,
    extract_emails_html,
    extract_emails_jsonld,
    is_valid_tld
)

class TestEmailExtractor(unittest.TestCase):
    def test_validate_and_normalize_email(self):
        # Test des emails valides
        self.assertEqual(
            validate_and_normalize_email("test@example.com"),
            "test@example.com"
        )
        self.assertEqual(
            validate_and_normalize_email("TEST@EXAMPLE.COM"),
            "test@example.com"
        )
        self.assertEqual(
            validate_and_normalize_email("test.email+label@example.com"),
            "test.email+label@example.com"
        )

        # Test des emails invalides
        self.assertIsNone(validate_and_normalize_email("invalid.email"))
        self.assertIsNone(validate_and_normalize_email("test@.com"))
        self.assertIsNone(validate_and_normalize_email("@example.com"))
        
        # Test des TLD invalides
        self.assertIsNone(validate_and_normalize_email("test@example.invalidtld"))
        self.assertIsNone(validate_and_normalize_email("test@example.comextra"))
        self.assertIsNone(validate_and_normalize_email("sales@domain.comcontactreturns"))

    def test_valid_tld(self):
        # Test des TLD valides
        self.assertTrue(is_valid_tld("test@example.com"))
        self.assertTrue(is_valid_tld("test@example.org"))
        self.assertTrue(is_valid_tld("test@example.net"))
        self.assertTrue(is_valid_tld("test@example.io"))
        
        # Test des TLD invalides
        self.assertFalse(is_valid_tld("test@example.invalidtld"))
        self.assertFalse(is_valid_tld("test@example.comextra"))
        self.assertFalse(is_valid_tld("test@example"))

    def test_extract_emails_html(self):
        html_text = """
        Contact us at support@example.com or sales@example.com
        Invalid email: not.an.email
        Another valid email: info@subdomain.example.co.uk
        Test invalid TLD: test@example.invalidtld
        Test concatenated: sales@company.comcontactus
        """
        emails = extract_emails_html(html_text)
        
        # Vérifier les emails valides extraits
        self.assertEqual(len(emails), 3)
        self.assertIn("support@example.com", emails)
        self.assertIn("sales@example.com", emails)
        self.assertIn("info@subdomain.example.co.uk", emails)
        
        # Vérifier que les emails invalides ne sont pas extraits
        self.assertNotIn("test@example.invalidtld", emails)
        self.assertNotIn("sales@company.comcontactus", emails)

    def test_extract_emails_jsonld(self):
        json_ld = """
        <script type="application/ld+json">
        {
            "email": "contact@example.com",
            "nested": {
                "email": "support@example.com"
            },
            "array": [
                {"email": "sales@example.com"},
                {"email": "invalid@example.comextra"},
                {"email": "test@example.invalidtld"}
            ]
        }
        </script>
        """
        soup = BeautifulSoup(json_ld, 'html.parser')
        emails = extract_emails_jsonld(soup)
        
        # Vérifier les emails valides extraits
        self.assertEqual(len(emails), 3)
        self.assertIn("contact@example.com", emails)
        self.assertIn("support@example.com", emails)
        self.assertIn("sales@example.com", emails)
        
        # Vérifier que les emails invalides ne sont pas extraits
        self.assertNotIn("invalid@example.comextra", emails)
        self.assertNotIn("test@example.invalidtld", emails)

if __name__ == '__main__':
    unittest.main()