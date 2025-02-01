<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';

const username = ref('');
const password = ref('');
const error = ref<string | null>(null);
const router = useRouter();
const userStore = useUserStore();

const login = async () => {
  error.value = null;
  try {
    const response = await axios.post('/api/auth/login', { username: username.value, password: password.value });
    userStore.setToken(response.data.token);
    await router.push('/');
  } catch (err: any) {
    error.value = err.message || 'Login failed. Please check your credentials.';
  }
};

const isLoggedIn = computed(() => {
  return userStore.isLoggedIn;
})
</script>