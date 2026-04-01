/* frontend/src/components/BookGrid.js */
import BookCard from "./BookCard";

export default function BookGrid({ books, userId }) {
  return (
    <div className="book-grid">
      {books.map(book => (
        <BookCard key={book.book_id || book.google_books_id} book={book} userId={userId} />
      ))}
    </div>
  );
}