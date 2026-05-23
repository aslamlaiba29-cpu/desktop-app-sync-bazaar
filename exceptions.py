# exceptions.py
"""Top‑level exception module that re‑exports backend exceptions.
This allows imports like `from exceptions import SyncBazarException` used in app.py.
"""

from backend.exceptions import SyncBazarException, ProcessModelError

__all__ = ["SyncBazarException", "ProcessModelError"]
