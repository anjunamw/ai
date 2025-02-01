# frontend/src/components/Dashboard.vue
<template>
  <div>
    <h2>Dashboard</h2>
    <p>Welcome to your LLMCoder dashboard!</p>
    <nav>
      <router-link to="/dashboard/notes">Notes</router-link>
      <router-link to="/dashboard/todos">To-Do</router-link>
      <router-link to="/dashboard/email">Email</router-link>
      <router-link to="/dashboard/jira">JIRA</router-link>
      <router-link to="/dashboard/realtime">Real-time</router-link>
       <router-link to="/dashboard/social_media">Social Media</router-link>
       <router-link to="/dashboard/smart_home">Smart Home</router-link>
        <router-link to="/dashboard/travel">Travel</router-link>
        <router-link to="/dashboard/plan">Plan</router-link>
      <router-link to="/dashboard/reports">Reports</router-link>
      <router-link to="/dashboard/settings">Settings</router-link>
    </nav>

    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">

</script>