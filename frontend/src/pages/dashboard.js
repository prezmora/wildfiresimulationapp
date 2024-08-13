import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { supabase } from '../utils/supabaseClient';

export default function Dashboard() {
  const [selectedDate, setSelectedDate] = useState(() => {
    return new Date(2023, 9, 30); // Set the initial date to January 1, 2024
  });
  const [location, setLocation] = useState('');
  const [email, setEmail] = useState('');
  const [mapSrc, setMapSrc] = useState('');
  const [historicalData, setHistoricalData] = useState([]); // State to store historical data
  const [predictions, setPredictions] = useState([]); // State to store predictions
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
  }, [router]);

  useEffect(() => {
    const fetchHistoricalData = async () => {
      try {
        // Fetch historical data from the backend
        const response = await fetch(`${backendUrl}/api/historical-data?date=${selectedDate.toISOString().split('T')[0]}`);
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        setHistoricalData(data.queried_data || []);
        console.log('Historical Data:', data);

        // Now fetch the predictions based on the historical data
        fetchPredictions(data.queried_data || []);
      } catch (error) {
        console.error('Error fetching historical data:', error);
      }
    };

    fetchHistoricalData();
  }, [selectedDate]);

  const fetchPredictions = async (historicalData) => {
    try {
      // Attempt to fetch predictions from the model_predict API
      const response = await fetch(`${backendUrl}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ historical_data: historicalData }), // Send historical data to the API
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      if (data && data.predictions && data.predictions.length > 0) {
        setPredictions(data.predictions); // Use dynamic data if available
        updateMapMarkers(data.predictions); // Update the map with new markers
        setMessage(''); // Clear any previous message
      } else {
        setPredictions([]); // Clear predictions
        setMessage('No predictions available for the selected date.'); // Set message
        updateMapMarkers([]); // Clear markers on the map
      }
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setPredictions([]); // Clear predictions
      setMessage('Error fetching predictions. Please try again later.'); // Set error message
      updateMapMarkers([]); // Clear markers on the map
    }
  };

  const handleDateChange = (date) => {
    setSelectedDate(date);
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
      setMapSrc(
        `https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=${matchedPrediction.lat},${matchedPrediction.lon}&zoom=12&markers=${matchedPrediction.lat},${matchedPrediction.lon}`
      );
    } else {
      // Fallback to a generic Google Maps search if locality is not found
      try {
        const response = await fetch(
          `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(
            location
          )}&key=${googleMapsApiKey}`
        );
        const data = await response.json();

        if (data.status === 'OK') {
          const { lat, lon } = data.results[0].geometry.location;
          setMapSrc(
            `https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=${lat},${lon}&zoom=12&markers=${lat},${lon}`
          );
        } else {
          alert('Location not found. Please try again.');
        }
      } catch (error) {
        alert('An error occurred while fetching the location. Please try again.');
      }
    }
  };

  const updateMapMarkers = (predictions) => {
    if (predictions.length > 0) {
      // Construct the markers from predictions
      const markers = predictions.map((prediction) => `${prediction.lat},${prediction.lon}`).join('|');
      setMapSrc(
        `https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=56.1304,-106.3468&zoom=4&markers=${markers}`
      );
    } else {
      setMapSrc(
        `https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=56.1304,-106.3468&zoom=4`
      );
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
        <div className="map-container" style={{ position: 'relative', width: '100%', height: '500px' }}>
          <iframe
            src={setMapSrc}
            width="100%"
            height="100%"
            frameBorder="0"
            style={{ border: 0 }}
            allowFullScreen=""
            aria-hidden="false"
            tabIndex="0"
          ></iframe>
          <div className="legend">
            <span className="low">Low</span>
            <span className="medium">Medium</span>
            <span class="high">High</span>
            <span className="very-high">Very High</span>
            <span className="extreme">Extreme</span>
          </div>
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
        <div>
          {/* Example of rendering markers or other data points on the map */}
          {predictions.map((prediction, index) => (
            <div key={index}>
              <p>Time: {prediction.time_idx}, Locality: {prediction.locality}, Lat: {prediction.lat}, Lon: {prediction.lon}, Prediction: {prediction.prediction}</p>
              {/* You can use this data to add markers to Google Maps or other visualizations */}
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
