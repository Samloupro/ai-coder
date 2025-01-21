import asyncio
from concurrent.futures import ThreadPoolExecutor
from config.settings import WORKERS, logger
from utils.link_analyzer import analyze_links
from utils.link_scraper import is_valid_url
from utils.social_links import extract_social_links

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

def process_scraping_results(results, include_emails=True, include_phones=True, include_social_links=True):
    emails, phones, visited_links = {}, {}, set()
    
    for result in results:
        if result:
            emails.update(result[0])
            phones.update(result[1])
            visited_links.update(result[2])
    
    social_links = {}
    if include_social_links:
        social_links = extract_social_links(visited_links)
        
    return emails, phones, social_links, visited_links