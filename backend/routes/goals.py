# backend/routes/goals.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Goal, UserBook, ReadingLog
from sqlalchemy import func

goals_bp = Blueprint("goals", __name__)

from datetime import datetime
from models import UserBook, ReadingLog

@goals_bp.route("/api/goals", methods=["GET"])
def get_goals():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    goals = Goal.query.filter_by(user_id=user_id).all()

    results = []

    for g in goals:
        query = (
            db.session.query(UserBook)
            .join(ReadingLog, ReadingLog.user_book_id == UserBook.user_book_id)
            .filter(UserBook.user_id == user_id)
            .filter(UserBook.status == "completed")
        )

        if g.period_type == "yearly":
            query = query.filter(
                func.strftime("%Y", ReadingLog.end_date) == str(g.year)
            )

        elif g.period_type == "monthly":
            query = query.filter(
                func.strftime("%Y", ReadingLog.end_date) == str(g.year),
                func.strftime("%m", ReadingLog.end_date) == f"{int(g.month):02d}",
            )

        completed_count = query.count()

        progress = (
            min(int((completed_count / g.target_value) * 100), 100)
            if g.target_value
            else 0
        )

        results.append(
            {**g.to_dict(), "completed": completed_count, "progress_percent": progress}
        )

    return jsonify(results)

@goals_bp.route("/api/goals", methods=["POST"])
def add_goal():
    data = request.json
    goal = Goal(
        user_id=data["user_id"],
        period_type=data["period_type"],
        target_value=data["target_value"],
        month=data.get("month") if data.get("period_type") == "monthly" else None,
        year=data.get("year"),
    )
    db.session.add(goal)
    db.session.commit()
    return jsonify({"message": "Goal added", "goal_id": goal.goal_id}), 201

@goals_bp.route("/api/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    data = request.json

    goal.period_type = data.get("period_type", goal.period_type)
    goal.target_value = data.get("target_value", goal.target_value)
    goal.month = data.get("month", goal.month)
    goal.year = data.get("year", goal.year)

    db.session.commit()
    return jsonify({"message": "Goal updated"})


# Delete a goal
@goals_bp.route("/api/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"message": "Goal deleted"})

@goals_bp.route("/api/goals/progress", methods=["GET"])
def get_goal_progress():
    user_id = request.args.get("user_id", type=int)
    year = request.args.get("year", type=int)

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    if not year:
        from datetime import date

        year = date.today().year

    goal = Goal.query.filter_by(
        user_id=user_id, period_type="yearly", year=year
    ).first()

    if not goal:
        return jsonify({"target": 0, "completed": 0, "percent": 0})

    completed = (
        db.session.query(func.count(UserBook.user_book_id))
        .join(ReadingLog, ReadingLog.user_book_id == UserBook.user_book_id)
        .filter(
            UserBook.user_id == user_id,
            UserBook.status == "completed",
            func.strftime("%Y", ReadingLog.end_date) == str(year),
        )
        .scalar()
    )

    percent = (
        round((completed / goal.target_value) * 100, 1) if goal.target_value else 0
    )

    return jsonify(
        {
            "target": goal.target_value,
            "completed": completed,
            "percent": min(percent, 100),
        }
    )
