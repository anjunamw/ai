# frontend/src/components/SocialMediaComponent.vue
<template>
  <div>
      <h2>Social Media</h2>
    <button @click="fetchPosts">Fetch Posts</button>
       <div v-if="posts.length > 0">
         <div v-for="post in posts" :key="post.id">
            <h3>{{ post.text }}</h3>
           <p>Created: {{ post.created_at }}</p>
         </div>
       </div>
      <div v-if="draftedPost">
          <h3>Drafted Post</h3>
         <MarkdownEditor v-model="draftedPost"/>
          <button @click="publishPost">Publish</button>
      </div>
    <button @click="draftPost">Draft Post</button>
        <p v-if="error">{{error}}</p>
        <p v-if="message">{{message}}</p>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import type { SocialMediaPost } from '../types';
import MarkdownEditor from './MarkdownEditor.vue';

const posts = ref<SocialMediaPost[]>([]);
const draftedPost = ref<string | null>(null);
const error = ref<string | null>(null);
const message = ref<string | null>(null);

const fetchPosts = async () => {
  error.value = null;
  try {
    const response = await axios.get('/api/social_media/posts');
    posts.value = response.data;
  } catch(err:any){
    error.value = err.message || 'Failed to fetch social media posts';
  }
}
const draftPost = async () => {
  error.value = null;
  try {
    const response = await axios.post('/api/social_media/draft_post');
    draftedPost.value = response.data.post;
  } catch (err:any) {
      error.value = err.message || 'Failed to draft a post'
  }
}
const publishPost = async () => {
  error.value = null;
  if(draftedPost.value){
    try {
      const response = await axios.post('/api/social_media/publish_post',{post:draftedPost.value})
      message.value = response.data.message
      draftedPost.value = null;
    } catch (err:any) {
        error.value = err.message || 'Failed to publish post'
    }
  }
}
</script>