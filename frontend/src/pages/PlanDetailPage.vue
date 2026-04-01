<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import { usePlansStore } from '@/stores/plansStore'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import PlanHeader from '@/components/plan/PlanHeader.vue'
import ProgressCard from '@/components/plan/ProgressCard.vue'
import GapsList from '@/components/plan/GapsList.vue'
import ActionTimeline from '@/components/plan/ActionTimeline.vue'
import type { ActionStatus } from '@/types'

const route = useRoute()
const router = useRouter()
const confirm = useConfirm()
const toast = useToast()

const authStore = useAuthStore()
const plansStore = usePlansStore()
const { currentPlan } = storeToRefs(plansStore)
const generatingMore = ref(false)

onMounted(async () => {
  const id = route.params.id as string
  await plansStore.loadPlan(id)
  if (!currentPlan.value) router.replace('/home')
})

function handleToggle(actionId: string) {
  if (!currentPlan.value) return
  const action = currentPlan.value.actions.find((a) => a.id === actionId)
  if (!action) return
  const newStatus: ActionStatus = action.status === 'pendente' ? 'concluida' : 'pendente'
  plansStore.updateActionStatus(currentPlan.value.id, actionId, newStatus)
}

function handleDelete(actionId: string) {
  if (!currentPlan.value) return
  if (currentPlan.value.actions.length <= 1) {
    toast.add({ severity: 'warn', summary: 'Ação bloqueada', detail: 'Seu plano precisa ter pelo menos uma ação.', life: 3000 })
    return
  }
  confirm.require({
    message: 'Essa ação removerá esta atividade do seu plano de desenvolvimento.',
    header: 'Excluir ação',
    acceptLabel: 'Excluir',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await plansStore.deleteAction(currentPlan.value!.id, actionId)
        toast.add({ severity: 'success', summary: 'Pronto', detail: 'Item removido do plano.', life: 3000 })
      } catch {
        toast.add({ severity: 'error', summary: 'Erro', detail: 'Não foi possível remover o item. Tente novamente.', life: 3000 })
      }
    },
  })
}

async function handleGenerateMore() {
  if (!currentPlan.value) return
  generatingMore.value = true
  try {
    await plansStore.generateMoreActions(currentPlan.value.id)
    toast.add({ severity: 'success', summary: 'Pronto', detail: 'Novas ações adicionadas ao plano.', life: 3000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Erro', detail: 'Não foi possível gerar novas ações. Tente novamente.', life: 3000 })
  } finally {
    generatingMore.value = false
  }
}
</script>

<template>
  <DefaultLayout>
    <div v-if="currentPlan" class="w-full max-w-3xl mx-auto p-4 sm:p-6 space-y-6 dark:bg-slate-900 dark:rounded-xl">
      <PlanHeader
        :plan="currentPlan"
        :user="authStore.user"
        @back="router.push('/home')"
      />
      <ProgressCard :progress="currentPlan.progress" />
      <GapsList :gaps="currentPlan.gaps" />
      <ActionTimeline
        :actions="currentPlan.actions"
        :generating-more="generatingMore"
        @toggle="handleToggle"
        @delete="handleDelete"
        @generate-more="handleGenerateMore"
      />
    </div>
  </DefaultLayout>
</template>
