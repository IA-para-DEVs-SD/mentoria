import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import LoginPage from '@/pages/LoginPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/auth/callback',
      name: 'auth-callback',
      component: () => import('@/pages/AuthCallbackPage.vue'),
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/pages/HomePage.vue'),
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: () => import('@/pages/OnboardingPage.vue'),
    },
    {
      path: '/loading',
      name: 'loading',
      component: () => import('@/pages/LoadingAIPage.vue'),
    },
    {
      path: '/plan/:id',
      name: 'plan-detail',
      component: () => import('@/pages/PlanDetailPage.vue'),
    },
  ],
})

const publicRoutes = ['/', '/auth/callback']

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (!publicRoutes.includes(to.path) && !auth.isAuthenticated) {
    return '/'
  }

  if (to.path === '/' && auth.isAuthenticated) {
    return '/home'
  }
})

export default router
