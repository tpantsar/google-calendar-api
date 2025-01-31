import axios from 'axios'

// Vite uses import.meta.env for environment variables
const apiClient = axios.create({
  baseURL: import.meta.env.BACKEND_API_URL || 'http://localhost:5000/api',
})

console.log('Using backend API baseURL:', apiClient.defaults.baseURL)

export default apiClient
