import React from 'react';
import LocationSearch from '../components/Location/LocationSearch';
import CityList from '../components/Location/CityList';

function LocationPage() {
  return (
    <div className="location-page">
      <h2>Find Location</h2>
      <LocationSearch />
      <CityList />
    </div>
  );
}

export default LocationPage;