# models.py
"""Top-level models module that re-exports backend models and the db instance.
This file allows the Flask app to import `db` directly from `models` as requested.
"""

from backend.models import (
    db,
    User,
    Product,
    CartItem,
    WishlistItem,
    Order,
    OrderItem,
    Review,
    Notification,
    SPIRecord,
    CodeSmell,
    CodeReview,
    TestResult
)

__all__ = [
    "db",
    "User",
    "Product",
    "CartItem",
    "WishlistItem",
    "Order",
    "OrderItem",
    "Review",
    "Notification",
    "SPIRecord",
    "CodeSmell",
    "CodeReview",
    "TestResult"
]
