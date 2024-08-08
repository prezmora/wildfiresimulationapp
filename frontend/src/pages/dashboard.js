// src/pages/dashboard.js
import { useEffect, useState } from 'react';
import { supabase } from '../utils/supabaseClient';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import Header from '../components/Header';

export default function Dashboard() {
  const [Email, setEmail] = useState('');
  const router = useRouter();

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

  return (
    <Layout>
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl mb-4">Dashboard</h2>
        {/* Dashboard content goes here */}
      </div>
    </Layout>
  );
}
