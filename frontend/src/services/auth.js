// Placeholder for authentication service functions
import { supabase } from '../supabaseClient';

export const signUp = async (email, password) => {
  return await supabase.auth.signUp({ email, password });
};

export const signIn = async (email, password) => {
  return await supabase.auth.signIn({ email, password });
};
