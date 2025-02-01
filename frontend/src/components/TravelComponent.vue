# frontend/src/components/TravelComponent.vue
<template>
  <div>
      <h2>Travel Planning</h2>
    <button @click="searchFlights">Search Flights</button>
      <div v-if="searchResults.length > 0">
        <div v-for="result in searchResults" :key="result.id">
          <h3>Flight to {{result.destination}}</h3>
          <p>Price: {{result.price}}</p>
        </div>
      </div>
        <p v-if="error">{{error}}</p>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import type { TravelResult } from '../types';

const searchResults = ref<TravelResult[]>([]);
const error = ref<string | null>(null);

const searchFlights = async () => {
  error.value = null;
    try{
      const response = await axios.get('/api/travel/flights')
      searchResults.value = response.data
    } catch (err:any){
        error.value = err.message || 'Failed to load flights';
    }
}
</script>