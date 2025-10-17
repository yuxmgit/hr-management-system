// src/services/auth.js
import api from './api'

export default {
  async login(username, password) {
    try {
      // 首先获取CSRF token
      await api.get('csrf/') // 如果后端提供了CSRF token接口
      
      const response = await api.post('login/', { username, password })
      if (response.data.success && response.data.user.is_staff) {
        localStorage.setItem('adminUser', JSON.stringify(response.data.user))
        return response.data
      } else if (!response.data.user.is_staff) {
        throw new Error('没有管理员权限')
      } else {
        throw new Error('登录失败')
      }
    } catch (error) {
      if (error.response?.status === 403) {
        throw new Error('CSRF验证失败，请刷新页面重试')
      }
      throw error.response?.data || { message: '登录失败' }
    }
  },

  async logout() {
    try {
      await api.post('logout/')
      localStorage.removeItem('adminUser')
      return { success: true }
    } catch (error) {
      localStorage.removeItem('adminUser')
      return { success: true }
    }
  },

  getUser() {
    const user = localStorage.getItem('adminUser')
    return user ? JSON.parse(user) : null
  },

  isLoggedIn() {
    return !!this.getUser()
  }
}