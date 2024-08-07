import React, { useEffect } from 'react';
import { AzureMapsProvider, AzureMap } from 'react-azure-maps';

function MapView() {
  useEffect(() => {
    // Initialize map and add layers here
  }, []);

  return (
    <AzureMapsProvider>
      <AzureMap options={{
        center: [-110, 50],
        zoom: 4,
        style: 'night'
      }} />
    </AzureMapsProvider>
  );
}

export default MapView;