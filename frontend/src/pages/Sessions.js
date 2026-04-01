/* frontend/src/pages/Session.js */
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { API_BASE } from '../config';

export default function Sessions({ userId }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchSessions = useCallback(async () => {
    setLoading(true);
    try {
      // The backend filters by user_book_id, but we need all sessions for a user dashboard
      // Note: If you want all sessions for a user, you may need a /api/sessions/user/<id> route
      // For now, this assumes the endpoint returns what the user is allowed to see
      const res = await axios.get(`${API_BASE}/sessions`);
      setSessions(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  return (
    <div className="sessions-page">
      <h2 className="nes-text is-primary">Reading Log</h2>
      <div className="nes-table-responsive">
        <table className="nes-table is-bordered is-centered" style={{ width: '100%' }}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Book</th>
              <th>Pages</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="4">Loading...</td></tr>
            ) : sessions.map((s) => (
              <tr key={s.session_id}>
                <td>{s.session_date}</td>
                <td>{s.book_title}</td>
                <td>{s.pages_read}</td>
                <td>{s.minutes_read}m</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}