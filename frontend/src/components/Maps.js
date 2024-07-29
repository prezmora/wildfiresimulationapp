import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

const Map = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.post('/api/predict', { inputs: /* your inputs here */ });
      setPredictions(response.data.prediction);
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Fire Behavior Map</h1>
      <MapContainer center={[56.1304, -106.3468]} zoom={4} style={{ height: '600px', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {predictions.map((prediction, index) => (
          <Marker key={index} position={[prediction.lat, prediction.lon]}>
            <Popup>
              Fire Intensity: {prediction.intensity}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default Map;
