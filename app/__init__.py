from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
def create_app():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import os

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import incidents_bp
    app.register_blueprint(incidents_bp, url_prefix='/')

    # --- NEW: Do DB setup and sample data inside app context ---
    with app.app_context():
        db.create_all()
        from app.models import Incident
        if Incident.query.count() == 0:
            sample_incidents = [
                Incident(
                    title="AI model produced biased output",
                    description="The model generated output that favored one demographic over another.",
                    severity="High"
                ),
                Incident(
                    title="Unexpected system shutdown",
                    description="The AI safety monitoring system shut down without warning.",
                    severity="Medium"
                ),
                Incident(
                    title="False positive alert",
                    description="A benign event was flagged as a critical incident.",
                    severity="Low"
                ),
            ]
            db.session.bulk_save_objects(sample_incidents)
            db.session.commit()
    # --- END NEW ---

    return app
