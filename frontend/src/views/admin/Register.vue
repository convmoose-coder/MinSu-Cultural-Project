<template>
  <div class="register-container">
    <div class="register-form">
      <div class="register-header">
        <h2>创建管理员账号</h2>
        <p>请填写以下信息完成注册</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入密码（至少8位）"
            required
            minlength="8"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
          />
        </div>
        
        <button type="submit" class="register-btn" :disabled="isLoading || !isFormValid">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="login-link">
          已有账号？<router-link to="/admin/login">立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/admin/authService';

const router = useRouter();
const isLoading = ref(false);
const error = ref('');

interface RegisterForm {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const form = ref<RegisterForm>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// 表单验证
const isFormValid = computed(() => {
  return form.value.username && 
         form.value.email.includes('@') && 
         form.value.password.length >= 8 && 
         form.value.password === form.value.confirmPassword;
});

const handleRegister = async () => {
  if (!isFormValid.value) {
    error.value = '请检查表单填写是否正确';
    return;
  }
  
  isLoading.value = true;
  error.value = '';
  
  try {
    await authService.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      confirmPassword: form.value.confirmPassword
    });
    
    // 注册成功后跳转到登录页面
    router.push({
      path: '/admin/login',
      query: { registered: 'true' }
    });
  } catch (err) {
    error.value = err instanceof Error ? err.message : '注册失败，请重试';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-form {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  padding: 40px;
  width: 100%;
  max-width: 450px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  color: #1e293b;
  margin: 0 0 10px 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.register-header p {
  color: #64748b;
  margin: 0;
  font-size: 1rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  color: #334155;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="password"] {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input[type="text"]:focus,
.form-group input[type="email"]:focus,
.form-group input[type="password"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.register-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
  margin-top: 10px;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
  margin-top: 10px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #64748b;
  font-size: 0.9rem;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.login-link a:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .register-form {
    padding: 30px 20px;
  }
  
  .register-header h2 {
    font-size: 1.5rem;
  }
}
</style>