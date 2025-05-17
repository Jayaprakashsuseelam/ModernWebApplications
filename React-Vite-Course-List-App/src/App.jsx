// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import CourseList from './components/CourseList.jsx';
import Enquiries from './components/Enquiries.jsx';

function App() {
  return (
    <Router>
      <div style={{ padding: '20px' }}>
        <nav>
          <Link to="/">Courses</Link> | <Link to="/enquiries">View Enquiries</Link>
        </nav>
        <Routes>
          <Route path="/" element={<CourseList />} />
          <Route path="/enquiries" element={<Enquiries />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
