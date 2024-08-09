import { useState } from 'react';
import { supabase } from '../utils/supabaseClient';
import { useRouter } from 'next/router';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [location, setLocation] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleSignup = async (e) => {
    e.preventDefault();
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      alert('Error signing up: ' + error.message);
    } else {
      alert('Signup successful! Please check your email for confirmation.');
      router.push('/login');
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-100">
      <div className="w-full max-w-md bg-white rounded shadow-md p-8">
        <form onSubmit={handleSignup}>
          <div className="mb-4">
            <label className="block text-gray-700">Email Address</label>
            <input
              type="email"
              className="w-full px-3 py-2 border rounded"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Location</label>
            <input
              type="text"
              className="w-full px-3 py-2 border rounded"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700">Password</label>
            <input
              type="password"
              className="w-full px-3 py-2 border rounded"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-black text-white py-2 rounded hover:bg-gray-800"
          >
            Sign Up
          </button>
        </form>
        <div className="mt-4 text-center">
          <p>
            if you have an existing account, please{' '}
            <a
              href="/login"
              className="text-black hover:underline"
              onClick={(e) => {
                e.preventDefault();
                router.push('/login');
              }}
            >
              login
            </a>{' '}
            here.
          </p>
        </div>
      </div>
    </div>
  );
}
