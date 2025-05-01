from . import db

class Subspecialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    articles = db.relationship("Article", backref="subspecialty", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug
        }

