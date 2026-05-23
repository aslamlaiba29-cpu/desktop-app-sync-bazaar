# backend/routes/legacy.py
from flask import Blueprint, request, jsonify
from backend.models import db, CodeSmell
import os
import re
import json
import logging

bp = Blueprint('legacy', __name__)

# Search path for static analysis is the root of the workspace
WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

@bp.route('/scan', methods=['POST'])
def scan_codebase():
    # Clear previously unresolved smells before running a fresh scan
    CodeSmell.query.filter_by(resolved=False).delete()
    
    found_smells = []
    
    # Files to analyze
    target_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Ignore virtual environments, git metadata, and caches
        if any(ignored in root for ignored in ['.git', 'venv', '__pycache__', 'instance', 'logs', 'tests']):
            continue
        for file in files:
            if file.endswith('.py'):
                target_files.append(os.path.join(root, file))

    for filepath in target_files:
        rel_path = os.path.relpath(filepath, WORKSPACE_DIR)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                
                # Rule 1: Long Lines (> 100 chars)
                if len(line) > 100 and "Created At:" not in line and "Task Description" not in line:
                    smell = CodeSmell(
                        file_path=rel_path,
                        line_start=idx,
                        line_end=idx,
                        smell_type="Long Line",
                        description=f"Line of length {len(line)} exceeds target maximum (100 characters)."
                    )
                    db.session.add(smell)
                    found_smells.append(smell)

                # Rule 2: Global Keyword (Global State Dependency)
                if re.match(r"\bglobal\b", clean_line):
                    smell = CodeSmell(
                        file_path=rel_path,
                        line_start=idx,
                        line_end=idx,
                        smell_type="Global State",
                        description="Use of 'global' keyword increases coupling and violates clean modular boundaries."
                    )
                    db.session.add(smell)
                    found_smells.append(smell)

                # Rule 3: Long Parameter List (> 5 params)
                func_match = re.match(r"^def\s+\w+\((.*?)\):", clean_line)
                if func_match:
                    params_str = func_match.group(1)
                    # Simple count of commas in the parameters section
                    params_count = len([p for p in params_str.split(',') if p.strip()])
                    if params_count > 5:
                        smell = CodeSmell(
                            file_path=rel_path,
                            line_start=idx,
                            line_end=idx,
                            smell_type="Long Parameter List",
                            description=f"Function has {params_count} parameters, exceeding the clean limit (max 5)."
                        )
                        db.session.add(smell)
                        found_smells.append(smell)
                        
        except Exception as e:
            logging.error(f"Error scanning file {filepath}: {str(e)}")

    db.session.commit()
    logging.info(f"Legacy code scan completed: found {len(found_smells)} smells")

    results = []
    for s in found_smells:
        results.append({
            "id": s.id,
            "file_path": s.file_path,
            "line_start": s.line_start,
            "line_end": s.line_end,
            "smell_type": s.smell_type,
            "description": s.description,
            "resolved": s.resolved
        })

    return jsonify({"status": "success", "smells": results, "count": len(results)})

@bp.route('/smells', methods=['GET'])
def get_smells():
    smells = CodeSmell.query.order_by(CodeSmell.resolved.asc(), CodeSmell.file_path.asc()).all()
    results = []
    for s in smells:
        results.append({
            "id": s.id,
            "file_path": s.file_path,
            "line_start": s.line_start,
            "line_end": s.line_end,
            "smell_type": s.smell_type,
            "description": s.description,
            "resolved": s.resolved
        })
    return jsonify({"status": "success", "smells": results})

@bp.route('/resolve/<int:smell_id>', methods=['POST'])
def resolve_smell(smell_id):
    smell = CodeSmell.query.get_or_404(smell_id)
    smell.resolved = True
    db.session.commit()
    logging.info(f"Code smell #{smell_id} marked as resolved")
    return jsonify({"status": "success", "message": "Code smell refactored/resolved successfully!"})

@bp.route('/logs', methods=['GET'])
def get_logs():
    log_file_path = os.path.join(WORKSPACE_DIR, 'logs', 'app.log')
    logs = []
    
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Read last 100 log items
                for line in reversed(lines[-100:]):
                    try:
                        logs.append(json.loads(line))
                    except Exception:
                        logs.append({
                            "time": "N/A",
                            "level": "INFO",
                            "module": "system",
                            "message": line.strip()
                        })
        except Exception as e:
            logs.append({
                "time": "N/A",
                "level": "ERROR",
                "module": "logs",
                "message": f"Could not read logs: {str(e)}"
            })
    else:
        logs.append({
            "time": "N/A",
            "level": "WARNING",
            "module": "logs",
            "message": "Logs file not found yet. Perform some actions to write logs."
        })

    return jsonify({"status": "success", "logs": logs})
