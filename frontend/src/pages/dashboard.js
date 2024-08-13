import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { supabase } from '../utils/supabaseClient';

export default function Dashboard() {
  const [selectedDate, setSelectedDate] = useState(() => {
    return new Date(2023, 9, 30); // Set the initial date
  });
  const [location, setLocation] = useState('');
  const [email, setEmail] = useState('');
  const [predictions, setPredictions] = useState([]); // State to store predictions
  const [map, setMap] = useState(null); // Store map instance
  const [message, setMessage] = useState(''); // State to store messages (e.g., no predictions)
  const router = useRouter();
  const googleMapsApiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000'; // Use environment variable for flexibility

  useEffect(() => {
    const checkUser = async () => {
      const { data: { session }, error } = await supabase.auth.getSession();

      if (error || !session) {
        router.push('/login');
      } else {
        setEmail(session.user.email);
      }
    };

    checkUser();

    // Load Google Maps script dynamically
    if (!window.google) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}`;
      script.async = true;
      script.defer = true;
      document.head.appendChild(script);
      script.onload = () => {
        initializeMap([]); // Initialize the map when the script is loaded
      };
    } else {
      initializeMap([]); // Initialize the map immediately if the script is already loaded
    }
  }, [router]);

  const handleDateChange = (date) => {
    setSelectedDate(date);
    // Re-fetch predictions when the date changes
    fetchDataAndPredictions(date);
  };

  const handleLocationSearch = async (e) => {
    e.preventDefault();
    if (!location) {
      alert('Please enter a location.');
      return;
    }

    // Check if the location matches any locality from the predictions
    const matchedPrediction = predictions.find(prediction => prediction.locality.toLowerCase() === location.toLowerCase());

    if (matchedPrediction) {
      // Update map based on the matched locality's lat and lon
      const mapOptions = {
        center: { lat: matchedPrediction.lat, lng: matchedPrediction.lon },
        zoom: 12,
      };
      if (map) {
        map.setOptions(mapOptions);
        clearMarkers(); // Clear existing markers
        addMarker({ lat: matchedPrediction.lat, lng: matchedPrediction.lon }, map); // Add new marker
      }
      setMessage(`Prediction: ${matchedPrediction.prediction}`);
    } else {
      alert('Location not found in predictions. Please try again.');
    }
  };

  const fetchDataAndPredictions = async (date) => {
    try {
      // Fetch historical data and predictions from the backend
      const response = await fetch(`${backendUrl}/api/historical-data?date=${date.toISOString().split('T')[0]}`);
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();

      if (data && data.predictions && data.predictions.length > 0) {
        setPredictions(data.predictions); // Use dynamic data if available
        setMessage(''); // Clear any previous message
        initializeMap(data.predictions); // Initialize map with predictions
      } else {
        setPredictions([]); // Clear predictions
        setMessage('No wildfire predictions available for the selected date.'); // Set message
        initializeMap([]); // Initialize blank map
      }
    } catch (error) {
      console.error('Error fetching data or predictions:', error);
      setPredictions([]); // Clear predictions
      setMessage('Error fetching data or predictions.'); // Set error message
      initializeMap([]); // Initialize blank map
    }
  };

  const initializeMap = (predictions) => {
    const canadaCenter = { lat: 56.1304, lng: -106.3468 };

    // Initialize the map
    const mapOptions = {
      center: canadaCenter,
      zoom: 4,
    };

    if (!map) {
      const mapInstance = new google.maps.Map(document.getElementById('map'), mapOptions);
      setMap(mapInstance);
      addMarkers(predictions, mapInstance); // Add markers to the newly created map instance
    } else {
      clearMarkers(); // Clear any existing markers if map is already initialized
      addMarkers(predictions, map); // Add new markers
    }
  };

  const addMarker = (position, mapInstance) => {
    return new google.maps.Marker({
      position: position,
      map: mapInstance,
    });
  };

  const addMarkers = (predictions, mapInstance) => {
    const markers = predictions.map(prediction => {
      return addMarker({ lat: prediction.lat, lng: prediction.lon }, mapInstance);
    });

    // Save markers to map instance for future reference
    mapInstance.markers = markers;
  };

  const clearMarkers = () => {
    if (map && map.markers) {
      map.markers.forEach(marker => marker.setMap(null));
      map.markers = [];
    }
  };

  return (
    <Layout>
      <div className="relative w-full h-full">
        <div className="date-picker-wrapper">
          <DatePicker
            selected={selectedDate}
            onChange={handleDateChange}
            className="px-3 py-2 border rounded"
            dateFormat="yyyy/MM/dd"
            maxDate={new Date()}
          />
        </div>
        <div>
          <form onSubmit={handleLocationSearch} className="w-full flex items-center mt-4">
            <input
              type="text"
              className="flex-grow px-3 py-2 border rounded"
              placeholder="Search locality"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
            <button
              type="submit"
              className="ml-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Search
            </button>
          </form>
        </div>
        {message && <p className="text-red-500 mt-4">{message}</p>} {/* Display message if no predictions */}
        <div id="map" className="map-container" style={{ position: 'relative', width: '100%', height: '500px' }}></div>
        <div>
          {predictions.map((prediction, index) => (
            <div key={index}>
              <p>Time: {prediction.time_idx}, Locality: {prediction.locality}, Lat: {prediction.lat}, Lon: {prediction.lon}, Prediction: {prediction.prediction}</p>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
