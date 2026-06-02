from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProcessModel(db.Model):
    __tablename__ = 'process_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    config_json = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "config_json": self.config_json
        }

class SPIRecord(db.Model):
    __tablename__ = 'spi_record'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('process_model.id'), nullable=False)
    metrics_json = db.Column(db.JSON, nullable=False)
    maturity_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    model = db.relationship('ProcessModel', backref=db.backref('spi_records', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "metrics_json": self.metrics_json,
            "maturity_score": self.maturity_score,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
