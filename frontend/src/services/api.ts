import axios from 'axios';
import { Experiment } from '../types/types';

const BASE_URL = 'http://localhost:8000/api';
console.log('API Base URL:', BASE_URL);

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
  validateStatus: (status) => status < 500,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.code === 'ECONNREFUSED') {
      throw new Error('Cannot connect to server. Please ensure the backend is running.');
    }
    throw error;
  }
);

export const submitPrompt = async (data: { prompt: string; systemPrompt: string; models: string[] }) => {
  try {
    const response = await api.post('/experiments', data);
    return response.data;
  } catch (error) {
    console.error('Error submitting prompt:', error);
    throw error;
  }
};

export const getExperiments = async (): Promise<Experiment[]> => {
  try {
    const response = await api.get('/experiments');
    return response.data;
  } catch (error) {
    console.error('Error fetching experiments:', error);
    throw error;
  }
};

export default api;