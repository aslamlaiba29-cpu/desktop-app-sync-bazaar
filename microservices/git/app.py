from flask import Flask, request, jsonify
from models import db, GitRepo
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///git.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "git"})

@app.route('/api/git/repos', methods=['GET'])
def get_repos():
    repos = GitRepo.query.all()
    return jsonify([r.to_dict() for r in repos])

@app.route('/api/git/repos', methods=['POST'])
def add_repo():
    data = request.json
    repo = GitRepo(
        path=data.get('path'),
        current_branch=data.get('current_branch', 'main'),
        last_commit_hash=data.get('last_commit_hash'),
        history_json=data.get('history_json')
    )
    db.session.add(repo)
    db.session.commit()
    return jsonify(repo.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
