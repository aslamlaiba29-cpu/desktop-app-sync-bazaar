from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProcessModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)        # Agile, Waterfall, etc.
    maturity_level = db.Column(db.Integer, default=1)       # CMMI Level (1-5)
    defect_density = db.Column(db.Float, default=0.0)       # SPI Metric
    velocity = db.Column(db.Integer, default=0)             # SPI Metric

class CodeReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    code_smells = db.Column(db.Integer, default=0)          # Refactoring metric
    status = db.Column(db.String(50), default='Pending')    # Approved, Changes Requested
    comments = db.Column(db.Text)
