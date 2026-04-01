<script setup lang="ts">
import type { Plan } from '@/types'
import type { User } from '@/types'
import { ChevronLeft } from 'lucide-vue-next'

defineProps<{
  plan: Plan
  user: User | null
}>()

defineEmits<{
  back: []
}>()

const PLACEHOLDER_AVATAR = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'
</script>

<template>
  <div class="flex items-center gap-3">
    <button
      class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700 text-gray-500 dark:text-gray-400"
      aria-label="Voltar para Home"
      @click="$emit('back')"
    >
      <ChevronLeft class="w-5 h-5" />
    </button>
    <img
      :src="user?.photo_url ?? PLACEHOLDER_AVATAR"
      :alt="user?.name ?? 'Usuário'"
      class="w-10 h-10 rounded-full border-2 border-white dark:border-slate-700 shadow"
    />
    <div class="min-w-0">
      <h2 class="font-bold text-lg truncate dark:text-gray-100">{{ plan.name }}</h2>
      <p class="text-xs text-gray-500 dark:text-gray-400">{{ user?.name ?? '' }}</p>
    </div>
  </div>
</template>
