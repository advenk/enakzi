"""
Central configuration file for all components.
This allows running all components locally without Docker.
"""
import os

# pass: password
# Database configuration
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "archillect"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASS", "password"),
}

# API configuration
API_CONFIG = {
    "host": os.environ.get("API_HOST", "localhost"),
    "port": os.environ.get("API_PORT", "8000"),
    "base_url": os.environ.get("API_BASE_URL", "http://localhost:8000"),
    "images_dir": os.environ.get("IMAGES_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))),
}

# Crawler configuration
CRAWLER_CONFIG = {
    "images_dir": os.environ.get("IMAGES_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))),
    "nima_model_path": os.environ.get("NIMA_MODEL_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crawler", "nima_weights", "model.pth"))),
}

# Web configuration
WEB_CONFIG = {
    "port": os.environ.get("WEB_PORT", "3000"),
    "api_url": os.environ.get("REACT_APP_API_URL", "http://localhost:8000"),
}

def get_db_connection_string():
    """Return a PostgreSQL connection string based on the configuration."""
    return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}" 