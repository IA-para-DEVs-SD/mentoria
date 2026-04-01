<script setup lang="ts">
import type { Gap } from '@/types'
import { Zap } from 'lucide-vue-next'

defineProps<{
  gaps: Gap[]
}>()
</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-200 dark:border-slate-700 p-5 space-y-4">
    <h3 class="font-bold text-sm text-gray-900 dark:text-gray-100 flex items-center gap-2">
      <Zap class="w-4 h-4 text-amber-500" /> Gaps de Competência
    </h3>
    <div v-for="gap in gaps" :key="gap.id" class="space-y-1">
      <div class="flex justify-between text-xs font-semibold">
        <span class="text-gray-700 dark:text-gray-300">{{ gap.description }}</span>
        <span class="text-indigo-600 dark:text-indigo-400">Relevância: {{ gap.relevance }}/10</span>
      </div>
      <div class="h-1.5 bg-gray-100 dark:bg-slate-700 rounded-full overflow-hidden">
        <div class="h-full bg-amber-400 rounded-full" :style="{ width: `${gap.relevance * 10}%` }" />
      </div>
    </div>
  </div>
</template>
