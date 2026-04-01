from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    print("Connecting to database to fix enum values...")
    db.session.execute(
        text("UPDATE user_books SET status = 'want_to_read' WHERE status = 'to_read'")
    )
    db.session.commit()
    print("Database updated: 'to_read' changed to 'want_to_read'.")