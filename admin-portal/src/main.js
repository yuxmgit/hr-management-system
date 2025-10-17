import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 引入 Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.css'
// 引入 Bootstrap JS（可选）
import 'bootstrap/dist/js/bootstrap.bundle.js'

createApp(App).use(router).mount('#app')