<template>
  <div class="login-container">
    <div class="login-form">
      <div class="login-header">
        <h2>后台管理系统</h2>
        <p>请输入管理员账号密码登录</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="form">
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
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>
        
        <div class="form-group remember">
          <label>
            <input type="checkbox" v-model="form.remember" />
            记住我
          </label>
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
        
        <button type="submit" class="login-btn" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/admin/authService';

const router = useRouter();
const isLoading = ref(false);
const error = ref('');

interface LoginForm {
  username: string;
  password: string;
  remember: boolean;
}

const form = ref<LoginForm>({
  username: '',
  password: '',
  remember: false
});

const handleLogin = async () => {
  isLoading.value = true;
  error.value = '';
  
  try {
    // 调用认证服务进行登录
    const response = await authService.login({
      username: form.value.username,
      password: form.value.password,
      remember: form.value.remember
    });
    
    // 保存token
    localStorage.setItem('admin-token', response.token);
    
    // 跳转到仪表盘
    router.push('/admin/dashboard');
  } catch (err) {
    error.value = err instanceof Error ? err.message : '登录失败，请重试';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-form {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #1e293b;
  margin: 0 0 10px 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.login-header p {
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
.form-group input[type="password"] {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input[type="text"]:focus,
.form-group input[type="password"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group.remember {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.form-group.remember label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 400;
}

.forgot-password {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: #764ba2;
  text-decoration: underline;
}

.login-btn {
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

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.login-btn:disabled {
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

/* 响应式设计 */
@media (max-width: 480px) {
  .login-form {
    padding: 30px 20px;
  }
  
  .login-header h2 {
    font-size: 1.5rem;
  }
}
</style>