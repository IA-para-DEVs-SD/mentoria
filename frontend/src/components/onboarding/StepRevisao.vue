<script setup lang="ts">
import type { ProfileData } from '@/types'
import Chip from 'primevue/chip'
import { ClipboardCheck } from 'lucide-vue-next'

defineProps<{
  profile: ProfileData
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
      <ClipboardCheck class="w-5 h-5 text-indigo-600" /> Revisão do Perfil
    </h3>

    <p class="text-sm text-gray-500">Confira seus dados antes de gerar o plano.</p>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700">Trajetória Profissional</h4>
      <div
        v-for="(exp, i) in profile.experiencias"
        :key="i"
        class="bg-white border border-gray-200 rounded-lg p-3 text-sm space-y-1"
      >
        <p class="font-medium">{{ exp.cargo }} — {{ exp.senioridade }}</p>
        <p v-if="exp.empresa" class="text-gray-500">{{ exp.empresa }}</p>
        <p class="text-gray-400">{{ formatMonth(exp.dataInicio) }} — {{ formatMonth(exp.dataFim) }}</p>
      </div>
    </div>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700">Formação Acadêmica</h4>
      <div
        v-for="(form, i) in profile.formacoes"
        :key="i"
        class="bg-white border border-gray-200 rounded-lg p-3 text-sm space-y-1"
      >
        <p class="font-medium">{{ form.titulo }} — {{ form.nivel }}</p>
        <p class="text-gray-500">{{ form.instituicao }} · {{ form.areaEstudo }}</p>
        <p class="text-gray-400">{{ formatFull(form.dataInicio) }} — {{ formatFull(form.dataFim) }}</p>
      </div>
    </div>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700">Habilidades</h4>
      <div class="flex flex-wrap gap-2">
        <Chip v-for="h in profile.habilidades" :key="h" :label="h" />
      </div>
    </div>

    <div class="space-y-2">
      <h4 class="font-medium text-gray-700">Objetivo de Carreira</h4>
      <p class="text-sm bg-indigo-50 text-indigo-700 px-3 py-2 rounded-lg inline-block">
        {{ profile.objetivo }}
      </p>
    </div>
  </div>
</template>
