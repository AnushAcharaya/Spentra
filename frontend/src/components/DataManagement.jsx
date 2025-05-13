import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';
import { toast } from 'react-hot-toast';
import { ArrowDownTrayIcon, ArrowUpTrayIcon } from '@heroicons/react/24/outline';

const DataManagement = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    try {
      const response = await api.get('/export-data/', {
        responseType: 'blob'
      });
      
      // Create a blob from the response data
      const blob = new Blob([response.data], { type: 'application/json' });
      
      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `spentra-data-${new Date().toISOString().split('T')[0]}.json`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
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

    // Validate file type
    if (file.type !== 'application/json') {
      toast.error('Please select a JSON file');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      await api.post('/import-data/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('Data imported successfully');
      
      // Refresh the page to show updated data
      window.location.reload();
    } catch (error) {
      console.error('Error importing data:', error);
      toast.error(error.response?.data?.detail || 'Failed to import data');
    } finally {
      setLoading(false);
      // Reset the file input
      event.target.value = '';
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-800">Data Management</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Export Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Export Data</h2>
          <p className="text-gray-600 mb-4">
            Download all your transactions, budgets, and settings in JSON format.
          </p>
          <button
            onClick={handleExport}
            disabled={loading}
            className="w-full bg-green-500 text-white px-4 py-2 rounded-lg flex items-center justify-center gap-2 hover:bg-green-600 transition-colors disabled:opacity-50"
          >
            <ArrowDownTrayIcon className="h-5 w-5" />
            {loading ? 'Exporting...' : 'Export Data'}
          </button>
        </div>

        {/* Import Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Import Data</h2>
          <p className="text-gray-600 mb-4">
            Import your data from a previously exported JSON file.
          </p>
          <div className="relative">
            <input
              type="file"
              accept=".json"
              onChange={handleImport}
              disabled={loading}
              className="hidden"
              id="import-file"
            />
            <label
              htmlFor="import-file"
              className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center justify-center gap-2 hover:bg-blue-600 transition-colors disabled:opacity-50 cursor-pointer"
            >
              <ArrowUpTrayIcon className="h-5 w-5" />
              {loading ? 'Importing...' : 'Import Data'}
            </label>
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="mt-8 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Instructions</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-medium text-gray-800">Exporting Data</h3>
            <p className="text-gray-600">
              Click the "Export Data" button to download all your data in JSON format. This includes your transactions, budgets, and settings.
            </p>
          </div>
          <div>
            <h3 className="font-medium text-gray-800">Importing Data</h3>
            <p className="text-gray-600">
              To import data, click the "Import Data" button and select a previously exported JSON file. This will restore your transactions, budgets, and settings.
            </p>
          </div>
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
            <p className="text-yellow-700">
              <strong>Note:</strong> Importing data will replace your current data. Make sure to export your current data before importing if you want to keep it.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DataManagement; 