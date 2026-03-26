<script setup lang="ts">
import type { ExperienceForm } from '@/types'
import { SENIORITY_LABELS } from '@/types'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import Button from 'primevue/button'
import { Briefcase, X } from 'lucide-vue-next'

const model = defineModel<ExperienceForm[]>({ required: true })

const SENIORITY_OPTIONS = Object.entries(SENIORITY_LABELS).map(([value, label]) => ({ label, value }))

function addExperience() {
  model.value.push({ role: '', seniority: null, company: '', start_date: null, end_date: null })
}

function removeExperience(index: number) {
  model.value.splice(index, 1)
}

if (model.value.length === 0) addExperience()
</script>

<template>
  <div class="space-y-6">
    <h3 class="text-lg font-semibold flex items-center gap-2">
      <Briefcase class="w-5 h-5 text-indigo-600" /> Trajetória Profissional
    </h3>

    <div
      v-for="(exp, i) in model"
      :key="i"
      class="bg-white border border-gray-200 rounded-xl p-4 space-y-4 relative"
    >
      <button
        v-if="model.length > 1"
        type="button"
        class="absolute top-3 right-3 text-gray-400 hover:text-red-500"
        @click="removeExperience(i)"
        :aria-label="`Remover experiência ${i + 1}`"
      >
        <X class="w-4 h-4" />
      </button>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Cargo *</label>
          <InputText v-model="exp.role" placeholder="Ex: Desenvolvedor Frontend" class="w-full" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Senioridade *</label>
          <Select
            v-model="exp.seniority"
            :options="SENIORITY_OPTIONS"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecione o nível"
            class="w-full"
          />
        </div>
      </div>

      <div class="space-y-1">
        <label class="text-sm font-medium text-gray-700">Empresa</label>
        <InputText v-model="exp.company" placeholder="Ex: Empresa XYZ" class="w-full" />
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Data de Início *</label>
          <DatePicker
            v-model="exp.start_date"
            view="month"
            dateFormat="mm/yy"
            placeholder="MM/AAAA"
            :maxDate="new Date()"
            class="w-full"
          />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Data de Fim</label>
          <DatePicker
            v-model="exp.end_date"
            view="month"
            dateFormat="mm/yy"
            placeholder="Vazio = atual"
            :minDate="exp.start_date ?? undefined"
            :maxDate="new Date()"
            class="w-full"
          />
        </div>
      </div>
    </div>

    <Button
      label="Adicionar experiência"
      icon="pi pi-plus"
      severity="secondary"
      outlined
      size="small"
      @click="addExperience"
    />
  </div>
</template>
