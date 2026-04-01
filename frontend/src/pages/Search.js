/* src/pages/Search.js */
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  searchBooks,
  getLibrary,
  addBook,
  updateBook
} from "../services/bookService";

const BookResultCard = ({ book, onAdd, onViewDetails, libraryStatus }) => {
  const [status, setStatus] = useState(libraryStatus || "want_to_read");

  useEffect(() => {
    if (libraryStatus) {
      setStatus(libraryStatus);
    }
  }, [libraryStatus]);

  return (
    <div
      className="book-card nes-container is-rounded"
      style={{ display: "flex", flexDirection: "column" }}
    >

      <div
        style={{
          height: "180px",
          display: "flex",
          justifyContent: "center",
          marginBottom: "10px"
        }}
      >
        <img
          src={book.image_url || "https://placehold.co/128x192?text=No+Cover"}
          alt={book.title}
          onClick={() => onViewDetails(book.google_books_id)}
          style={{
            cursor: "pointer",
            maxHeight: "100%",
            width: "auto",
            border: "2px solid black"
          }}
        />
      </div>

      <h3
        onClick={() => onViewDetails(book.google_books_id)}
        style={{
          cursor: "pointer",
          fontSize: "0.8rem",
          marginBottom: "5px",
          minHeight: "2.4rem"
        }}
      >
        {book.title}
      </h3>

      <div className="add-controls" style={{ marginTop: "auto" }}>

        <div className="nes-select is-small">
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="want_to_read">To Read</option>
            <option value="reading">Reading</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        <button
          className={`nes-btn is-small ${
            libraryStatus ? "is-warning" : "is-primary"
          }`}
          onClick={() => onAdd(book, status)}
          style={{ marginTop: "8px", width: "100%" }}
        >
          {libraryStatus ? "Update" : "+ Add"}
        </button>

      </div>
    </div>
  );
};

const Search = ({ userId }) => {

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [libraryMap, setLibraryMap] = useState({});
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const syncLibrary = async () => {
    if (!userId) return;
    const library = await getLibrary(userId);
    const mapping = {};
    library.forEach((item) => {
      if (item.google_books_id) {
        mapping[String(item.google_books_id)] = {
          status: item.status,
          user_book_id: item.user_book_id
        };
      }

    });

    setLibraryMap(mapping);
  };

  useEffect(() => {
    syncLibrary();
  }, [userId]);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await searchBooks(query);
      await syncLibrary();
      setResults(data);
    } catch (err) {
      console.error("Search error:", err);
    }

    setLoading(false);
  };

  const saveBookToLibrary = async (book, status) => {
    const gid = String(book.google_books_id);
    const existing = libraryMap[gid];

    try {
      if (existing) {
        await updateBook(existing.user_book_id, { status });
        setLibraryMap((prev) => ({
          ...prev,
          [gid]: {
            ...existing,
            status
          }
        }));

      } else {
        const res = await addBook({
          user_id: userId,
          google_books_id: gid,
          title: book.title,
          authors: book.authors,
          image_url: book.image_url,
          description: book.description,
          page_count: book.page_count,
          published_year: book.published_year,
          genres: book.genres,
          status
        });

        setLibraryMap((prev) => ({
          ...prev,
          [gid]: {
            status,
            user_book_id: res.user_book_id
          }
        }));

      }

    } catch (err) {
      console.error(err);
      alert("Error saving book.");
    }
  };
  
  return (
    <div className="search-page">
      <section className="nes-container with-title">
        <p className="title">Search Books</p>
        <div style={{ display: "flex", gap: "10px" }}>

          <input
            className="nes-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />

          <button
            className="nes-btn is-primary"
            onClick={handleSearch}
          >
            Search
          </button>

        </div>

      </section>

      <section
        className="book-grid"
        style={{
          marginTop: "20px",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
          gap: "20px"
        }}
      >

        {loading ? (

          <p>Searching...</p>

        ) : (

          results.map((book) => {

            const gid = String(book.google_books_id);

            return (
              <BookResultCard
                key={gid}
                book={book}
                libraryStatus={libraryMap[gid]?.status}
                onAdd={saveBookToLibrary}
                onViewDetails={(gid) => navigate(`/book/${gid}`)}
              />
            );

          })

        )}

      </section>

    </div>
  );
};

export default Search;