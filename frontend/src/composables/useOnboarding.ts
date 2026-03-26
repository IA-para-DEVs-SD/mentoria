import { ref, computed } from 'vue'
import type { ProfileForm } from '@/types'

const STEPS = ['1', '2', '3', '4', '5']

export function useOnboarding(profile: ProfileForm) {
  const currentStep = ref('1')

  function isStepValid(step: string): boolean {
    switch (step) {
      case '1':
        return profile.experiences.length > 0 && profile.experiences.every((e) =>
          e.role.trim() !== '' && e.seniority !== null && e.start_date !== null
        )
      case '2':
        return profile.educations.length > 0 && profile.educations.every((f) =>
          f.institution.trim() !== '' && f.level !== null && f.title.trim() !== '' && f.study_area.trim() !== '' && f.start_date !== null
        )
      case '3':
        return profile.skills.length > 0
      case '4':
        return profile.career_goal !== null
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
