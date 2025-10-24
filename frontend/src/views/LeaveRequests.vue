<template>
  <div class="leave-requests-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="h2 mb-0">请假申请</h1>
      <button class="btn btn-primary" @click="showModal = true">
        <i class="fas fa-plus"></i> 新申请
      </button>
    </div>

    <!-- Responsive table container -->
    <div class="card shadow">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-bordered table-hover">
            <thead class="thead-light">
              <tr>
                <th>类型</th>
                <th>日期</th>
                <th>状态</th>
                <th>申请日期</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in leaveRequests" :key="request.id">
                <td>{{ formatLeaveType(request.leave_type) }}</td>
                <td>{{ formatDate(request.start_date) }} 至 {{ formatDate(request.end_date) }}</td>
                <td>
                  <span :class="getStatusClass(request.status)">{{ getStatusText(request.status) }}</span>
                </td>
                <td>{{ formatDate(request.applied_date) }}</td>
                <td>
                  <button class="btn btn-sm btn-info mr-1" @click="viewRequest(request)">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button v-if="request.status === 'pending'" class="btn btn-sm btn-danger"
                    @click="deleteRequest(request.id)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="leaveRequests.length === 0">
                <td colspan="5" class="text-center">暂无请假申请记录</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal for new request -->
<!-- Replace the existing modal section with this corrected version -->
<div class="modal fade" :class="{ show: showModal }" v-if="showModal" tabindex="-1"
  style="display: block; background-color: rgba(0,0,0,0.5);">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">新请假申请</h5>
        <button type="button" class="btn-close" @click="showModal = false"></button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="submitRequest">
          <div class="mb-3">
            <label for="leaveType" class="form-label">请假类型</label>
            <select class="form-select" id="leaveType" v-model="newRequest.leave_type" required>
              <option value="annual">年假</option>
              <option value="sick">病假</option>
              <option value="personal">事假</option>
              <option value="maternity">产假</option>
            </select>
          </div>

          <div class="mb-3">
            <label for="startDate" class="form-label">开始日期</label>
            <input type="date" class="form-control" id="startDate" v-model="newRequest.start_date" required>
          </div>

          <div class="mb-3">
            <label for="endDate" class="form-label">结束日期</label>
            <input type="date" class="form-control" id="endDate" v-model="newRequest.end_date" required>
          </div>

          <div class="mb-3">
            <label for="reason" class="form-label">请假原因</label>
            <textarea class="form-control" id="reason" v-model="newRequest.reason" rows="3"></textarea>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="showModal = false">取消</button>
        <button type="button" class="btn btn-primary" @click="submitRequest">提交</button>
      </div>
    </div>
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
      loading: true,
      showModal: false,
      newRequest: {
        leave_type: 'annual',
        start_date: '', 
        end_date: '',
        reason: ''
      }
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
    },
    // Added missing methods
    viewRequest(request) {
      // Implement view request functionality
      console.log('Viewing request:', request)
      // You can implement a modal or route to a detail page
    },
    async deleteRequest(id) {
      // Implement delete request functionality
      if (confirm('确定要删除这个请假申请吗？')) {
        try {
          await api.delete(`leave-requests/${id}/`)
          // Reload the requests after deletion
          await this.loadLeaveRequests()
        } catch (error) {
          console.error('删除请假申请失败:', error)
        }
      }
    },
    async submitRequest() {
      try {
        // Add applied_date and set status to pending
        const requestData = {
          ...this.newRequest,
          applied_date: new Date().toISOString().split('T')[0],
          status: 'pending'
        };
        
        await api.post('leave-requests/', requestData);
        this.showModal = false;
        this.resetForm();
        await this.loadLeaveRequests(); // Reload the list
      } catch (error) {
        console.error('提交请假申请失败:', error);
        // Handle error (show message to user)
      }
    },
    resetForm() {
      this.newRequest = {
        leave_type: 'annual',
        start_date: '',
        end_date: '',
        reason: ''
      };
    }
  }
}
</script>

<style scoped>
.leave-requests-container {
  padding: 20px;
}

/* Mobile responsive improvements */
@media (max-width: 767px) {
  .leave-requests-container {
    padding: 10px;
  }

  h1.h2 {
    font-size: 1.5rem;
  }

  .table-responsive {
    font-size: 0.85rem;
  }

  .table th,
  .table td {
    padding: 0.5rem;
  }

  .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }

  .mr-1 {
    margin-right: 0.25rem;
  }

  /* Stack action buttons on very small screens */
  @media (max-width: 400px) {
    .btn-sm {
      display: block;
      width: 100%;
      margin-bottom: 0.25rem;
    }

    .mr-1 {
      margin-right: 0;
    }
  }
}

.modal {
  z-index: 1050;
}

.modal.show {
  display: block;
}

.table-responsive {
  overflow-x: auto;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.shadow {
  box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
}
</style>