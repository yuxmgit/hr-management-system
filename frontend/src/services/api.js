import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true,  // 重要：允许发送cookies
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从cookie中获取CSRF token
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 403) {
      // CSRF token 失效，可能需要刷新页面或重新获取
      console.warn('CSRF token might be invalid');
    }
    return Promise.reject(error);
  }
);

export default api;