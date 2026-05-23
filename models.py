# models.py
"""Top-level models module that re-exports backend models and the db instance.
This file allows the Flask app to import `db` directly from `models` as requested.
"""

# Import the actual implementations from the backend package
from backend.models import db, ProcessModel, CodeReview

__all__ = ["db", "ProcessModel", "CodeReview"]
