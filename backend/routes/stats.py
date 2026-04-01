# backend/routes/stats.py
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from extensions import db
from models import ReadingLog, UserBook, Book, Author, Genre
from models.associations import book_authors, book_genres

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/api/stats/filter-options", methods=["GET"])
def get_filter_options():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    # Years
    years_query = (
        db.session.query(func.strftime("%Y", ReadingLog.end_date))
        .join(UserBook, UserBook.user_book_id == ReadingLog.user_book_id)
        .filter(UserBook.user_id == user_id)
        .filter(ReadingLog.end_date.isnot(None))
        .distinct()
        .all()
    )
    years = [y[0] for y in years_query if y[0]] or ["2026"]

    # Authors
    authors = (
        db.session.query(Author)
        .join(book_authors)
        .join(Book)
        .join(UserBook)
        .filter(UserBook.user_id == user_id)
        .group_by(Author.author_id)
        .order_by(Author.name)
        .all()
    )

    # Genres
    genres = (
        db.session.query(Genre)
        .join(book_genres)
        .join(Book)
        .join(UserBook)
        .filter(UserBook.user_id == user_id)
        .group_by(Genre.genre_id)
        .order_by(Genre.genre_name)
        .all()
    )

    months = [
        {"val": "01", "name": "Jan"},
        {"val": "02", "name": "Feb"},
        {"val": "03", "name": "Mar"},
        {"val": "04", "name": "Apr"},
        {"val": "05", "name": "May"},
        {"val": "06", "name": "Jun"},
        {"val": "07", "name": "Jul"},
        {"val": "08", "name": "Aug"},
        {"val": "09", "name": "Sep"},
        {"val": "10", "name": "Oct"},
        {"val": "11", "name": "Nov"},
        {"val": "12", "name": "Dec"},
    ]

    return jsonify(
        {
            "years": sorted(years, reverse=True),
            "months": months,
            "authors": [{"id": a.author_id, "name": a.name} for a in authors],
            "genres": [{"id": g.genre_id, "name": g.genre_name} for g in genres],
        }
    )


@stats_bp.route("/api/stats", methods=["GET"])
def get_statistics():

    user_id = request.args.get("user_id", type=int)
    year = request.args.get("year")
    month = request.args.get("month")
    author_id = request.args.get("author_id", type=int)
    genre_id = request.args.get("genre_id", type=int)

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    query = (
        db.session.query(UserBook)
        .join(Book)
        .outerjoin(book_authors)
        .outerjoin(Author)
        .outerjoin(book_genres)
        .outerjoin(Genre)
        .filter(UserBook.user_id == user_id, UserBook.status == "completed")
    )

    if author_id:
        query = query.filter(Author.author_id == author_id)

    if genre_id:
        query = query.filter(Genre.genre_id == genre_id)

    user_books = query.distinct().all()

    completed_books = []
    total_pages = 0
    ratings = []

    for ub in user_books:
        book = ub.book

        log = ReadingLog.query.filter_by(user_book_id=ub.user_book_id).first()

        finish_date = log.end_date if log else None

        if year and year != "all":
            if not finish_date or finish_date.strftime("%Y") != year:
                continue

        if month and month != "all":
            if not finish_date or finish_date.strftime("%m") != month:
                continue

        pages = book.page_count or 0
        total_pages += pages

        if ub.rating:
            ratings.append(ub.rating)

        completed_books.append(
            {
                "title": book.title,
                "finish_date": (
                    finish_date.strftime("%Y-%m-%d") if finish_date else "N/A"
                ),
                "pages": pages,
                "rating": ub.rating or 0,
            }
        )

    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return jsonify(
        {
            "aggregates": {
                "total_books_finished": len(completed_books),
                "total_pages_read": total_pages,
                "average_rating": avg_rating,
            },
            "completed_books": completed_books,
        }
    )