import os
import logging

# Configuration from environment variables
WORKERS = int(os.getenv('WORKERS', '4'))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '60'))
MAX_LINKS_DEFAULT = int(os.getenv('MAX_LINKS_DEFAULT', '100'))
SCRIPT_VERSION = "V 1.9 / Docker Ready"

def configure_logging():
    logging.basicConfig(
        level=os.getenv('LOG_LEVEL', 'INFO'),
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = configure_logging()

def configure_app(app):
    app.config['WORKERS'] = WORKERS
    app.config['REQUEST_TIMEOUT'] = REQUEST_TIMEOUT
    app.config['MAX_LINKS_DEFAULT'] = MAX_LINKS_DEFAULT
    app.config['SCRIPT_VERSION'] = SCRIPT_VERSION
    return app