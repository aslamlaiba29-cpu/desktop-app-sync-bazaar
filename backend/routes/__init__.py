# backend/routes/__init__.py
"""Export all API route blueprints."""

from .auth import bp as auth_bp
from .products import bp as products_bp
from .cart import bp as cart_bp
from .orders import bp as orders_bp
from .process import bp as process_bp
from .git import bp as git_bp
from .legacy import bp as legacy_bp
from .testing import bp as testing_bp

__all__ = [
    "auth_bp",
    "products_bp",
    "cart_bp",
    "orders_bp",
    "process_bp",
    "git_bp",
    "legacy_bp",
    "testing_bp"
]
