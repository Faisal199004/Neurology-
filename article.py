from . import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False) # Using Text for potentially long article content
    summary = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(255), nullable=True)
    subspecialty_id = db.Column(db.Integer, db.ForeignKey("subspecialty.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self, include_content=False):
        data = {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "author": self.author,
            "subspecialty_id": self.subspecialty_id,
            "subspecialty_name": self.subspecialty.name if self.subspecialty else None,
            "subspecialty_slug": self.subspecialty.slug if self.subspecialty else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_published": self.is_published
        }
        if include_content:
            data["content"] = self.content
        return data

