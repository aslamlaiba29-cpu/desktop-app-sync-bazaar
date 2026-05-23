# backend/routes/auth.py
from flask import Blueprint, request, jsonify, session
from backend.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import logging

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'Customer')
    email = data.get('email')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username already exists"}), 409

    # Using werkzeug security for hashing
    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash, role=role, email=email)
    db.session.add(user)
    db.session.commit()

    logging.info(f"User registered: {username} as {role}")
    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "user": {"id": user.id, "username": user.username, "role": user.role}
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401

    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role

    logging.info(f"User logged in: {username}")
    return jsonify({
        "status": "success",
        "message": "Logged in successfully",
        "user": {"id": user.id, "username": user.username, "role": user.role}
    })

@bp.route('/logout', methods=['POST'])
def logout():
    username = session.get('username')
    session.clear()
    if username:
        logging.info(f"User logged out: {username}")
    return jsonify({"status": "success", "message": "Logged out successfully"})

@bp.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not authenticated", "user": None}), 401
    
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({"status": "error", "message": "User not found", "user": None}), 404

    return jsonify({
        "status": "success",
        "user": {"id": user.id, "username": user.username, "role": user.role, "email": user.email}
    })
