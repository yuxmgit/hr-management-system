import api from './api'

export default {
  async login(username, password) {
    try {
      const response = await api.post('login/', {
        username: username,
        password: password
      })
      return response.data
    } catch (error) {
      // Re-throw the error so it can be handled in the component
      throw error
    }
  },
  
  logout() {
    // Handle logout
    return api.post('logout/')
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