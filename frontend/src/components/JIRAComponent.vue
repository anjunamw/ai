<template>
  <div>
    <h2>JIRA Integration</h2>
    <button @click="fetchIssues">Fetch JIRA Issues</button>
    <div v-if="issues.length > 0">
      <div v-for="issue in issues" :key="issue.id">
        <h3>{{ issue.key }}: {{ issue.summary }}</h3>
        <p>Status: {{ issue.status }}</p>
        <button @click="draftComment(issue)">Draft Comment</button>
      </div>
    </div>
    <div v-if="draftedComment">
      <h3>Drafted Comment</h3>
      <MarkdownEditor v-model="draftedComment"/>
      <button @click="addComment">Add Comment</button>
    </div>
    <p v-if="error">{{ error }}</p>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import MarkdownEditor from './MarkdownEditor.vue';
import type { JIRAIssue } from '../types';


const issues = ref<JIRAIssue[]>([]);
const draftedComment = ref<string | null>(null);
const error = ref<string | null>(null);
const message = ref<string | null>(null);

const fetchIssues = async () => {
  error.value = null;
  try {
    const response = await axios.get('/api/jira/issues');
    issues.value = response.data;
  } catch (err:any) {
    error.value = err.message || 'Failed to fetch JIRA issues.';
  }
};
const draftComment = async (issue:JIRAIssue) => {
  error.value = null;
  try {
    const response = await axios.post('/api/jira/draft_comment',{issueId: issue.id})
    draftedComment.value = response.data.comment
  } catch(err:any){
    error.value = err.message || 'Failed to draft a comment'
  }
}
const addComment = async () => {
  error.value = null;
  try {
    if(draftedComment.value){
      const response = await axios.post('/api/jira/add_comment',{comment:draftedComment.value})
      message.value = response.data.message
      draftedComment.value = null;
    }
  } catch (err:any){
    error.value = err.message || 'Failed to add a comment'
  }
}
</script>