import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue'), meta: { public: true } },
    { path: '/', name: 'Home', component: () => import('../views/HomeView.vue') },
    { path: '/bills', name: 'Bills', component: () => import('../views/BillListView.vue') },
    { path: '/add', name: 'Add', component: () => import('../views/AddBillView.vue') },
    { path: '/reports', name: 'Reports', component: () => import('../views/ReportView.vue') },
    { path: '/profile', name: 'Profile', component: () => import('../views/ProfileView.vue') },
    { path: '/categories', name: 'Categories', component: () => import('../views/CategoryManageView.vue') },
  ]
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isLoggedIn()) {
    next('/login')
  } else if (to.path === '/login' && auth.isLoggedIn()) {
    next('/')
  } else {
    next()
  }
})

export default router
