# Contact Scraper

Application de scraping pour extraire les contacts, emails, numéros de téléphone et liens sociaux des sites web.

## Configuration Docker

### Prérequis
- Docker
- Docker Compose

### Variables d'Environnement

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

### Développement Local

1. Cloner le repository :
```bash
git clone [votre-repo]
cd contact-scraper
```

2. Créer le fichier `.env` avec vos configurations

3. Lancer l'application avec Docker Compose :
```bash
docker-compose up --build
```

L'application sera accessible sur `http://localhost:5000`

### Déploiement sur Coolify

1. Installer Coolify sur votre serveur
2. Dans l'interface Coolify :
   - Connecter votre repository Git
   - Créer un nouveau service
   - Sélectionner "Docker Compose"
   - Configurer les variables d'environnement
   - Déployer !

## API Endpoints

### Health Check
```
GET /health
```
Vérifie l'état de l'application.

### Scraping
```
GET /scrape?url=https://example.com
```

Paramètres :
- `url` (requis) : URL du site à analyser
- `include_emails` (optionnel) : Inclure les emails (true/false)
- `include_phones` (optionnel) : Inclure les numéros de téléphone (true/false)
- `include_social_links` (optionnel) : Inclure les liens sociaux (true/false)
- `include_unique_links` (optionnel) : Inclure tous les liens uniques (true/false)
- `max_link` (optionnel) : Nombre maximum de liens à analyser (défaut: 100)

## Monitoring

L'application inclut :
- Healthcheck Docker
- Logs structurés
- Métriques de ressources via Docker

## Sécurité

- Les variables sensibles doivent être configurées via l'interface Coolify
- Les fichiers sensibles sont exclus via .gitignore
- L'image Docker utilise une base slim pour réduire la surface d'attaque
