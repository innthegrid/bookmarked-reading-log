# backend/models/book.py
from extensions import db
from .associations import book_authors, book_genres

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    google_books_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False, index=True)
    page_count = db.Column(db.Integer)
    published_year = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    description = db.Column(db.Text)
    series_position = db.Column(db.Integer)

    # Foreign Keys
    series_id = db.Column(db.Integer, db.ForeignKey("series.series_id"))

    # Relationships
    authors = db.relationship("Author", secondary=book_authors, back_populates="books")
    genres = db.relationship("Genre", secondary=book_genres, back_populates="books")
    series = db.relationship("Series", back_populates="books")
    user_instances = db.relationship(
        "UserBook", back_populates="book", cascade="all, delete"
    )

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "google_books_id": self.google_books_id,
            "title": self.title,
            "page_count": self.page_count,
            "published_year": self.published_year,
            "image_url": self.image_url,
            "description": self.description,
            "series": self.series.series_name if self.series else None,
            "series_position": self.series_position,
            "authors": [a.name for a in self.authors],
            "genres": [g.genre_name for g in self.genres],
        }
