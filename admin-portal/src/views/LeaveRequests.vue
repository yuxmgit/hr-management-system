<!-- src/views/LeaveRequests.vue -->
<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h2">请假申请管理</h1>
      <div>
        <select class="form-select d-inline-block w-auto me-2" v-model="filterStatus">
          <option value="">所有状态</option>
          <option value="pending">待处理</option>
          <option value="approved">已批准</option>
          <option value="rejected">已拒绝</option>
        </select>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>员工</th>
              <th>类型</th>
              <th>日期</th>
              <th>天数</th>
              <th>原因</th>
              <th>申请时间</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in filteredRequests" :key="request.id">
              <td>{{ request.employee_name }} ({{ request.employee_id }})</td>
              <td>{{ formatLeaveType(request.leave_type) }}</td>
              <td>{{ formatDate(request.start_date) }} 至 {{ formatDate(request.end_date) }}</td>
              <td>{{ calculateDays(request.start_date, request.end_date) }} 天</td>
              <td>{{ request.reason.substring(0, 30) }}{{ request.reason.length > 30 ? '...' : '' }}</td>
              <td>{{ formatDate(request.applied_date) }}</td>
              <td>
                <span :class="getStatusClass(request.status)">{{ getStatusText(request.status) }}</span>
              </td>
              <td>
                <div v-if="request.status === 'pending'">
                  <button class="btn btn-sm btn-success me-1" @click="approveRequest(request.id)">批准</button>
                  <button class="btn btn-sm btn-danger" @click="showRejectModal(request.id)">拒绝</button>
                </div>
                <div v-else>
                  <span v-if="request.status === 'approved'" class="text-success">已批准</span>
                  <span v-if="request.status === 'rejected'" class="text-danger">已拒绝</span>
                </div>
              </td>
            </tr>
            <tr v-if="filteredRequests.length === 0">
              <td colspan="8" class="text-center">暂无请假申请记录</td>
            </tr>
          </tbody>
        </table>
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
  name: 'LeaveRequestsManagement',
  data() {
    return {
      leaveRequests: [],
      filterStatus: '',
      currentRejectId: null,
      rejectReason: ''
    }
  },
  computed: {
    filteredRequests() {
      if (!this.filterStatus) {
        return this.leaveRequests
      }
      return this.leaveRequests.filter(request => request.status === this.filterStatus)
    }
  },
  async created() {
    await this.loadLeaveRequests()
  },
  methods: {
    async loadLeaveRequests() {
      try {
        const response = await api.get('leave-requests/')
        this.leaveRequests = response.data
      } catch (error) {
        console.error('加载请假申请失败:', error)
      }
    },
    // 批准请假// 修改 approveRequest 方法
    // Replace your current approveRequest and rejectRequest methods with:

    async approveRequest(id) {
      try {
        const response = await api.post(`leave-requests/${id}/`, {
          action: 'approve'
        });
        // this.$toast.success('请假申请已批准');
        await this.loadLeaveRequests();
      } catch (error) {
        console.error('批准失败:', error);
        this.$toast.error('批准失败');
      }
    },

    async rejectRequest() {
      try {
        const response = await api.post(`leave-requests/${this.currentRejectId}/`, {
          action: 'reject',
          reason: this.rejectReason
        });
        // this.$toast.success('请假申请已拒绝');
        Modal.getInstance(document.getElementById('rejectModal')).hide();
        await this.loadLeaveRequests();
      } catch (error) {
        console.error('拒绝失败:', error);
        this.$toast.error('拒绝失败');
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