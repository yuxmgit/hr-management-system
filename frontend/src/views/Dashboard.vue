<template>
  <div class="dashboard-container">
    <h1 class="h2 mb-4">仪表板</h1>
    
    <div class="row">
      <div class="col-xl-4 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                  待处理请假申请
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.pendingRequests }}</div>
              </div>
              <div class="col-auto">
                <i class="fas fa-clock fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-4 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  已批准申请
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.approvedRequests }}</div>
              </div>
              <div class="col-auto">
                <i class="fas fa-check-circle fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-4 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                  总申请数
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.totalRequests }}</div>
              </div>
              <div class="col-auto">
                <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row">
      <div class="col-md-12">
        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h5 class="m-0 font-weight-bold text-primary">最近请假申请</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-bordered table-hover">
                <thead class="thead-light">
                  <tr>
                    <th>类型</th>
                    <th>日期</th>
                    <th>状态</th>
                    <th>申请日期</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in recentRequests" :key="request.id">
                    <td>{{ request.leave_type }}</td>
                    <td>{{ formatDate(request.start_date) }} 至 {{ formatDate(request.end_date) }}</td>
                    <td>
                      <span :class="getStatusClass(request.status)">{{ getStatusText(request.status) }}</span>
                    </td>
                    <td>{{ formatDate(request.applied_date) }}</td>
                  </tr>
                  <tr v-if="recentRequests.length === 0">
                    <td colspan="4" class="text-center">暂无请假申请记录</td>
                  </tr>
                </tbody>
              </table>
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
  name: 'Dashboard',
  data() {
    return {
      stats: {
        pendingRequests: 0,
        approvedRequests: 0,
        totalRequests: 0
      },
      recentRequests: []
    }
  },
  async created() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        const response = await api.get('leave-requests/')
        const requests = response.data
        
        this.stats.totalRequests = requests.length
        this.stats.pendingRequests = requests.filter(r => r.status === 'pending').length
        this.stats.approvedRequests = requests.filter(r => r.status === 'approved').length
        
        // 获取最近5条申请记录
        this.recentRequests = requests.slice(0, 5)
      } catch (error) {
        console.error('加载仪表板数据失败:', error)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('zh-CN')
    },
    getStatusClass(status) {
      const classes = {
        pending: 'badge bg-warning text-dark',
        approved: 'badge bg-success',
        rejected: 'badge bg-danger'
      }
      return classes[status] || 'badge bg-secondary'
    },
    getStatusText(status) {
      const texts = {
        pending: '待处理',
        approved: '已批准',
        rejected: '已拒绝'
      }
      return texts[status] || status
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.card {
  border: none;
  border-radius: 0.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.border-left-primary {
  border-left: 0.25rem solid #4e73df !important;
}

.border-left-success {
  border-left: 0.25rem solid #1cc88a !important;
}

.border-left-info {
  border-left: 0.25rem solid #36b9cc !important;
}

.text-xs {
  font-size: .7rem;
}

.table-responsive {
  overflow-x: auto;
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.font-weight-bold {
  font-weight: 700 !important;
}

.text-gray-800 {
  color: #5a5c69 !important;
}

.shadow {
  box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
}

.py-2 {
  padding-top: 0.5rem !important;
  padding-bottom: 0.5rem !important;
}

.fa-2x {
  font-size: 2em;
}

.text-gray-300 {
  color: #dddfeb !important;
}
</style>