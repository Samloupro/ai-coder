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
    Parse a phone number with caching to avoid repeated parsing.
    """
    try:
        return phonenumbers.parse(phone_str, country_code)
    except phonenumbers.NumberParseException:
        return None

def validate_phone(phone, country_code="US"):
    """
    Validates a phone number efficiently.
    """
    parsed = parse_phone(phone, country_code)
    return parsed and phonenumbers.is_valid_number(parsed)

def validate_phones(phones, country_code="US"):
    """
    Compatibility function for the old API.
    Validates a list of phone numbers and returns a set of valid numbers.
    """
    valid_phones = set()
    for phone in phones:
        if validate_phone(phone, country_code):
            valid_phones.add(phone)
    return valid_phones

def format_phone(parsed_number):
    """
    Formats a parsed phone number into the international E.164 format.
    """
    if not parsed_number or not phonenumbers.is_valid_number(parsed_number):
        return None  # Return None for invalid numbers

    # Format the number in E.164
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    return formatted_number

def extract_phones_html(text, country_code="US"):
    """
    Extracts phone numbers from HTML text with configurable country support.
    """
    phones = set()
    for match in PhoneNumberMatcher(text, country_code):
        formatted = format_phone(match.number)
        if formatted:
            phones.add(formatted)
    if phones:
        logging.info(f"Extracted phones from HTML: {phones}")
    return phones

def extract_phones_jsonld(soup, country_code="US"):
    """
    Extracts phone numbers from JSON-LD with configurable country support.
    """
    phones = set()
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                data = [data]  # Ensure it's a list
            for entry in data:
                if "telephone" in entry:
                    phone = entry["telephone"]
                    parsed = parse_phone(phone, country_code)
                    if parsed and validate_phone(phone, country_code):
                        formatted = format_phone(parsed)
                        if formatted:
                            phones.add(formatted)
        except (json.JSONDecodeError, TypeError):
            continue
    if phones:
        logging.info(f"Extracted phones from JSON-LD: {phones}")
    return phones
