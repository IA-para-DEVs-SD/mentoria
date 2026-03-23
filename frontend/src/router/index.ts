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

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.path !== '/' && !auth.isAuthenticated) {
    return '/'
  }

  if (to.path === '/' && auth.isAuthenticated) {
    return '/home'
  }
})

export default router
