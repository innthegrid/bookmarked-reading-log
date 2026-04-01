# backend/models/author.py
from extensions import db
from models.associations import book_authors

class Author(db.Model):
    __tablename__ = "authors"
    
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Relationships
    books = db.relationship("Book", secondary=book_authors, back_populates="authors")

    def to_dict(self):
        return {
            "author_id": self.author_id,
            "name": self.name,
        }