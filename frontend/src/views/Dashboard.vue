<template>
    <div>
      <h1 class="h2 mb-4">仪表板</h1>
      
      <div class="row">
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3">
            <div class="card-body">
              <h5 class="card-title">待处理请假申请</h5>
              <p class="card-text display-4">{{ stats.pendingRequests }}</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3">
            <div class="card-body">
              <h5 class="card-title">已批准申请</h5>
              <p class="card-text display-4">{{ stats.approvedRequests }}</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="card text-white bg-info mb-3">
            <div class="card-body">
              <h5 class="card-title">总申请数</h5>
              <p class="card-text display-4">{{ stats.totalRequests }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title">最近请假申请</h5>
            </div>
            <div class="card-body">
              <table class="table table-striped">
                <thead>
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
          pending: 'badge bg-warning',
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