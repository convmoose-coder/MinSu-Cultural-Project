<template>
  <div class="admin-login-container">
    <div class="login-form-wrapper">
      <h1 class="login-title">管理员登录</h1>
      <el-form 
        :model="loginForm" 
        :rules="rules" 
        ref="loginFormRef"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="用户名"
            prefix-icon="el-icon-user"
            :disabled="loading"
          ></el-input>
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            placeholder="密码"
            prefix-icon="el-icon-lock"
            show-password
            :disabled="loading"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="rememberMe">记住登录</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button"
            @click="handleLogin"
            :loading="loading"
            :disabled="loading"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage, ElForm } from 'element-plus';
import { useRouter } from 'vue-router';
import type { FormInstance, FormRules } from 'element-plus';
import authService from '@/services/admin/authService';

const router = useRouter();
const loginFormRef = ref<InstanceType<typeof ElForm>>();
const loading = ref(false);
const errorMessage = ref('');
const rememberMe = ref(false);

const loginForm = reactive({
  username: 'admin',
  password: 'admin'
});

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 5, max: 20, message: '密码长度在 5 到 20 个字符之间', trigger: 'blur' }
  ]
});

const handleLogin = async () => {
  errorMessage.value = '';
  
  // 表单验证
  if (loginFormRef.value) {
    try {
      await loginFormRef.value.validate();
      
      // 验证通过，继续登录逻辑
      loading.value = true;
      try {
        const response = await authService.login({
  username: loginForm.username,
  password: loginForm.password,
  remember: rememberMe.value
});
        console.log('Login response:', response);
        
        // 存储登录状态
        const { token, user } = response;
        localStorage.setItem('admin-token', token);
        localStorage.removeItem('adminUser'); // 不再需要这个，使用token即可
        
        // 如果选择记住登录，可以使用localStorage
        if (rememberMe.value) {
          localStorage.setItem('rememberAdmin', 'true');
        } else {
          localStorage.removeItem('rememberAdmin');
        }
        
        // 登录成功，跳转到仪表盘
        ElMessage.success('登录成功');
        router.push('/admin/dashboard');
      } catch (error) {
        console.error('Login error:', error);
        errorMessage.value = error.response?.data?.message || '登录失败，请检查用户名和密码';
        ElMessage.error(errorMessage.value);
      } finally {
        loading.value = false;
      }
    } catch (error: any) {
      console.error('登录失败:', error);
      if (error.response?.data?.message) {
        errorMessage.value = error.response.data.message;
      } else {
        errorMessage.value = '登录失败，请检查用户名和密码';
        ElMessage.error('登录失败');
      }
    } finally {
      loading.value = false;
    }
  }
};

// 初始化时检查是否记住登录
const initRememberLogin = () => {
  const remember = localStorage.getItem('rememberAdmin');
  if (remember === 'true') {
    rememberMe.value = true;
    // 可以在这里自动填充用户名（如果安全允许）
  }
};

initRememberLogin();
</script>

<style scoped>
.admin-login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  background-image: 
    radial-gradient(#e5e9f0 1px, transparent 0),
    radial-gradient(#e5e9f0 1px, transparent 0);
  background-size: 20px 20px;
  background-position: 0 0, 10px 10px;
}

.login-form-wrapper {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  position: relative;
  overflow: hidden;
}

.login-form-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(103, 119, 255, 0.05), transparent);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(10deg); }
}

.login-title {
  text-align: center;
  color: #1f2937;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.login-form {
  position: relative;
  z-index: 1;
}

.login-form-item {
  margin-bottom: 1.5rem;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  background: linear-gradient(135deg, #6b46c1, #4c1d95);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(107, 70, 193, 0.4);
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
}

.error-message {
  color: #e53e3e;
  font-size: 0.875rem;
  text-align: center;
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fef2f2;
  border-radius: 6px;
  border: 1px solid #fee2e2;
}

/* 输入框样式优化 */
:deep(.el-input__wrapper) {
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:focus-within) {
  box-shadow: 0 0 0 3px rgba(107, 70, 193, 0.1);
}

:deep(.el-checkbox) {
  color: #4b5563;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-form-wrapper {
    margin: 1rem;
    padding: 2rem 1.5rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>