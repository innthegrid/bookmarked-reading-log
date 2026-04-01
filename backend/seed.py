import os
import random
import requests
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, insert, select

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
DB_PATH = 'sqlite:///library.db'


def get_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'key': GOOGLE_API_KEY,
        'maxResults': 10,
        'orderBy': 'relevance'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json().get('items', [])
    except:
        return []


def seed():
    engine = create_engine(DB_PATH)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    books_t = metadata.tables['books']
    authors_t = metadata.tables['authors']
    genres_t = metadata.tables['genres']
    book_authors_t = metadata.tables['book_authors']
    book_genres_t = metadata.tables['book_genres']
    user_books_t = metadata.tables['user_books']
    reading_logs_t = metadata.tables['reading_logs']
    users_t = metadata.tables['users']

    specific_queries = [
        "The Hunger Games Suzanne Collins",
        "To Kill a Mockingbird Harper Lee",
        "Dante's Inferno",
        "Atomic Habits James Clear",
        "The Secret History Donna Tartt",
        "The Seven Husbands of Evelyn Hugo",
        "Normal People Sally Rooney",
        "The Silent Patient Freida McFadden",
        "Circe Madeline Miller",
        "Crying in H Mart Michelle Zauner",
        "Deep Work Cal Newport",
        "The Song of Achilles",
        "Tomorrow and Tomorrow and Tomorrow",
        "Yellowface Rebecca Kuang",
        "Educated Tara Westover"
    ]

    print("Seeding books with genres...")

    with engine.begin() as conn:

        # Ensure demo user exists
        if not conn.execute(
            select(users_t).where(users_t.c.user_id == 1)
        ).fetchone():
            conn.execute(insert(users_t).values(user_id=1, username="ingrid_t"))

        logs_count = 0

        for query in specific_queries:
            items = get_books(query)
            if not items:
                continue

            item = items[0]
            info = item.get('volumeInfo', {})

            title = info.get('title')
            authors = info.get('authors', [])
            raw_genres = info.get('categories', [])
            g_id = item.get('id')

            if not title or not authors:
                continue

            # --- Book ---
            book_check = conn.execute(
                select(books_t.c.book_id).where(
                    books_t.c.google_books_id == g_id
                )
            ).fetchone()

            if book_check:
                b_id = book_check[0]
            else:
                res = conn.execute(insert(books_t).values(
                    google_books_id=g_id,
                    title=title,
                    page_count=info.get('pageCount', random.randint(250, 450)),
                    published_year=int(info.get('publishedDate', '2020')[:4]) if info.get('publishedDate') else 2020,
                    image_url=info.get('imageLinks', {}).get('thumbnail'),
                    description=(info.get('description', '')[:490] + "...") if info.get('description') else ""
                ))
                b_id = res.inserted_primary_key[0]

            # --- Authors ---
            for a_name in authors:
                a_res = conn.execute(
                    select(authors_t.c.author_id).where(authors_t.c.name == a_name)
                ).fetchone()

                if a_res:
                    a_id = a_res[0]
                else:
                    a_id = conn.execute(
                        insert(authors_t).values(name=a_name)
                    ).inserted_primary_key[0]

                # link book-author
                existing = conn.execute(
                    select(book_authors_t).where(
                        book_authors_t.c.book_id == b_id,
                        book_authors_t.c.author_id == a_id
                    )
                ).fetchone()

                if not existing:
                    conn.execute(
                        insert(book_authors_t).values(
                            book_id=b_id,
                            author_id=a_id
                        )
                    )

            # --- Genres (FIXED) ---
            for raw in raw_genres:
                if not raw:
                    continue

                parts = [g.strip() for g in raw.split("/")]

                for genre_name in parts:
                    if not genre_name:
                        continue

                    # find or create genre
                    g_res = conn.execute(
                        select(genres_t.c.genre_id).where(
                            genres_t.c.genre_name == genre_name
                        )
                    ).fetchone()

                    if g_res:
                        genre_id = g_res[0]
                    else:
                        genre_id = conn.execute(
                            insert(genres_t).values(genre_name=genre_name)
                        ).inserted_primary_key[0]

                    # link book-genre
                    existing = conn.execute(
                        select(book_genres_t).where(
                            book_genres_t.c.book_id == b_id,
                            book_genres_t.c.genre_id == genre_id
                        )
                    ).fetchone()

                    if not existing:
                        conn.execute(
                            insert(book_genres_t).values(
                                book_id=b_id,
                                genre_id=genre_id
                            )
                        )

            # --- User Book ---
            ub_check = conn.execute(
                select(user_books_t.c.user_book_id).where(
                    user_books_t.c.user_id == 1,
                    user_books_t.c.book_id == b_id
                )
            ).fetchone()

            if not ub_check:
                ub_id = conn.execute(insert(user_books_t).values(
                    user_id=1,
                    book_id=b_id,
                    status="completed",
                    rating=random.randint(4, 5)
                )).inserted_primary_key[0]

                # Spread dates
                year = random.choice([2024, 2025, 2026])
                month = random.randint(1, 12)
                if year == 2026 and month > 3:
                    month = 3

                end_dt = datetime(year, month, random.randint(1, 28))

                conn.execute(insert(reading_logs_t).values(
                    user_book_id=ub_id,
                    start_date=end_dt - timedelta(days=random.randint(5, 15)),
                    end_date=end_dt,
                    pages_read=info.get('pageCount', 300)
                ))

                logs_count += 1
                print(f"Added: {title}")

            time.sleep(0.2)

    print(f"\nSeeding complete. {logs_count} books added.")


if __name__ == "__main__":
    seed()