import re
import json
import logging
from email_validator import validate_email, EmailNotValidError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_and_normalize_email(email: str) -> str | None:
    """
    Valide et normalise une adresse email.
    Ne vérifie que la syntaxe, pas le DNS.
    """
    try:
        valid = validate_email(
            email.strip().rstrip('.').lower(),
            check_deliverability=False,
            test_environment=True
        )
        return valid.normalized.lower()
    except EmailNotValidError:
        return None

def extract_emails_html(text: str) -> set[str]:
    """
    Extrait les emails du texte HTML.
    """
    email_pattern = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
    
    emails = set()
    potential_emails = re.findall(email_pattern, text, re.IGNORECASE)
    
    for email in potential_emails:
        normalized_email = validate_and_normalize_email(email)
        if normalized_email:
            emails.add(normalized_email)
            logger.info(f"Email extrait : {normalized_email}")
    
    return emails

def extract_emails_from_json(data) -> set[str]:
    """
    Extrait récursivement les emails des données JSON.
    """
    emails = set()
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() == "email" and isinstance(value, str):
                normalized_email = validate_and_normalize_email(value)
                if normalized_email:
                    emails.add(normalized_email)
            elif isinstance(value, (dict, list)):
                emails.update(extract_emails_from_json(value))
    elif isinstance(data, list):
        for item in data:
            emails.update(extract_emails_from_json(item))
            
    return emails

def extract_emails_jsonld(soup) -> set[str]:
    """
    Extrait les emails des balises script JSON-LD.
    """
    emails = set()
    scripts = soup.find_all("script", type="application/ld+json")
    
    for script in scripts:
        try:
            data = json.loads(script.string)
            emails.update(extract_emails_from_json(data))
        except (json.JSONDecodeError, TypeError, Exception):
            continue
    
    return emails
