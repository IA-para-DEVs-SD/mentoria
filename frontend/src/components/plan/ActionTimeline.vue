<script setup lang="ts">
import type { Action } from '@/types'
import ActionItem from './ActionItem.vue'
import Button from 'primevue/button'
import { Target } from 'lucide-vue-next'

defineProps<{
  actions: Action[]
  generatingMore?: boolean
}>()

defineEmits<{
  toggle: [actionId: string]
  delete: [actionId: string]
  'generate-more': []
}>()
</script>

<template>
  <div class="space-y-4">
    <h3 class="font-bold text-gray-900 flex items-center gap-2">
      <Target class="w-4 h-4 text-indigo-600" /> Plano de Ação
    </h3>

    <div class="relative space-y-3 pl-5 before:absolute before:left-[9px] before:top-3 before:bottom-3 before:w-0.5 before:bg-gray-200">
      <div v-for="action in actions" :key="action.id" class="relative">
        <div class="absolute -left-5 top-5 w-2.5 h-2.5 rounded-full border-2 border-indigo-400 bg-white z-10" />
        <ActionItem
          :action="action"
          @toggle="$emit('toggle', action.id)"
          @delete="$emit('delete', action.id)"
        />
      </div>
    </div>

    <div class="flex justify-center pt-2">
      <Button
        label="Gerar mais ações"
        icon="pi pi-plus"
        severity="secondary"
        outlined
        size="small"
        :loading="generatingMore"
        @click="$emit('generate-more')"
      />
    </div>
  </div>
</template>
