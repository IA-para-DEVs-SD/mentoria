<script setup lang="ts">
import type { ProfileForm, Seniority, EducationLevel, CareerGoal } from '@/types'
import { SENIORITY_LABELS, EDUCATION_LEVEL_LABELS, CAREER_GOAL_LABELS } from '@/types'
import Chip from 'primevue/chip'
import { ClipboardCheck } from 'lucide-vue-next'

defineProps<{
  profile: ProfileForm
}>()

function formatMonth(d: Date | null | undefined): string {
  if (!d) return 'Atual'
  return d.toLocaleDateString('pt-BR', { month: '2-digit', year: 'numeric' })
}

function formatFull(d: Date | null | undefined): string {
  if (!d) return 'Em andamento'
  return d.toLocaleDateString('pt-BR')
}
</script>

<template>
  <div class="space-y-6">
    <h3 class="text-lg font-semibold flex items-center gap-2">
      <ClipboardCheck class="w-5 h-5 text-indigo-600 dark:text-indigo-400" /> Revisão do Perfil
    </h3>

    <p class="text-sm text-gray-500 dark:text-gray-400">Confira seus dados antes de gerar o plano.</p>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700 dark:text-gray-300">Trajetória Profissional</h4>
      <div
        v-for="(exp, i) in profile.experiences"
        :key="i"
        class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg p-3 text-sm space-y-1"
      >
        <p class="font-medium dark:text-gray-100">{{ exp.role }} — {{ exp.seniority ? SENIORITY_LABELS[exp.seniority as Seniority] : '' }}</p>
        <p v-if="exp.company" class="text-gray-500 dark:text-gray-400">{{ exp.company }}</p>
        <p class="text-gray-400 dark:text-gray-500">{{ formatMonth(exp.start_date) }} — {{ formatMonth(exp.end_date) }}</p>
      </div>
    </div>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700 dark:text-gray-300">Formação Acadêmica</h4>
      <div
        v-for="(form, i) in profile.educations"
        :key="i"
        class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg p-3 text-sm space-y-1"
      >
        <p class="font-medium dark:text-gray-100">{{ form.title }} — {{ form.level ? EDUCATION_LEVEL_LABELS[form.level as EducationLevel] : '' }}</p>
        <p class="text-gray-500 dark:text-gray-400">{{ form.institution }} · {{ form.study_area }}</p>
        <p class="text-gray-400 dark:text-gray-500">{{ formatFull(form.start_date) }} — {{ formatFull(form.end_date) }}</p>
      </div>
    </div>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700 dark:text-gray-300">Habilidades</h4>
      <div class="flex flex-wrap gap-2">
        <Chip v-for="h in profile.skills" :key="h" :label="h" />
      </div>
    </div>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700 dark:text-gray-300">Objetivo de Carreira</h4>
      <p class="text-sm bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 px-3 py-2 rounded-lg inline-block">
        {{ profile.career_goal ? CAREER_GOAL_LABELS[profile.career_goal as CareerGoal] : '' }}
      </p>
    </div>
  </div>
</template>
