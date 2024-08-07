import React from 'react';
import WeatherSummary from '../components/Dashboard/WeatherSummary';
import FireAdvisory from '../components/Dashboard/FireAdvisory';
import Forecast from '../components/Dashboard/Forecast';

function DashboardPage() {
  return (
    <div className="dashboard-page">
      <h2>Dashboard</h2>
      <WeatherSummary />
      <FireAdvisory />
      <Forecast />
    </div>
  );
}

export default DashboardPage;