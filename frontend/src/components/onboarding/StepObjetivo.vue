<script setup lang="ts">
import type { CareerGoal } from '@/types'
import { CAREER_GOAL_LABELS } from '@/types'
import { Target } from 'lucide-vue-next'

const model = defineModel<CareerGoal | null>({ required: true })

const GOALS: { value: CareerGoal; label: string; icon: string }[] = [
  { value: 'Crescer_na_carreira_atual', label: CAREER_GOAL_LABELS['Crescer_na_carreira_atual'], icon: '📈' },
  { value: 'Assumir_cargos_de_lideranca', label: CAREER_GOAL_LABELS['Assumir_cargos_de_lideranca'], icon: '👥' },
  { value: 'Mudar_de_area', label: CAREER_GOAL_LABELS['Mudar_de_area'], icon: '🔄' },
]
</script>

<template>
  <div class="space-y-6">
    <h3 class="text-lg font-semibold flex items-center gap-2">
      <Target class="w-5 h-5 text-indigo-600" /> Objetivo de Carreira
    </h3>

    <p class="text-sm text-gray-500">Selecione um objetivo para continuar.</p>

    <div class="grid grid-cols-1 gap-3">
      <button
        v-for="obj in GOALS"
        :key="obj.value"
        type="button"
        :class="[
          'text-left p-4 rounded-xl border-2 transition-all',
          model === obj.value
            ? 'border-indigo-600 bg-indigo-50'
            : 'border-gray-200 hover:border-gray-300',
        ]"
        @click="model = obj.value"
      >
        <span class="text-lg mr-2">{{ obj.icon }}</span>
        <span class="font-medium">{{ obj.label }}</span>
      </button>
    </div>
  </div>
</template>
