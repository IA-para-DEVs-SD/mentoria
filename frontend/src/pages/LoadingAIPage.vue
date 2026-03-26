<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profileStore'
import { usePlansStore } from '@/stores/plansStore'
import { storeToRefs } from 'pinia'
import ProgressSpinner from 'primevue/progressspinner'
import Button from 'primevue/button'
import { Sparkles } from 'lucide-vue-next'

const router = useRouter()
const profileStore = useProfileStore()
const plansStore = usePlansStore()
const { loading, error } = storeToRefs(plansStore)

async function generate() {
  if (!profileStore.profile) {
    router.replace('/onboarding')
    return
  }
  try {
    const plan = await plansStore.generatePlan()
    router.replace(`/plan/${plan.id}`)
  } catch {
    // error is set in store
  }
}

onMounted(generate)
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-700 to-purple-800 px-4">
    <div class="text-center text-white space-y-6 max-w-md">
      <!-- Loading -->
      <template v-if="loading">
        <Sparkles class="w-12 h-12 mx-auto text-amber-300" />
        <h1 class="text-2xl font-bold">✨ O Gemini está criando seu futuro...</h1>
        <p class="text-indigo-200 italic text-sm">
          Analisando seu perfil e gerando um plano personalizado de desenvolvimento.
        </p>
        <ProgressSpinner
          style="width: 50px; height: 50px"
          strokeWidth="4"
          animationDuration="1s"
        />
      </template>

      <!-- Error -->
      <template v-if="!loading && error">
        <div class="bg-white/10 backdrop-blur rounded-xl p-6 space-y-4">
          <p class="text-lg font-semibold">{{ error }}</p>
          <Button
            label="Tentar novamente"
            icon="pi pi-refresh"
            @click="generate"
            severity="warning"
          />
        </div>
      </template>
    </div>
  </div>
</template>
