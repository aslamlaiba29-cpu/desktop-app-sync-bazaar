# backend/routes/git.py
from flask import Blueprint, request, jsonify
from backend.models import db, GitRepo, CodeReview
import hashlib
import random
import logging

bp = Blueprint('git', __name__)

def get_or_create_repo():
    repo = GitRepo.query.first()
    if not repo:
        repo = GitRepo(
            path='intelligent-kepler',
            current_branch='main',
            last_commit_hash='dc62b817aa554544cc2a50e1582c3e77174ac8eb',
            history_json=[
                {
                    "hash": "dc62b817aa554544cc2a50e1582c3e77174ac8eb",
                    "author": "aslamlaiba29-cpu <aslam.laiba29@gmail.com>",
                    "date": "2026-05-23 11:38:55",
                    "message": "Initial commit: Sync Bazar desktop app skeleton"
                }
            ]
        )
        db.session.add(repo)
        db.session.commit()
    return repo

@bp.route('/status', methods=['GET'])
def get_git_status():
    repo = get_or_create_repo()
    
    # Mock some untracked changes if there are no commits pending
    untracked = ["backend/models.py", "backend/routes/git.py", "frontend/templates/index.html"]
    
    return jsonify({
        "status": "success",
        "repository": {
            "path": repo.path,
            "current_branch": repo.current_branch,
            "last_commit_hash": repo.last_commit_hash,
            "uncommitted_files": untracked
        }
    })

@bp.route('/commit', methods=['POST'])
def make_commit():
    repo = get_or_create_repo()
    data = request.get_json() or {}
    message = data.get('message')
    author = data.get('author', 'aslamlaiba29-cpu <aslam.laiba29@gmail.com>')
    branch = data.get('branch', repo.current_branch)

    if not message:
        return jsonify({"status": "error", "message": "Commit message is required"}), 400

    # Generate a random commit hash
    commit_hash = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:40]
    
    history = list(repo.history_json)
    new_commit = {
        "hash": commit_hash,
        "author": author,
        "date": request.date if hasattr(request, 'date') else request.headers.get('Date', ''),
        "message": message
    }
    
    # Format date nicely
    from datetime import datetime
    new_commit["date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    history.insert(0, new_commit)
    
    repo.current_branch = branch
    repo.last_commit_hash = commit_hash
    repo.history_json = history
    
    db.session.commit()
    logging.info(f"Mock git committed: {message} ({commit_hash[:7]}) on branch {branch}")

    return jsonify({
        "status": "success",
        "message": "Mock Git commit successful!",
        "commit": new_commit
    })

@bp.route('/history', methods=['GET'])
def get_git_history():
    repo = get_or_create_repo()
    return jsonify({"status": "success", "history": repo.history_json})

@bp.route('/reviews', methods=['GET'])
def get_code_reviews():
    reviews = CodeReview.query.order_by(CodeReview.created_at.desc()).all()
    results = []
    for r in reviews:
        results.append({
            "id": r.id,
            "file_name": r.file_name,
            "code_smells": r.code_smells,
            "status": r.status,
            "comments": r.comments,
            "created_at": r.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({"status": "success", "reviews": results})

@bp.route('/reviews', methods=['POST'])
def request_code_review():
    data = request.get_json() or {}
    file_name = data.get('file_name')
    code_smells = int(data.get('code_smells', 0))
    comments = data.get('comments', '')

    if not file_name:
        return jsonify({"status": "error", "message": "File name is required"}), 400

    review = CodeReview(file_name=file_name, code_smells=code_smells, status='Pending', comments=comments)
    db.session.add(review)
    db.session.commit()

    logging.info(f"Code review requested for file: {file_name}")

    return jsonify({
        "status": "success",
        "message": "Code review requested successfully",
        "review_id": review.id
    }), 201

@bp.route('/reviews/<int:review_id>/status', methods=['POST'])
def update_code_review_status(review_id):
    review = CodeReview.query.get_or_404(review_id)
    data = request.get_json() or {}
    status = data.get('status')  # Approved, Changes Requested
    comments = data.get('comments', '')

    if status not in ['Approved', 'Changes Requested']:
        return jsonify({"status": "error", "message": "Invalid code review status"}), 400

    review.status = status
    if comments:
        review.comments = comments
        
    db.session.commit()
    logging.info(f"Code review #{review.id} status updated to: {status}")

    return jsonify({"status": "success", "message": f"Code review status set to '{status}'"})
