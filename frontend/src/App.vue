<template>
  <div id="app">
    <nav v-if="$route.path !== '/login' && $route.path !== '/register'" class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">人力资源管理系统</a>
        <div class="navbar-nav ms-auto">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" @click.prevent="toggleDropdown" ref="dropdownToggle">
              <i class="bi bi-person-circle"></i> {{ currentUser?.first_name }} {{ currentUser?.last_name }}
            </a>
            <ul class="dropdown-menu" :class="{ show: isDropdownOpen }" ref="dropdownMenu">
              <li><a class="dropdown-item" href="#" @click.prevent="logout">退出登录</a></li>
            </ul>
          </li>
        </div>
      </div>
    </nav>

    <!-- Rest of your template remains the same -->
    <div class="container-fluid">
      <div class="row">
        <nav v-if="$route.path !== '/login' && $route.path !== '/register'" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
          <div class="position-sticky pt-3">
            <ul class="nav flex-column">
              <li class="nav-item">
                <router-link to="/dashboard" class="nav-link" active-class="active">
                  <i class="bi bi-speedometer2"></i> 仪表板
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/apply-leave" class="nav-link" active-class="active">
                  <i class="bi bi-calendar-plus"></i> 申请请假
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/leave-requests" class="nav-link" active-class="active">
                  <i class="bi bi-list-task"></i> 我的请假记录
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/attendance" class="nav-link" active-class="active">
                  <i class="bi bi-clock"></i> 考勤记录
                </router-link>
              </li>
            </ul>
          </div>
        </nav>

        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
          <router-view @user-updated="loadCurrentUser"/>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import auth from './services/auth'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

export default {
  name: 'App',
  data() {
    return {
      currentUser: null,
      isDropdownOpen: false
    }
  },
  async created() {
    if (auth.isLoggedIn()) {
      await this.loadCurrentUser()
    }
    
    // Add global click listener to handle closing dropdown when clicking outside
    document.addEventListener('click', this.handleOutsideClick)
  },
  beforeUnmount() {
    // Clean up event listener
    document.removeEventListener('click', this.handleOutsideClick)
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen
    },
    handleOutsideClick(event) {
      // Close dropdown if clicked outside
      if (!this.$refs.dropdownToggle || !this.$refs.dropdownMenu) return
      
      const isClickInsideToggle = this.$refs.dropdownToggle.contains(event.target)
      const isClickInsideMenu = this.$refs.dropdownMenu.contains(event.target)
      
      if (!isClickInsideToggle && !isClickInsideMenu) {
        this.isDropdownOpen = false
      }
    },
    async loadCurrentUser() {
      try {
        const userData = await auth.getCurrentUser()
        this.currentUser = userData.user
        localStorage.setItem('user', JSON.stringify(userData.user))
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    },
    async logout() {
      try {
        // Close dropdown first
        this.isDropdownOpen = false
        
        // Perform logout
        await auth.logout()
        
        // Redirect to login page
        this.$router.push('/login')
      } catch (error) {
        console.error('退出登录错误:', error)
      }
    }
  }
}
</script>

<style>
.sidebar {
  position: fixed;
  top: 56px;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 48px 0 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.nav-link.active {
  background-color: #e9ecef;
  color: #000;
}
</style>