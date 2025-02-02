import unittest
from .phone_extractor import (
    parse_phone,
    validate_phone,
    extract_phones_html,
    extract_phones_jsonld
)
from bs4 import BeautifulSoup

class TestPhoneExtractor(unittest.TestCase):
    def test_parse_phone_cache(self):
        """Test que le cache fonctionne pour le parsing"""
        # Premier appel - mise en cache
        result1 = parse_phone("+33123456789", "FR")
        # Deuxième appel - devrait utiliser le cache
        result2 = parse_phone("+33123456789", "FR")
        self.assertEqual(result1, result2)

    def test_validate_phone(self):
        """Test la validation des numéros"""
        valid_numbers = [
            ("+33123456789", "FR"),
            ("+14155552671", "US")
        ]
        invalid_numbers = [
            "123",  # Trop court
            "abcdefghijk",  # Non numérique
        ]

        for phone, country in valid_numbers:
            self.assertTrue(validate_phone(phone, country))

        for phone in invalid_numbers:
            self.assertFalse(validate_phone(phone))

    def test_extract_phones_html(self):
        """Test l'extraction depuis le HTML"""
        text = """
        Contactez-nous au +33 1 23 45 67 89
        ou au +1 415 555 2671
        """
        phones_fr = extract_phones_html(text, "FR")
        phones_us = extract_phones_html(text, "US")
        
        self.assertIn("+33123456789", phones_fr)
        self.assertIn("+14155552671", phones_us)

    def test_extract_phones_jsonld(self):
        """Test l'extraction depuis JSON-LD"""
        html = '''
        <script type="application/ld+json">
        {"telephone": "+33123456789"}
        </script>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        phones = extract_phones_jsonld(soup, "FR")
        
        self.assertIn("+33123456789", phones)

if __name__ == '__main__':
    unittest.main()