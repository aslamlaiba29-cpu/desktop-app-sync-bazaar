# backend/extensions.py
"""Initialize Flask extensions used across the app.
We keep the objects separate from the app factory to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import sys
import os

# Extension instances – will be attached to the app in create_app()
db = SQLAlchemy()
migrate = Migrate()

def init_logging(app):
    """Configure JSON-structured logging to a file.
    Logs are written to ``logs/app.log`` relative to the project root.
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clean existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers = []

    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
    )

    # File handler
    file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Stream handler for console output (useful during dev)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

class Logger:
    @staticmethod
    def init_app(app):
        init_logging(app)

logger = Logger()
