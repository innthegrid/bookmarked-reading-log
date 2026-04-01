/* frontend/src/components/BookCard.js */
import { Link } from "react-router-dom";

export default function BookCard({ book }) {
  const cover =
    book.image_url ||
    "https://via.placeholder.com/150x220?text=No+Cover";

  return (
    <div className="book-card nes-container is-rounded">
      <Link to={`/book/${book.google_books_id}`}>
        <img src={cover} alt={book.title} />
      </Link>
      <h3>{book.title}</h3>
      <p>{book.authors?.join(", ")}</p>
    </div>
  );
}