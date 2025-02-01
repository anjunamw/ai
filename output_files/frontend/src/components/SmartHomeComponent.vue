# frontend/src/components/SmartHomeComponent.vue
<template>
  <div>
    <h2>Smart Home Integration</h2>
      <button @click="fetchDevices">Fetch Devices</button>
    <div v-if="devices.length > 0">
      <div v-for="device in devices" :key="device.id">
          <h3>{{ device.name }}</h3>
          <p>Status: {{ device.status }}</p>
          <button @click="toggleDevice(device)">Toggle</button>
      </div>
    </div>
      <p v-if="error">{{error}}</p>
        <p v-if="message">{{message}}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import type { SmartHomeDevice } from '../types';

const devices = ref<SmartHomeDevice[]>([]);
const error = ref<string | null>(null);
const message = ref<string | null>(null);

const fetchDevices = async () => {
    error.value = null;
    try {
        const response = await axios.get('/api/smart_home/devices');
        devices.value = response.data
    } catch (err:any) {
        error.value = err.message || 'Failed to fetch devices';
    }
};

const toggleDevice = async (device:SmartHomeDevice) => {
    error.value = null;
  try {
      const response = await axios.post('/api/smart_home/toggle_device', {deviceId: device.id})
      message.value = response.data.message
        fetchDevices();
  } catch (err:any){
    error.value = err.message || 'Failed to toggle device'
  }
}

</script>