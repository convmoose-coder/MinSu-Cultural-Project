import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  root: resolve(__dirname),
  base: '/admin/',
  build: {
    outDir: resolve(__dirname, 'dist/admin'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'admin.html')
      }
    }
  },
  server: {
    port: 5174,
    strictPort: true,
    host: '0.0.0.0'
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
})