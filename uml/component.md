# Component Diagram – overall system layout
```mermaid
%% Component diagram for Sync Bazar
graph TD
    %% Front‑end
    UI[Frontend: index.html<br/>Tailwind + Alpine.js]
    
    %% Backend Flask app
    FlaskApp[Flask Application (app.py)]
    
    %% Blueprints (modules)
    ProcessBP[Blueprint: process (api/process)]
    GitBP[Blueprint: git (api/git)]
    TestBP[Blueprint: testing (api/testing)]
    
    %% Core extensions
    DB[SQLAlchemy DB (backend/extensions.py)]
    MIG[Flask‑Migrate (backend/extensions.py)]
    LOG[Logging (backend/extensions.py)]
    
    %% Domain models
    ProcessModel[ProcessModel<br/>SQLAlchemy]
    CodeReview[CodeReview<br/>SQLAlchemy]
    SPIRecord[SPIRecord<br/>SQLAlchemy]
    TestResult[TestResult<br/>SQLAlchemy]
    
    %% Exceptions
    Exceptions[Custom Exceptions (backend/exceptions.py)]

    %% Relations
    UI -->|fetch() calls| ProcessBP
    UI -->|fetch() calls| GitBP
    UI -->|fetch() calls| TestBP

    FlaskApp -->|register| ProcessBP
    FlaskApp -->|register| GitBP
    FlaskApp -->|register| TestBP
    FlaskApp -->|uses| DB
    FlaskApp -->|uses| MIG
    FlaskApp -->|uses| LOG
    FlaskApp -->|handles| Exceptions

    ProcessBP -->|CRUD on| ProcessModel
    ProcessBP -->|uses| SPIRecord
    GitBP -->|CRUD on| CodeReview
    TestBP -->|reports| TestResult

    DB -->|stores| ProcessModel
    DB -->|stores| CodeReview
    DB -->|stores| SPIRecord
    DB -->|stores| TestResult
```
