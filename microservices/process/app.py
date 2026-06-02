from flask import Flask, request, jsonify
from models import db, ProcessModel, SPIRecord
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///process.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "process"})

@app.route('/api/process/models', methods=['GET'])
def get_process_models():
    models = ProcessModel.query.all()
    return jsonify([m.to_dict() for m in models])

@app.route('/api/process/models', methods=['POST'])
def create_process_model():
    data = request.json
    model = ProcessModel(
        name=data.get('name'),
        description=data.get('description'),
        config_json=data.get('config_json')
    )
    db.session.add(model)
    db.session.commit()
    return jsonify(model.to_dict()), 201

@app.route('/api/process/models/<int:model_id>/spi', methods=['POST'])
def add_spi_record(model_id):
    data = request.json
    record = SPIRecord(
        model_id=model_id,
        metrics_json=data.get('metrics_json'),
        maturity_score=data.get('maturity_score')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@app.route('/api/process/trigger-error', methods=['GET'])
def trigger_error():
    return jsonify({"status": "error", "message": "SPI Metric Assessment failed: Defect density is too high for CMMI Level 3!"}), 400

@app.route('/api/process/spi/run', methods=['GET'])
def run_spi():
    return jsonify({"result": "Defect Density is within limits for CMMI Level 3."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
