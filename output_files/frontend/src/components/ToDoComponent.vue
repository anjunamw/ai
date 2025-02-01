# frontend/src/components/ToDoComponent.vue
<template>
    <div>
        <h2>To-Do List</h2>
      <button @click="createTask">Create New Task</button>
        <div v-if="todos.length > 0">
            <div v-for="todo in todos" :key="todo.id">
                <h3>{{ todo.description }}</h3>
                <p>Priority: {{ todo.priority_user_set }}</p>
              <button @click="editTask(todo)">Edit</button>
            </div>
        </div>
      <div v-if="selectedTask">
          <h3>{{ selectedTask.id ? 'Edit Task' : 'New Task' }}</h3>
          <input type="text" placeholder="Description" v-model="selectedTask.description"/>
          <select v-model="selectedTask.priority_user_set">
              <option value="High">High</option>
              <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
          <button @click="saveTask">Save Task</button>
          <button v-if="selectedTask.id" @click="deleteTask">Delete Task</button>
      </div>
        <p v-if="error">{{error}}</p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import type { ToDoItem } from '../types';

const todos = ref<ToDoItem[]>([]);
const selectedTask = ref<ToDoItem | null>(null)
const error = ref<string|null>(null);

const fetchTasks = async () => {
    error.value = null;
  try {
      const response = await axios.get('/api/general/todos');
      todos.value = response.data;
  } catch(err:any){
    error.value = err.message || 'Failed to load tasks';
  }
}
fetchTasks();
const createTask = () => {
    selectedTask.value = { description: '', priority_user_set: 'Medium' }
};
const editTask = (task:ToDoItem) => {
    selectedTask.value = {...task}
};
const saveTask = async () => {
  error.value = null;
  if(selectedTask.value){
    try {
      if(selectedTask.value.id){
         await axios.put(`/api/general/todos/${selectedTask.value.id}`, selectedTask.value);
      } else{
          await axios.post('/api/general/todos',selectedTask.value)
      }
      fetchTasks();
      selectedTask.value = null;
    } catch (err:any){
      error.value = err.message || 'Failed to save task';
    }
  }
}
const deleteTask = async () => {
  error.value = null;
  if(selectedTask.value && selectedTask.value.id){
    try{
       await axios.delete(`/api/general/todos/${selectedTask.value.id}`)
        fetchTasks();
        selectedTask.value = null;
    } catch (err:any){
       error.value = err.message || 'Failed to delete task'
    }
  }
}

</script>