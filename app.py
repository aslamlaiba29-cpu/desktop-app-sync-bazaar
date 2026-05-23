from flask import Flask, jsonify, render_template
from config import Config
from models import db
from exceptions import SyncBazarException, ProcessModelError
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database
    db.init_app(app)
    with app.app_context():
        db.create_all() # Yeh aapki database file auto-create kar dega

        db.create_all()  # Auto‑create SQLite file

    # Configure logging to file
    logging.basicConfig(filename='sync_bazar_debug.log', level=logging.ERROR)

    # Register blueprints
    app.register_blueprint(process_bp, url_prefix='/api/process')

    # Global error handler for custom exceptions
    @app.errorhandler(SyncBazarException)
    def handle_sync_bazar_error(error):
        logging.error(f"Error: {error.message}")
        return jsonify({"status": "error", "message": error.message}), error.status_code

    # Main UI route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Route to test Exception Handling
    @app.route('/trigger-error')
    def trigger_error():
        # Intentional error for testing
        raise ProcessModelError(
            "SPI Metric Assessment failed: Defect density is too high for CMMI Level 3!",
            status_code=400,
        )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
