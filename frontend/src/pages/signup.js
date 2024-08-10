import { useEffect, useState } from 'react';
import { supabase } from '../utils/supabaseClient';
import { useRouter } from 'next/router';

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession();
        if (error) throw error;
        
        if (session) {
          // Redirect to the notification prompt page instead of directly to the dashboard
          router.push('/NotificationPrompt');
        } else {
          router.push('/login');
        }
      } catch (error) {
        console.error('Error checking session:', error.message);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

   
