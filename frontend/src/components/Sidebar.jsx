import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, useEffect } from 'react';
import {
  BarChart3,
  CreditCard,
  Wallet,
  User,
  FileDown,
  FileUp,
  ChevronLeft,
  ChevronRight,
  HelpCircle,
  Settings,
  LogOut
} from 'lucide-react';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { toast } from 'react-hot-toast';
import api from '../api/api';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { to: '/transactions', label: 'Transactions', icon: CreditCard },
  { to: '/budgets', label: 'Budgets', icon: Wallet },
  { to: '/reports', label: 'Reports', icon: BarChart3 },
  { to: '/profile', label: 'Profile', icon: User },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ className, isOpen, onClose, collapsed, setCollapsed }) {
  const location = useLocation();
  const { user, logout } = useAuth();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setCollapsed(true);
      } else {
        setCollapsed(false);
      }
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Fixed sidebar with fixed width
  const sidebarWidth = collapsed ? 'w-16' : 'w-72';

  const handleExport = async () => {
    setLoading(true);
    try {
      const response = await api.get('/transactions/export-data/');
      
      // Create a blob from the JSON string
      const blob = new Blob([response.data], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `spentra-data-${new Date().toISOString().split('T')[0]}.json`;
      
      document.body.appendChild(link);
      link.click();
      
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast.success('Data exported successfully');
    } catch (error) {
      console.error('Error exporting data:', error);
      toast.error(error.response?.data?.detail || 'Failed to export data');
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type !== 'application/json') {
      toast.error('Please select a JSON file');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      await api.post('/transactions/import-data/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('Data imported successfully');
      window.location.reload();
    } catch (error) {
      console.error('Error importing data:', error);
      toast.error(error.response?.data?.detail || 'Failed to import data');
    } finally {
      setLoading(false);
      event.target.value = '';
    }
  };

  return (
    <div
      className={`
        fixed z-50 inset-y-0 left-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0
        transition-transform duration-300 ease-in-out
        flex flex-col h-full min-h-screen bg-gradient-to-b from-green-600 via-green-400 to-green-100 pb-6 border-r border-green-700 shadow-2xl
        ${sidebarWidth}
        ${className || ''}
      `}
      style={{ maxWidth: collapsed ? '4rem' : '17.5rem' }}
    >
      {/* Close button for mobile */}
      <div className="lg:hidden flex justify-end p-2">
        <button onClick={onClose} className="h-8 w-8 rounded-full bg-white shadow-md flex items-center justify-center border border-gray-200">
          <ChevronLeftIcon className="h-4 w-4" />
        </button>
      </div>
      {/* Logo and Company Name */}
      <div className={`py-6 flex justify-center items-center ${collapsed ? 'px-2' : 'px-4'}`}>
        <div className="flex items-center gap-3">
          <img src="/assets/Logo.png" alt="Logo" className="h-16 w-16 object-contain" />
          {!collapsed && (
            <div>
              <span className="text-lg font-semibold text-green-800">Spentra</span>
              <div className="text-xs text-green-600 font-light">Smart Money, Greener Future</div>
            </div>
          )}
        </div>
      </div>
      {/* Main Navigation */}
      <div className={`py-2 ${collapsed ? 'px-2' : 'px-3'}`}>
        <div className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link key={item.to} to={item.to}>
                <button
                  className={`w-full flex items-center rounded-lg font-medium transition-all duration-200 ${collapsed ? 'justify-center px-0 py-3' : 'justify-start pl-4 py-2'} ${location.pathname === item.to ? 'bg-green-700 text-white font-semibold border-l-4 border-white' : 'hover:bg-green-200 text-white/90 hover:text-green-900'}`}
                  title={collapsed ? item.label : undefined}
                >
                  <Icon className={`h-5 w-5 ${!collapsed && 'mr-3'} ${location.pathname === item.to && 'scale-110'}`} />
                  {!collapsed && item.label}
                </button>
              </Link>
            );
          })}
        </div>
      </div>
      {/* Data Management Section */}
      {!collapsed && (
        <div className="px-4 mt-6">
          <div className="bg-green-50 rounded-xl p-3 shadow-sm border border-green-200">
            <h3 className="text-xs font-semibold text-gray-500 mb-2">Data Management</h3>
            <div className="space-y-1.5">
              <button
                onClick={handleExport}
                disabled={loading}
                className="w-full flex items-center gap-2 rounded px-3 py-2 text-green-900 bg-green-200/60 hover:bg-green-300"
              >
                <FileDown className="mr-2 h-4 w-4" /> Export Data
              </button>
              <label className="w-full flex items-center gap-2 rounded px-3 py-2 text-green-900 bg-green-200/60 hover:bg-green-300 cursor-pointer">
                <FileUp className="mr-2 h-4 w-4" /> Import Data
                <input
                  type="file"
                  accept=".json"
                  onChange={handleImport}
                  disabled={loading}
                  className="hidden"
                />
              </label>
            </div>
          </div>
        </div>
      )}
      {/* Collapsed Data Management Icons */}
      {collapsed && (
        <div className="px-2 mt-6 flex flex-col gap-2 items-center">
          <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm hover:bg-green-100 cursor-pointer" title="Export Data">
            <FileDown className="h-4 w-4 text-green-700" />
          </div>
          <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm hover:bg-green-100 cursor-pointer" title="Import Data">
            <FileUp className="h-4 w-4 text-green-700" />
          </div>
        </div>
      )}
      {/* Support and Help */}
      {!collapsed && (
        <div className="px-3 mt-6">
          <div className="space-y-1">
            <Link to="/help">
              <button className={`w-full flex items-center gap-2 rounded px-3 py-2 font-medium transition-all duration-200 ${location.pathname === '/help' ? 'bg-green-200 text-green-900 font-semibold border-l-4 border-green-600' : 'text-gray-500 hover:bg-green-100'}`}>
                <HelpCircle className="h-4 w-4" /> Help & Support
              </button>
            </Link>
          </div>
        </div>
      )}
      {/* Collapsed Support Icons */}
      {collapsed && (
        <div className="px-2 mt-4 flex flex-col gap-2 items-center">
          <Link to="/help">
            <div className={`w-10 h-10 rounded-full bg-white flex items-center justify-center hover:bg-green-100 cursor-pointer ${location.pathname === '/help' ? 'ring-2 ring-green-600' : ''}`} title="Help & Support">
              <HelpCircle className="h-4 w-4 text-gray-500" />
            </div>
          </Link>
        </div>
      )}
      {/* User Profile */}
      <div className="mt-auto">
        {!collapsed ? (
          <div className="px-3">
            <div className="border-t border-gray-200 pt-3 mb-1">
              <div className="bg-white rounded-lg p-3 shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-green-200 flex items-center justify-center text-green-800 font-semibold shadow-sm flex-shrink-0">
                    {user?.email ? user.email[0].toUpperCase() : 'U'}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium truncate">{user?.email || 'User'}</p>
                    <p className="text-xs text-gray-500 truncate">{user?.email || 'user@example.com'}</p>
                  </div>
                </div>
                <button onClick={logout} className="w-full flex items-center gap-2 rounded px-3 py-2 mt-2 text-gray-500 hover:text-red-600 hover:bg-red-50 font-semibold transition">
                  <LogOut className="h-4 w-4" /> Logout
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="px-2 border-t border-gray-200 pt-3 flex justify-center">
            <div className="w-10 h-10 rounded-full bg-green-200 flex items-center justify-center text-green-800 font-semibold shadow-sm cursor-pointer" title={user?.email || 'User'}>
              {user?.email ? user.email[0].toUpperCase() : 'U'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 