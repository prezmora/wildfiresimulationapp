import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import Header from '../components/Header';
import { supabase } from '../utils/supabaseClient';

const MapWithNoSSR = dynamic(() => import('react-leaflet').then((mod) => mod.Map), { ssr: false });

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch('/api/simulation');
      const result = await response.json();
      setData(result.predictions);
    }
    fetchData();
  }, []);

  return (
    <>
      <Header Email={supabase.auth.user()?.email || 'User'} />
      <div className="p-4">
        <h1 className="text-2xl mb-4">Wildfire Simulation</h1>
        <MapWithNoSSR />
        {/* Render your map or any other UI elements using the data */}
      </div>
    </>
  );
}
