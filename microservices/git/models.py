from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GitRepo(db.Model):
    __tablename__ = 'git_repo'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    current_branch = db.Column(db.String(64), nullable=False)
    last_commit_hash = db.Column(db.String(40), nullable=True)
    history_json = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "current_branch": self.current_branch,
            "last_commit_hash": self.last_commit_hash,
            "history_json": self.history_json
        }
