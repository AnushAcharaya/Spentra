import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';

const ProfileModal = ({ open, onClose }) => {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({ name: '', email: '' });
  const [passwords, setPasswords] = useState({ current: '', new: '', confirm: '' });
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  useEffect(() => {
    if (user) setForm({ name: user.name || '', email: user.email || '' });
  }, [user, open]);

  if (!open) return null;

  const handleChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  const handlePwChange = e => setPasswords(p => ({ ...p, [e.target.name]: e.target.value }));

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setMsg(''); setErr('');
    try {
      const res = await api.put('/users/me/', form);
      setUser(res.data);
      setMsg('Profile updated!');
    } catch {
      setErr('Failed to update profile.');
    } finally { setLoading(false); }
  };

  const handlePwSubmit = async e => {
    e.preventDefault();
    setLoading(true); setMsg(''); setErr('');
    if (passwords.new !== passwords.confirm) {
      setErr('Passwords do not match.'); setLoading(false); return;
    }
    try {
      await api.post('/users/change-password/', passwords);
      setMsg('Password changed!');
      setPasswords({ current: '', new: '', confirm: '' });
    } catch {
      setErr('Failed to change password.');
    } finally { setLoading(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-xl shadow-2xl p-6 w-full max-w-lg mx-2 relative animate-fade-in">
        <button onClick={onClose} className="absolute top-3 right-3 p-1 rounded hover:bg-green-100 text-green-700 text-xl">×</button>
        <h1 className="text-2xl font-bold text-green-900 mb-4">User Profile</h1>
        {msg && <div className="mb-4 text-green-700">{msg}</div>}
        {err && <div className="mb-4 text-red-600">{err}</div>}
        <form onSubmit={handleSubmit} className="space-y-4 mb-8">
          <div>
            <label className="block text-green-800 mb-1">Name</label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-green-200 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>
          <div>
            <label className="block text-green-800 mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-green-200 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              disabled
            />
          </div>
          <div className="flex justify-end">
            <button type="submit" className="px-4 py-2 rounded-md bg-green-600 text-white font-semibold hover:bg-green-700" disabled={loading}>Update Profile</button>
          </div>
        </form>
        <form onSubmit={handlePwSubmit} className="space-y-4">
          <h2 className="text-lg font-semibold text-green-800 mb-2">Change Password</h2>
          <div>
            <label className="block text-green-800 mb-1">Current Password</label>
            <input
              type="password"
              name="current"
              value={passwords.current}
              onChange={handlePwChange}
              className="w-full px-3 py-2 border border-green-200 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              required
            />
          </div>
          <div>
            <label className="block text-green-800 mb-1">New Password</label>
            <input
              type="password"
              name="new"
              value={passwords.new}
              onChange={handlePwChange}
              className="w-full px-3 py-2 border border-green-200 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              required
            />
          </div>
          <div>
            <label className="block text-green-800 mb-1">Confirm New Password</label>
            <input
              type="password"
              name="confirm"
              value={passwords.confirm}
              onChange={handlePwChange}
              className="w-full px-3 py-2 border border-green-200 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400"
              required
            />
          </div>
          <div className="flex justify-end">
            <button type="submit" className="px-4 py-2 rounded-md bg-green-600 text-white font-semibold hover:bg-green-700" disabled={loading}>Change Password</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfileModal; 