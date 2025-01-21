FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Configuration de Gunicorn avec variables d'environnement
CMD ["sh", "-c", "gunicorn --workers ${WORKERS:-4} --timeout ${TIMEOUT:-300} --bind 0.0.0.0:${PORT:-5000} main:app"]