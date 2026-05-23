# backend/exceptions.py
"""Custom exception hierarchy for the Sync Bazar application.
All API errors inherit from SyncBazarException which provides attributes for status and JSON payloads.
"""

class SyncBazarException(Exception):
    """Base class for Sync Bazar application exceptions."""
    def __init__(self, message: str, status_code: int = 400, error_code: str = "error"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def to_dict(self):
        return {"status": "error", "error": self.error_code, "message": self.message}

class APIError(SyncBazarException):
    """General API errors."""
    pass

# Specific domain errors

class ProcessModelError(APIError):
    def __init__(self, message="Invalid process model configuration", status_code=422):
        super().__init__(message, status_code=status_code, error_code="process_model_error")

class VersionControlException(APIError):
    def __init__(self, message="Version control operation failed", status_code=500):
        super().__init__(message, status_code=status_code, error_code="version_control_error")

class LegacyCodeException(APIError):
    def __init__(self, message="Legacy code processing error", status_code=500):
        super().__init__(message, status_code=status_code, error_code="legacy_code_error")

class TestingException(APIError):
    def __init__(self, message="Testing service error", status_code=500):
        super().__init__(message, status_code=status_code, error_code="testing_error")
