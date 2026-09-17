import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ImportView from "@/views/ImportView.vue";
import TranslateView from "@/views/TranslateView.vue";
import TranslationMaintenanceView from "@/views/TranslationMaintenanceView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: DashboardView,
    },
    {
      path: '/import',
      name: 'import',
      component: ImportView,
    },
    {
      path: '/translate',
      name: 'translate',
      component: TranslateView,
    },
    {
      path: '/translation-maintenance',
      name: 'translation-maintenance',
      component: TranslationMaintenanceView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
