from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProcessModel(db.Model):
    __tablename__ = 'process_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    config_json = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<ProcessModel {self.name}>"

class SPIRecord(db.Model):
    __tablename__ = 'spi_record'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('process_model.id'), nullable=False)
    metrics_json = db.Column(db.JSON, nullable=False)
    maturity_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    model = db.relationship('ProcessModel', backref=db.backref('spi_records', lazy=True))

    def __repr__(self):
        return f"<SPIRecord {self.id} score={self.maturity_score}>"

class GitRepo(db.Model):
    __tablename__ = 'git_repo'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    current_branch = db.Column(db.String(64), nullable=False)
    last_commit_hash = db.Column(db.String(40), nullable=True)
    # For mock data we store JSON history
    history_json = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f"<GitRepo {self.path}>"

class CodeSmell(db.Model):
    __tablename__ = 'code_smell'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(256), nullable=False)
    line_start = db.Column(db.Integer, nullable=False)
    line_end = db.Column(db.Integer, nullable=False)
    smell_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resolved = db.Column(db.Boolean, default=False)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CodeSmell {self.smell_type} in {self.file_path}>"

class TestResult(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(16), nullable=False)  # PASSED, FAILED, SKIPPED
    duration = db.Column(db.Float, nullable=True)  # seconds
    output = db.Column(db.Text, nullable=True)
    run_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TestResult {self.test_name} {self.status}>"
