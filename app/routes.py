from flask import Blueprint, jsonify, request
from app.models import Incident
from app import db

incidents_bp = Blueprint('incidents', __name__)

ALLOWED_SEVERITIES = {"Low", "Medium", "High"}

@incidents_bp.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.order_by(Incident.reported_at.desc()).all()
    result = [incident.to_dict() for incident in incidents]
    return jsonify(result), 200

@incidents_bp.route('/incidents', methods=['POST'])
def create_incident():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Malformed JSON"}), 400

    required_fields = {"title", "description", "severity"}
    extra_fields = set(data.keys()) - required_fields
    missing_fields = required_fields - set(data.keys())

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    if extra_fields:
        return jsonify({"error": f"Unexpected fields: {', '.join(extra_fields)}"}), 400

    title = data.get("title")
    description = data.get("description")
    severity = data.get("severity")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title must be a non-empty string"}), 400
    if not isinstance(description, str) or not description.strip():
        return jsonify({"error": "Description must be a non-empty string"}), 400
    if severity not in ALLOWED_SEVERITIES:
        return jsonify({"error": f"Severity must be one of {', '.join(ALLOWED_SEVERITIES)}"}), 400

    incident = Incident(title=title.strip(), description=description.strip(), severity=severity)
    db.session.add(incident)
    db.session.commit()

    return jsonify(incident.to_dict()), 201

@incidents_bp.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if incident is None:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident.to_dict()), 200

@incidents_bp.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if incident is None:
        return jsonify({"error": "Incident not found"}), 404

    db.session.delete(incident)
    db.session.commit()
    return '', 204

# ----------------
# Error Handlers
# ----------------

@incidents_bp.app_errorhandler(404)
def handle_404(error):
    return jsonify({"error": "Resource not found"}), 404

@incidents_bp.app_errorhandler(405)
def handle_405(error):
    return jsonify({"error": "Method not allowed"}), 405

@incidents_bp.app_errorhandler(400)
def handle_400(error):
    return jsonify({"error": "Bad request"}), 400

@incidents_bp.app_errorhandler(500)
def handle_500(error):
    return jsonify({"error": "Internal server error"}), 500
