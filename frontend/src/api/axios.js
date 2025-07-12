import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Ajusta si usas otro puerto/backend
});

export default instance;