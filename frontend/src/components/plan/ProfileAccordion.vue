<script setup lang="ts">
import type { ProfileOut, Seniority, EducationLevel, CareerGoal } from '@/types'
import { SENIORITY_LABELS, EDUCATION_LEVEL_LABELS, CAREER_GOAL_LABELS } from '@/types'
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
import Chip from 'primevue/chip'
import { UserCircle, Briefcase, GraduationCap, Lightbulb, Target } from 'lucide-vue-next'

defineProps<{
  profile: ProfileOut
}>()

function formatDate(iso: string | null): string {
  if (!iso) return 'Atual'
  const d = new Date(iso)
  return d.toLocaleDateString('pt-BR', { month: '2-digit', year: 'numeric' })
}
</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-2xl border border-gray-200 dark:border-slate-700">
    <Accordion>
      <AccordionPanel value="profile">
        <AccordionHeader>
          <span class="flex items-center gap-2 font-bold text-sm">
            <UserCircle class="w-4 h-4 text-indigo-600 dark:text-indigo-400" /> Dados do Perfil
          </span>
        </AccordionHeader>
        <AccordionContent>
        <div class="space-y-5 pt-2">
          <!-- Trajetória -->
          <div class="space-y-2">
            <h4 class="font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2 text-sm">
              <Briefcase class="w-4 h-4 text-indigo-500 dark:text-indigo-400" /> Trajetória Profissional
            </h4>
            <div
              v-for="exp in profile.experiences"
              :key="exp.id"
              class="bg-gray-50 dark:bg-slate-800 rounded-lg p-3 text-sm space-y-1"
            >
              <p class="font-medium dark:text-gray-100">{{ exp.role }} — {{ SENIORITY_LABELS[exp.seniority as Seniority] }}</p>
              <p v-if="exp.company" class="text-gray-500 dark:text-gray-400">{{ exp.company }}</p>
              <p class="text-gray-400 dark:text-gray-500">{{ formatDate(exp.start_date) }} — {{ formatDate(exp.end_date) }}</p>
            </div>
          </div>

          <!-- Formação -->
          <div class="space-y-2">
            <h4 class="font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2 text-sm">
              <GraduationCap class="w-4 h-4 text-indigo-500 dark:text-indigo-400" /> Formação Acadêmica
            </h4>
            <div
              v-for="edu in profile.educations"
              :key="edu.id"
              class="bg-gray-50 dark:bg-slate-800 rounded-lg p-3 text-sm space-y-1"
            >
              <p class="font-medium dark:text-gray-100">{{ edu.title }} — {{ EDUCATION_LEVEL_LABELS[edu.level as EducationLevel] }}</p>
              <p class="text-gray-500 dark:text-gray-400">{{ edu.institution }} · {{ edu.study_area }}</p>
              <p class="text-gray-400 dark:text-gray-500">{{ formatDate(edu.start_date) }} — {{ formatDate(edu.end_date) }}</p>
            </div>
          </div>

          <!-- Habilidades -->
          <div class="space-y-2">
            <h4 class="font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2 text-sm">
              <Lightbulb class="w-4 h-4 text-indigo-500 dark:text-indigo-400" /> Habilidades
            </h4>
            <div class="flex flex-wrap gap-2">
              <Chip v-for="skill in profile.skills" :key="skill" :label="skill" />
            </div>
          </div>

          <!-- Objetivo -->
          <div class="space-y-2">
            <h4 class="font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2 text-sm">
              <Target class="w-4 h-4 text-indigo-500 dark:text-indigo-400" /> Objetivo de Carreira
            </h4>
            <p class="text-sm bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 px-3 py-2 rounded-lg inline-block">
              {{ CAREER_GOAL_LABELS[profile.career_goal as CareerGoal] }}
            </p>
          </div>
        </div>
      </AccordionContent>
    </AccordionPanel>
  </Accordion>
  </div>
</template>
