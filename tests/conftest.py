# tests/conftest.py
import pytest
import os
import tempfile
from backend import create_app
from backend.extensions import db as _db

@pytest.fixture(scope='session')
def app():
    """Create and configure a new Flask app instance for testing."""
    # Create a temporary file to isolate the database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{db_path}",
        'SECRET_KEY': 'test-secret-key'
    })

    # Establish an application context before running the tests
    with app.app_context():
        _db.create_all()
        yield app

    # Teardown the temp database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    """Provide a clean database session context for each test function."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
