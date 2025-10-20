<template>
    <div class="leave-requests-container">
      <div class="header d-flex justify-content-between align-items-center mb-4">
        <h1 class="page-title">我的请假记录</h1>
        <router-link to="/apply-leave" class="btn btn-primary apply-btn">
          <i class="bi bi-plus-circle"></i> 新申请
        </router-link>
      </div>
      
      <div class="card shadow-sm">
        <div class="card-body p-4">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">加载中...</span>
            </div>
          </div>
          <table v-else class="table table-hover table-bordered">
            <thead class="table-light">
              <tr>
                <th>类型</th>
                <th>日期</th>
                <th>天数</th>
                <th>状态</th>
                <th>申请日期</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in leaveRequests" :key="request.id">
                <td>{{ formatLeaveType(request.leave_type) }}</td>
                <td>{{ formatDate(request.start_date) }} 至 {{ formatDate(request.end_date) }}</td>
                <td>{{ calculateDays(request.start_date, request.end_date) }} 天</td>
                <td>
                  <span :class="getStatusClass(request.status)">{{ getStatusText(request.status) }}</span>
                </td>
                <td>{{ formatDate(request.applied_date) }}</td>
              </tr>
              <tr v-if="leaveRequests.length === 0">
                <td colspan="5" class="text-center text-muted">暂无请假记录</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../services/api'
  
  export default {
    name: 'LeaveRequests',
    data() {
      return {
        leaveRequests: [],
        loading: true
      }
    },
    async created() {
      await this.loadLeaveRequests()
    },
    methods: {
      async loadLeaveRequests() {
        try {
          this.loading = true
          const response = await api.get('leave-requests/')
          this.leaveRequests = response.data
        } catch (error) {
          console.error('加载请假记录失败:', error)
        } finally {
          this.loading = false
        }
      },
      formatLeaveType(type) {
        const types = {
          annual: '年假',
          sick: '病假',
          personal: '事假',
          maternity: '产假'
        }
        return types[type] || type
      },
      formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('zh-CN')
      },
      calculateDays(startDate, endDate) {
        const start = new Date(startDate)
        const end = new Date(endDate)
        const diffTime = Math.abs(end - start)
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
        return diffDays
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