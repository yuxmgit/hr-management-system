<!-- src/views/Login.vue -->
<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mt-5">
            <div class="card-header">
              <h3 class="text-center">管理员登录 - HR管理系统</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="username" class="form-label">用户名</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    v-model="username" 
                    required
                  >
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">密码</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="password" 
                    required
                  >
                </div>
                <div v-if="error" class="alert alert-danger">{{ error }}</div>
                <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                  {{ loading ? '登录中...' : '登录' }}
                </button>
              </form>
              
              <div class="text-center mt-3">
                <button @click="refreshCSRF" class="btn btn-sm btn-outline-secondary">
                  刷新安全令牌
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import auth from '../services/auth'
  import api from '../services/api'
  
  export default {
    name: 'AdminLogin',
    data() {
      return {
        username: '',
        password: '',
        error: '',
        loading: false
      }
    },
    methods: {
      async handleLogin() {
        this.loading = true
        this.error = ''
        
        try {
          const result = await auth.login(this.username, this.password)
          if (result.success) {
            this.$router.push('/dashboard')
          } else {
            this.error = result.message
          }
        } catch (error) {
          if (error.message && error.message.includes('CSRF')) {
            this.error = '安全验证失败，请点击下方按钮刷新安全令牌后重试'
          } else {
            this.error = error.message || '登录失败'
          }
        } finally {
          this.loading = false
        }
      },
      async refreshCSRF() {
        try {
          await api.get('csrf/')
          this.error = '安全令牌已刷新，请重新尝试登录'
        } catch (error) {
          this.error = '刷新安全令牌失败'
        }
      }
    }
  }
  </script>