import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/recipe': 'http://127.0.0.1:5000', // Replace with your Flask server URL
    },
  },
})
