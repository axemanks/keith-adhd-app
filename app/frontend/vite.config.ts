import react from '@vitejs/plugin-react'
import { dirname, resolve } from 'path'
import { fileURLToPath } from 'url'
import { defineConfig } from 'vite'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: resolve(__dirname, '../backend/static'),
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
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
