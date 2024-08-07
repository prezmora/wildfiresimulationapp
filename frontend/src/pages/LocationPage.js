import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LocationSearch from '../components/Location/LocationSearch';
import CityList from '../components/Location/CityList';

const LocationPage = () => {
  return (
    <div>
      <Header />
      <main>
        <LocationSearch />
        <CityList />
      </main>
      <Footer />
    </div>
  );
};

export default LocationPage;
