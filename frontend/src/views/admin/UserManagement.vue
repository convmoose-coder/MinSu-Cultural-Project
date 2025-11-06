<template>
  <AdminLayout>
    <div class="user-management-container">
      <h2 class="page-title">用户管理</h2>
      
      <!-- 搜索和操作区域 -->
      <div class="toolbar">
        <div class="search-area">
          <el-input 
            v-model="searchQuery" 
            placeholder="搜索用户名、邮箱或昵称" 
            prefix-icon="Search"
            clearable
            style="width: 300px;"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
          
          <el-select 
            v-model="roleFilter" 
            placeholder="用户角色" 
            clearable
            style="width: 150px; margin-left: 10px;"
            @change="handleSearch"
          >
            <el-option 
              v-for="role in roleOptions" 
              :key="role.value" 
              :label="role.label" 
              :value="role.value"
            />
          </el-select>
          
          <el-select 
            v-model="statusFilter" 
            placeholder="用户状态" 
            clearable
            style="width: 150px; margin-left: 10px;"
            @change="handleSearch"
          >
            <el-option label="正常" value="active" />
            <el-option label="禁用" value="disabled" />
            <el-option label="未激活" value="inactive" />
          </el-select>
          
          <el-button type="primary" @click="handleSearch" style="margin-left: 10px;">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </div>
        
        <div class="action-area">
          <el-button type="success" @click="handleAddUser">
            <el-icon><Plus /></el-icon>
            添加用户
          </el-button>
          
          <el-button type="warning" @click="handleBatchOperation">
            <el-icon><Operation /></el-icon>
            批量操作
          </el-button>
        </div>
      </div>
      
      <!-- 用户数据表格 -->
      <el-table 
        v-loading="loading" 
        :data="userList" 
        style="width: 100%"
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="id" label="用户ID" width="80" />
        
        <el-table-column prop="username" label="用户名" min-width="120" />
        
        <el-table-column prop="email" label="邮箱" min-width="180" />
        
        <el-table-column prop="nickname" label="昵称" min-width="120" />
        
        <el-table-column prop="role" label="角色" width="100">
          <template #default="scope">
            <el-tag 
              :type="getRoleType(scope.row.role)"
              size="small"
            >
              {{ getRoleLabel(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="80">
          <template #default="scope">
            <el-tag 
              :type="scope.row.status === 'active' ? 'success' : 'danger'"
              size="small"
            >
              {{ scope.row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="createdAt" label="注册时间" width="160">
          <template #default="scope">
            {{ formatDate(scope.row.createdAt) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="lastLogin" label="最后登录" width="160">
          <template #default="scope">
            {{ scope.row.lastLogin ? formatDate(scope.row.lastLogin) : '从未登录' }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              @click="handleEditUser(scope.row)"
            >
              编辑
            </el-button>
            
            <el-button 
              v-if="scope.row.status === 'active'"
              type="warning" 
              size="small" 
              @click="handleToggleStatus(scope.row)"
            >
              禁用
            </el-button>
            
            <el-button 
              v-else
              type="success" 
              size="small" 
              @click="handleToggleStatus(scope.row)"
            >
              启用
            </el-button>
            
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDeleteUser(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
      
      <!-- 添加/编辑用户对话框 -->
      <el-dialog 
        v-model="dialogVisible" 
        :title="dialogTitle" 
        width="500px"
        :close-on-click-modal="false"
      >
        <el-form 
          ref="userFormRef" 
          :model="userForm" 
          :rules="userRules"
          label-width="80px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="userForm.username" placeholder="请输入用户名" />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="userForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="userForm.nickname" placeholder="请输入昵称" />
          </el-form-item>
          
          <el-form-item label="角色" prop="role">
            <el-select v-model="userForm.role" placeholder="请选择角色">
              <el-option 
                v-for="role in roleOptions" 
                :key="role.value" 
                :label="role.label" 
                :value="role.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="userForm.status">
              <el-radio label="active">正常</el-radio>
              <el-radio label="disabled">禁用</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item v-if="!isEdit" label="密码" prop="password">
            <el-input 
              v-model="userForm.password" 
              type="password" 
              placeholder="请输入密码" 
              show-password
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSubmit">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Operation } from '@element-plus/icons-vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'

// 表格数据
const userList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索条件
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')

// 角色选项
const roleOptions = [
  { label: '普通用户', value: 'user' },
  { label: '内容编辑', value: 'editor' },
  { label: '管理员', value: 'admin' },
  { label: '超级管理员', value: 'superadmin' }
]

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('添加用户')
const userFormRef = ref()
const isEdit = ref(false)

// 表单数据
const userForm = reactive({
  id: '',
  username: '',
  email: '',
  nickname: '',
  role: 'user',
  status: 'active',
  password: ''
})

// 表单验证规则
const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择用户角色', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

// 多选
const selectedUsers = ref([])

// 获取角色标签类型
const getRoleType = (role: string) => {
  const types = {
    user: '',
    editor: 'warning',
    admin: 'danger',
    superadmin: 'success'
  }
  return types[role] || ''
}

// 获取角色标签文本
const getRoleLabel = (role: string) => {
  const roleMap = {
    user: '普通用户',
    editor: '内容编辑',
    admin: '管理员',
    superadmin: '超级管理员'
  }
  return roleMap[role] || role
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

// 搜索用户
const handleSearch = () => {
  currentPage.value = 1
  loadUserList()
}

// 加载用户列表
const loadUserList = async () => {
  loading.value = true
  try {
    // 模拟API调用
    // const response = await userApi.getUserList({
    //   page: currentPage.value,
    //   size: pageSize.value,
    //   search: searchQuery.value,
    //   role: roleFilter.value,
    //   status: statusFilter.value
    // })
    
    // 模拟数据
    userList.value = [
      {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        nickname: '系统管理员',
        role: 'superadmin',
        status: 'active',
        createdAt: '2024-01-01T00:00:00',
        lastLogin: '2024-01-15T10:30:00'
      },
      {
        id: 2,
        username: 'editor1',
        email: 'editor1@example.com',
        nickname: '内容编辑1',
        role: 'editor',
        status: 'active',
        createdAt: '2024-01-02T00:00:00',
        lastLogin: '2024-01-14T15:20:00'
      }
    ]
    total.value = 2
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

// 添加用户
const handleAddUser = () => {
  isEdit.value = false
  dialogTitle.value = '添加用户'
  Object.assign(userForm, {
    id: '',
    username: '',
    email: '',
    nickname: '',
    role: 'user',
    status: 'active',
    password: ''
  })
  dialogVisible.value = true
}

// 编辑用户
const handleEditUser = (user: any) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  Object.assign(userForm, {
    id: user.id,
    username: user.username,
    email: user.email,
    nickname: user.nickname,
    role: user.role,
    status: user.status,
    password: ''
  })
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await userFormRef.value.validate()
    
    if (isEdit.value) {
      // 编辑用户
      ElMessage.success('用户信息更新成功')
    } else {
      // 添加用户
      ElMessage.success('用户添加成功')
    }
    
    dialogVisible.value = false
    loadUserList()
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

// 切换用户状态
const handleToggleStatus = async (user: any) => {
  const newStatus = user.status === 'active' ? 'disabled' : 'active'
  const action = newStatus === 'active' ? '启用' : '禁用'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.username}" 吗？`,
      '提示',
      { type: 'warning' }
    )
    
    // 模拟API调用
    // await userApi.updateUserStatus(user.id, newStatus)
    
    ElMessage.success(`用户${action}成功`)
    loadUserList()
  } catch (error) {
    // 用户取消操作
  }
}

// 删除用户
const handleDeleteUser = async (user: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`,
      '警告',
      { type: 'warning' }
    )
    
    // 模拟API调用
    // await userApi.deleteUser(user.id)
    
    ElMessage.success('用户删除成功')
    loadUserList()
  } catch (error) {
    // 用户取消操作
  }
}

// 批量操作
const handleBatchOperation = () => {
  if (selectedUsers.value.length === 0) {
    ElMessage.warning('请先选择要操作的用户')
    return
  }
  
  // 实现批量操作逻辑
  ElMessage.info(`已选择 ${selectedUsers.value.length} 个用户`)
}

// 多选变化
const handleSelectionChange = (selection: any[]) => {
  selectedUsers.value = selection
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadUserList()
}

// 当前页变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadUserList()
}

onMounted(() => {
  loadUserList()
})
</script>

<style scoped>
.user-management-container {
  max-width: 100%;
  padding: 20px;
}

.page-title {
  color: #1e293b;
  margin-bottom: 24px;
  font-size: 1.8rem;
  font-weight: 600;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.search-area {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.action-area {
  display: flex;
  gap: 10px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-area {
    justify-content: center;
  }
  
  .action-area {
    justify-content: center;
  }
}
</style>