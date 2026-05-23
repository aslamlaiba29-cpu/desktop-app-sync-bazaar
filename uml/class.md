```mermaid
classDiagram
    class BaseConfig {
        <<config>>
        +SECRET_KEY: str
        +SQLALCHEMY_TRACK_MODIFICATIONS: bool
        +JSONIFY_PRETTYPRINT_REGULAR: bool
        +CORS_ORIGINS: str
    }
    class DevelopmentConfig {
        <<config>>
        +DEBUG: bool = True
        +ENV: str = "development"
        +SQLALCHEMY_DATABASE_URI: str
    }
    class ProductionConfig {
        <<config>>
        +DEBUG: bool = False
        +ENV: str = "production"
        +SQLALCHEMY_DATABASE_URI: str
    }
    BaseConfig <|-- DevelopmentConfig
    BaseConfig <|-- ProductionConfig
    class DB {
        +SQLAlchemy()
        +init_app(app)
    }
    class Migrate {
        +Migrate()
        +init_app(app, db)
    }
    class Logger {
        +basicConfig(...)
    }
    DB --> "1" FlaskApp : used by
    Migrate --> "1" FlaskApp : used by
    Logger --> "1" FlaskApp : used by
    class ProcessModel {
        +id: int {PK}
        +name: str
        +maturity_level: int
        +defect_density: float
        +velocity: int
    }
    class CodeReview {
        +id: int {PK}
        +file_name: str
        +code_smells: int
        +status: str
        +comments: str
    }
    class SPIRecord {
        +id: int {PK}
        +process_model_id: int {FK}
        +metric_name: str
        +value: float
    }
    class TestResult {
        +id: int {PK}
        +suite_name: str
        +passed: int
        +failed: int
        +duration_sec: float
    }
    ProcessModel --> "0..*" SPIRecord : 1-to-many
    ProcessModel --> "0..*" CodeReview : optional
    ProcessModel --> "0..*" TestResult : optional
    class SyncBazarException {
        +message: str
        +status_code: int
        +error_code: str
    }
    class ProcessModelError {
        <<extends>> SyncBazarException
    }
    class GitOperationError {
        <<extends>> SyncBazarException
    }
    class TestingError {
        <<extends>> SyncBazarException
    }
    SyncBazarException <|-- ProcessModelError
    SyncBazarException <|-- GitOperationError
    SyncBazarException <|-- TestingError
```
