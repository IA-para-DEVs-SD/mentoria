import { ref } from 'vue'
import { defineStore } from 'pinia'
import { planService } from '@/services/planService'
import type { Plan, PlanSummary, ActionStatus } from '@/types'

export const usePlansStore = defineStore('plans', () => {
  const plans = ref<PlanSummary[]>([])
  const currentPlan = ref<Plan | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadPlans() {
    plans.value = await planService.getPlans()
  }

  async function loadPlan(id: string) {
    currentPlan.value = await planService.getPlanById(id)
  }

  async function generatePlan() {
    loading.value = true
    error.value = null
    try {
      const plan = await planService.generatePlan()
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

  async function updateActionStatus(planId: string, actionId: string, status: ActionStatus) {
    await planService.updateActionStatus(planId, actionId, status)
    await loadPlan(planId)
  }

  async function deleteAction(planId: string, actionId: string) {
    const { progress } = await planService.deleteAction(planId, actionId)
    if (currentPlan.value && currentPlan.value.id === planId) {
      currentPlan.value.actions = currentPlan.value.actions.filter((a) => a.id !== actionId)
      currentPlan.value.progress = progress
    }
  }

  async function generateMoreActions(planId: string) {
    await planService.generateMoreActions(planId)
    await loadPlan(planId)
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
    updateActionStatus,
    deleteAction,
    generateMoreActions,
  }
})
