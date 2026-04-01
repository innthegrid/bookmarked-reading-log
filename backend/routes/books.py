# backend/routes/books.py
import os
import requests
from flask import Blueprint, request, jsonify
from models import Book
from dotenv import load_dotenv

load_dotenv()

books_bp = Blueprint('books', __name__)

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

@books_bp.route('/api/search', methods=['GET'])
def search_books():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"error": "No search query provided"}), 400
    
    google_books_url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=20&key={GOOGLE_BOOKS_API_KEY}'

    try:
        response = requests.get(google_books_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()

        results = []
        
        for item in data.get('items', []):
            vol = item.get('volumeInfo', {})
            
            year = None
            published = vol.get('publishedDate')
            if published and len(published) >= 4:
                year = published[:4]

            results.append({
                'google_books_id': item.get('id'),
                'title': vol.get('title'),
                'authors': vol.get('authors', []),
                'genres': vol.get('categories', []),
                'description': vol.get('description'),
                'page_count': vol.get('pageCount'),
                'published_year': year,
                'image_url': vol.get('imageLinks', {}).get('thumbnail'),
            })

        return jsonify(results)

    except Exception as e:
        print(f"Search Route Error: {e}")
        return jsonify({'error': str(e)}), 500

@books_bp.route('/api/book/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({
        'book_id': book.book_id,
        'title': book.title,
        'authors': [a.name for a in book.authors],
        'genres': [g.genre_name for g in book.genres],
        'description': book.description,
        'page_count': book.page_count,
        'image_url': book.image_url,
        'series': book.series.series_name if book.series else None
    })
    
@books_bp.route('/api/search/external/<google_id>', methods=['GET'])
def get_external_book_details(google_id):
    google_books_url = f'https://www.googleapis.com/books/v1/volumes/{google_id}?key={GOOGLE_BOOKS_API_KEY}'
    
    try:
        response = requests.get(google_books_url, timeout=10)
        response.raise_for_status()
        
        item = response.json()
        vol = item.get('volumeInfo', {})
        
        return jsonify({
            'google_books_id': item.get('id'),
            'title': vol.get('title'),
            'authors': vol.get('authors', []),
            'genres': vol.get('categories', []),
            'published_year': vol.get('publishedDate')[:4] if vol.get('publishedDate') else None,
            'description': vol.get('description'),
            'page_count': vol.get('pageCount'),
            'image_url': vol.get('imageLinks', {}).get('thumbnail')
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500