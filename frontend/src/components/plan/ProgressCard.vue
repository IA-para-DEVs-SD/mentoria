<script setup lang="ts">
import ProgressBar from 'primevue/progressbar'
import { Rocket } from 'lucide-vue-next'

defineProps<{
  progress: number
}>()
</script>

<template>
  <div class="bg-indigo-600 dark:bg-indigo-700 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
    <div class="relative z-10 space-y-3">
      <div class="flex justify-between items-center">
        <span class="text-xs font-bold uppercase tracking-wider text-indigo-200">Progresso do Roadmap</span>
        <span class="text-2xl font-black">{{ progress }}%</span>
      </div>
      <ProgressBar :value="progress" :showValue="false" class="!h-2 !bg-indigo-400/30" />
    </div>
    <Rocket class="absolute -bottom-6 -right-6 w-32 h-32 text-white opacity-10 rotate-12" />
  </div>
</template>
