import React, { useEffect, useState } from 'react';
import supabase from '../../supabaseClient';

const Verification = () => {
  const [isVerified, setIsVerified] = useState(false);

  useEffect(() => {
    const checkVerification = async () => {
      const user = supabase.auth.user();
      if (user && user.email_confirmed_at) {
        setIsVerified(true);
      }
    };

    checkVerification();
  }, []);

  return (
    <div>
      {isVerified ? (
        <p>Your email is verified.</p>
      ) : (
        <p>Please verify your email to access all features.</p>
      )}
    </div>
  );
};

export default Verification;
