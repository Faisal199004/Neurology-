import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS # Import CORS

# Import database and models
from src.models import db
from src.models.subspecialty import Subspecialty # Import Subspecialty model
from src.models.article import Article # Import Article model

# Import blueprints
from src.routes.content import content_bp # Import the content blueprint

app = Flask(__name__, static_folder=None) # Disable default static folder handling
CORS(app) # Enable CORS for all routes, allowing frontend to call API
app.config["SECRET_KEY"] = "a_very_secret_key_for_neuroportal" # Changed secret key

# Register blueprints
app.register_blueprint(content_bp, url_prefix="/api") # Register content blueprint

# Database configuration (already uncommented)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
    # Seed initial data if needed for testing
    if Subspecialty.query.count() == 0:
        print("Seeding initial subspecialties...")
        subspecialties_data = [
            { "name": "Neuro-oncology", "slug": "neuro-oncology" },
            { "name": "Movement Disorders", "slug": "movement-disorders" },
            { "name": "Epilepsy", "slug": "epilepsy" },
            { "name": "Stroke", "slug": "stroke" },
            { "name": "Neuromuscular Diseases", "slug": "neuromuscular-diseases" },
            { "name": "Multiple Sclerosis", "slug": "multiple-sclerosis" },
            { "name": "Headache", "slug": "headache" },
            { "name": "Cognitive Neurology", "slug": "cognitive-neurology" },
            { "name": "Neurocritical Care", "slug": "neurocritical-care" },
            { "name": "Pediatric Neurology", "slug": "pediatric-neurology" },
            { "name": "Neuroimmunology", "slug": "neuroimmunology" },
            { "name": "Sleep Neurology", "slug": "sleep-neurology" },
        ]
        for data in subspecialties_data:
            db.session.add(Subspecialty(**data))
        db.session.commit()
        print("Subspecialties seeded.")

    # Seed a sample article if none exist
    if Article.query.count() == 0:
        print("Seeding sample article...")
        # Find the 'Stroke' subspecialty to associate the article with
        stroke_subspecialty = Subspecialty.query.filter_by(slug="stroke").first()
        if stroke_subspecialty:
            sample_article = Article(
                title="Management of Acute Ischemic Stroke",
                slug="management-of-acute-ischemic-stroke",
                summary="Overview of the current guidelines for managing acute ischemic stroke, including thrombolysis and thrombectomy.",
                content="## Introduction\nAcute ischemic stroke (AIS) is a medical emergency...\n\n### Thrombolysis\nIntravenous thrombolysis with alteplase remains a cornerstone of treatment...\n\n### Mechanical Thrombectomy\nFor patients with large vessel occlusion...\n\n## Conclusion\nRapid diagnosis and treatment are crucial...",
                author="Dr. AI Neurologist",
                subspecialty_id=stroke_subspecialty.id,
                is_published=True
            )
            db.session.add(sample_article)
            db.session.commit()
            print("Sample article seeded.")
        else:
            print("Could not find 'Stroke' subspecialty to seed sample article.")


# Remove the default static file serving, Next.js will handle frontend routing
# @app.route("/")
# def serve_index():
#     # This route is no longer needed as Next.js handles the frontend
#     return "Flask Backend Running", 200

if __name__ == "__main__":
    # Use port 5001 to avoid conflict with Next.js default port 3000
    app.run(host="0.0.0.0", port=5001, debug=True)


