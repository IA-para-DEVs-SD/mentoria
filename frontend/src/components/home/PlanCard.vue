<script setup lang="ts">
import type { PlanSummary } from '@/types'
import ProgressBar from 'primevue/progressbar'
import Button from 'primevue/button'
import { Trash2, Calendar } from 'lucide-vue-next'

defineProps<{
  plan: PlanSummary
}>()

defineEmits<{
  view: []
  delete: []
}>()

function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-4 shadow-sm">
    <div class="flex items-start justify-between gap-2">
      <h3 class="font-semibold text-sm text-gray-900 leading-tight">{{ plan.name }}</h3>
      <button
        class="shrink-0 p-1 text-gray-300 hover:text-red-500"
        aria-label="Excluir plano"
        @click="$emit('delete')"
      >
        <Trash2 class="w-4 h-4" />
      </button>
    </div>

    <div class="flex items-center gap-1 text-xs text-gray-400">
      <Calendar class="w-3 h-3" />
      <span>{{ formatDate(plan.created_at) }}</span>
    </div>

    <div class="space-y-1">
      <div class="flex justify-between text-xs">
        <span class="text-gray-500">Progresso</span>
        <span class="font-semibold text-indigo-600">{{ plan.progress }}%</span>
      </div>
      <ProgressBar :value="plan.progress" :showValue="false" class="!h-2" />
    </div>

    <Button
      label="Ver Detalhes"
      severity="secondary"
      outlined
      size="small"
      class="w-full"
      @click="$emit('view')"
    />
  </div>
</template>
