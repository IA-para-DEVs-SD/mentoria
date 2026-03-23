<script setup lang="ts">
import type { Plan } from '@/types'
import type { User } from '@/types'
import { ChevronLeft } from 'lucide-vue-next'

defineProps<{
  plan: Plan
  user: User
}>()

defineEmits<{
  back: []
}>()
</script>

<template>
  <div class="flex items-center gap-3">
    <button
      class="p-2 rounded-lg hover:bg-gray-100 text-gray-500"
      aria-label="Voltar para Home"
      @click="$emit('back')"
    >
      <ChevronLeft class="w-5 h-5" />
    </button>
    <img :src="user.photo" :alt="user.name" class="w-10 h-10 rounded-full border-2 border-white shadow" />
    <div class="min-w-0">
      <h2 class="font-bold text-lg truncate">{{ plan.titulo }}</h2>
      <p class="text-xs text-gray-500">{{ user.name }}</p>
    </div>
  </div>
</template>
