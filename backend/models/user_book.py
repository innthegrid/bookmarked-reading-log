# backend/models/user_book.py
from extensions import db
from datetime import datetime, timezone

class UserBook(db.Model):
    __tablename__ = "user_books"

    __table_args__ = (
        db.UniqueConstraint("user_id", "book_id", name="unique_user_book"),
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="valid_rating"),
    )

    user_book_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.Enum("want_to_read", "reading", "completed", name="status_types"),
        default="want_to_read",
        nullable=False,
        index=True,
    )
    rating = db.Column(db.Integer)
    date_added = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date(),
    )

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="user_books")
    book = db.relationship("Book", back_populates="user_instances")
    reading_logs = db.relationship("ReadingLog", back_populates="user_book", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "user_book_id": self.user_book_id,
            "status": self.status,
            "rating": self.rating,
            "date_added": self.date_added,
            "google_books_id": self.book.google_books_id,
            "book": self.book.to_dict(),
        }