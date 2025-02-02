from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

def is_same_domain(url, domain):
    """
    Vérifie si l'URL appartient au même domaine.
    """
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc.endswith(domain)
    except Exception:
        return False

def normalize_url(url, base_url):
    """
    Normalise une URL en utilisant l'URL de base.
    """
    try:
        # Supprime les fragments (#) et les paramètres de requête (?)
        url = url.split('#')[0].split('?')[0]
        # Normalise l'URL en utilisant l'URL de base
        normalized = urljoin(base_url, url)
        return normalized
    except Exception as e:
        logger.error(f"Error normalizing URL {url}: {str(e)}")
        return None

def extract_links(soup, base_url, domain=None):
    """
    Extrait tous les liens d'une page web.
    Args:
        soup: BeautifulSoup object
        base_url: URL de base pour résoudre les liens relatifs
        domain: Domaine à filtrer (optionnel)
    Returns:
        set: Ensemble des liens uniques trouvés
    """
    links = set()
    try:
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            
            # Ignore les liens vides ou javascript:
            if not href or href.startswith(('javascript:', 'mailto:', 'tel:')):
                continue
                
            # Normalise l'URL
            normalized_url = normalize_url(href, base_url)
            if not normalized_url:
                continue
                
            # Vérifie le domaine si spécifié
            if domain and not is_same_domain(normalized_url, domain):
                continue
                
            links.add(normalized_url)
            
        logger.info(f"Extracted {len(links)} links from {base_url}")
    except Exception as e:
        logger.error(f"Error extracting links from {base_url}: {str(e)}")
    
    return links
