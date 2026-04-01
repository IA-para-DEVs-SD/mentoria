<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { BrainCircuit } from 'lucide-vue-next'
import GoogleLoginButton from '@/components/auth/GoogleLoginButton.vue'

const auth = useAuthStore()
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-purple-100 dark:from-slate-900 dark:to-slate-800 px-4">
    <div class="w-full max-w-sm text-center space-y-8">
      <div class="space-y-2">
        <div class="flex items-center justify-center gap-2">
          <BrainCircuit class="w-10 h-10 text-indigo-600 dark:text-indigo-400" />
          <h1 class="text-3xl font-bold text-indigo-600 dark:text-indigo-400">Mentoria.IA</h1>
        </div>
        <p class="text-gray-500 dark:text-gray-400 text-sm">
          Sua carreira impulsionada por Inteligência Artificial
        </p>
      </div>

      <div class="bg-white dark:bg-slate-800 rounded-xl shadow-md p-8 space-y-6">
        <p class="text-gray-600 dark:text-gray-300 text-sm">
          Faça login para começar seu plano de desenvolvimento personalizado.
        </p>
        <div class="flex justify-center">
          <GoogleLoginButton @click="auth.loginRedirect()" />
        </div>
      </div>
    </div>
  </div>
</template>
