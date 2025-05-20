import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user')) || null);
  const [access, setAccess] = useState(() => localStorage.getItem('access') || null);
  const [refresh, setRefresh] = useState(() => localStorage.getItem('refresh') || null);
  const [loading, setLoading] = useState(false);

  // Persist user and tokens in localStorage
  useEffect(() => {
    if (user) localStorage.setItem('user', JSON.stringify(user));
    else localStorage.removeItem('user');
    if (access) localStorage.setItem('access', access);
    else localStorage.removeItem('access');
    if (refresh) localStorage.setItem('refresh', refresh);
    else localStorage.removeItem('refresh');
  }, [user, access, refresh]);

  // Login function (JWT)
  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await api.post('/users/token/', { username: email, password });
      if (res.data.access) {
        setUser(res.data.user);
        setAccess(res.data.access);
        setRefresh(res.data.refresh);
        // Set the token in the default headers for future requests
        api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
      } else {
        throw new Error('No access token received');
      }
    } catch (err) {
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Google login
  const googleLogin = async (token) => {
    setLoading(true);
    try {
      const res = await api.post('/users/google-auth/', { token });
      if (res.data.access) {
        setUser(res.data.user);
        setAccess(res.data.access);
        setRefresh(res.data.refresh);
        // Set the token in the default headers for future requests
        api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`;
      } else {
        throw new Error('No access token received');
      }
    } catch (err) {
      console.error('Google login error:', err.response?.data || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Register function (JWT)
  const register = async (email, password) => {
    setLoading(true);
    try {
      const res = await api.post('/users/register/', { email, password });
      setUser(res.data.user);
      setAccess(res.data.access);
      setRefresh(res.data.refresh);
    } catch (err) {
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Forgot Password
  const forgotPassword = async (email) => {
    setLoading(true);
    try {
      const res = await api.post('/users/forgot-password/', { email });
      return res.data;
    } catch (err) {
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Verify OTP
  const verifyOtp = async (email, otp) => {
    setLoading(true);
    try {
      const res = await api.post('/users/verify-otp/', { email, otp });
      return res.data;
    } catch (err) {
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Set New Password
  const setNewPassword = async (email, otp, newPassword) => {
    setLoading(true);
    try {
      const res = await api.post('/users/set-new-password/', { email, otp, new_password: newPassword });
      return res.data;
    } catch (err) {
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout
  const logout = () => {
    setUser(null);
    setAccess(null);
    setRefresh(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, googleLogin, access, refresh, forgotPassword, verifyOtp, setNewPassword }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext); 