<!-- src/App.vue -->
<template>
  <div id="app">
    <nav v-if="$route.path !== '/login'" class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">HR管理后台</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link" active-class="active">仪表板</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/leave-requests" class="nav-link" active-class="active">请假审批</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/employees" class="nav-link" active-class="active">员工管理</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/attendance" class="nav-link" active-class="active">考勤记录</router-link>
            </li>
          </ul>
          <div class="navbar-nav">
            <li class="nav-item dropdown" @mouseover="showDropdown = true" @mouseleave="showDropdown = false">
              <a class="nav-link dropdown-toggle" href="#" role="button">
                <i class="bi bi-person-circle"></i> {{ currentUser?.first_name }} {{ currentUser?.last_name }}
              </a>
              <ul class="dropdown-menu" :class="{ show: showDropdown }">
                <li><a class="dropdown-item" href="#" @click="logout">退出登录</a></li>
              </ul>
            </li>
          </div>
        </div>
      </div>
    </nav>

    <main class="container-fluid mt-4">
      <router-view @user-updated="loadCurrentUser"/>
    </main>
  </div>
</template>

<script>
import auth from './services/auth'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

export default {
  name: 'AdminApp',
  data() {
    return {
    currentUser: null,
    showDropdown: false
  }
  },
  async created() {
    if (auth.isLoggedIn()) {
      this.currentUser = auth.getUser()
    }
  },
  methods: {
    async logout() {
      try {
        await auth.logout()
        this.$router.push('/login')
      } catch (error) {
        console.error('退出登录错误:', error)
      }
    }
  }
}
</script>