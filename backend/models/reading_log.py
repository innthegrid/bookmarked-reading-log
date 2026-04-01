# backend/models/reading_log.py
from extensions import db

class ReadingLog(db.Model):
    __tablename__ = "reading_logs"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    pages_read = db.Column(db.Integer)

    # Foreign keys
    user_book_id = db.Column(db.Integer, db.ForeignKey("user_books.user_book_id"), nullable=False)
    
    # Relationship to UserBook
    user_book = db.relationship("UserBook", back_populates="reading_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "pages_read": self.pages_read
        }