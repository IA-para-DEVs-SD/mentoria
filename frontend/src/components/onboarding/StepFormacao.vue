<script setup lang="ts">
import type { Formacao, NivelFormacao } from '@/types'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import Button from 'primevue/button'
import { GraduationCap, X } from 'lucide-vue-next'

const model = defineModel<Formacao[]>({ required: true })

const NIVEIS: NivelFormacao[] = [
  'Ensino Médio', 'Técnico', 'Tecnólogo', 'Bacharelado', 'Licenciatura',
  'Pós-graduação', 'MBA', 'Mestrado', 'Doutorado', 'Pós-doutorado',
]

function addFormacao() {
  model.value.push({ instituicao: '', nivel: null, titulo: '', areaEstudo: '', dataInicio: null, dataFim: null })
}

function removeFormacao(index: number) {
  model.value.splice(index, 1)
}

if (model.value.length === 0) addFormacao()
</script>

<template>
  <div class="space-y-6">
    <h3 class="text-lg font-semibold flex items-center gap-2">
      <GraduationCap class="w-5 h-5 text-indigo-600" /> Formação Acadêmica
    </h3>

    <div
      v-for="(form, i) in model"
      :key="i"
      class="bg-white border border-gray-200 rounded-xl p-4 space-y-4 relative"
    >
      <button
        v-if="model.length > 1"
        type="button"
        class="absolute top-3 right-3 text-gray-400 hover:text-red-500"
        @click="removeFormacao(i)"
        :aria-label="`Remover formação ${i + 1}`"
      >
        <X class="w-4 h-4" />
      </button>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Instituição *</label>
          <InputText v-model="form.instituicao" placeholder="Ex: USP" class="w-full" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Nível de Formação *</label>
          <Select
            v-model="form.nivel"
            :options="NIVEIS"
            placeholder="Selecione o nível"
            class="w-full"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Título da Formação *</label>
          <InputText v-model="form.titulo" placeholder="Ex: Ciência da Computação" class="w-full" />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Área de Estudo *</label>
          <InputText v-model="form.areaEstudo" placeholder="Ex: Tecnologia" class="w-full" />
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Data de Início *</label>
          <DatePicker
            v-model="form.dataInicio"
            dateFormat="dd/mm/yy"
            placeholder="DD/MM/AAAA"
            :maxDate="new Date()"
            class="w-full"
          />
        </div>
        <div class="space-y-1">
          <label class="text-sm font-medium text-gray-700">Data de Fim</label>
          <DatePicker
            v-model="form.dataFim"
            dateFormat="dd/mm/yy"
            placeholder="Vazio = em andamento"
            :minDate="form.dataInicio ?? undefined"
            class="w-full"
          />
        </div>
      </div>
    </div>

    <Button
      label="Adicionar formação"
      icon="pi pi-plus"
      severity="secondary"
      outlined
      size="small"
      @click="addFormacao"
    />
  </div>
</template>
