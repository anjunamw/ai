# frontend/src/components/RealTimeComponent.vue
<template>
  <div>
    <h2>Real-time Communication</h2>
      <p>This section will activate the various real-time components to analyze and display.</p>
    <button @click="startRealTime">Start Realtime</button>
    <button @click="stopRealTime">Stop Realtime</button>
    <p v-if="message">{{ message }}</p>
        <p v-if="error">{{ error }}</p>
  </div>
</template>
<script setup lang="ts">
    import { ref } from 'vue';
    import axios from 'axios';

    const message = ref<string | null>(null);
    const error = ref<string | null>(null);

    const startRealTime = async () => {
       error.value = null;
        try {
            const response = await axios.post('/api/general/start_realtime');
            message.value = response.data.message
        } catch(err:any){
           error.value = err.message || 'Failed to start real-time capture';
        }
    }
  const stopRealTime = async () => {
      error.value = null;
      try {
         const response = await axios.post('/api/general/stop_realtime')
        message.value = response.data.message
      } catch(err:any){
         error.value = err.message || 'Failed to stop real-time capture';
      }
    }

</script>