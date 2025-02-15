from flask import request, jsonify
from config.settings import MAX_LINKS_DEFAULT, SCRIPT_VERSION, logger
from services.domain_service import get_root_domain
from services.scraper_service import analyze_links_parallel, process_scraping_results
from formatters.response_formatter import format_scraping_response, format_error_response
from utils.scrapers.link_scraper import link_scraper, is_valid_url
from utils.scrapers.user_agent import get_user_agent_headers
import time

def register_routes(app):
    @app.route('/health')
    def health_check():
        """Endpoint pour le healthcheck Coolify"""
        from utils.scrapers.health_checker import get_system_health
        
        health_status = get_system_health()
        
        # Vérifie si le système est en bonne santé
        components = health_status["components"]
        if (components["scraper_service"]["status"] == "unhealthy" or
            components["system"]["memory"]["percent"] > 90 or
            components["system"]["cpu"]["percent"] > 90):
            return "Service Unavailable", 503
            
        # Retourne exactement ce que Coolify attend
        return "OK", 200

    @app.route('/scrape', methods=['GET'])
    def scrape():
        start_time = time.time()
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
            
            # Récupérer les liens du domaine et tous les liens
            domain_links, all_links, error = link_scraper(url, headers, max_link)
            if error:
                logger.error(f"Error scraping links: {error}")
                return jsonify(format_error_response(error)), 500

            root_domain = get_root_domain(url, headers)
            emails, phones, social_links = {}, {}, {}
            visited_links = set()

            if include_unique_links and not (include_emails or include_phones or include_social_links):
                # Si on veut uniquement les liens uniques, pas besoin d'analyse supplémentaire
                valid_links = [link for link in domain_links if is_valid_url(link)]
                visited_links.update(valid_links)
            else:
                if include_emails or include_phones or include_unique_links:
                    # Analyser seulement les liens du domaine pour les emails et téléphones
                    results = analyze_links_parallel(domain_links, headers, root_domain)
                    emails, phones, social_links, visited_links = process_scraping_results(
                        results,
                        domain_links,
                        all_links,  # Passer tous les liens pour l'extraction des réseaux sociaux
                        include_emails,
                        include_phones,
                        include_social_links
                    )

            result = format_scraping_response(
                url=url,
                root_domain=root_domain,
                visited_links=visited_links,
                emails=emails,
                phones=phones,
                social_links=social_links,
                include_emails=include_emails,
                include_phones=include_phones,
                include_social_links=include_social_links,
                include_unique_links=include_unique_links,
                start_time=start_time
            )

            logger.info(f"Completed scraping for URL: {url}")
            return jsonify(result)

        except Exception as e:
            logger.error(f"Unexpected error processing URL {url}: {str(e)}")
            return jsonify(format_error_response(f"An unexpected error occurred: {str(e)}")), 500

    return app