<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <h2>人力资源管理系统</h2>
        <p>专业的企业人才管理平台</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label for="username" class="input-label">用户名</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              required 
              :disabled="loading"
              placeholder="请输入用户名"
            />
          </div>
        </div>
        
        <div class="input-group">
          <label for="password" class="input-label">密　码</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              required 
              :disabled="loading"
              placeholder="请输入密码"
            />
          </div>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" :disabled="loading" class="login-button">
          <span v-if="!loading">登录系统</span>
          <span v-else class="loading">
            <svg class="spinner" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"></circle>
            </svg>
            登录中...
          </span>
        </button>
      </form>
      
      <div class="features">
        <div class="feature-item">
          <svg class="feature-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>员工信息管理</span>
        </div>
        <div class="feature-item">
          <svg class="feature-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <span>薪酬福利管理</span>
        </div>
        <div class="feature-item">
          <svg class="feature-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor">
            <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"></polyline>
          </svg>
          <span>绩效考核系统</span>
        </div>
      </div>
      
      <div class="login-footer">
        <p>© 2023 人力资源管理系统. 保留所有权利.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'AdminLogin',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: ''
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';
      
      try {
        // First, get CSRF token
        const csrfResponse = await api.get('csrf-token/');
        const csrfToken = csrfResponse.data.csrfToken;
        
        // Set CSRF token in headers
        api.defaults.headers.common['X-CSRFToken'] = csrfToken;
        
        // Perform login
        const response = await api.post('login/', {
          username: this.username,
          password: this.password
        });
        
        if (response.data.success) {
          // Store user data in localStorage
          localStorage.setItem('adminUser', JSON.stringify(response.data.user));
           // Debugging logs
      console.log('Login successful, redirecting to dashboard');
      console.log('Current routes:', this.$router.options.routes);
      this.$router.push('/dashboard').catch(err => {
        console.error('Navigation error:', err);
      });
    } else {
      this.error = response.data.message || '登录失败';
    }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message;
        } else {
          this.error = '登录过程中发生错误，请重试';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f4c75, #3282b8);
  padding: 1rem;
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  transform: rotate(30deg);
  z-index: 0;
}

.login-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  color: white;
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
  color: #4dabf7;
}

.login-header h2 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  background: linear-gradient(to right, #4dabf7, #74c0fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.login-header p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
}

.input-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
}

.input-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 0.5px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: rgba(255, 255, 255, 0.6);
}

.input-wrapper input {
  width: 100%;
  padding: 0.9rem 0.9rem 0.9rem 3rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #4dabf7;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 3px rgba(77, 171, 247, 0.2);
}

.input-wrapper input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.input-wrapper input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #4dabf7, #3b5bdb);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  box-shadow: 0 4px 15px rgba(59, 91, 219, 0.3);
}

.login-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #5bb5f9, #4a6aec);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 91, 219, 0.4);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  animation: spin 1s linear infinite;
  width: 18px;
  height: 18px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #ff8787;
  background-color: rgba(255, 135, 135, 0.15);
  border: 1px solid rgba(255, 135, 135, 0.3);
  margin-bottom: 1rem;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.features {
  display: flex;
  justify-content: space-between;
  margin: 2rem 0;
  padding: 1.5rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 33%;
  padding: 0 0.5rem;
}

.feature-icon {
  margin-bottom: 0.5rem;
  color: #74c0fc;
}

.feature-item span {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
}

.login-footer {
  text-align: center;
  margin-top: 1rem;
}

.login-footer p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }
  
  .login-header h2 {
    font-size: 1.5rem;
  }
  
  .features {
    flex-direction: column;
    gap: 1rem;
  }
  
  .feature-item {
    width: 100%;
    flex-direction: row;
    justify-content: flex-start;
    gap: 0.8rem;
  }
  
  .feature-item span {
    font-size: 0.9rem;
  }
}
</style>