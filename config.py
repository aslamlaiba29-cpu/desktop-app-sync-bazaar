# config.py
"""Application configuration classes.

Separate configurations allow easy switching between development and production
environments. The development config enables debugging and uses a local SQLite
database located in the project directory.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    # CORS for local development
    CORS_ORIGINS = "*"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    # Ensure SQLite DB is stored within the project workspace directory
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'dev.db')}"

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    
    # Render and Heroku database URLs start with 'postgres://', 
    # but SQLAlchemy requires 'postgresql://' to function correctly.
    db_url = os.environ.get("DATABASE_URL", "sqlite:///prod.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = db_url

# Determine the active config class based on the environment.
# Render automatically injects the 'RENDER' environment variable.
if os.environ.get("RENDER") is not None or os.environ.get("FLASK_ENV") == "production":
    Config = ProductionConfig
else:
    Config = DevelopmentConfig
