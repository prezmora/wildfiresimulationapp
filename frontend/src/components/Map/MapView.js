import React, { useEffect } from 'react';
import atlas from 'azure-maps-control';

const MapView = () => {
  useEffect(() => {
    const map = new atlas.Map('map', {
      center: [-123.121, 49.2827],
      zoom: 10,
      language: 'en-US',
      authOptions: {
        authType: 'subscriptionKey',
        subscriptionKey: 'YOUR_AZURE_MAPS_SUBSCRIPTION_KEY'
      }
    });

    map.events.add('ready', function () {
      map.controls.add(new atlas.control.ZoomControl(), {
        position: 'top-right'
      });
    });
  }, []);

  return <div id="map" style={{ width: '100%', height: '500px' }}></div>;
};

export default MapView;
