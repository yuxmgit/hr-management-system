<!-- src/views/Dashboard.vue -->
<template>
  <div>
    <h1 class="h2 mb-4">管理仪表板</h1>

    <div class="row">
      <div class="col-md-3">
        <div class="card text-white bg-primary mb-3">
          <div class="card-body">
            <h5 class="card-title">总员工数</h5>
            <p class="card-text display-4">{{ stats.totalEmployees }}</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-warning mb-3">
          <div class="card-body">
            <h5 class="card-title">待审批申请</h5>
            <p class="card-text display-4">{{ stats.pendingRequests }}</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-success mb-3">
          <div class="card-body">
            <h5 class="card-title">已批准申请</h5>
            <p class="card-text display-4">{{ stats.approvedRequests }}</p>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-info mb-3">
          <div class="card-body">
            <h5 class="card-title">今日签到</h5>
            <p class="card-text display-4">{{ stats.todayAttendance }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title">待处理请假申请</h5>
          </div>
          <div class="card-body">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>员工</th>
                  <th>类型</th>
                  <th>日期</th>
                  <th>天数</th>
                  <th>申请时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in pendingRequests" :key="request.id">
                  <td>{{ request.employee_name }} ({{ request.employee_id }})</td>
                  <td>{{ formatLeaveType(request.leave_type) }}</td>
                  <td>{{ formatDate(request.start_date) }} 至 {{ formatDate(request.end_date) }}</td>
                  <td>{{ calculateDays(request.start_date, request.end_date) }} 天</td>
                  <td>{{ formatDate(request.applied_date) }}</td>
                  <td>
                    <button class="btn btn-sm btn-success me-1" @click="approveRequest(request.id)">批准</button>
                    <button class="btn btn-sm btn-danger" @click="showRejectModal(request.id)">拒绝</button>
                  </td>
                </tr>
                <tr v-if="pendingRequests.length === 0">
                  <td colspan="6" class="text-center">暂无待处理申请</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 拒绝原因模态框 -->
    <div class="modal fade" id="rejectModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">拒绝申请</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="rejectReason" class="form-label">拒绝原因</label>
              <textarea class="form-control" id="rejectReason" rows="3" v-model="rejectReason"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-danger" @click="rejectRequest">确认拒绝</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalEmployees: 0,
        pendingRequests: 0,
        approvedRequests: 0,
        todayAttendance: 0
      },
      pendingRequests: [],
      currentRejectId: null,
      rejectReason: ''
    }
  },
  async created() {
    try {
      const user = localStorage.getItem('adminUser')
      if (!user) {
        // No user data found, redirect to login
        this.$router.push('/login')
        return
      }

      const userData = JSON.parse(user)
      // Check if user exists and is staff
      // if (!userData.user || !userData.user.is_staff) {
      //   // If not admin, redirect to login
      //   this.$router.push('/login')
      //   return
      // }

      // User is authenticated and is admin, load dashboard data
      console.log('User authenticated, loading dashboard')
      await this.loadDashboardData()
    } catch (error) {
      console.error('Authentication check failed:', error)
      this.$router.push('/login')
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        // 获取统计信息
        const employeesResponse = await api.get('employees/')
        const requestsResponse = await api.get('leave-requests/')
        const attendanceResponse = await api.get('attendance/')

        this.stats.totalEmployees = employeesResponse.data.length
        this.stats.pendingRequests = requestsResponse.data.filter(r => r.status === 'pending').length
        this.stats.approvedRequests = requestsResponse.data.filter(r => r.status === 'approved').length

        // 获取今天的考勤记录
        const today = new Date().toISOString().split('T')[0]
        this.stats.todayAttendance = attendanceResponse.data.filter(a =>
          a.date === today && a.check_in
        ).length

        // 获取待处理申请
        this.pendingRequests = requestsResponse.data
          .filter(r => r.status === 'pending')
          .slice(0, 5)
      } catch (error) {
        console.error('加载仪表板数据失败:', error)
        // 安全地显示错误消息
        let errorMsg = '加载仪表板数据失败'
        if (error.response && error.response.status === 403) {
          errorMsg = '权限不足，请重新登录'
        }
        if (this.$toast && this.$toast.error) {
          this.$toast.error(errorMsg)
        } else {
          console.error('错误:', errorMsg)
        }
      }
    },

    // 重新加载数据（用于审批后刷新）
    async reloadData() {
      try {
        const requestsResponse = await api.get('leave-requests/')
        this.stats.pendingRequests = requestsResponse.data.filter(r => r.status === 'pending').length
        this.stats.approvedRequests = requestsResponse.data.filter(r => r.status === 'approved').length

        // 重新获取待处理申请
        this.pendingRequests = requestsResponse.data
          .filter(r => r.status === 'pending')
          .slice(0, 5)
      } catch (error) {
        console.error('重新加载数据失败:', error)
        this.$toast.error('重新加载数据失败')
      }
    },

    // 批准请假请求
    async approveRequest(id) {
      if (confirm('确定要批准此申请吗？')) {
        try {
          // Send action in the request body instead of URL
          await api.post(`leave-requests/${id}/`, { action: 'approve' })
          await this.reloadData()
          if (this.$toast && this.$toast.success) {
            this.$toast.success('申请已批准')
          } else {
            console.log('申请已批准')
          }
        } catch (error) {
          console.error('批准申请失败:', error)
          let errorMsg = '批准申请失败'
          if (error.response) {
            if (error.response.data && error.response.data.detail) {
              errorMsg = error.response.data.detail
            } else if (error.response.data && error.response.data.error) {
              errorMsg = error.response.data.error
            } else if (error.response.status === 403) {
              errorMsg = '权限不足，请重新登录'
            } else if (error.response.status === 400) {
              errorMsg = '请求参数错误'
            }
          }
          if (this.$toast && this.$toast.error) {
            this.$toast.error(errorMsg)
          } else {
            console.error('错误:', errorMsg)
          }
        }
      }
    },

    // 拒绝请假请求
    async rejectRequest() {
      try {
        // Send action in the request body instead of URL
        await api.post(`leave-requests/${this.currentRejectId}/`, {
          action: 'reject',
          reason: this.rejectReason
        })
        await this.reloadData()
        const modalElement = document.getElementById('rejectModal')
        if (modalElement) {
          const modal = Modal.getInstance(modalElement)
          if (modal) {
            modal.hide()
          }
        }
        if (this.$toast && this.$toast.success) {
          this.$toast.success('申请已拒绝')
        } else {
          console.log('申请已拒绝')
        }
      } catch (error) {
        // ... error handling code remains the same
      }
    },

    showRejectModal(id) {
      this.currentRejectId = id
      this.rejectReason = ''
      const modal = new Modal(document.getElementById('rejectModal'))
      modal.show()
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
    }
  }
}
</script>