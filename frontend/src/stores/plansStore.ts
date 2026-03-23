import { ref } from 'vue'
import { defineStore } from 'pinia'
import { planService } from '@/services/planService'
import type { Plan, ProfileData } from '@/types'

export const usePlansStore = defineStore('plans', () => {
  const plans = ref<Plan[]>([])
  const currentPlan = ref<Plan | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadPlans() {
    plans.value = await planService.getPlans()
  }

  async function loadPlan(id: string) {
    currentPlan.value = (await planService.getPlanById(id)) ?? null
  }

  async function generatePlan(profile: ProfileData) {
    loading.value = true
    error.value = null
    try {
      const plan = await planService.generatePlan(profile)
      plans.value.unshift(plan)
      currentPlan.value = plan
      return plan
    } catch {
      error.value = 'Não foi possível gerar o plano. Tente novamente.'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function deletePlan(id: string) {
    await planService.deletePlan(id)
    plans.value = plans.value.filter((p) => p.id !== id)
  }

  async function toggleAction(planId: string, actionId: string) {
    const updated = await planService.toggleAction(planId, actionId)
    if (updated) currentPlan.value = updated
  }

  async function deleteAction(planId: string, actionId: string) {
    const updated = await planService.deleteAction(planId, actionId)
    if (updated) currentPlan.value = updated
  }

  async function generateMoreActions(planId: string) {
    const updated = await planService.generateMoreActions(planId)
    if (updated) currentPlan.value = updated
  }

  return {
    plans,
    currentPlan,
    loading,
    error,
    loadPlans,
    loadPlan,
    generatePlan,
    deletePlan,
    toggleAction,
    deleteAction,
    generateMoreActions,
  }
})
