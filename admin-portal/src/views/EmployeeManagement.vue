<!-- src/views/EmployeeManagement.vue -->
<template>
    <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h2">员工管理</h1>
        <button class="btn btn-primary" @click="showAddEmployeeModal">
          <i class="bi bi-plus-circle"></i> 添加员工
        </button>
      </div>
      
      <div class="card">
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-6">
              <input type="text" class="form-control" placeholder="搜索员工..." v-model="searchTerm">
            </div>
          </div>
          
          <table class="table table-striped">
            <thead>
              <tr>
                <th>员工编号</th>
  <th>姓名</th>
                <th>部门</th>
                <th>职位</th>
                <th>入职日期</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="employee in filteredEmployees" :key="employee.id">
                <td>{{ employee.employee_id }}</td>
                <td>{{ employee.user.first_name }} {{ employee.user.last_name }}</td>
                <td>{{ employee.department }}</td>
                <td>{{ employee.position }}</td>
                <td>{{ formatDate(employee.hire_date) }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="editEmployee(employee)">编辑</button>
                  <button class="btn btn-sm btn-outline-danger" @click="deleteEmployee(employee.id)">删除</button>
                </td>
              </tr>
              <tr v-if="filteredEmployees.length === 0">
                <td colspan="6" class="text-center">暂无员工记录</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 添加/编辑员工模态框 -->
      <div class="modal fade" id="employeeModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ isEditing ? '编辑员工' : '添加员工' }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveEmployee">
                <div class="mb-3">
                  <label for="employeeId" class="form-label">员工编号</label>
                  <input type="text" class="form-control" id="employeeId" v-model="currentEmployee.employee_id" required>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label">名字</label>
                    <input type="text" class="form-control" id="firstName" v-model="currentEmployee.first_name" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label">姓氏</label>
                    <input type="text" class="form-control" id="lastName" v-model="currentEmployee.last_name" required>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">邮箱</label>
                  <input type="email" class="form-control" id="email" v-model="currentEmployee.email" required>
                </div>
                <div class="mb-3">
                  <label for="department" class="form-label">部门</label>
                  <input type="text" class="form-control" id="department" v-model="currentEmployee.department" required>
                </div>
                <div class="mb-3">
                  <label for="position" class="form-label">职位</label>
                  <input type="text" class="form-control" id="position" v-model="currentEmployee.position" required>
                </div>
                <div class="mb-3">
                  <label for="hireDate" class="form-label">入职日期</label>
                  <input type="date" class="form-control" id="hireDate" v-model="currentEmployee.hire_date" required>
                </div>
                <div v-if="!isEditing" class="mb-3">
                  <label for="password" class="form-label">密码</label>
                  <input type="password" class="form-control" id="password" v-model="currentEmployee.password" required>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
              <button type="button" class="btn btn-primary" @click="saveEmployee">保存</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../services/api'
  // 引入Bootstrap模态框
  import { Modal } from 'bootstrap'
  export default {
    name: 'EmployeeManagement',
    data() {
      return {
        employees: [],
        searchTerm: '',
        isEditing: false,
        currentEmployee: {
          id: null,
          employee_id: '',
          first_name: '',
          last_name: '',
          email: '',
          department: '',
          position: '',
          hire_date: '',
          password: ''
        }
      }
    },
    computed: {
      filteredEmployees() {
        if (!this.searchTerm) {
          return this.employees
        }
        const term = this.searchTerm.toLowerCase()
        return this.employees.filter(emp => 
          emp.employee_id.toLowerCase().includes(term) ||
          emp.user.first_name.toLowerCase().includes(term) ||
          emp.user.last_name.toLowerCase().includes(term) ||
          emp.department.toLowerCase().includes(term) ||
          emp.position.toLowerCase().includes(term)
        )
      }
    },
    async created() {
      await this.loadEmployees()
    },
    methods: {
      async loadEmployees() {
        try {
          const response = await api.get('employees/')
          this.employees = response.data
        } catch (error) {
          console.error('加载员工信息失败:', error)
        }
      },
      showAddEmployeeModal() {
        this.isEditing = false
        this.currentEmployee = {
          id: null,
          employee_id: '',
          first_name: '',
          last_name: '',
          email: '',
          department: '',
          position: '',
          hire_date: '',
          password: ''
        }
        const modal = new Modal(document.getElementById('employeeModal'))
        modal.show()
      },
      editEmployee(employee) {
        this.isEditing = true
        this.currentEmployee = {
          id: employee.id,
          employee_id: employee.employee_id,
          first_name: employee.user.first_name,
          last_name: employee.user.last_name,
          email: employee.user.email,
          department: employee.department,
          position: employee.position,
          hire_date: employee.hire_date
        }
        const modal = new Modal(document.getElementById('employeeModal'))
        modal.show()
      },
      async saveEmployee() {
        try {
          if (this.isEditing) {
            // 编辑员工（需要后端支持）
            await api.put(`employees/${this.currentEmployee.id}/`, this.currentEmployee)
            this.$toast.success('员工信息已更新')
          } else {
            // 添加员工（需要后端添加注册API）
            await api.post('register/', this.currentEmployee)
            this.$toast.success('员工已添加')
          }
          const modal = Modal.getInstance(document.getElementById('employeeModal'))
          if (modal) modal.hide()
          await this.loadEmployees()
        } catch (error) {
          console.error('保存员工信息失败:', error)
          this.$toast.error(`保存员工信息失败: ${error?.response?.data?.message || error.message || '未知错误'}`)
        }
      },
      async deleteEmployee(id) {
        if (confirm('确定要删除此员工吗？')) {
          try {
            await api.delete(`employees/${id}/`)
            await this.loadEmployees()
            this.$toast.success('员工已删除')
          } catch (error) {
            console.error('删除员工失败:', error)
            this.$toast.error(`删除员工失败: ${error?.response?.data?.message || error.message || '未知错误'}`)
          }
        }
      },
      formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('zh-CN')
      }
    }
  }
  </script>