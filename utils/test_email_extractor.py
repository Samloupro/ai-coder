import unittest
from bs4 import BeautifulSoup
from utils.email_extractor import (
    validate_and_normalize_email,
    extract_emails_html,
    extract_emails_jsonld
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

    def test_extract_emails_html(self):
        html_text = """
        Contact us at support@example.com or sales@example.com
        Invalid email: not.an.email
        Another valid email: info@subdomain.example.co.uk
        """
        emails = extract_emails_html(html_text)
        
        self.assertEqual(len(emails), 3)
        self.assertIn("support@example.com", emails)
        self.assertIn("sales@example.com", emails)
        self.assertIn("info@subdomain.example.co.uk", emails)

    def test_extract_emails_jsonld(self):
        json_ld = """
        <script type="application/ld+json">
        {
            "email": "contact@example.com",
            "nested": {
                "email": "support@example.com"
            },
            "array": [
                {"email": "sales@example.com"}
            ]
        }
        </script>
        """
        soup = BeautifulSoup(json_ld, 'html.parser')
        emails = extract_emails_jsonld(soup)
        
        self.assertEqual(len(emails), 3)
        self.assertIn("contact@example.com", emails)
        self.assertIn("support@example.com", emails)
        self.assertIn("sales@example.com", emails)

if __name__ == '__main__':
    unittest.main()