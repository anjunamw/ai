// src/main.ts
import './assets/main.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import axios from 'axios';

// Configure Axios base URL (using VITE_API_BASE_URL set via Docker/Vite environment)
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount('#app');