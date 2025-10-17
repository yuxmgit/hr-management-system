import api from './api'

export default {
  async login(username, password) {
    try {
      const response = await api.post('login/', { username, password })
      if (response.data.success) {
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      return response.data
    } catch (error) {
      throw error.response?.data || { message: '登录失败' }
    }
  },

  async logout() {
    try {
      await api.post('logout/')
      localStorage.removeItem('user')
      return { success: true }
    } catch (error) {
      localStorage.removeItem('user')
      return { success: true }
    }
  },

  async getCurrentUser() {
    try {
      const response = await api.get('current-user/')
      return response.data
    } catch (error) {
      throw error.response?.data || { message: '获取用户信息失败' }
    }
  },

  getUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  isLoggedIn() {
    return !!this.getUser()
  }
}