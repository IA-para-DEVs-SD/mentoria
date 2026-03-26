<script setup lang="ts">
import type { Action } from '@/types'
import Tag from 'primevue/tag'
import { CheckCircle2, Circle, Trash2 } from 'lucide-vue-next'

defineProps<{
  action: Action
}>()

defineEmits<{
  toggle: []
  delete: []
}>()

const PRIORITY_SEVERITY: Record<string, 'danger' | 'warn' | 'success'> = {
  'ALTA': 'danger',
  'MEDIA': 'warn',
  'BAIXA': 'success',
}
</script>

<template>
  <div
    :class="['p-4 rounded-xl border transition-all', action.status === 'concluida' ? 'bg-gray-50 opacity-60' : 'bg-white border-gray-200 shadow-sm']"
  >
    <div class="flex items-start gap-3">
      <button
        class="mt-0.5 shrink-0"
        :aria-label="action.status === 'concluida' ? 'Desmarcar ação' : 'Marcar como concluída'"
        @click="$emit('toggle')"
      >
        <CheckCircle2 v-if="action.status === 'concluida'" class="w-6 h-6 text-green-500" />
        <Circle v-else class="w-6 h-6 text-gray-300 hover:text-indigo-400" />
      </button>

      <div class="flex-1 min-w-0 space-y-2">
        <div class="flex flex-wrap items-center gap-2">
          <Tag :value="action.priority" :severity="PRIORITY_SEVERITY[action.priority]" class="!text-[10px]" />
          <Tag :value="action.category" severity="info" class="!text-[10px]" />
        </div>
        <h4 :class="['font-semibold text-sm', action.status === 'concluida' && 'line-through text-gray-400']">
          {{ action.title }}
        </h4>
        <p class="text-xs text-gray-600">{{ action.objective }}</p>
        <p class="text-xs text-gray-400 italic">{{ action.context }}</p>
      </div>

      <button
        class="shrink-0 p-1 text-gray-300 hover:text-red-500"
        aria-label="Excluir ação"
        @click="$emit('delete')"
      >
        <Trash2 class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>
