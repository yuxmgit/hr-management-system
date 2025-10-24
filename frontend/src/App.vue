<template>
  <div id="app">
    <nav v-if="isLoggedIn" class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">HR管理系统</a>

        <!-- Mobile menu button -->
        <div class="d-flex align-items-center">
          <button class="navbar-toggler me-2" type="button" @click="toggleMobileMenu">
            <span class="navbar-toggler-icon"></span>
          </button>

          <!-- User profile icon for mobile -->
          <div class="dropdown d-lg-none">
            <button class="btn btn-outline-light rounded-circle" type="button" id="userDropdown"
              data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fas fa-user"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
              <!-- <li><a class="dropdown-item" href="#">个人资料</a></li>
              <li><a class="dropdown-item" href="#">设置</a></li> -->
              <li>
                <hr class="dropdown-divider">
              </li>
              <li><a class="dropdown-item" href="#" @click="logout">退出登录</a></li>
            </ul>
          </div>
        </div>

        <!-- Desktop navigation -->
        <div class="collapse navbar-collapse" :class="{ show: isMobileMenuOpen }">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">仪表板</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/leave-requests">请假申请</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/attendance">考勤中心</router-link>
            </li>
          </ul>

          <!-- Desktop user menu -->
          <ul class="navbar-nav mb-2 mb-lg-0 d-none d-lg-flex">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" @click="toggleDropdown" aria-expanded="false">
                <i class="fas fa-user-circle"></i> 用户名
              </a>
              <ul class="dropdown-menu dropdown-menu-end" :class="{ show: isDropdownOpen }">
                <!-- <li><a class="dropdown-item" href="#">个人资料</a></li>
                <li><a class="dropdown-item" href="#">设置</a></li> -->
                <li>
                  <hr class="dropdown-divider">
                </li>
                <li><a class="dropdown-item" href="#" @click="handleLogout">退出登录</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container-fluid">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import '@fortawesome/fontawesome-free/css/all.css';
import auth from './services/auth'

export default {
  name: 'App',
  data() {
    return {
      isMobileMenuOpen: false,
      isDropdownOpen: false,
      isLoggedIn: false
    }
  },
  created() {
    // Check authentication status when app loads
    this.checkAuthStatus();
  },
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    checkAuthStatus() {
      // Check if user has valid token
      const user = localStorage.getItem('user');
      this.isLoggedIn = !!user; // Convert to boolean
      console.log('Checking auth status. User exists:', !!user); // Debug log
    },
    async handleLogout() {
      try {
        localStorage.removeItem('user');
        this.isLoggedIn = false; // Explicitly set to false
        await auth.logout()
        // Redirect to login page
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }
  },
  watch: {
    '$route'() {
      // Close mobile menu when route changes
      this.isMobileMenuOpen = false;
      // Re-check auth status on route change
      this.checkAuthStatus();
    }
  },
  mounted() {
  // Listen for storage changes (in case of logout in another tab)
  window.addEventListener('storage', this.checkAuthStatus);
},
beforeUnmount() {
  window.removeEventListener('storage', this.checkAuthStatus);
}
}
</script>

<style>
/* Additional responsive styles */
@media (max-width: 991.98px) {
  .navbar-brand {
    font-size: 1.25rem;
  }

  .navbar-nav .nav-link {
    padding: 0.5rem 1rem;
  }

  .dropdown-menu {
    position: absolute;
  }
}

.btn-outline-light {
  border-width: 2px;
}

.rounded-circle {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-toggler {
  padding: 0.25rem 0.5rem;
  font-size: 1.1rem;
}
</style>