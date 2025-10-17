// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import LeaveRequests from '../views/LeaveRequests.vue'
import EmployeeManagement from '../views/EmployeeManagement.vue'
import AttendanceRecords from '../views/AttendanceRecords.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard },
  { path: '/leave-requests', component: LeaveRequests },
  { path: '/employees', component: EmployeeManagement },
  { path: '/attendance', component: AttendanceRecords }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('adminUser')
  if (to.path !== '/login' && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router