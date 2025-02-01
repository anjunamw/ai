<template>
  <div>
    <h2>Email Integration</h2>
    <button @click="fetchEmails">Fetch Emails</button>
    <div v-if="emails.length > 0">
      <div v-for="email in emails" :key="email.id">
        <h3>{{ email.subject }}</h3>
        <p>From: {{ email.from }}</p>
        <button @click="draftReply(email)">Draft Reply</button>
      </div>
    </div>
    <div v-if="draftedReply">
      <h3>Drafted Reply</h3>
      <MarkdownEditor v-model="draftedReply" />
      <button @click="sendEmail">Send Email</button>
    </div>
    <p v-if="error">{{ error }}</p>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import MarkdownEditor from './MarkdownEditor.vue'
import type { Email } from '../types';

const emails = ref<Email[]>([]);
const draftedReply = ref<string | null>(null);
const error = ref<string | null>(null);
const message = ref<string | null>(null);

const fetchEmails = async () => {
  error.value = null;
  try {
    const response = await axios.get('/api/email/emails');
    emails.value = response.data;
  } catch (err:any) {
    error.value = err.message || 'Failed to fetch emails.';
  }
};
const draftReply = async (email:Email) => {
  error.value = null;
  try {
    const response = await axios.post('/api/email/draft_reply',{emailId: email.id});
    draftedReply.value = response.data.reply;
  } catch (err:any) {
    error.value = err.message || 'Failed to draft a reply';
  }
};
const sendEmail = async () => {
  error.value = null;
  try {
    if(draftedReply.value){
      const response = await axios.post('/api/email/send_reply',{reply:draftedReply.value});
      message.value = response.data.message
      draftedReply.value = null
    }
  } catch(err:any){
    error.value = err.message || 'Failed to send email';
  }
}
</script>