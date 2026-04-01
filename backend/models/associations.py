# backend/models/associations.py
from extensions import db

# Many-to-many relationship between books and authors
book_authors = db.Table(
    "book_authors",
    db.Column("book_id", db.Integer, db.ForeignKey("books.book_id"), primary_key=True),
    db.Column(
        "author_id", db.Integer, db.ForeignKey("authors.author_id"), primary_key=True
    ),
)

# Many-to-many relationship between books and genres
book_genres = db.Table(
    "book_genres",
    db.Column("book_id", db.Integer, db.ForeignKey("books.book_id"), primary_key=True),
    db.Column(
        "genre_id", db.Integer, db.ForeignKey("genres.genre_id"), primary_key=True
    ),
)
