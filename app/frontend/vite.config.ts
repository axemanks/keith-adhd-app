import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, '../backend/static'),
    emptyOutDir: true,
    // Generate assets with hash for cache busting
    assetsDir: 'assets',
    // Generate source maps for production
    sourcemap: true,
  },
  // Configure the development server
  server: {
    port: 5173,
    // Proxy API requests to the backend
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
