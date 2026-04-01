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
import type { ProfileForm, ProfileData, CareerGoal } from '@/types'

const route = useRoute()
const router = useRouter()
const profileStore = useProfileStore()

const isNewPlan = computed(() => route.query.mode === 'new-plan')

function buildInitialForm(): ProfileForm {
  const p = profileStore.profile
  if (!p) {
    return { experiences: [], educations: [], skills: [], career_goal: null }
  }
  return {
    experiences: p.experiences.map((e) => ({
      role: e.role,
      seniority: e.seniority,
      company: e.company ?? '',
      start_date: new Date(e.start_date),
      end_date: e.end_date ? new Date(e.end_date) : null,
    })),
    educations: p.educations.map((ed) => ({
      institution: ed.institution,
      level: ed.level,
      title: ed.title,
      study_area: ed.study_area,
      start_date: new Date(ed.start_date),
      end_date: ed.end_date ? new Date(ed.end_date) : null,
    })),
    skills: [...p.skills],
    career_goal: p.career_goal,
  }
}

const profile = reactive<ProfileForm>(buildInitialForm())

const { currentStep, canAdvance, nextStep, prevStep } = useOnboarding(profile)

function formatDate(d: Date | null): string | null {
  if (!d) return null
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

async function handleFinish() {
  const data: ProfileData = {
    experiences: profile.experiences.map((e) => ({
      role: e.role,
      seniority: e.seniority!,
      company: e.company || null,
      start_date: formatDate(e.start_date)!,
      end_date: formatDate(e.end_date),
    })),
    educations: profile.educations.map((ed) => ({
      institution: ed.institution,
      level: ed.level!,
      title: ed.title,
      study_area: ed.study_area,
      start_date: formatDate(ed.start_date)!,
      end_date: formatDate(ed.end_date),
    })),
    skills: profile.skills,
    career_goal: profile.career_goal as CareerGoal,
  }
  await profileStore.saveProfile(data)
  router.push('/loading')
}
</script>

<template>
  <DefaultLayout>
    <div class="w-full max-w-3xl mx-auto p-4 sm:p-6 space-y-6 dark:bg-slate-900 dark:rounded-xl">
      <h2 class="text-2xl font-bold text-center sm:text-left dark:text-gray-100">Mapa de Perfil</h2>

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
            <StepTrajetoria v-model="profile.experiences" />
          </StepPanel>
          <StepPanel value="2">
            <StepFormacao v-model="profile.educations" />
          </StepPanel>
          <StepPanel value="3">
            <StepHabilidades v-model="profile.skills" />
          </StepPanel>
          <StepPanel value="4">
            <StepObjetivo v-model="profile.career_goal" />
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
