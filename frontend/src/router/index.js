import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'  // 添加这一行
import Dashboard from '../views/Dashboard.vue'
import LeaveRequests from '../views/LeaveRequests.vue'
import ApplyLeave from '../views/ApplyLeave.vue'
import Attendance from '../views/Attendance.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },  // 添加注册路由
  { path: '/dashboard', component: Dashboard },
  { path: '/leave-requests', component: LeaveRequests },
  { path: '/apply-leave', component: ApplyLeave },
  { path: '/attendance', component: Attendance }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('user')
  if (to.path !== '/login' && to.path !== '/register' && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router