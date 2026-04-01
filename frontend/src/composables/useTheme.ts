import { ref, computed, watchEffect } from 'vue'

type Theme = 'light' | 'dark'
const STORAGE_KEY = 'mentoria-theme'

function getInitial(): Theme {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'light' || stored === 'dark') return stored
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const theme = ref<Theme>(getInitial())

// Apply immediately so there's no flash
document.documentElement.classList.toggle('dark', theme.value === 'dark')

export function useTheme() {
  watchEffect(() => {
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
    localStorage.setItem(STORAGE_KEY, theme.value)
  })

  const isDark = computed(() => theme.value === 'dark')

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  return { theme, isDark, toggle }
}
