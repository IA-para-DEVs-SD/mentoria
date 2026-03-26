import api from './api'
import type { Plan, PlanSummary, Action, ActionStatus, ProgressOut } from '@/types'

export const planService = {
  async getPlans(): Promise<PlanSummary[]> {
    const { data } = await api.get<PlanSummary[]>('/plans')
    return data
  },

  async getPlanById(id: string): Promise<Plan> {
    const { data } = await api.get<Plan>(`/plans/${id}`)
    return data
  },

  async generatePlan(): Promise<Plan> {
    const { data } = await api.post<Plan>('/plans')
    return data
  },

  async deletePlan(id: string): Promise<void> {
    await api.delete(`/plans/${id}`)
  },

  async updateActionStatus(planId: string, actionId: string, status: ActionStatus): Promise<Action> {
    const { data } = await api.patch<Action>(`/plans/${planId}/actions/${actionId}`, { status })
    return data
  },

  async deleteAction(planId: string, actionId: string): Promise<ProgressOut> {
    const { data } = await api.delete<ProgressOut>(`/plans/${planId}/actions/${actionId}`)
    return data
  },

  async generateMoreActions(planId: string): Promise<Action[]> {
    const { data } = await api.post<Action[]>(`/plans/${planId}/actions/generate`)
    return data
  },
}
