<script setup lang="ts">
import type { PlanSummary } from '@/types'
import PlanCard from './PlanCard.vue'

defineProps<{
  plans: PlanSummary[]
}>()

defineEmits<{
  view: [planId: string]
  delete: [planId: string]
}>()
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
    <PlanCard
      v-for="plan in plans"
      :key="plan.id"
      :plan="plan"
      @view="$emit('view', plan.id)"
      @delete="$emit('delete', plan.id)"
    />
  </div>
</template>
