import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/components/Header.css';

function Header() {
  return (
    <header className="header">
      <h1>Wildfire Prediction App</h1>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/dashboard">Dashboard</Link></li>
          <li><Link to="/map">Map</Link></li>
          <li><Link to="/air-quality">Air Quality</Link></li>
          <li><Link to="/location">Location</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;