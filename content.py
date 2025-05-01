from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from src.models import db
from src.models.subspecialty import Subspecialty
from src.models.article import Article

content_bp = Blueprint("content", __name__)

# --- Subspecialty Routes ---

@content_bp.route("/subspecialties", methods=["GET"])
def get_subspecialties():
    """Returns a list of all subspecialties."""
    try:
        subspecialties = Subspecialty.query.order_by(Subspecialty.name).all()
        return jsonify([s.to_dict() for s in subspecialties]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_bp.route("/subspecialties/<slug>", methods=["GET"])
def get_subspecialty_by_slug(slug):
    """Returns details for a specific subspecialty by slug."""
    try:
        subspecialty = Subspecialty.query.filter_by(slug=slug).first()
        if subspecialty:
            return jsonify(subspecialty.to_dict()), 200
        else:
            return jsonify({"error": "Subspecialty not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Article Routes ---

@content_bp.route("/articles", methods=["GET"])
def get_articles():
    """Returns a list of articles, optionally filtered by subspecialty slug."""
    subspecialty_slug = request.args.get("subspecialty")
    try:
        query = Article.query.filter_by(is_published=True)
        if subspecialty_slug:
            subspecialty = Subspecialty.query.filter_by(slug=subspecialty_slug).first()
            if subspecialty:
                query = query.filter_by(subspecialty_id=subspecialty.id)
            else:
                return jsonify([]), 200 # Return empty list if subspecialty doesn't exist

        articles = query.order_by(Article.updated_at.desc()).all()
        # Exclude full content in list view
        return jsonify([a.to_dict(include_content=False) for a in articles]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_bp.route("/articles/<slug>", methods=["GET"])
def get_article_by_slug(slug):
    """Returns details for a specific article by slug, including content."""
    try:
        article = Article.query.filter_by(slug=slug, is_published=True).first()
        if article:
            # Include full content when fetching a single article
            return jsonify(article.to_dict(include_content=True)), 200
        else:
            return jsonify({"error": "Article not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Search Route ---

@content_bp.route("/search", methods=["GET"])
def search_articles():
    """Searches articles based on a query parameter."""
    query_param = request.args.get("q")
    if not query_param:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    try:
        search_term = f"%{query_param}%"
        # Search in title, summary, and content (case-insensitive)
        articles = Article.query.filter(
            Article.is_published == True,
            or_(
                Article.title.ilike(search_term),
                Article.summary.ilike(search_term),
                Article.content.ilike(search_term)
            )
        ).order_by(Article.updated_at.desc()).all()

        # Exclude full content in search results
        return jsonify([a.to_dict(include_content=False) for a in articles]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# TODO: Add routes for creating/updating/deleting content (likely requiring authentication)

