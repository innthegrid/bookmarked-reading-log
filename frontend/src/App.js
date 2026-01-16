import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/hello')
      .then(res => setMessage(res.data.message))
      .catch(err => setMessage("Backend not reached"));
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Reading Log Tracker</h1>
      <p>Backend Status: <strong>{message}</strong></p>
    </div>
  );
}

export default App;
