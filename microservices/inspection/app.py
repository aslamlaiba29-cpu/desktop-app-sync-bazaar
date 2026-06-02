from flask import Flask, request, jsonify
from models import db, CodeSmell
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///inspection.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "inspection"})

@app.route('/api/inspection/smells', methods=['GET'])
def get_smells():
    smells = CodeSmell.query.all()
    return jsonify([s.to_dict() for s in smells])

@app.route('/api/inspection/smells', methods=['POST'])
def add_smell():
    data = request.json
    smell = CodeSmell(
        file_path=data.get('file_path'),
        line_start=data.get('line_start'),
        line_end=data.get('line_end'),
        smell_type=data.get('smell_type'),
        description=data.get('description'),
        resolved=data.get('resolved', False)
    )
    db.session.add(smell)
    db.session.commit()
    return jsonify(smell.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
