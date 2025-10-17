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
      await this.loadDashboardData()
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
        }
      },
      async approveRequest(id) {
        try {
          await api.post(`leave-requests/${id}/approve/`)
          await this.loadDashboardData()
          this.$toast.success('申请已批准')
        } catch (error) {
          console.error('批准申请失败:', error)
          this.$toast.error('批准申请失败')
        }
      },
      showRejectModal(id) {
        this.currentRejectId = id
        this.rejectReason = ''
        const modal = new bootstrap.Modal(document.getElementById('rejectModal'))
        modal.show()
      },
      async rejectRequest() {
        try {
          await api.post(`leave-requests/${this.currentRejectId}/reject/`, {
            reason: this.rejectReason
          })
          await this.loadDashboardData()
          bootstrap.Modal.getInstance(document.getElementById('rejectModal')).hide()
          this.$toast.success('申请已拒绝')
        } catch (error) {
          console.error('拒绝申请失败:', error)
          this.$toast.error('拒绝申请失败')
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
      }
    }
  }
  </script>