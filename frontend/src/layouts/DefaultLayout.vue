<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { useTheme } from '@/composables/useTheme'
import { useRouter } from 'vue-router'
import { BrainCircuit, LogOut, Sun, Moon } from 'lucide-vue-next'
import Button from 'primevue/button'

const auth = useAuthStore()
const router = useRouter()
const { isDark, toggle } = useTheme()

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-slate-900">
    <header class="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800">
      <router-link to="/home" class="flex items-center gap-2 no-underline">
        <BrainCircuit class="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
        <span class="text-lg font-bold text-indigo-600 dark:text-indigo-400">Mentoria.IA</span>
      </router-link>
      <div class="flex items-center gap-1">
        <Button
          severity="secondary"
          text
          size="small"
          :aria-label="isDark ? 'Alternar para modo claro' : 'Alternar para modo escuro'"
          @click="toggle"
        >
          <template #icon>
            <Sun v-if="isDark" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </template>
        </Button>
        <Button
          severity="secondary"
          text
          size="small"
          aria-label="Sair"
          @click="handleLogout"
        >
          <template #icon>
            <LogOut class="w-4 h-4" />
          </template>
          <span class="hidden sm:inline ml-1">Sair</span>
        </Button>
      </div>
    </header>
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>
