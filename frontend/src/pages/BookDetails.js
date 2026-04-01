/* frontend/src/pages/BookDetails.js */
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getExternalBook,
  getLibrary,
  addBook,
  updateBook,
  deleteBook
} from "../services/bookService";

import StarRating from "../components/StarRating";
import StatusDropdown from "../components/StatusDropdown";

export default function BookDetails({ userId }) {

  const { googleId } = useParams();

  const [book, setBook] = useState(null);
  const [userBook, setUserBook] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!googleId) return;
    loadBook();
  }, [googleId]);

  const loadBook = async () => {
    try {

      setLoading(true);

      const bookData = await getExternalBook(googleId);
      setBook(bookData);
      const library = await getLibrary(userId);
      const match = library.find(
        b => String(b.google_books_id) === String(googleId)
      );

      if (match) {
        setUserBook(match);
      } else {
        setUserBook(null);
      }

    } catch (err) {
      console.error("Failed to load book", err);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (status) => {

    try {
      if (!userBook) {

        const res = await addBook({
          user_id: userId,
          google_books_id: googleId,
          title: book.title,
          image_url: book.image_url,
          page_count: book.page_count,
          published_year: book.published_year,
          description: book.description,
          authors: book.authors || [],
          genres: book.genres || [],
          status
        });

        setUserBook({
          ...book,
          user_book_id: res.user_book_id,
          status,
          rating: 0
        });

      } else {

        await updateBook(userBook.user_book_id, { status });

        setUserBook({
          ...userBook,
          status
        });

      }

    } catch (err) {
      console.error("Status update failed", err);
    }
  };

  const updateRating = async (rating) => {
    if (!userBook) return;
    try {
      await updateBook(userBook.user_book_id, { rating });
      setUserBook({
        ...userBook,
        rating
      });
    } catch (err) {
      console.error("Rating update failed", err);
    }
  };

  const removeBook = async () => {
    if (!userBook) return;
    try {
      await deleteBook(userBook.user_book_id);
      setUserBook(null);
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  if (loading) {
    return <div className="nes-container">Loading...</div>;
  }

  if (!book) {
    return <div className="nes-container">Book not found.</div>;
  }

  return (
    <div className="nes-container with-title">
      <p className="title">{book.title}</p>

      <img
        src={book.image_url || "https://via.placeholder.com/200x300?text=No+Cover"}
        width="200"
        alt={book.title}
      />

      <p>
        <b>Authors:</b>{" "}
        {book.authors?.length ? book.authors.join(", ") : "Unknown"}
      </p>

      <p>
        <b>Genres:</b>{" "}
        {book.genres?.length ? book.genres.join(", ") : "Unknown"}
      </p>

      <p>
        <b>Published:</b>{" "}
        {book.published_year || "Unknown"}
      </p>

      <StatusDropdown
        status={userBook?.status || ""}
        onChange={updateStatus}
      />

      <div style={{ margin: '12px 0' }}>
        <label style={{ display: 'block', marginBottom: '4px' }}>
          Rating:
        </label>
        <StarRating
          rating={userBook?.rating || 0}
          onChange={updateRating}
        />
      </div>

      {userBook && (
        <button
          className="nes-btn is-error"
          onClick={removeBook}
        >
          Remove From Library
        </button>
      )}

      <p style={{ marginTop: "20px", whiteSpace: "pre-line" }}>
        {book.description
          ? book.description
            .replace(/<\/p>/gi, "\n\n")
            .replace(/<br\s*\/?>/gi, "\n")
            .replace(/<[^>]+>/g, "")
          : "No description available."}
      </p>

    </div>
  );
}