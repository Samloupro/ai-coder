# Contact Scraper

Application de scraping pour extraire les contacts, emails, numéros de téléphone et liens sociaux des sites web.

## File Structure
```
.
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
├── api/
│   ├── __init__.py
│   └── routes.py
├── config/
│   └── settings.py
├── formatters/
│   └── response_formatter.py
├── services/
│   ├── __init__.py
│   ├── domain_service.py
│   └── scraper_service.py
└── utils/
    ├── __init__.py
    ├── email_extractor.py
    ├── health_checker.py
    ├── link_analyzer.py
    ├── link_classifier.py
    ├── link_explorer.py
    ├── link_scraper.py
    ├── phone_extractor.py
    ├── README.md
    ├── social_links.py
    ├── test_email_extractor.py
    ├── test_link_classifier.py
    ├── test_phone_extractor.py
    ├── test_social_links.py
    └── user_agent.py
```

## Dockerization
This application is Dockerized, allowing for easy deployment and management in containerized environments. To run the application using Docker, follow the instructions below.

### Configuration Docker

1. **Prérequis**:
   - Docker
   - Docker Compose

2. **Variables d'Environnement**:
   Les variables suivantes peuvent être configurées via le fichier `.env` ou dans l'interface Coolify :
   ```env
   # Service
   SERVICE_NAME=contact-scraper    # Nom du service
   PORT=5000                       # Port d'exposition

   # Performance
   WORKERS=4                       # Nombre de workers Gunicorn
   TIMEOUT=300                     # Timeout Gunicorn (secondes)
   REQUEST_TIMEOUT=60              # Timeout des requêtes (secondes)
   MAX_LINKS_DEFAULT=100          # Nombre maximum de liens à analyser

   # Ressources
   MEMORY_LIMIT=512M              # Limite de mémoire
   MEMORY_RESERVE=256M            # Réservation de mémoire
   CPU_LIMIT=0.5                  # Limite CPU (50%)
   CPU_RESERVE=0.25               # Réservation CPU (25%)

   # Logs
   LOG_LEVEL=INFO                 # Niveau de log (DEBUG, INFO, WARNING, ERROR)
   ```

3. **Développement Local**:
   - Cloner le repository :
   ```bash
   git clone [votre-repo]
   cd contact-scraper
   ```

   - Créer le fichier `.env` avec vos configurations.

   - Lancer l'application avec Docker Compose :
   ```bash
   docker-compose up --build
   ```

   L'application sera accessible sur `http://localhost:5000`.

# Application Architecture Overview

## Entry Point
- **main.py**: The entry point of the application, initializing a Flask app and registering routes.

## API Routes
- **/health**: Health check endpoint to monitor system status.
- **/scrape**: Endpoint to initiate scraping for a given URL, with various query parameters to customize the scraping behavior.

## Configuration
- **config/settings.py**: Contains configuration settings sourced from environment variables, including:
  - `WORKERS`: Number of worker threads (default: 4).
  - `REQUEST_TIMEOUT`: Timeout duration for requests (default: 60 seconds).
  - `MAX_LINKS_DEFAULT`: Maximum number of links to scrape (default: 100).
  - `SCRIPT_VERSION`: Version of the script.

## Services
- **services/domain_service.py**: Provides functionality to retrieve the root domain from a URL.
- **services/scraper_service.py**: Contains functions for analyzing links in parallel and processing scraping results.

## Utilities
- **utils/link_scraper.py**: Contains functions for validating URLs, extracting links from HTML, and scraping links from a web page.
- **utils/social_links.py**: Extracts social media links from a list of unique links using regex patterns.

## Logging
The application uses logging to track important events and errors throughout the scraping process.

## Usage Examples

### Health Check
To check the health of the application, send a GET request to `/health`:
```
GET /health
```
**Expected Response**:
```
HTTP/1.1 200 OK
```

### Scraping
To scrape a URL, send a GET request to `/scrape` with the required parameters:
```
GET /scrape?url=https://example.com&include_emails=true&include_phones=true&include_social_links=true&max_link=100
```
**Expected Response**:
```json
{
  "url": "https://example.com",
  "root_domain": "example.com",
  "visited_links": ["https://example.com/page1", "https://example.com/page2"],
  "emails": {"example@example.com": ["https://example.com/contact"]},
  "phones": {"+123456789": ["https://example.com/contact"]},
  "social_links": {
    "facebook": "https://facebook.com/example",
    "twitter": "https://twitter.com/example"
  }
}
```

## Summary
The application is structured to provide a robust scraping service, with clear separation of concerns between configuration, routing, services, and utility functions. The use of Flask allows for easy API integration, while the logging mechanism ensures that the application can be monitored effectively.