# backend/routes/process.py
from flask import Blueprint, request, jsonify
from backend.models import db, SPIRecord, ProcessModel
from backend.exceptions import ProcessModelError
import logging

bp = Blueprint('process', __name__)

@bp.route('/models', methods=['GET'])
def get_process_models():
    models = ProcessModel.query.all()
    results = []
    for m in models:
        results.append({
            "id": m.id,
            "name": m.name,
            "description": m.description,
            "config_json": m.config_json
        })
    return jsonify({"status": "success", "models": results})

@bp.route('/assess', methods=['POST'])
def run_spi_assessment():
    data = request.get_json() or {}
    defect_density = float(data.get('defect_density', 0.0))
    velocity = int(data.get('velocity', 0))
    maturity_level = int(data.get('maturity_level', 3))  # Target CMMI level

    # Software Process Improvement Validation Constraint
    if maturity_level >= 3 and defect_density > 0.5:
        # Raise ProcessModelError (which is intercepted and logged as APIError)
        raise ProcessModelError(
            f"SPI Metric Assessment failed: Defect density ({defect_density}) is too high for CMMI Level {maturity_level}! Threshold is 0.5."
        )

    # Calculate SPI Maturity Score (1.0 to 10.0 scale)
    base_score = 10.0 - (defect_density * 8.0) + (velocity / 10.0)
    maturity_score = max(1.0, min(10.0, round(base_score, 2)))

    record = SPIRecord(defect_density=defect_density, velocity=velocity, maturity_score=maturity_score)
    db.session.add(record)
    db.session.commit()

    logging.info(f"SPI Assessment Run: Defect Density={defect_density}, Velocity={velocity}, Score={maturity_score}")

    return jsonify({
        "status": "success",
        "message": "SPI assessment completed successfully",
        "assessment": {
            "id": record.id,
            "defect_density": record.defect_density,
            "velocity": record.velocity,
            "maturity_score": record.maturity_score,
            "created_at": record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@bp.route('/history', methods=['GET'])
def get_spi_history():
    records = SPIRecord.query.order_by(SPIRecord.created_at.asc()).all()
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "defect_density": r.defect_density,
            "velocity": r.velocity,
            "maturity_score": r.maturity_score,
            "created_at": r.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({"status": "success", "history": results})
