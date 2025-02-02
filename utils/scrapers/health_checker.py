import psutil
from datetime import datetime
import requests
from typing import Dict, Any
import os

def get_memory_usage() -> Dict[str, Any]:
    """Récupère les informations d'utilisation de la mémoire"""
    memory = psutil.virtual_memory()
    return {
        "total": f"{memory.total / (1024 * 1024):.2f}MB",
        "used": f"{memory.used / (1024 * 1024):.2f}MB",
        "available": f"{memory.available / (1024 * 1024):.2f}MB",
        "percent": memory.percent
    }

def get_cpu_usage() -> Dict[str, Any]:
    """Récupère les informations d'utilisation du CPU"""
    return {
        "percent": psutil.cpu_percent(interval=1),
        "load": os.getloadavg()[0]
    }

def check_scraper_service() -> Dict[str, Any]:
    """Vérifie l'état du service de scraping"""
    try:
        # Test avec une URL simple et rapide
        test_url = "http://example.com"
        response = requests.get(test_url, timeout=5)
        
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "last_check": datetime.utcnow().isoformat(),
            "response_time": response.elapsed.total_seconds()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "last_check": datetime.utcnow().isoformat(),
            "error": str(e)
        }

def get_system_health() -> Dict[str, Any]:
    """Récupère l'état de santé complet du système"""
    return {
        "status": "healthy",
        "components": {
            "scraper_service": check_scraper_service(),
            "system": {
                "memory": get_memory_usage(),
                "cpu": get_cpu_usage()
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }