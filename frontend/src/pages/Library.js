/* frontend/src/pages/Library.js */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { API_BASE } from '../config';
import StarRating from '../components/StarRating';

export default function Library({ userId }) {
  const [library, setLibrary] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const fetchLibrary = async () => {
    if (!userId) return;

    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/library`, {
        params: {
          user_id: userId,
          status: statusFilter || undefined
        }
      });

      setLibrary(res.data);
    } catch (err) {
      console.error("Failed to fetch library:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLibrary();
  }, [userId, statusFilter]);

  const deleteBook = async (userBookId) => {
    if (!window.confirm("Remove this book from your library?")) return;

    try {
      await axios.delete(`${API_BASE}/library/${userBookId}`);
      setLibrary(prev => prev.filter(b => b.user_book_id !== userBookId));
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Failed to remove book. Please try again.");
    }
  };

  const updateBook = async (userBookId, newStatus, newRating = null) => {
    try {
      await axios.patch(`${API_BASE}/library/${userBookId}`, {
        status: newStatus,
        ...(newRating !== null && { rating: newRating })
      });

      setLibrary(prev =>
        prev.map(b =>
          b.user_book_id === userBookId
            ? { ...b, status: newStatus, rating: newRating ?? b.rating }
            : b
        )
      );
    } catch (err) {
      console.error("Update failed:", err);
      alert("Failed to update book. Please try again.");
    }
  };

  return (
    <div>
      <section className="nes-container with-title">
        <p className="title">My Library</p>

        <div className="nes-select">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All</option>
            <option value="reading">Reading</option>
            <option value="completed">Completed</option>
            <option value="want_to_read">To Read</option>
          </select>
        </div>
      </section>

      <div className="book-grid">
        {loading ? (
          <p>Loading...</p>
        ) : library.map(book => (
          <div className="book-card nes-container is-rounded" key={book.user_book_id}>
            <img
              src={book.image_url || 'https://placehold.co/128x192?text=No+Cover'}
              alt={book.title}
              onClick={() => navigate(`/book/${book.google_books_id}`)}
              style={{ cursor: 'pointer' }}
            />

            <h3 onClick={() => navigate(`/book/${book.google_books_id}`)}>
              {book.title}
            </h3>

            <div className="nes-field" style={{ marginBottom: '8px' }}>
              <label>Status:</label>
              <div className="nes-select is-small">
                <select
                  value={book.status}
                  onChange={(e) => updateBook(book.user_book_id, e.target.value)}
                >
                  <option value="want_to_read">To Read</option>
                  <option value="reading">Reading</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
            </div>

            <div style={{ marginBottom: '8px' }}>
              <label>Rating:</label>
              <StarRating
                rating={book.rating || 0}
                onChange={(newRating) =>
                  updateBook(book.user_book_id, book.status, newRating)
                }
              />
            </div>

            <button
              className="nes-btn is-error is-small"
              onClick={() => deleteBook(book.user_book_id)}
            >
              Remove
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}