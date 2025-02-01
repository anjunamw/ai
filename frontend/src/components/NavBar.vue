<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
    <router-link v-if="isLoggedIn" to="/dashboard">Dashboard</router-link>
    <button v-if="isLoggedIn" @click="logout">Logout</button>
    <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';

const userStore = useUserStore();
const router = useRouter();

const isLoggedIn = computed(() => userStore.isLoggedIn);

const logout = () => {
  userStore.clearToken();
  router.push('/login');
};
</script>