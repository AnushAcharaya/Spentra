// src/api/auth.js
import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const loginUser = async (loginData) => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/login/`, {
      email: loginData.username, // assuming the backend expects `email` even though it's called username in the form
      password: loginData.password,
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      throw new Error("Invalid credentials");
    } else if (error.response && error.response.status === 404) {
      throw new Error("User does not exist, please signup first");
    } else {
      throw new Error("Something went wrong, please try again");
    }
  }
};
