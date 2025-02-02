from bs4 import BeautifulSoup
import requests
import logging
from urllib.parse import urlparse
from utils.extractors.email_extractor import extract_emails_html, extract_emails_jsonld
from utils.extractors.phone_extractor import extract_phones_html, extract_phones_jsonld, validate_phones

logger = logging.getLogger(__name__)

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def analyze_links(link, headers, domain):
    emails = {}
    phones = {}
    visited_links = set()

    if link in visited_links:
        return emails, phones, visited_links

    logger.info(f"Analyzing link: {link}")
    visited_links.add(link)

    try:
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Utiliser get_text avec separator pour éviter les collages de texte
        html_text = soup.get_text(separator=' ')
        
        # Utiliser l'opération union (|) pour les sets au lieu de l'addition
        emails_found = extract_emails_html(html_text) | extract_emails_jsonld(soup)
        for email in emails_found:
            emails.setdefault(email, []).append(link)

        # Pour les téléphones, vérifier le type de retour de ces fonctions
        phones_found = set(extract_phones_html(html_text)) | set(extract_phones_jsonld(soup))
        for phone in validate_phones(phones_found):
            phones.setdefault(phone, []).append(link)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to process link {link}: {e}")

    return emails, phones, visited_links
