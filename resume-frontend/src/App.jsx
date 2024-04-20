// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ResumeUploader from './components/ResumeUploader';
import RefinedResume from './components/RefinedResume';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Resume Revamper</h1>
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<ResumeUploader />} />
            <Route path="/refined" element={<RefinedResume />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
