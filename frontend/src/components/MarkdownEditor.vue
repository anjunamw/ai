<template>
  <div ref="editorContainer" style="height: 100%; width: 100%;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import * as monaco from 'monaco-editor';
import 'monaco-editor/esm/vs/language/markdown/markdown.contribution';


const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  readOnly: {
    type: Boolean,
    default: false
  }
});
const emit = defineEmits(['update:modelValue', 'change']);


const editorContainer = ref<HTMLElement | null>(null);
let editor: monaco.editor.IStandaloneCodeEditor | null = null;

onMounted(() => {
  if (editorContainer.value) {
    editor = monaco.editor.create(editorContainer.value, {
      value: props.modelValue,
      language: 'markdown',
      readOnly: props.readOnly,
      theme: 'vs-dark'
    });

    editor.onDidChangeModelContent(() => {
      if(editor){
        emit('update:modelValue', editor.getValue());
        emit('change', editor.getValue());
      }
    });
  }
});
watch(() => props.modelValue, (newValue) => {
  if (editor && editor.getValue() !== newValue) {
    editor.setValue(newValue);
  }
});

watch(() => props.readOnly, (newReadOnly) => {
  if (editor) {
    editor.updateOptions({ readOnly: newReadOnly });
  }
});

onBeforeUnmount(() => {
  if (editor) {
    editor.dispose();
    editor = null;
  }
});

</script>