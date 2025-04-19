// src/api/registerUser.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/auth/register/'; // Replace with your actual backend URL

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(API_URL, userData);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw error.response.data;
    } else {
      throw new Error('Network error');
    }
  }
};
