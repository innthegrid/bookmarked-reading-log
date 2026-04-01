# backend/services/google_books_service.py
import requests

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query):

    response = requests.get(
        GOOGLE_BOOKS_URL,
        params={"q": query, "maxResults": 20}
    )

    data = response.json()

    results = []

    for item in data.get("items", []):
        volume = item.get("volumeInfo", {})

        results.append({
            "google_books_id": item.get("id"),
            "title": volume.get("title"),
            "authors": volume.get("authors", []),
            "genres": volume.get("categories", []),
            "page_count": volume.get("pageCount"),
            "published_year": volume.get("publishedDate", "")[:4],
        })

    return results