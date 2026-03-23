<script setup lang="ts">
import type { Gap } from '@/types'
import { Zap } from 'lucide-vue-next'

defineProps<{
  gaps: Gap[]
}>()

function gapWidth(level: string): string {
  const map: Record<string, string> = { 'Iniciante': '25%', 'Básico': '25%', 'Intermediário': '50%', 'Avançado': '75%', 'Especialista': '100%' }
  return map[level] ?? '30%'
}
</script>

<template>
  <div class="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
    <h3 class="font-bold text-sm text-gray-900 flex items-center gap-2">
      <Zap class="w-4 h-4 text-amber-500" /> Gaps de Competência
    </h3>
    <div v-for="gap in gaps" :key="gap.skill" class="space-y-1">
      <div class="flex justify-between text-xs font-semibold">
        <span class="text-gray-700">{{ gap.skill }}</span>
        <span class="text-indigo-600">{{ gap.level }} → {{ gap.ideal }}</span>
      </div>
      <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div class="h-full bg-amber-400 rounded-full" :style="{ width: gapWidth(gap.level) }" />
      </div>
    </div>
  </div>
</template>
