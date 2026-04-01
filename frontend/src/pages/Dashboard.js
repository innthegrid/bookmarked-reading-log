/* frontend/src/pages/Dashboard.js */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { API_BASE } from '../config';

const Dashboard = ({ userId }) => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [goalProgress, setGoalProgress] = useState(null);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [dashRes, goalRes] = await Promise.all([
          axios.get(`${API_BASE}/dashboard`, { params: { user_id: userId } }),
          axios.get(`${API_BASE}/goals/progress`, { params: { user_id: userId } })
        ]);

        setSummary(dashRes.data);
        setGoalProgress(goalRes.data);
      } catch (err) {
        console.error("Dashboard error", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAll();
  }, [userId]);

  if (loading) {
    return (
      <div className="main-content">
        <p>Loading your library...</p>
      </div>
    );
  }

  const stats = summary?.stats || {};

  return (
    <div className="dashboard">
      <section className="nes-container with-title is-centered">
        <p className="title">Welcome back!</p>
        <p>Keep the story going.</p>
      </section>

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '1rem' }}>

        <div className="nes-container is-rounded" style={{ flex: 1, minWidth: '250px' }}>
          <p style={{ fontSize: '1.2rem' }}>Reading Stats</p>

          <ul className="nes-list is-disc">
            <li>Books Completed: {stats.books_completed || 0}</li>
            <li>Total Books: {stats.total_books || 0}</li>
            <li>Pages Read: {stats.total_pages_read || 0}</li>
            <li>Avg Rating: {stats.average_rating || 0} / 5</li>
          </ul>

          <div style={{ marginTop: '15px' }}>
            <p style={{ fontSize: '0.8rem' }}>
              {goalProgress?.label}
            </p>

            <progress
              className="nes-progress is-success"
              value={goalProgress?.percent || 0}
              max="100"
            />

            <p style={{ fontSize: '0.7rem', marginTop: '5px' }}>
              {goalProgress
                ? `${goalProgress.completed}/${goalProgress.target} books (${goalProgress.percent}%)`
                : "Set a goal to track progress"}
            </p>
          </div>
        </div>

        <div className="nes-container is-rounded" style={{ flex: 2, minWidth: '300px' }}>
          <p style={{ fontSize: '1.2rem' }}>Currently Reading</p>

          <div style={{
            display: 'flex',
            gap: '15px',
            flexWrap: 'wrap',
            justifyContent: 'center'
          }}>
            {summary?.currently_reading?.length > 0 ? (
              summary.currently_reading.map(book => (
                <div key={book.user_book_id} style={{ width: '120px', textAlign: 'center' }}>
                  <div className="nes-container is-rounded is-centered" style={{ padding: '10px' }}>
                    <img
                      src={book.image_url}
                      alt={book.title}
                      style={{ width: '80px', height: '110px', objectFit: 'cover' }}
                    />
                  </div>

                  <p style={{
                    fontSize: '0.7rem',
                    marginTop: '5px',
                    height: '2.4em',
                    overflow: 'hidden'
                  }}>
                    {book.title}
                  </p>
                </div>
              ))
            ) : (
              <p>No books currently reading.</p>
            )}
          </div>
        </div>
      </div>

      <section style={{ marginTop: '2rem', textAlign: 'center' }}>
        <Link to="/search" className="nes-btn is-primary">
          Find a New Book
        </Link>
      </section>
    </div>
  );
};

export default Dashboard;