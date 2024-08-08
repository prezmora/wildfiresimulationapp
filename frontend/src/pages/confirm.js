// src/pages/confirm.js
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { supabase } from '../utils/supabaseClient';

export default function Confirm() {
  const router = useRouter();

  useEffect(() => {
    const confirmEmail = async () => {
      const { data: { session }, error } = await supabase.auth.getSessionFromUrl({ storeSession: true });

      if (error || !session) {
        alert('Invalid or expired confirmation link.');
        router.push('/login');
      } else {
        // Save session to local storage if not already done
        localStorage.setItem('supabaseSession', JSON.stringify(session));
        router.push('/dashboard');
      }
    };

    confirmEmail();
  }, [router]);

  return (
    <div className="flex justify-center items-center h-screen">
      <p>Confirming your email...</p>
    </div>
  );
}
