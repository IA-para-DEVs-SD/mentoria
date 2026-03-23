<script setup lang="ts">
import { ref } from 'vue'
import InputText from 'primevue/inputtext'
import Chip from 'primevue/chip'
import Button from 'primevue/button'
import { Lightbulb } from 'lucide-vue-next'

const model = defineModel<string[]>({ required: true })
const input = ref('')

const SUGESTOES = [
  'React', 'Node.js', 'Python', 'Liderança', 'Gestão de Projetos',
  'UI/UX', 'SQL', 'Cloud Computing', 'Agile', 'Inglês',
]

function normalize(s: string) {
  return s.trim().toLowerCase()
}

function addHabilidade(value?: string) {
  const raw = (value ?? input.value).trim()
  if (!raw) return
  if (model.value.some((h) => normalize(h) === normalize(raw))) return
  model.value.push(raw)
  input.value = ''
}

function removeHabilidade(index: number) {
  model.value.splice(index, 1)
}

function isSugestaoAdded(s: string) {
  return model.value.some((h) => normalize(h) === normalize(s))
}
</script>

<template>
  <div class="space-y-6">
    <h3 class="text-lg font-semibold flex items-center gap-2">
      <Lightbulb class="w-5 h-5 text-indigo-600" /> Habilidades
    </h3>

    <div class="flex gap-2">
      <InputText
        v-model="input"
        placeholder="Digite uma habilidade..."
        class="flex-1"
        @keyup.enter="addHabilidade()"
      />
      <Button icon="pi pi-plus" severity="secondary" @click="addHabilidade()" :disabled="!input.trim()" />
    </div>

    <div v-if="model.length === 0" class="text-sm text-gray-500">
      Adicione pelo menos uma habilidade.
    </div>

    <div v-if="model.length > 0" class="flex flex-wrap gap-2">
      <Chip
        v-for="(h, i) in model"
        :key="h"
        :label="h"
        removable
        @remove="removeHabilidade(i)"
      />
    </div>

    <div class="space-y-2">
      <p class="text-sm text-gray-500">Sugestões:</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="s in SUGESTOES"
          :key="s"
          type="button"
          :class="[
            'px-3 py-1.5 rounded-full text-sm transition-all border',
            isSugestaoAdded(s)
              ? 'bg-indigo-600 text-white border-indigo-600'
              : 'bg-gray-100 text-gray-600 border-gray-200 hover:bg-gray-200',
          ]"
          @click="isSugestaoAdded(s) ? undefined : addHabilidade(s)"
        >
          {{ s }}
        </button>
      </div>
    </div>
  </div>
</template>
