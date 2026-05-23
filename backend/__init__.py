# backend/__init__.py
"""Backend package initialization.
Creates the Flask app, loads configuration, registers extensions and blueprints.
"""

from flask import Flask, jsonify
from .extensions import db, migrate, logger
from . import routes


def create_app():
    app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
    # Load configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    logger.init_app(app)

    # Register blueprints
    app.register_blueprint(routes.process.bp, url_prefix="/api/process")
    app.register_blueprint(routes.git.bp, url_prefix="/api/git")
    app.register_blueprint(routes.legacy.bp, url_prefix="/api/legacy")
    app.register_blueprint(routes.testing.bp, url_prefix="/api/testing")

    # Global error handler – JSON responses
    @app.errorhandler(Exception)
    def handle_exception(e):
        # If the exception is a custom API error, use its payload
        from .exceptions import APIError
        if isinstance(e, APIError):
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response
        # Unhandled exceptions – 500
        response = jsonify({"error": "internal_server_error", "message": str(e)})
        response.status_code = 500
        return response

    @app.route('/')
    def index():
        # Render the main dashboard page
        from flask import render_template
        return render_template('dashboard.html')

    return app
