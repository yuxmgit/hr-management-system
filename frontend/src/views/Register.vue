<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mt-5">
            <div class="card-header">
              <h3 class="text-center">注册 - 人力资源管理系统</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleRegister">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label">名字</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="firstName" 
                      v-model="formData.first_name" 
                      required
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label">姓氏</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="lastName" 
                      v-model="formData.last_name" 
                      required
                    >
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="username" class="form-label">用户名</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    v-model="formData.username" 
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <label for="email" class="form-label">邮箱</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    v-model="formData.email" 
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <label for="password" class="form-label">密码</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="formData.password" 
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">确认密码</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="confirmPassword" 
                    v-model="formData.confirmPassword" 
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <label for="employeeId" class="form-label">员工编号</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="employeeId" 
                    v-model="formData.employee_id" 
                    required
                  >
                </div>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="department" class="form-label">部门</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="department" 
                      v-model="formData.department" 
                      required
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="position" class="form-label">职位</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="position" 
                      v-model="formData.position" 
                      required
                    >
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="hireDate" class="form-label">入职日期</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="hireDate" 
                    v-model="formData.hire_date" 
                    required
                  >
                </div>
                
                <div v-if="error" class="alert alert-danger">{{ error }}</div>
                
                <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                  {{ loading ? '注册中...' : '注册' }}
                </button>
              </form>
              
              <div class="text-center mt-3">
                <p>已有账户？<router-link to="/login">点击登录</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../services/api'
  
  export default {
    name: 'Register',
    data() {
      return {
        formData: {
          first_name: '',
          last_name: '',
          username: '',
          email: '',
          password: '',
          confirmPassword: '',
          employee_id: '',
          department: '',
          position: '',
          hire_date: ''
        },
        error: '',
        loading: false
      }
    },
    methods: {
      async handleRegister() {
        // 验证密码匹配
        if (this.formData.password !== this.formData.confirmPassword) {
          this.error = '两次输入的密码不一致'
          return
        }
        
        this.loading = true
        this.error = ''
        
        try {
          // 发送注册请求到后端
          const response = await api.post('register/', this.formData)
          
          if (response.data.success) {
            // 注册成功后自动登录
            const loginResponse = await api.post('login/', {
              username: this.formData.username,
              password: this.formData.password
            })
            
            if (loginResponse.data.success) {
              localStorage.setItem('user', JSON.stringify(loginResponse.data.user))
              this.$router.push('/dashboard')
            }
          } else {
            this.error = response.data.message || '注册失败'
          }
        } catch (error) {
          console.error('注册错误:', error)
          if (error.response) {
            this.error = error.response.data.message || '注册失败'
          } else if (error.request) {
            this.error = '网络错误，请检查网络连接'
          } else {
            this.error = '注册失败，请重试'
          }
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>