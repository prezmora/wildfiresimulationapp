import React from 'react';
import MapView from '../components/Map/MapView';
import MapControls from '../components/Map/MapControls';
import Legend from '../components/Map/Legend';

function MapPage() {
  return (
    <div className="map-page">
      <h2>Wildfire Forecast Map</h2>
      <div className="map-container">
        <MapView />
        <MapControls />
        <Legend />
      </div>
    </div>
  );
}

export default MapPage;