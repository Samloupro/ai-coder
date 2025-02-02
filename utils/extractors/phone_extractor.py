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

def validate_phones(phones, country_code="US"):
    """
    Fonction de compatibilité pour l'ancienne API.
    Valide une liste de numéros de téléphone et retourne un set de numéros valides.
    """
    valid_phones = set()
    for phone in phones:
        if validate_phone(phone, country_code):
            valid_phones.add(phone)
    return valid_phones

def format_phone(parsed_number):
    """
    Formate un numéro parsé en format international E.164 et le rend plus lisible.
    """
    if not parsed_number or not phonenumbers.is_valid_number(parsed_number):
        return None  # Return None for invalid numbers

    # Format the number in E.164
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    
    # Remove leading zeros and non-numeric characters
    formatted_number = ''.join(filter(str.isdigit, formatted_number))
    
    # Unified formatting style: Country Code - Operator Prefix - Local Number
    country_code = formatted_number[:2]  # Get the country code
    operator_prefix = formatted_number[1:4]  # Default operator prefix
    local_number = formatted_number[4:]  # Remaining local number

    # Format the output
    return f"+{country_code} {operator_prefix} {local_number[:2]} {local_number[2:4]} {local_number[4:]}"

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
