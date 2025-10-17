<!-- src/views/AttendanceRecords.vue -->
<template>
    <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h2">考勤记录</h1>
        <div>
          <input type="date" class="form-control d-inline-block w-auto me-2" v-model="filterDate">
          <button class="btn btn-secondary" @click="loadAttendanceRecords">筛选</button>
        </div>
      </div>
      
      <div class="card">
        <div class="card-body">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>员工</th>
                <th>日期</th>
                <th>签到时间</th>
                <th>签退时间</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in attendanceRecords" :key="record.id">
                <td>{{ record.employee_name }}</td>
                <td>{{ formatDate(record.date) }}</td>
                <td>{{ record.check_in || '-' }}</td>
                <td>{{ record.check_out || '-' }}</td>
                <td>
                  <span :class="getStatusClass(record.status)">{{ getStatusText(record.status) }}</span>
                </td>
              </tr>
              <tr v-if="attendanceRecords.length === 0">
                <td colspan="5" class="text-center">暂无考勤记录</td>
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
    name: 'AttendanceRecords',
    data() {
      return {
        attendanceRecords: [],
        filterDate: ''
      }
    },
    async created() {
      // 默认显示今天的记录
      this.filterDate = new Date().toISOString().split('T')[0]
      await this.loadAttendanceRecords()
    },
    methods: {
      async loadAttendanceRecords() {
        try {
          let url = 'attendance/'
          if (this.filterDate) {
            url += `?date=${this.filterDate}`
          }
          const response = await api.get(url)
          this.attendanceRecords = response.data
        } catch (error) {
          console.error('加载考勤记录失败:', error)
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
      }
    }
  }
  </script>