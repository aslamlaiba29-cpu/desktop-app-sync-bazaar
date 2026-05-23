# backend/__init__.py
"""Backend package initialization.
Creates the Flask app, loads configuration, registers extensions and blueprints, and seeds database.
"""

from flask import Flask, jsonify, render_template, Response
from flask_cors import CORS
from .extensions import db, migrate, logger
from .routes import (
    auth_bp,
    products_bp,
    cart_bp,
    orders_bp,
    process_bp,
    git_bp,
    legacy_bp,
    testing_bp
)
from .sync import broker
from werkzeug.security import generate_password_hash
import os

def create_app():
    app = Flask(
        __name__,
        static_folder="../frontend/static",
        template_folder="../frontend/templates"
    )
    # Enable CORS
    CORS(app)

    # Load configuration
    app.config.from_object('config.Config')

    # Ensure SQLite parent directory exists
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if db_uri and db_uri.startswith('sqlite:///'):
        db_path = db_uri[9:]
        if db_path.startswith('//'):
            db_path = db_path[2:]
        # Strip leading slash if followed by a drive letter on Windows
        if os.name == 'nt' and db_path.startswith('/') and len(db_path) > 2 and db_path[2] == ':':
            db_path = db_path[1:]
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    logger.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api")  # /api/cart and /api/wishlist
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
    app.register_blueprint(process_bp, url_prefix="/api/process")
    app.register_blueprint(git_bp, url_prefix="/api/git")
    app.register_blueprint(legacy_bp, url_prefix="/api/legacy")
    app.register_blueprint(testing_bp, url_prefix="/api/testing")

    # Real-Time SSE Stream Endpoint
    @app.route('/api/sync/stream')
    def sse_stream():
        def event_generator():
            q = broker.listen()
            try:
                # Send immediate connection success message
                yield "data: {\"type\": \"connected\", \"data\": \"SSE stream initialized\"}\n\n"
                while True:
                    msg = q.get()
                    yield msg
            except GeneratorExit:
                broker.remove_listener(q)
        return Response(event_generator(), mimetype="text/event-stream")

    # Serve the main GUI page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Global Exception Handler
    from backend.exceptions import SyncBazarException
    @app.errorhandler(Exception)
    def handle_exception(e):
        # If the exception is a custom SyncBazarException, serialize it
        if isinstance(e, SyncBazarException):
            app.logger.error(f"SyncBazar API Error: {e.message}")
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response
            
        # Generic unhandled errors (Internal Server Error)
        import traceback
        app.logger.error(f"Internal Server Error: {str(e)}\n{traceback.format_exc()}")
        response = jsonify({"status": "error", "error": "internal_server_error", "message": str(e)})
        response.status_code = 500
        return response

    # Auto‑create SQLite file and seed data
    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    from backend.models import User, Product, ProcessModel, GitRepo
    
    # 1. Seed Users
    if User.query.count() == 0:
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="Admin",
            email="admin@syncbazar.com"
        )
        vendor1 = User(
            username="vendor1",
            password_hash=generate_password_hash("vendor123"),
            role="Vendor",
            email="vendor1@syncbazar.com"
        )
        vendor2 = User(
            username="vendor2",
            password_hash=generate_password_hash("vendor123"),
            role="Vendor",
            email="vendor2@syncbazar.com"
        )
        customer1 = User(
            username="customer1",
            password_hash=generate_password_hash("customer123"),
            role="Customer",
            email="customer1@syncbazar.com"
        )
        db.session.add_all([admin, vendor1, vendor2, customer1])
        db.session.commit()

        # 2. Seed Products
        if Product.query.count() == 0:
            p1 = Product(
                name="Super Widget 3000",
                description="High performance, multi-threaded electronic widget suited for developers.",
                category="Electronics",
                price=299.99,
                stock=15,
                image_url="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=400",
                vendor_id=vendor1.id,
                status="Approved"
            )
            p2 = Product(
                name="Vintage Leather Jacket",
                description="Genuine brown cowhide leather jacket with quilted lining.",
                category="Apparel",
                price=120.00,
                stock=5,
                image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=400",
                vendor_id=vendor1.id,
                status="Approved"
            )
            p3 = Product(
                name="Organic Arabica Coffee",
                description="Medium roast single-origin whole bean coffee from Colombia.",
                category="Groceries",
                price=14.50,
                stock=50,
                image_url="https://images.unsplash.com/photo-1559056199-641a0ac8b55e?q=80&w=400",
                vendor_id=vendor2.id,
                status="Approved"
            )
            p4 = Product(
                name="Design Patterns Book",
                description="Elements of Reusable Object-Oriented Software classic guide.",
                category="Books",
                price=49.99,
                stock=20,
                image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400",
                vendor_id=vendor2.id,
                status="Approved"
            )
            db.session.add_all([p1, p2, p3, p4])
            db.session.commit()

    # 3. Seed Process Models
    if ProcessModel.query.count() == 0:
        pm1 = ProcessModel(
            name="Agile/Scrum Framework",
            description="Highly collaborative, iterative development model optimized for quick releases.",
            config_json={"cmmi_target": 3, "defect_density_limit": 0.5, "velocity_floor": 20}
        )
        pm2 = ProcessModel(
            name="Waterfall Process Model",
            description="Linear-sequential development model characterized by rigid, well-defined phases.",
            config_json={"cmmi_target": 2, "defect_density_limit": 1.2, "velocity_floor": 10}
        )
        pm3 = ProcessModel(
            name="DevSecOps Integration Model",
            description="Continuous deployment process incorporating automated unit testing and container security audits.",
            config_json={"cmmi_target": 5, "defect_density_limit": 0.2, "velocity_floor": 40}
        )
        db.session.add_all([pm1, pm2, pm3])
        db.session.commit()

    # 4. Seed Mock Git
    if GitRepo.query.count() == 0:
        repo = GitRepo(
            path='intelligent-kepler',
            current_branch='main',
            last_commit_hash='dc62b817aa554544cc2a50e1582c3e77174ac8eb',
            history_json=[
                {
                    "hash": "dc62b817aa554544cc2a50e1582c3e77174ac8eb",
                    "author": "aslamlaiba29-cpu <aslam.laiba29@gmail.com>",
                    "date": "2026-05-23 11:38:55",
                    "message": "Initial commit: Sync Bazar desktop app skeleton"
                }
            ]
        )
        db.session.add(repo)
        db.session.commit()
