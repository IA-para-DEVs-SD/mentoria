<script setup lang="ts">
import { computed, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profileStore'
import { useOnboarding } from '@/composables/useOnboarding'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from 'primevue/button'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import StepItem from 'primevue/stepitem'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'
import StepTrajetoria from '@/components/onboarding/StepTrajetoria.vue'
import StepFormacao from '@/components/onboarding/StepFormacao.vue'
import StepHabilidades from '@/components/onboarding/StepHabilidades.vue'
import StepObjetivo from '@/components/onboarding/StepObjetivo.vue'
import StepRevisao from '@/components/onboarding/StepRevisao.vue'
import type { ProfileData } from '@/types'

const route = useRoute()
const router = useRouter()
const profileStore = useProfileStore()

const isNewPlan = computed(() => route.query.mode === 'new-plan')

const profile = reactive<ProfileData>(
  profileStore.profile
    ? JSON.parse(JSON.stringify(profileStore.profile))
    : { experiencias: [], formacoes: [], habilidades: [], objetivo: null as ProfileData['objetivo'] }
)

const { currentStep, canAdvance, nextStep, prevStep } = useOnboarding(profile)

async function handleFinish() {
  await profileStore.saveProfile({ ...profile } as ProfileData)
  router.push('/loading')
}
</script>

<template>
  <DefaultLayout>
    <div class="w-full max-w-2xl mx-auto p-4 sm:p-6 space-y-6">
      <h2 class="text-2xl font-bold text-center sm:text-left">Mapa de Perfil</h2>

      <Stepper v-model:value="currentStep" linear>
        <StepList>
          <Step value="1">Trajetória</Step>
          <Step value="2">Formação</Step>
          <Step value="3">Habilidades</Step>
          <Step value="4">Objetivo</Step>
          <Step value="5">Revisão</Step>
        </StepList>
        <StepPanels>
          <StepPanel value="1">
            <StepTrajetoria v-model="profile.experiencias" />
          </StepPanel>
          <StepPanel value="2">
            <StepFormacao v-model="profile.formacoes" />
          </StepPanel>
          <StepPanel value="3">
            <StepHabilidades v-model="profile.habilidades" />
          </StepPanel>
          <StepPanel value="4">
            <StepObjetivo v-model="profile.objetivo" />
          </StepPanel>
          <StepPanel value="5">
            <StepRevisao :profile="profile" />
          </StepPanel>
        </StepPanels>
      </Stepper>

      <div class="flex gap-4">
        <Button
          v-if="currentStep !== '1'"
          label="Voltar"
          severity="secondary"
          outlined
          class="flex-1"
          @click="prevStep"
        />
        <Button
          v-if="currentStep !== '5'"
          label="Continuar"
          :disabled="!canAdvance"
          class="flex-[2]"
          @click="nextStep"
        />
        <Button
          v-else
          :label="isNewPlan ? '✨ Gerar Novo Plano' : '✨ Gerar Mentoria IA'"
          :disabled="!canAdvance"
          class="flex-[2]"
          @click="handleFinish"
        />
      </div>
    </div>
  </DefaultLayout>
</template>
