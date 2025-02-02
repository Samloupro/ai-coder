import asyncio
from concurrent.futures import ThreadPoolExecutor
from config.settings import WORKERS, logger
from utils.analyzers.link_analyzer import analyze_links
from utils.scrapers.link_scraper import is_valid_url
from utils.extractors.social_links import extract_social_links

def analyze_links_parallel(links, headers, domain):
    """
    Analyse les liens en parallèle en utilisant un pool de threads.
    """
    if not links:
        logger.warning("No links to analyze")
        return []

    valid_links = [link for link in links if is_valid_url(link)]
    if not valid_links:
        logger.warning("No valid links found to analyze")
        return []

    logger.info(f"Starting parallel analysis of {len(valid_links)} links")
    
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Créer les tâches pour chaque lien
        tasks = [
            loop.run_in_executor(executor, analyze_links, link, headers, domain)
            for link in valid_links
        ]
        
        try:
            # Exécuter toutes les tâches en parallèle
            results = loop.run_until_complete(asyncio.gather(*tasks))
            logger.info(f"Successfully analyzed {len(results)} links")
            return results
        except Exception as e:
            logger.error(f"Error in parallel analysis: {str(e)}")
            return []
        finally:
            loop.close()

def process_scraping_results(results, domain_links, all_links, include_emails=True, include_phones=True, include_social_links=True):
    """
    Traite les résultats du scraping et combine les données.
    Args:
        results: Résultats de l'analyse des liens du domaine
        domain_links: Liste des liens du même domaine
        all_links: Liste de tous les liens trouvés (pour l'extraction des réseaux sociaux)
        include_*: Flags pour inclure/exclure certains types de données
    """
    emails = {}
    phones = {}
    visited_links = set(domain_links)  # Initialiser avec les liens du domaine
    social_links = {}
    
    # Log initial state
    logger.info(f"Processing {len(results)} scraping results")
    logger.info(f"Total domain links: {len(domain_links)}")
    logger.info(f"Total all links: {len(all_links)}")
    
    # Traiter chaque résultat
    for result in results:
        if result:
            result_emails, result_phones, result_visited = result
            
            # Ajouter les emails trouvés
            if include_emails and result_emails:
                for email, links in result_emails.items():
                    if email in emails:
                        emails[email].extend(links)
                    else:
                        emails[email] = links
                logger.info(f"Found {len(result_emails)} emails in current result")
            
            # Ajouter les numéros de téléphone trouvés
            if include_phones and result_phones:
                for phone, links in result_phones.items():
                    if phone in phones:
                        phones[phone].extend(links)
                    else:
                        phones[phone] = links
                logger.info(f"Found {len(result_phones)} phones in current result")
    
    # Extraire les liens sociaux de tous les liens trouvés
    if include_social_links and all_links:
        social_links = extract_social_links(all_links)
        logger.info(f"Extracted social links from {len(all_links)} total links")
    
    # Log final results
    logger.info(f"Total unique emails found: {len(emails)}")
    logger.info(f"Total unique phones found: {len(phones)}")
    logger.info(f"Total links visited: {len(visited_links)}")
    
    return emails, phones, social_links, visited_links