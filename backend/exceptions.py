# backend/exceptions.py
"""Custom exception hierarchy for the Sync Bazar application.
All API errors inherit from APIError which provides a ``to_dict`` method for JSON responses.
"""

class APIError(Exception):
    """Base class for API errors.
    Attributes:
        status_code (int): HTTP status code for the response.
        error_code (str): Machine‑readable error identifier.
        message (str): Human‑readable description.
    """

    def __init__(self, message: str, error_code: str = "error", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

    def to_dict(self):
        return {"error": self.error_code, "message": self.message}

# Specific domain errors

class ProcessModelError(APIError):
    def __init__(self, message="Invalid process model configuration"):
        super().__init__(message, error_code="process_model_error", status_code=422)

class VersionControlException(APIError):
    def __init__(self, message="Version control operation failed"):
        super().__init__(message, error_code="version_control_error", status_code=500)

class LegacyCodeException(APIError):
    def __init__(self, message="Legacy code processing error"):
        super().__init__(message, error_code="legacy_code_error", status_code=500)

class TestingException(APIError):
    def __init__(self, message="Testing service error"):
        super().__init__(message, error_code="testing_error", status_code=500)

