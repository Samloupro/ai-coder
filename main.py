import os
from flask import Flask
from config.settings import configure_app, logger, SCRIPT_VERSION, WORKERS, REQUEST_TIMEOUT, MAX_LINKS_DEFAULT
from api.routes import register_routes

# Create the Flask application instance
app = Flask(__name__)
configure_app(app)
register_routes(app)

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    logger.info(f"Starting script version: {SCRIPT_VERSION}")
    logger.info(f"Workers: {WORKERS}, Timeout: {REQUEST_TIMEOUT}s, Max Links: {MAX_LINKS_DEFAULT}")
    app.run(host='0.0.0.0', port=port)
