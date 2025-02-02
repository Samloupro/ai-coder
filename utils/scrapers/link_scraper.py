from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import logging
import json
from utils.extractors.link_explorer import extract_links, is_same_domain, normalize_url

logger = logging.getLogger(__name__)

def is_valid_url(url):
    """
    Vérifie si l'URL est valide.
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except Exception:
        return False

def extract_links_jsonld(soup, base_url):
    """
    Extrait les liens du JSON-LD sans filtrage par domaine.
    """
    links = set()
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            if script.string:
                data = json.loads(script.string)
                if "sameAs" in data:
                    for link in data["sameAs"]:
                        if link:
                            normalized_url = normalize_url(link, base_url)
                            if normalized_url and is_valid_url(normalized_url):
                                links.add(normalized_url)
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Error parsing JSON-LD: {str(e)}")
            continue
    return links

def link_scraper(url, headers, max_link=None):
    """
    Scrape les liens d'une page web.
    Retourne deux ensembles de liens :
    1. Les liens du même domaine pour l'exploration
    2. Tous les liens valides pour l'extraction des réseaux sociaux
    """
    if not url or not is_valid_url(url):
        logger.error(f"Invalid URL provided: {url}")
        return [], [], 'Invalid URL provided.'

    try:
        # Extraire le domaine de l'URL
        domain = urlparse(url).netloc
        
        # Faire la requête HTTP
        logger.info(f"Requesting URL: {url}")
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        
        # Log de la réponse
        logger.info(f"Response status: {response.status_code}")
        if response.status_code == 200:
            logger.info("HTML fetch successful")
            
        # Parser le HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraire tous les liens sans filtrage de domaine
        all_links = extract_links(soup, url)
        jsonld_links = extract_links_jsonld(soup, url)
        all_links.update(jsonld_links)
        
        # Filtrer les liens par domaine pour l'exploration
        domain_links = {link for link in all_links if is_same_domain(link, domain)}
        
        # Convertir en liste et positionner l'URL racine en premier
        domain_links = [url] + [link for link in domain_links if link != url]
        
        # Limiter le nombre de liens si nécessaire
        if max_link and max_link > 0:
            domain_links = domain_links[:max_link]
        
        # Log des résultats
        logger.info(f"Found {len(domain_links)} domain links and {len(all_links)} total links")
        logger.debug(f"Domain links: {domain_links}")
        logger.debug(f"All links: {all_links}")
        
        return list(domain_links), list(all_links), None
        
    except requests.RequestException as e:
        error_msg = f"Error scraping {url}: {str(e)}"
        logger.error(error_msg)
        return [], [], error_msg
    except Exception as e:
        error_msg = f"Unexpected error while scraping {url}: {str(e)}"
        logger.error(error_msg)
        return [], [], error_msg
