# backend/routes/dashboard.py
from flask import Blueprint, request, jsonify
from models import UserBook

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def get_dashboard():

    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    reading = UserBook.query.filter_by(
        user_id=user_id,
        status="reading"
    ).all()

    completed_books = UserBook.query.filter_by(
        user_id=user_id,
        status="completed"
    ).all()

    total_books = UserBook.query.filter_by(
        user_id=user_id
    ).count()

    # Stats
    total_pages = sum(
        ub.book.page_count or 0 for ub in completed_books
    )

    ratings = [ub.rating for ub in completed_books if ub.rating]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return jsonify({
        "currently_reading": [
            {
                "user_book_id": ub.user_book_id,
                "title": ub.book.title,
                "image_url": ub.book.image_url
            } for ub in reading
        ],
        "stats": {
            "books_completed": len(completed_books),
            "total_books": total_books,
            "total_pages_read": total_pages,
            "average_rating": avg_rating
        }
    })