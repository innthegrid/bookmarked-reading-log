# backend/models/goal.py
from extensions import db

class Goal(db.Model):
    __tablename__ = "goals"
    
    goal_id = db.Column(db.Integer, primary_key=True)
    period_type = db.Column(db.String(20), nullable=False)  # monthly, yearly
    target_value = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="goals")

    def to_dict(self):
        return {
            "goal_id": self.goal_id,
            "period_type": self.period_type,
            "target_value": self.target_value,
            "month": self.month,
            "year": self.year,
        }