# backend/models/user.py
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Relationships
    user_books = db.relationship(
        "UserBook", back_populates="user", cascade="all, delete-orphan"
    )
    goals = db.relationship("Goal", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
        }