import React from 'react';
import MapView from '../components/Map/MapView';
import Legend from '../components/Map/Legend';
import MapControls from '../components/Map/MapControls';

const MapPage = () => {
  return (
    <div>
      <MapControls />
      <Legend />
      <MapView />
    </div>
  );
};

export default MapPage;
