<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import Button from 'primevue/button'

defineEmits<{
  generate: []
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center text-center py-16 px-4 space-y-4">
    <Sparkles class="w-12 h-12 text-indigo-300 dark:text-indigo-500" />
    <h2 class="text-xl font-bold text-gray-700 dark:text-gray-200">Você ainda não tem planos de desenvolvimento</h2>
    <p class="text-sm text-gray-500 dark:text-gray-400">Gere seu primeiro plano para começar sua jornada.</p>
    <Button label="Gerar Primeiro Plano" icon="pi pi-sparkles" @click="$emit('generate')" />
  </div>
</template>
