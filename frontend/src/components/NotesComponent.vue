<template>
  <div>
    <h2>Notes</h2>
    <button @click="createNote">Create New Note</button>
    <div v-if="notes.length > 0">
      <div v-for="note in notes" :key="note.id">
        <h3>{{ note.title }}</h3>
        <button @click="editNote(note)">Edit</button>
      </div>
    </div>
    <div v-if="selectedNote">
      <h3>{{ selectedNote.id ? 'Edit' : 'New' }} Note</h3>
      <input type="text" placeholder="Title" v-model="selectedNote.title"/>
      <MarkdownEditor v-model="selectedNote.content" />
      <button @click="saveNote">Save</button>
      <button v-if="selectedNote.id" @click="deleteNote">Delete</button>
    </div>
    <p v-if="error">{{error}}</p>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import MarkdownEditor from './MarkdownEditor.vue';
import type { Note } from '../types';

const notes = ref<Note[]>([]);
const selectedNote = ref<Note | null>(null);
const error = ref<string | null>(null);

const fetchNotes = async () => {
  error.value = null;
  try {
    const response = await axios.get('/api/general/notes');
    notes.value = response.data
  } catch(err:any){
    error.value = err.message || 'Failed to load notes';
  }
}
fetchNotes();

const createNote = () => {
  selectedNote.value = { title: '', content: '' }
}
const editNote = (note:Note) => {
  selectedNote.value = { ...note }
}
const saveNote = async () => {
  error.value = null;
  if(selectedNote.value){
    try {
      if(selectedNote.value.id){
        await axios.put(`/api/general/notes/${selectedNote.value.id}`, selectedNote.value)
      } else{
        await axios.post(`/api/general/notes`, selectedNote.value)
      }
      fetchNotes();
      selectedNote.value = null
    } catch(err:any){
      error.value = err.message || 'Failed to save note'
    }
  }
}
const deleteNote = async () => {
  error.value = null;
  if (selectedNote.value && selectedNote.value.id) {
    try {
      await axios.delete(`/api/general/notes/${selectedNote.value.id}`)
      fetchNotes();
      selectedNote.value = null;
    } catch (err:any) {
      error.value = err.message || 'Failed to delete note'
    }
  }
};
</script>