import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import WeatherSummary from '../components/Dashboard/WeatherSummary';
import FireAdvisory from '../components/Dashboard/FireAdvisory';
import Forecast from '../components/Dashboard/Forecast';

const DashboardPage = () => {
  return (
    <div>
      <Header />
      <main>
        <WeatherSummary />
        <FireAdvisory />
        <Forecast />
      </main>
      <Footer />
    </div>
  );
};

export default DashboardPage;
