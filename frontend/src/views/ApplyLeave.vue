<template>
    <div>
      <h1 class="h2 mb-4">申请请假</h1>
      
      <div class="card">
        <div class="card-body">
          <form @submit.prevent="submitLeaveRequest">
            <div class="mb-3">
              <label for="leaveType" class="form-label">请假类型</label>
              <select class="form-select" id="leaveType" v-model="formData.leave_type" required>
                <option value="">请选择请假类型</option>
                <option value="annual">年假</option>
                <option value="sick">病假</option>
                <option value="personal">事假</option>
                <option value="maternity">产假</option>
              </select>
            </div>
            
            <div class="row">
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="startDate" class="form-label">开始日期</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="startDate" 
                    v-model="formData.start_date" 
                    required
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="endDate" class="form-label">结束日期</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="endDate" 
                    v-model="formData.end_date" 
                    required
                  >
                </div>
              </div>
            </div>
            
            <div class="mb-3">
              <label for="reason" class="form-label">请假原因</label>
              <textarea 
                class="form-control" 
                id="reason" 
                rows="4" 
                v-model="formData.reason" 
                placeholder="请详细说明请假原因"
                required
              ></textarea>
            </div>
            
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
              {{ loading ? '提交中...' : '提交申请' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../services/api'
  
  export default {
    name: 'ApplyLeave',
    data() {
      return {
        formData: {
          leave_type: '',
          start_date: '',
          end_date: '',
          reason: ''
        },
        loading: false
      }
    },
    methods: {
      async submitLeaveRequest() {
        this.loading = true
        
        try {
          await api.post('leave-requests/', this.formData)
          this.$router.push('/leave-requests')
          // 可以添加成功消息提示
        } catch (error) {
          console.error('提交请假申请失败:', error)
          alert('提交请假申请失败')
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>