import re
import json
import logging
from email_validator import validate_email, EmailNotValidError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Liste des TLD valides (extrait des plus communs, à compléter si nécessaire)
VALID_TLDS = {
    # Generic TLDs
    'com', 'org', 'net', 'edu', 'gov', 'mil', 'int',
    # Business and Professional
    'biz', 'info', 'name', 'pro',
    # Country Code TLDs
    'uk', 'us', 'ca', 'au', 'de', 'fr', 'it', 'es', 'nl', 'be', 'ch', 'at',
    'dk', 'no', 'se', 'fi', 'ie', 'nz', 'jp', 'cn', 'kr', 'ru', 'br', 'mx',
    # New gTLDs
    'io', 'co', 'ai', 'app', 'dev', 'cloud', 'online', 'store', 'shop',
    'tech', 'digital', 'agency', 'business', 'company', 'network', 'systems',
    'solutions', 'services', 'media', 'marketing', 'consulting', 'design',
    'software', 'technology'
}

def is_valid_tld(email: str) -> bool:
    """
    Vérifie si le TLD de l'email est valide.
    """
    try:
        domain = email.split('@')[1]
        tld = domain.split('.')[-1].lower()
        return tld in VALID_TLDS
    except IndexError:
        return False

def validate_and_normalize_email(email: str) -> str | None:
    """
    Valide et normalise une adresse email.
    Vérifie la syntaxe et le TLD.
    """
    try:
        # Nettoyage initial
        email = email.strip().rstrip('.').lower()
        
        # Vérification du TLD
        if not is_valid_tld(email):
            return None
            
        # Validation complète
        valid = validate_email(
            email,
            check_deliverability=False,
            test_environment=True
        )
        return valid.normalized.lower()
    except EmailNotValidError:
        return None

def extract_emails_html(html_content: str) -> set[str]:
    """
    Extrait les emails du texte HTML avec une validation stricte.
    """
    # Pattern plus strict pour les emails
    email_pattern = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
    
    emails = set()
    potential_emails = re.findall(email_pattern, html_content, re.IGNORECASE)
    
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
