import React, { useEffect, useRef } from 'react';
import * as atlas from 'azure-maps-control';

const AzureMap = () => {
  const mapRef = useRef(null);

  useEffect(() => {
    const map = new atlas.Map(mapRef.current, {
      center: [-106.3468, 56.1304], // Center on Canada
      zoom: 4,
      language: 'en-US',
      authOptions: {
        authType: 'subscriptionKey',
        subscriptionKey: process.env.REACT_APP_AZURE_MAPS_KEY
      }
    });

    map.events.add('ready', function () {
      new atlas.HtmlMarker({
        color: 'DodgerBlue',
        text: '1',
        position: [-106.3468, 56.1304]
      }).setMap(map);
    });

    return () => {
      map.dispose();
    };
  }, []);

  return (
    <div ref={mapRef} style={{ width: '100%', height: '600px' }}></div>
  );
};

export default AzureMap;
