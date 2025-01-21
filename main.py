import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import uuid
import logging
from urllib.parse import urlparse
from utils.email_extractor import extract_emails_html, extract_emails_jsonld
from utils.phone_extractor import extract_phones_html, extract_phones_jsonld, validate_phones
from utils.social_links import extract_social_links
from utils.link_scraper import link_scraper, extract_links, is_valid_url
from utils.user_agent import get_user_agent_headers
from utils.link_analyzer import analyze_links
import requests

# Configuration from environment variables
WORKERS = int(os.getenv('WORKERS', '4'))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '60'))
MAX_LINKS_DEFAULT = int(os.getenv('MAX_LINKS_DEFAULT', '100'))

app = Flask(__name__)
SCRIPT_VERSION = "V 1.9 / Docker Ready"

# Configuration des logs
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def analyze_links_parallel(links, headers, domain):
    valid_links = [link for link in links if is_valid_url(link)]
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [
            loop.run_in_executor(executor, analyze_links, link, headers, domain)
            for link in valid_links
        ]
        try:
            results = loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            logger.error(f"Error in parallel analysis: {str(e)}")
            results = []
        finally:
            loop.close()
    return results

@app.route('/health')
def health_check():
    """Endpoint pour le healthcheck de Docker"""
    return jsonify({
        "status": "healthy",
        "version": SCRIPT_VERSION
    })

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        headers = get_user_agent_headers()
        include_emails = request.args.get('include_emails', 'true').lower() == 'true'
        include_phones = request.args.get('include_phones', 'true').lower() == 'true'
        include_social_links = request.args.get('include_social_links', 'true').lower() == 'true'
        include_unique_links = request.args.get('include_unique_links', 'true').lower() == 'true'
        
        max_link = request.args.get('max_link')
        max_link = int(max_link) if max_link else MAX_LINKS_DEFAULT

        logger.info(f"Starting scrape for URL: {url} with max_link: {max_link}")
        
        links, error = link_scraper(url, headers, max_link)
        if error:
            logger.error(f"Error scraping links: {error}")
            return jsonify({'error': error}), 500

        domain = urlparse(url).netloc
        emails, phones, visited_links = {}, {}, set()

        if include_unique_links and not (include_emails or include_phones or include_social_links):
            valid_links = [link for link in links if is_valid_url(link)]
            visited_links.update(valid_links)
        else:
            if include_emails or include_phones or include_unique_links:
                results = analyze_links_parallel(links, headers, domain)
                for result in results:
                    if result:  # Vérification que le résultat n'est pas None
                        emails.update(result[0])
                        phones.update(result[1])
                        visited_links.update(result[2])

            social_links = {}
            if include_social_links:
                social_links = extract_social_links(visited_links)

        result = {
            "request_id": str(uuid.uuid4()),
            "domain": domain,
            "query": url,
            "status": "OK",
            "data": [
                {
                    "emails": [{"value": email, "sources": sources} for email, sources in emails.items()] if include_emails else [],
                    "phone_numbers": [{"value": phone, "sources": sources} for phone, sources in phones.items()] if include_phones else [],
                    "social_links": social_links if include_social_links else {},
                    "unique_links": sorted(list(visited_links)) if include_unique_links else []
                }
            ]
        }

        logger.info(f"Completed scraping for URL: {url}")
        return jsonify(result)

    except Exception as e:
        logger.error(f"Unexpected error processing URL {url}: {str(e)}")
        return jsonify({
            'error': f"An unexpected error occurred: {str(e)}",
            'status': 'ERROR'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    logger.info(f"Starting script version: {SCRIPT_VERSION}")
    logger.info(f"Workers: {WORKERS}, Timeout: {REQUEST_TIMEOUT}s, Max Links: {MAX_LINKS_DEFAULT}")
    app.run(host='0.0.0.0', port=port)
