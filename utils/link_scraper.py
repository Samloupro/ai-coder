from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import logging
import json
from utils.link_explorer import extract_links, is_same_domain, normalize_url

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

def extract_links_jsonld(soup, base_url, domain=None):
    """
    Extrait les liens du JSON-LD.
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
                                if not domain or is_same_domain(normalized_url, domain):
                                    links.add(normalized_url)
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Error parsing JSON-LD: {str(e)}")
            continue
    return links

def link_scraper(url, headers, max_link=None):
    """
    Scrape les liens d'une page web.
    """
    if not url or not is_valid_url(url):
        logger.error(f"Invalid URL provided: {url}")
        return [], 'Invalid URL provided.'

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
        
        # Extraire les liens du HTML et du JSON-LD
        html_links = extract_links(soup, url, domain)
        jsonld_links = extract_links_jsonld(soup, url, domain)
        
        # Combiner et filtrer les liens
        all_links = html_links.union(jsonld_links)
        filtered_links = [link for link in all_links if is_valid_url(link)]
        
        # Limiter le nombre de liens si nécessaire
        if max_link and max_link > 0:
            filtered_links = filtered_links[:max_link]
        
        # Log des résultats
        logger.info(f"Found {len(filtered_links)} valid links")
        logger.debug(f"Extracted links: {filtered_links}")
        
        return filtered_links, None
        
    except requests.RequestException as e:
        error_msg = f"Error scraping {url}: {str(e)}"
        logger.error(error_msg)
        return [], error_msg
    except Exception as e:
        error_msg = f"Unexpected error while scraping {url}: {str(e)}"
        logger.error(error_msg)
        return [], error_msg
