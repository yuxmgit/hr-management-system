import api from './api'

export default {
  async login(username, password) {
    try {
      const response = await api.post('login/', { username, password })
      if (response.data.success) {
        localStorage.setItem('adminUser', JSON.stringify(response.data.user))
      }
      return response.data
    } catch (error) {
      throw error.response?.data || { message: '登录失败' }
    }
  },

  logout() {
    // Ensure this returns a promise
    return new Promise((resolve) => {
      localStorage.removeItem('token');
      localStorage.removeItem('adminUser');
      // Any other cleanup
      resolve();
    });
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
    const user = localStorage.getItem('adminUser')
    return user ? JSON.parse(user) : null
  },

  isLoggedIn() {
    return !!this.getUser()
  }
}