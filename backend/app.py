from datetime import datetime, timezone
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import event

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db' # DB is stored in library.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Stop warnings when we modify the DB, reduces overhead
db = SQLAlchemy(app) # Creates DB object, we use it to interact with the DB

# DEFINE SCHEMA

# book_authors - many-to-many relationship between books and authors
book_authors = db.Table('book_authors',
                        db.Column('book_id', db.Integer, db.ForeignKey('books.book_id'), primary_key=True),
                        db.Column('author_id', db.Integer, db.ForeignKey('authors.author_id'), primary_key=True)
)

class User(db.Model):
  __tablename__ = 'users'
  
  # Attributes
  user_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  
  # Relationships
  user_books = db.relationship('UserBook', back_populates='user')
  goals = db.relationship('Goal', back_populates='user')

class Book(db.Model):
  __tablename__ = 'books'
  
  # Attributes
  book_id = db.Column(db.Integer, primary_key=True)
  google_books_id = db.Column(db.String(50), unique=True, nullable=False)
  title = db.Column(db.String(200), nullable=False)
  page_count = db.Column(db.Integer)
  published_year = db.Column(db.Integer)
  fiction = db.Column(db.Boolean, default=True)
  image_url = db.Column(db.Text)
  description = db.Column(db.Text)
  
  # Foreign keys
  series_id = db.Column(db.Integer, db.ForeignKey('series.series_id'))
  genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
  
  # Relationships
  authors = db.relationship('Author', secondary=book_authors, back_populates='books')
  genre = db.relationship('Genre', back_populates='books')
  series = db.relationship('Series', back_populates='books')
  user_instances = db.relationship('UserBook', back_populates='book')

class Author(db.Model):
  __tablename__ = 'authors'
  
  # Attributes
  author_id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100), unique=True, nullable=False) # we assume author names are unique for simplicity, even if it doesn't refelct real world
  
  # Relationships
  books = db.relationship('Book', secondary=book_authors, back_populates='authors')

class Genre(db.Model):
  __tablename__ = 'genres'
  
  # Attributes
  genre_id = db.Column(db.Integer, primary_key=True)
  genre_name = db.Column(db.String(50), unique=True, nullable=False)
  
  # Relationships
  books = db.relationship('Book', back_populates='genre')

class Series(db.Model):
  __tablename__ = 'series'
  
  # Attributes
  series_id = db.Column(db.Integer, primary_key=True)
  series_name = db.Column(db.String(100), nullable=False)
  
  # Relationships
  books = db.relationship('Book', back_populates='series')

class UserBook(db.Model):
  __tablename__ = 'user_books'
  
  # Ensure a user can only have one entry per book - avoid duplicates
  __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique_user_book'),)
  
  # Attributes
  user_book_id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.Enum('want_to_read', 'reading', 'completed', name='status_types'),
                     default='want_to_read',
                     nullable=False
  )
  rating = db.Column(db.Integer) # 1-5
  date_added = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
  
  # Foreign keys
  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
  
  # Relationships
  user = db.relationship('User', back_populates='user_books')
  book = db.relationship('Book', back_populates='user_instances')
  
  # Cascade deletes: if user_book entry is deleted, also delete their reading logs and sessions
  reading_logs = db.relationship('ReadingLog', back_populates='user_book', cascade='all, delete-orphan')
  sessions = db.relationship('ReadingSession', back_populates='user_book', cascade='all, delete-orphan')
  
class ReadingLog(db.Model):
  __tablename__ = 'reading_logs'
  
  # Attributes
  log_id = db.Column(db.Integer, primary_key=True)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date)
  
  # Foreign keys
  user_book_id = db.Column(db.Integer, db.ForeignKey('user_books.user_book_id'), nullable=False)

  # Relationships
  user_book = db.relationship('UserBook', back_populates='reading_logs')

@event.listens_for(UserBook.status, 'set')
def handle_re_reading_logic(target, value, oldvalue, initiator):
  today = datetime.now(timezone.utc).date()
  
  # Set status to "reading" -> start new log
  if value == 'reading':
    new_log = ReadingLog(start_date=today)
    target.reading_logs.append(new_log)
  
  # Set status to "completed"
  if value == 'completed' and oldvalue == 'reading':
    current_log = next((log for log in target.reading_logs if log.end_date is None), None)
    if current_log:
      current_log.end_date = today
      
class ReadingSession(db.Model):
  __tablename__ = 'reading_sessions'
  
  # Attributes
  session_id = db.Column(db.Integer, primary_key=True)
  session_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
  pages_read = db.Column(db.Integer)
  minutes_read = db.Column(db.Integer)
  notes = db.Column(db.Text)
  
  # Foreign keys
  user_book_id = db.Column(db.Integer, db.ForeignKey('user_books.user_book_id'), nullable=False)
  
  # Relationships
  user_book = db.relationship('UserBook', back_populates='sessions')
  
class Goal(db.Model):
  __tablename__ = 'goals'
  
  # Attributes
  goal_id = db.Column(db.Integer, primary_key=True)
  goal_type = db.Column(db.String(20), nullable=False) # books, page, time
  period_type = db.Column(db.String(20), nullable=False) # monthly, yearly
  target_value = db.Column(db.Integer, nullable=False)
  month = db.Column(db.Integer)
  year = db.Column(db.Integer)
  
  # Foreign keys
  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
  
  # Relationships
  user = db.relationship('User', back_populates='goals')

# DATABASE INITIALIZATION
with app.app_context():
  db.create_all()
  print("Database tables created successfully!")

if __name__ == '__main__':
  app.run(debug=True, port=5001)