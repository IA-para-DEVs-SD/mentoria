<script setup lang="ts">
// TODO: requer ajuste no backend para redirecionar para o frontend com token na URL
// Esperado: backend redireciona para http://localhost:5173/auth/callback?token=xxx&has_profile=true
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import ProgressSpinner from 'primevue/progressspinner'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  const token = route.query.token as string | undefined
  const hasProfile = route.query.has_profile === 'true'

  if (!token) {
    router.replace('/')
    return
  }

  authStore.handleCallback(token, hasProfile)
  router.replace(hasProfile ? '/home' : '/onboarding')
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-purple-100 dark:from-slate-900 dark:to-slate-800">
    <div class="text-center space-y-4">
      <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" animationDuration="1s" />
      <p class="text-gray-600 dark:text-gray-300 text-sm">Autenticando...</p>
    </div>
  </div>
</template>
