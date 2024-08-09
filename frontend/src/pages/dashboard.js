import { useEffect, useState } from 'react';
import { supabase } from '../utils/supabaseClient';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

export default function Dashboard() {
  const [Email, setEmail] = useState('');
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [location, setLocation] = useState('');
  const [mapSrc, setMapSrc] = useState('');
  const router = useRouter();
  const googleMapsApiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

  useEffect(() => {
    const checkUser = async () => {
      const session = JSON.parse(localStorage.getItem('supabaseSession'));

      if (!session) {
        router.push('/login');
      } else {
        const user = session.user;
        setEmail(user.email);
      }
    };

    checkUser();
  }, [router]);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setMapSrc(`https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=${latitude},${longitude}&zoom=12`);
        },
        (error) => {
          console.error('Error getting location:', error);
          // Default to Canada if location access is denied
          setMapSrc(`https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=56.1304,-106.3468&zoom=4`);
        }
      );
    } else {
      // Default to Canada if Geolocation is not supported
      setMapSrc(`https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=56.1304,-106.3468&zoom=4`);
    }
  }, [googleMapsApiKey]);

  const handleDateChange = (date) => {
    setSelectedDate(date);
    // Add logic to handle the date change, such as fetching data for the selected date
  };

  const handleLocationSearch = async (e) => {
    e.preventDefault();
    if (!location) {
      alert('Please enter a location.');
      return;
    }

    try {
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(location)}&key=${googleMapsApiKey}`
      );
      const data = await response.json();

      console.log('Geocoding response:', data); // Debugging information

      if (data.status === 'OK' && data.results.length > 0) {
        const { lat, lng } = data.results[0].geometry.location;
        setMapSrc(`https://www.google.com/maps/embed/v1/view?key=${googleMapsApiKey}&center=${lat},${lng}&zoom=12`);
      } else {
        alert('Location not found. Please try again.');
      }
    } catch (error) {
      console.error('Error fetching location:', error);
      alert('An error occurred while fetching the location. Please try again.');
    }
  };

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center w-full h-full p-4">
        <div className="w-full max-w-5xl mb-4">
          <DatePicker
            selected={selectedDate}
            onChange={handleDateChange}
            className="w-full px-3 py-2 border rounded"
            dateFormat="yyyy/MM/dd"
          />
        </div>
        <div className="w-full h-full max-w-5xl max-h-96 relative mb-4">
          <iframe
            src={mapSrc}
            width="100%"
            height="450"
            frameBorder="0"
            style={{ border: 0 }}
            allowFullScreen=""
            aria-hidden="false"
            tabIndex="0"
          ></iframe>
          <div className="absolute top-4 right-4 bg-white p-2 rounded shadow legend">
            <span className="low">Low</span>
            <span className="medium">Medium</span>
            <span className="high">High</span>
            <span className="very-high">Very High</span>
            <span className="extreme">Extreme</span>
          </div>
        </div>
        <form onSubmit={handleLocationSearch} className="w-full max-w-5xl flex items-center">
          <input
            type="text"
            className="flex-grow px-3 py-2 border rounded"
            placeholder="Search location"
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
    </Layout>
  );
}
