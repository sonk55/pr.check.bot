import Vue from 'vue'
import VueRouter from 'vue-router'
import AdminLogin from '../components/AdminLogin.vue'
import PrDashboard from '../components/Dashboard.vue'
import AdminSettings from '../components/AdminSettings.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    component: AdminLogin
  },
  {
    path: '/dashboard',
    component: PrDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: AdminSettings,
    meta: { requiresAuth: true }
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
