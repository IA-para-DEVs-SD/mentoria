<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { BrainCircuit, LogOut } from 'lucide-vue-next'
import Button from 'primevue/button'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-gray-200 bg-white">
      <router-link to="/home" class="flex items-center gap-2 no-underline">
        <BrainCircuit class="w-6 h-6 text-indigo-600" />
        <span class="text-lg font-bold text-indigo-600">Mentoria.IA</span>
      </router-link>
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
    </header>
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>
