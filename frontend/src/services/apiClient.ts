import axios from 'axios'

// Vite uses import.meta.env for environment variables
// Vite environment variables use VITE_ prefix
// Only VITE_SOME_KEY will be exposed as import.meta.env.VITE_SOME_KEY to your client
// See: https://vite.dev/guide/env-and-mode#env-files

// console.log(import.meta.env.VITE_SOME_KEY) // "123"
// console.log(import.meta.env.DB_PASSWORD) // undefined

const defaultUrl = 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || defaultUrl,
  headers: {
    'Content-type': 'application/json',
  },
})

console.log('VITE_BACKEND_URL:', import.meta.env.VITE_BACKEND_URL)
console.log('Using backend API baseURL:', apiClient.defaults.baseURL)

export default apiClient
