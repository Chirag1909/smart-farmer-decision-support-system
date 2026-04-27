import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import jwtDecode from 'jwt-decode';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import './App.css';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    const tok = localStorage.getItem('token');
    if (tok) {
      try {
        const decoded = jwtDecode(tok);
        setUser(decoded);
        setToken(tok);
      } catch (err) {
        localStorage.removeItem('token');
      }
    }
  }, []);

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        {!token ? (
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={<Navigate to="/login" />} />
          </Routes>
        ) : (
          <>
            <nav className="bg-green-600 text-white p-4 shadow-lg">
              <div className="max-w-6xl mx-auto flex justify-between items-center">
                <Link to="/dashboard" className="text-2xl font-bold flex items-center">
                  🌾 Crop Decision Support
                </Link>
                <div className="flex items-center space-x-4">
                  <span>Welcome, {user?.sub || 'Farmer'}</span>
                  <button onClick={logout} className="bg-red-500 px-4 py-1 rounded hover:bg-red-600">
                    Logout
                  </button>
                </div>
              </div>
            </nav>
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
          </>
        )}
      </div>
    </Router>
  );
};

export default App;

