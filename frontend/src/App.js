/* frontend/src/App.js */

import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Search from "./pages/Search";
import BookDetails from "./pages/BookDetails";
import Library from "./pages/Library";
import Statistics from "./pages/Statistics";
import Goals from "./pages/Goals";

import "./App.css";

function App() {
  const userId = 1; // Demo user

  return (
    <Router>
      <div className="App">
        <nav className="top-bar">
          <div className="brand">
            <Link
              to="/"
              style={{ textDecoration: "none", color: "inherit" }}
            >
              <h2 style={{ margin: 0 }}>BOOKMARKED</h2>
            </Link>
          </div>

          <div className="nav-icons">
            <Link to="/" className="nav-link" title="Dashboard">
              <i className="nes-icon is-small heart"></i>
              <span>Home</span>
            </Link>

            <Link to="/library" className="nav-link" title="Library">
              <i className="nes-icon is-small star"></i>
              <span>Library</span>
            </Link>

            <Link to="/stats" className="nav-link" title="Statistics">
              <i className="nes-icon is-small trophy"></i>
              <span>Stats</span>
            </Link>

            <Link to="/goals" className="nav-link" title="Goals">
              <i className="nes-icon is-small coin"></i>
              <span>Goals</span>
            </Link>

            <Link to="/search" className="nav-link" title="Search">
              <i className="nes-icon is-small google"></i>
              <span>Search</span>
            </Link>
          </div>
        </nav>

        <div className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard userId={userId} />} />

            <Route
              path="/search"
              element={<Search userId={userId} />}
            />

            <Route
              path="/library"
              element={<Library userId={userId} />}
            />

            <Route
              path="/stats"
              element={<Statistics userId={userId} />}
            />

            <Route
              path="/goals"
              element={<Goals userId={userId} />}
            />

            <Route
              path="/book/:googleId"
              element={<BookDetails userId={userId} />}
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;