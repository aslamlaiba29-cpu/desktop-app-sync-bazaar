from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TestResult(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(16), nullable=False)  # PASSED, FAILED, SKIPPED
    duration = db.Column(db.Float, nullable=True)  # seconds
    output = db.Column(db.Text, nullable=True)
    run_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "test_name": self.test_name,
            "status": self.status,
            "duration": self.duration,
            "output": self.output,
            "run_at": self.run_at.isoformat() if self.run_at else None
        }
