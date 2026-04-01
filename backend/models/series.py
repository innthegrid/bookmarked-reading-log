# backend/models/series.py
from extensions import db

class Series(db.Model):
    __tablename__ = "series"
    
    series_id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    books = db.relationship("Book", back_populates="series")

    def to_dict(self):
        return {
            "series_id": self.series_id,
            "series_name": self.series_name,
        }