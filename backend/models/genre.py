# backend/models/genre.py
from extensions import db
from models.associations import book_genres

class Genre(db.Model):
    __tablename__ = "genres"
    
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    books = db.relationship("Book", secondary=book_genres, back_populates="genres")

    def to_dict(self):
        return {
            "genre_id": self.genre_id,
            "genre_name": self.genre_name,
        }