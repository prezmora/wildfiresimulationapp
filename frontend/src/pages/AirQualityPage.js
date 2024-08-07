import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import AirQualityGauge from '../components/AirQuality/AirQualityGauge';
import AirQualityForecast from '../components/AirQuality/AirQualityForecast';

const AirQualityPage = () => {
  return (
    <div>
      <Header />
      <main>
        <AirQualityGauge />
        <AirQualityForecast />
      </main>
      <Footer />
    </div>
  );
};

export default AirQualityPage;
