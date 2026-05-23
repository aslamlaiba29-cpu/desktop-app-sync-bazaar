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
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///prod.db")

# Expose Config class so config.from_object('config.Config') works
Config = DevelopmentConfig
