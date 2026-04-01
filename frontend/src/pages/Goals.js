/* frontend/src/pages/Goals.js */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE } from "../config";

export default function Goals({ userId }) {
  const [goals, setGoals] = useState([]);

  // form state
  const [periodType, setPeriodType] = useState("yearly");
  const [target, setTarget] = useState("");
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchGoals = async () => {
    try {
      const res = await axios.get(`${API_BASE}/goals`, {
        params: { user_id: userId }
      });
      setGoals(res.data);
    } catch (err) {
      console.error("Goals error:", err);
    }
  };

  useEffect(() => {
    fetchGoals();
  }, [userId]);

  const createGoal = async () => {
    if (!target || !year || (periodType === "monthly" && !month)) {
      alert("Please fill all required fields.");
      return;
    }

    try {
      setLoading(true);

      await axios.post(`${API_BASE}/goals`, {
        user_id: userId,
        period_type: periodType,
        target_value: parseInt(target),
        year: parseInt(year),
        ...(periodType === "monthly" && { month: parseInt(month) })
      });

      // reset form
      setTarget("");
      setMonth("");

      await fetchGoals();

    } catch (err) {
      console.error("Create goal failed:", err);
      alert("Failed to create goal.");
    } finally {
      setLoading(false);
    }
  };

  const deleteGoal = async (goalId) => {
    if (!window.confirm("Delete this goal?")) return;

    try {
      await axios.delete(`${API_BASE}/goals/${goalId}`);
      setGoals(prev => prev.filter(g => g.goal_id !== goalId));
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  const formatLabel = (g) => {
    if (g.period_type === "yearly") {
      return `Read ${g.target_value} books in ${g.year}`;
    } else {
      const monthName = new Date(0, g.month - 1).toLocaleString("default", {
        month: "long"
      });
      return `Read ${g.target_value} books in ${monthName} ${g.year}`;
    }
  };

  return (
    <div className="nes-container with-title is-rounded">
      <p className="title">Reading Goals</p>

      {/* CREATE GOAL */}
      <div className="nes-container is-rounded" style={{ marginBottom: "20px" }}>
        <p><b>Create Goal</b></p>

        <div
          style={{
            display: "flex",
            gap: "10px",
            alignItems: "center"
          }}
        >
          {/* TYPE */}
          <div className="nes-select" style={{ flex: 1 }}>
            <select
              value={periodType}
              onChange={(e) => setPeriodType(e.target.value)}
            >
              <option value="yearly">Yearly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>

          {/* TARGET */}
          <input
            className="nes-input"
            type="number"
            placeholder="Target"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            style={{ flex: 1 }}
          />

          {/* YEAR */}
          <input
            className="nes-input"
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            style={{ flex: 1 }}
          />

          {/* MONTH (inline, next to year) */}
          {periodType === "monthly" && (
            <div className="nes-select" style={{ flex: 1 }}>
              <select
                value={month}
                onChange={(e) => setMonth(e.target.value)}
              >
                <option value="">Month</option>
                {Array.from({ length: 12 }, (_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {new Date(0, i).toLocaleString("default", {
                      month: "short"
                    })}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* BUTTON */}
          <button
            className="nes-btn is-primary"
            onClick={createGoal}
            disabled={loading}
            style={{ flex: 1 }}
          >
            {loading ? "Adding..." : "Add"}
          </button>
        </div>
      </div>

      {/* GOALS LIST */}
      {goals.length === 0 ? (
        <p>No goals set yet.</p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
          {goals.map((g) => (
            <div key={g.goal_id} className="nes-container is-rounded">

              <p><b>{formatLabel(g)}</b></p>

              <p style={{ fontSize: "0.8rem" }}>
                Progress: {g.completed} / {g.target_value} ({g.progress_percent}%)
              </p>

              <progress
                className="nes-progress is-primary"
                value={g.progress_percent}
                max="100"
              />

              <button
                className="nes-btn is-error is-small"
                style={{ marginTop: "10px" }}
                onClick={() => deleteGoal(g.goal_id)}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}