import { ref, computed } from 'vue'
import type { ProfileData } from '@/types'

const STEPS = ['1', '2', '3', '4', '5']

export function useOnboarding(profile: ProfileData) {
  const currentStep = ref('1')

  function isStepValid(step: string): boolean {
    switch (step) {
      case '1':
        return profile.experiencias.length > 0 && profile.experiencias.every((e) =>
          e.cargo.trim() !== '' && e.senioridade !== null && e.dataInicio !== null
        )
      case '2':
        return profile.formacoes.length > 0 && profile.formacoes.every((f) =>
          f.instituicao.trim() !== '' && f.nivel !== null && f.titulo.trim() !== '' && f.areaEstudo.trim() !== '' && f.dataInicio !== null
        )
      case '3':
        return profile.habilidades.length > 0
      case '4':
        return profile.objetivo !== null
      case '5':
        return isStepValid('1') && isStepValid('2') && isStepValid('3') && isStepValid('4')
      default:
        return false
    }
  }

  const canAdvance = computed(() => isStepValid(currentStep.value))

  function nextStep() {
    const idx = STEPS.indexOf(currentStep.value)
    if (idx >= 0 && idx < STEPS.length - 1 && canAdvance.value) {
      currentStep.value = STEPS[idx + 1]!
    }
  }

  function prevStep() {
    const idx = STEPS.indexOf(currentStep.value)
    if (idx > 0) {
      currentStep.value = STEPS[idx - 1]!
    }
  }

  return { currentStep, canAdvance, isStepValid, nextStep, prevStep }
}
