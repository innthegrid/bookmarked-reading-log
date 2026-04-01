# backend/routes/library.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Book, Author, Genre, UserBook, ReadingLog
from datetime import date
from flask_cors import cross_origin

library_bp = Blueprint("library", __name__)


@library_bp.route("/api/library", methods=["GET"])
def get_library():
    user_id = request.args.get("user_id", type=int)
    status = request.args.get("status")

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    query = UserBook.query.filter_by(user_id=user_id)

    if status and status != "all":
        query = query.filter_by(status=status)

    user_books = query.all()

    results = []
    for ub in user_books:
        book = ub.book
        results.append(
            {
                "user_book_id": ub.user_book_id,
                "book_id": book.book_id,
                "google_books_id": book.google_books_id,
                "title": book.title,
                "authors": [a.name for a in book.authors],
                "genres": [g.genre_name for g in book.genres],
                "series": book.series.series_name if book.series else None,
                "series_position": book.series_position,
                "page_count": book.page_count,
                "published_year": book.published_year,
                "description": book.description,
                "image_url": book.image_url,
                "status": ub.status,
                "rating": ub.rating,
                "date_added": ub.date_added,
            }
        )

    return jsonify(results)


@library_bp.route("/api/library/add", methods=["POST"])
def add_to_library():
    data = request.json
    user_id = data.get("user_id")
    google_id = data.get("google_books_id")

    if not user_id or not google_id:
        return jsonify({"error": "user_id and google_books_id required"}), 400

    book = Book.query.filter_by(google_books_id=google_id).first()

    if not book:
        book = Book(
            google_books_id=google_id,
            title=data.get("title"),
            image_url=data.get("image_url"),
            page_count=data.get("page_count"),
            published_year=data.get("published_year"),
            description=data.get("description"),
            series_position=data.get("series_position"),
        )
        db.session.add(book)
        db.session.flush()

    for author_name in data.get("authors", []):
        if not author_name:
            continue

        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.flush()

        if author not in book.authors:
            book.authors.append(author)

    for raw_genre in data.get("genres", []):
        if not raw_genre:
            continue

        parts = [g.strip() for g in raw_genre.split("/")]

        for genre_name in parts:
            if not genre_name:
                continue

            genre = Genre.query.filter_by(genre_name=genre_name).first()
            if not genre:
                genre = Genre(genre_name=genre_name)
                db.session.add(genre)
                db.session.flush()

            if genre not in book.genres:
                book.genres.append(genre)

    user_book = UserBook.query.filter_by(
        user_id=user_id,
        book_id=book.book_id
    ).first()

    status = data.get("status", "want_to_read")

    if user_book:
        old_status = user_book.status
        if status and old_status != status:
            user_book.status = status

            if old_status != "completed" and status == "completed":
                log = ReadingLog(
                    user_book_id=user_book.user_book_id,
                    end_date=date.today(),
                    pages_read=book.page_count,
                )
                db.session.add(log)

        db.session.commit()

        return jsonify({
            "message": "Book already in library",
            "user_book_id": user_book.user_book_id,
        }), 200

    user_book = UserBook(
        user_id=user_id,
        book_id=book.book_id,
        status=status
    )
    db.session.add(user_book)
    db.session.flush()

    if status == "completed":
        log = ReadingLog(
            user_book_id=user_book.user_book_id,
            end_date=date.today(),
            pages_read=book.page_count,
        )
        db.session.add(log)

    db.session.commit()

    return jsonify({
        "message": "Book added",
        "user_book_id": user_book.user_book_id
    }), 201


@library_bp.route("/api/library/<int:user_book_id>", methods=["PATCH", "OPTIONS"])
@cross_origin()
def update_user_book(user_book_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    ub = UserBook.query.get_or_404(user_book_id)
    data = request.json

    if "rating" in data:
        ub.rating = data["rating"]

    if "status" in data:
        old_status = ub.status
        new_status = data["status"]
        ub.status = new_status

        if old_status != "completed" and new_status == "completed":
            log = ReadingLog(
                user_book_id=ub.user_book_id,
                end_date=date.today(),
                pages_read=ub.book.page_count,
            )
            db.session.add(log)

    db.session.commit()
    return jsonify({"message": "Book updated"})


@library_bp.route("/api/library/<int:user_book_id>", methods=["DELETE", "OPTIONS"])
@cross_origin()
def remove_from_library(user_book_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    ub = UserBook.query.get_or_404(user_book_id)

    db.session.delete(ub)
    db.session.commit()

    return jsonify({"message": "Book removed"})
