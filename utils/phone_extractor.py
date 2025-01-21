import json
import phonenumbers
from phonenumbers import PhoneNumberMatcher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def validate_phones(phones):
    """
    Valide une liste de numéros de téléphone et retourne un set de numéros valides.
    """
    valid_phones = set()
    for phone in phones:
        try:
            parsed_phone = phonenumbers.parse(phone, "US")  # Use the appropriate country code
            if phonenumbers.is_valid_number(parsed_phone):
                valid_phones.add(phone)
        except phonenumbers.NumberParseException:
            continue
    return valid_phones

def extract_phones_html(text):
    """
    Extrait les numéros de téléphone du texte HTML et retourne un set.
    """
    phones = set()
    for match in PhoneNumberMatcher(text, "US"):  # Use the appropriate country code
        phones.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    if phones:
        logging.info(f"Extracted phones from HTML: {phones}")
    return phones

def extract_phones_jsonld(soup):
    """
    Extrait les numéros de téléphone du JSON-LD et retourne un set.
    """
    phones = set()
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if "telephone" in data:
                phone = data["telephone"]
                try:
                    parsed_phone = phonenumbers.parse(phone, "US")  # Use the appropriate country code
                    if phonenumbers.is_valid_number(parsed_phone):
                        phones.add(phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164))
                except phonenumbers.NumberParseException:
                    continue
        except (json.JSONDecodeError, TypeError):
            continue
    if phones:
        logging.info(f"Extracted phones from JSON-LD: {phones}")
    return phones
