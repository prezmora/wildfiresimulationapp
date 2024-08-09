// src/pages/confirm.js
import { useState } from 'react';
import { supabase } from '../utils/supabaseClient';
import { useRouter } from 'next/router';

export default function ConfirmPasswordReset() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleResetPassword = async (e) => {
    e.preventDefault();
    if (!email) {
      alert('Please enter your email address.');
      return;
    }

    setIsLoading(true);

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email);
      setIsLoading(false);

      if (error) {
        alert('Error sending password reset email: ' + error.message);
      } else {
        alert('Password reset email sent! Please check your inbox.');
        router.push('/login');
      }
    } catch (networkError) {
      setIsLoading(false);
      alert('Network error: ' + networkError.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-100">
      <div className="w-full max-w-md bg-white rounded shadow-md p-8">
        <h1 className="text-2xl font-semibold mb-6">Forgot Password</h1>
        <form onSubmit={handleResetPassword}>
          <div className="mb-4">
            <label className="block text-gray-700" htmlFor="email">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              className="w-full px-3 py-2 border rounded"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              aria-required="true"
              aria-describedby="emailHelp"
            />
            <small id="emailHelp" className="text-gray-600">
              We'll send a password reset link to this email.
            </small>
          </div>
          <button
            type="submit"
            className={`w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 ${
              isLoading && 'opacity-50 cursor-not-allowed'
            }`}
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : 'Reset Password'}
          </button>
        </form>
      </div>
    </div>
  );
}
