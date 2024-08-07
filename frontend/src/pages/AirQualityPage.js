import React from 'react';
import AirQualityGauge from '../components/AirQuality/AirQualityGauge';
import AirQualityForecast from '../components/AirQuality/AirQualityForecast';

function AirQualityPage() {
  return (
    <div className="air-quality-page">
      <h2>Air Quality</h2>
      <AirQualityGauge />
      <AirQualityForecast />
    </div>
  );
}

export default AirQualityPage;