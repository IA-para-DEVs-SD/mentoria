<script setup lang="ts">
import type { Action } from '@/types'
import Tag from 'primevue/tag'
import { CheckCircle2, Circle, Trash2 } from 'lucide-vue-next'

const props = defineProps<{
  action: Action
}>()

defineEmits<{
  toggle: []
  delete: []
}>()

const PRIORITY_SEVERITY: Record<string, 'danger' | 'warn' | 'success'> = {
  'ALTA': 'danger',
  'MÉDIA': 'warn',
  'BAIXA': 'success',
}
</script>

<template>
  <div
    :class="['p-4 rounded-xl border transition-all', action.concluida ? 'bg-gray-50 opacity-60' : 'bg-white border-gray-200 shadow-sm']"
  >
    <div class="flex items-start gap-3">
      <button
        class="mt-0.5 shrink-0"
        :aria-label="action.concluida ? 'Desmarcar ação' : 'Marcar como concluída'"
        @click="$emit('toggle')"
      >
        <CheckCircle2 v-if="action.concluida" class="w-6 h-6 text-green-500" />
        <Circle v-else class="w-6 h-6 text-gray-300 hover:text-indigo-400" />
      </button>

      <div class="flex-1 min-w-0 space-y-2">
        <div class="flex flex-wrap items-center gap-2">
          <Tag :value="action.prioridade" :severity="PRIORITY_SEVERITY[action.prioridade]" class="!text-[10px]" />
          <Tag :value="action.categoria" severity="info" class="!text-[10px]" />
        </div>
        <h4 :class="['font-semibold text-sm', action.concluida && 'line-through text-gray-400']">
          {{ action.titulo }}
        </h4>
        <p class="text-xs text-gray-600">{{ action.objetivo }}</p>
        <p class="text-xs text-gray-400 italic">{{ action.contexto }}</p>
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
