# frontend/src/main.ts
import './assets/main.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import * as monaco from 'monaco-editor';
import 'monaco-editor/esm/vs/editor/editor.main.css';
import axios from 'axios'

const pinia = createPinia();
const app = createApp(App);

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});


app.use(pinia);
app.use(router);

app.mount('#app');