# frontend/src/stores/userStore.ts
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        token: localStorage.getItem('token') || null,
    }),
    getters: {
      isLoggedIn: (state) => !!state.token,
    },
    actions: {
      setToken(token: string) {
        this.token = token;
        localStorage.setItem('token', token);
      },
      clearToken() {
        this.token = null;
        localStorage.removeItem('token');
      }
    },
});