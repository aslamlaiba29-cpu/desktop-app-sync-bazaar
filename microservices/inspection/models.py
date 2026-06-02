from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def to_dict(self):
        return {
            "id": self.id,
            "file_path": self.file_path,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "smell_type": self.smell_type,
            "description": self.description,
            "resolved": self.resolved,
            "reported_at": self.reported_at.isoformat() if self.reported_at else None
        }
