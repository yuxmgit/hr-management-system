<template>
    <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h2">考勤记录</h1>
        <button class="btn btn-primary" @click="checkIn" :disabled="checkedIn">
          <i class="bi bi-box-arrow-in-right"></i> 
          {{ checkedIn ? '已签到' : '签到' }}
        </button>
      </div>
      
      <div class="card">
        <div class="card-body">
          <table class="table table-striped">
            <thead>
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
                <td colspan="4" class="text-center">暂无考勤记录</td>
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
    name: 'Attendance',
    data() {
      return {
        attendanceRecords: [],
        checkedIn: false
      }
    },
    async created() {
      await this.loadAttendanceRecords()
      this.checkTodayCheckIn()
    },
    methods: {
      async loadAttendanceRecords() {
        try {
          const response = await api.get('attendance/')
          this.attendanceRecords = response.data
        } catch (error) {
          console.error('加载考勤记录失败:', error)
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
          alert('签到失败')
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
      }
    }
  }
  </script>