/* frontend/src/pages/Statistics.js */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE } from "../config";

export default function Statistics({ userId }) {
  const [report, setReport] = useState(null);
  const [filters, setFilters] = useState({
    year: "all",
    month: "all",
    author_id: "",
    genre_id: ""
  });
  const [options, setOptions] = useState({
    authors: [],
    genres: [],
    years: [],
    months: []
  });

  useEffect(() => {
    axios
      .get(`${API_BASE}/stats/filter-options`, {
        params: { user_id: userId }
      })
      .then((res) => setOptions(res.data))
      .catch((err) =>
        console.error("Failed to load filter options:", err)
      );
  }, [userId]);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/stats`, {
        params: { user_id: userId, ...filters }
      });
      setReport(res.data);
    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [userId, filters]);

  if (!report) return <p>Loading stats...</p>;

  return (
    <div className="nes-container with-title is-rounded">
      <p className="title">Reading Report</p>

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px",
          flexWrap: "wrap"
        }}
      >
        <div className="nes-select">
          <select
            value={filters.year}
            onChange={(e) =>
              setFilters({ ...filters, year: e.target.value })
            }
          >
            <option value="all">All Years</option>
            {options.years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>

        <div className="nes-select">
          <select
            value={filters.month}
            onChange={(e) =>
              setFilters({ ...filters, month: e.target.value })
            }
          >
            <option value="all">All Months</option>
            {options.months.map((m) => (
              <option key={m.val} value={m.val}>
                {m.name}
              </option>
            ))}
          </select>
        </div>

        <div className="nes-select">
          <select
            value={filters.author_id}
            onChange={(e) =>
              setFilters({ ...filters, author_id: e.target.value })
            }
          >
            <option value="">All Authors</option>
            {options.authors.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name}
              </option>
            ))}
          </select>
        </div>

        <div className="nes-select">
          <select
            value={filters.genre_id}
            onChange={(e) =>
              setFilters({ ...filters, genre_id: e.target.value })
            }
          >
            <option value="">All Genres</option>
            {options.genres.map((g) => (
              <option key={g.id} value={g.id}>
                {g.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="nes-container is-inset">
        <ul className="nes-list is-disc">
          <li>Books Finished: {report.aggregates.total_books_finished}</li>
          <li>Total Pages: {report.aggregates.total_pages_read}</li>
          <li>Avg Rating: {report.aggregates.average_rating} / 5</li>
        </ul>
      </div>

      <table
        className="nes-table is-bordered is-centered"
        style={{ width: "100%", marginTop: "20px" }}
      >
        <thead>
          <tr>
            <th>Title</th>
            <th>Finished Date</th>
            <th>Pages</th>
            <th>Rating</th> {/* ✅ NEW */}
          </tr>
        </thead>
        <tbody>
          {report.completed_books.map((book, idx) => (
            <tr key={idx}>
              <td>{book.title}</td>
              <td>{book.finish_date}</td>
              <td>{book.pages}</td>
              <td>{book.rating ? `${book.rating}/5` : "-"}</td> {/* ✅ NEW */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}