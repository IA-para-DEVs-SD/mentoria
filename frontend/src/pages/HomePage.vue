<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { usePlansStore } from '@/stores/plansStore'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import PlanList from '@/components/home/PlanList.vue'
import EmptyState from '@/components/home/EmptyState.vue'
import Button from 'primevue/button'

const router = useRouter()
const confirm = useConfirm()
const toast = useToast()
const plansStore = usePlansStore()
const { plans } = storeToRefs(plansStore)

onMounted(() => plansStore.loadPlans())

function goToOnboarding() {
  router.push('/onboarding?mode=new-plan')
}

function handleView(planId: string) {
  router.push(`/plan/${planId}`)
}

function handleDelete(planId: string) {
  confirm.require({
    message: 'Ao excluir este plano, você perderá seu progresso e histórico de desenvolvimento. Essa ação não pode ser desfeita.',
    header: 'Excluir plano',
    acceptLabel: 'Excluir',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await plansStore.deletePlan(planId)
        toast.add({ severity: 'success', summary: 'Pronto', detail: 'Plano excluído. Você pode criar um novo plano a qualquer momento.', life: 3000 })
      } catch {
        toast.add({ severity: 'error', summary: 'Erro', detail: 'Não foi possível excluir o plano. Tente novamente.', life: 3000 })
      }
    },
  })
}
</script>

<template>
  <DefaultLayout>
    <div class="w-full max-w-3xl mx-auto p-4 sm:p-6 space-y-6 dark:bg-slate-900 dark:rounded-xl">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold dark:text-gray-100">Meus Planos</h1>
        <Button
          v-if="plans.length > 0"
          label="Gerar Novo Plano"
          icon="pi pi-plus"
          size="small"
          @click="goToOnboarding"
        />
      </div>

      <PlanList
        v-if="plans.length > 0"
        :plans="plans"
        @view="handleView"
        @delete="handleDelete"
      />
      <EmptyState v-else @generate="goToOnboarding" />
    </div>
  </DefaultLayout>
</template>
