import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);

  return (
    <div className="App">
      <div className="main-container">
        <header>
          <h1>Bookmarked</h1>
          <p>Reading Log</p>
        </header>

        <main>
          <section className="nes-container with-title">
            <h3 className="title">My Library</h3>
            <p>Time to pick up a book!</p>
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;