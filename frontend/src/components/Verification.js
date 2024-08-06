import React, { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';

const Verification = () => {
  const [isVerified, setIsVerified] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const checkUser = async () => {
      const user = supabase.auth.user();
      if (user) {
        setIsVerified(user.email_confirmed_at);
        setMessage(user.email_confirmed_at ? 'Email verified!' : 'Email not verified. Please check your inbox.');
      } else {
        setMessage('No user logged in.');
      }
    };

    checkUser();
  }, []);

  return (
    <div>
      <h2>Email Verification</h2>
      <p>{message}</p>
    </div>
  );
};

export default Verification;
