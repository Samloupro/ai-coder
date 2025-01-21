import json
import phonenumbers
from phonenumbers import PhoneNumberMatcher
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@lru_cache(maxsize=100)
def parse_phone(phone_str, country_code="US"):
    """
    Parse un numéro de téléphone avec mise en cache pour éviter les parsing répétés.
    """
    try:
        return phonenumbers.parse(phone_str, country_code)
    except phonenumbers.NumberParseException:
        return None

def validate_phone(phone, country_code="US"):
    """
    Valide un numéro de téléphone de manière optimisée.
    """
    parsed = parse_phone(phone, country_code)
    return parsed and phonenumbers.is_valid_number(parsed)

def format_phone(parsed_number):
    """
    Formate un numéro parsé en format E164.
    """
    return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

def extract_phones_html(text, country_code="US"):
    """
    Extrait les numéros de téléphone du texte HTML avec support de pays configurable.
    """
    phones = set()
    for match in PhoneNumberMatcher(text, country_code):
        phones.add(format_phone(match.number))
    if phones:
        logging.info(f"Extracted phones from HTML: {phones}")
    return phones

def extract_phones_jsonld(soup, country_code="US"):
    """
    Extrait les numéros de téléphone du JSON-LD avec support de pays configurable.
    """
    phones = set()
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if "telephone" in data:
                phone = data["telephone"]
                parsed = parse_phone(phone, country_code)
                if parsed and validate_phone(phone, country_code):
                    phones.add(format_phone(parsed))
        except (json.JSONDecodeError, TypeError):
            continue
    if phones:
        logging.info(f"Extracted phones from JSON-LD: {phones}")
    return phones
