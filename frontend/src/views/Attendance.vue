<template>
  <div class="attendance-container">
    <div class="header d-flex justify-content-between align-items-center mb-4">
      <h1 class="page-title">考勤记录</h1>
      <div>
        <button class="btn btn-primary me-2 manual-btn" @click="openManualModal">
          <i class="bi bi-plus-circle"></i> 
          手动添加
        </button>
        <button class="btn btn-primary checkin-btn" @click="checkIn" :disabled="checkedIn">
          <i class="bi bi-box-arrow-in-right"></i> 
          {{ checkedIn ? '已签到' : '签到' }}
        </button>
      </div>
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
              <th>日期</th>
              <th>签到时间</th>
              <th>签退时间</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in attendanceRecords" :key="record.id">
              <td>{{ formatDate(record.date) }}</td>
              <td>{{ record.check_in || '-' }}</td>
              <td>{{ record.check_out || '-' }}</td>
              <td>
                <span :class="getStatusClass(record.status)">{{ getStatusText(record.status) }}</span>
              </td>
            </tr>
            <tr v-if="attendanceRecords.length === 0">
              <td colspan="4" class="text-center text-muted">暂无考勤记录</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Manual Attendance Modal -->
    <div class="modal fade" id="manualAttendanceModal" tabindex="-1" aria-labelledby="manualAttendanceModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="manualAttendanceModalLabel">手动添加考勤记录</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitManualAttendance">
              <div class="mb-3">
                <label for="date" class="form-label">日期</label>
                <input type="date" class="form-control" id="date" v-model="manualRecord.date" required>
              </div>
              <div class="mb-3">
                <label for="checkIn" class="form-label">签到时间</label>
                <input type="time" class="form-control" id="checkIn" v-model="manualRecord.check_in">
              </div>
              <div class="mb-3">
                <label for="checkOut" class="form-label">签退时间</label>
                <input type="time" class="form-control" id="checkOut" v-model="manualRecord.check_out">
              </div>
              <div class="mb-3">
                <label for="status" class="form-label">状态</label>
                <select class="form-select" id="status" v-model="manualRecord.status" required>
                  <option value="present">出勤</option>
                  <option value="absent">缺勤</option>
                  <option value="late">迟到</option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="submitManualAttendance">保存</button>
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
  name: 'Attendance',
  data() {
    return {
      attendanceRecords: [],
      checkedIn: false,
      loading: true,
      manualRecord: {
        date: '',
        check_in: '',
        check_out: '',
        status: 'present'
      },
      modal: null
    }
  },
  async created() {
    await this.loadAttendanceRecords()
    this.checkTodayCheckIn()
  },
  methods: {
    async loadAttendanceRecords() {
      try {
        this.loading = true
        const response = await api.get('attendance/')
        this.attendanceRecords = response.data
      } catch (error) {
        console.error('加载考勤记录失败:', error)
        alert('加载考勤记录失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    async checkIn() {
      try {
        const today = new Date().toISOString().split('T')[0]
        await api.post('attendance/', {
          date: today,
          check_in: new Date().toTimeString().split(' ')[0],
          status: 'present'
        })
        await this.loadAttendanceRecords()
        this.checkedIn = true
      } catch (error) {
        console.error('签到失败:', error)
        alert('签到失败: ' + error.message)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('zh-CN')
    },
    getStatusClass(status) {
      const classes = {
        present: 'badge bg-success',
        absent: 'badge bg-danger',
        late: 'badge bg-warning'
      }
      return classes[status] || 'badge bg-secondary'
    },
    getStatusText(status) {
      const texts = {
        present: '出勤',
        absent: '缺勤',
        late: '迟到'
      }
      return texts[status] || status
    },
    checkTodayCheckIn() {
      const today = new Date().toISOString().split('T')[0]
      const todayRecord = this.attendanceRecords.find(record => record.date === today)
      this.checkedIn = !!todayRecord && !!todayRecord.check_in
    },
    openManualModal() {
      // Set default date to today
      this.manualRecord.date = new Date().toISOString().split('T')[0]
      this.manualRecord.check_in = ''
      this.manualRecord.check_out = ''
      this.manualRecord.status = 'present'
      
      // Show modal using Bootstrap
      if (!this.modal) {
        this.modal = new Modal(document.getElementById('manualAttendanceModal'))
      }
      this.modal.show()
    },
    async submitManualAttendance() {
      try {
        // Prepare the data to send
        const payload = {
          date: this.manualRecord.date,
          status: this.manualRecord.status
        }
        
        // Only include check_in if it's not empty
        if (this.manualRecord.check_in) {
          payload.check_in = this.manualRecord.check_in
        }
        
        // Only include check_out if it's not empty
        if (this.manualRecord.check_out) {
          payload.check_out = this.manualRecord.check_out
        }
        
        console.log('Sending payload:', payload)
        
        // Send request to backend
        await api.post('attendance/', payload)
        
        // Reload records
        await this.loadAttendanceRecords()
        this.checkTodayCheckIn()
        
        // Hide modal
        if (this.modal) {
          this.modal.hide()
        }
        
        // Reset form
        this.manualRecord = {
          date: '',
          check_in: '',
          check_out: '',
          status: 'present'
        }
        
        alert('考勤记录添加成功')
      } catch (error) {
        console.error('添加考勤记录失败:', error.response?.data || error.message)
        alert('添加考勤记录失败: ' + (error.response?.data?.detail || error.message))
      }
    }
  }
}
</script>