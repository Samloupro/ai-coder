import requests
from urllib.parse import urlparse
from config.settings import REQUEST_TIMEOUT, logger

def get_root_domain(url, headers):
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=REQUEST_TIMEOUT)
        final_url = response.url
        return urlparse(final_url).netloc
    except Exception as e:
        logger.error(f"Error getting root domain for {url}: {str(e)}")
        return urlparse(url).netloc