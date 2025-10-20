<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-section">
        <div class="logo-icon">
          <i class="fas fa-users"></i>
        </div>
        <h2 class="app-title">人力资源管理系统</h2>
        <p class="app-subtitle">Employee Management Solution</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <div class="input-wrapper">
            <i class="fas fa-user input-icon"></i>
            <input 
              type="text" 
              class="form-input" 
              id="username" 
              placeholder="请输入用户名"
              v-model="username" 
              required
            >
          </div>
        </div>
        
        <div class="input-group">
          <div class="input-wrapper">
            <i class="fas fa-lock input-icon"></i>
            <input 
              type="password" 
              class="form-input" 
              id="password" 
              placeholder="请输入密码"
              v-model="password" 
              required
            >
          </div>
        </div>
        
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <i v-else class="fas fa-sign-in-alt button-icon"></i>
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="footer-links">
        <p>还没有账户？<router-link to="/register" class="register-link">立即注册</router-link></p>
        <p><a href="#" class="forgot-password">忘记密码？</a></p>
      </div>
    </div>
    
    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script>
import auth from '../services/auth'

export default {
  name: 'Login',
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
        this.error = error.message || '登录失败'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  padding: 40px 30px;
  backdrop-filter: blur(10px);
  z-index: 10;
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: white;
  font-size: 36px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.app-title {
  color: #333;
  font-weight: 700;
  margin: 0 0 5px;
  font-size: 24px;
}

.app-subtitle {
  color: #777;
  font-size: 14px;
  margin: 0;
}

.input-group {
  margin-bottom: 20px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
}

.form-input {
  width: 100%;
  padding: 15px 15px 15px 45px;
  border: 2px solid #e1e5ee;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  background-color: #fff;
}

.login-form {
  margin-bottom: 25px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.error-message i {
  margin-right: 8px;
}

.login-button {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.button-icon {
  margin-right: 8px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.footer-links {
  text-align: center;
  margin-top: 20px;
}

.footer-links p {
  margin: 10px 0;
  font-size: 14px;
  color: #666;
}

.register-link,
.forgot-password {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.register-link:hover,
.forgot-password:hover {
  color: #764ba2;
  text-decoration: underline;
}

.background-decoration .circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}


.circle-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 20%;
  right: 10%;
}

/* Add additional circles for better coverage */
.circle-4 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  right: 20%;
}

.circle-5 {
  width: 250px;
  height: 250px;
  top: 50%;
  left: -125px;
}
.login-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 20%),
    radial-gradient(circle at 90% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 20%),
    radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 30%);
  z-index: 1;
}

.login-card {
  /* ... existing styles ... */
  z-index: 10; /* This is already set correctly */
}

@media (max-width: 576px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .app-title {
    font-size: 20px;
  }
  
  .form-input {
    padding: 12px 12px 12px 40px;
  }
}
</style>