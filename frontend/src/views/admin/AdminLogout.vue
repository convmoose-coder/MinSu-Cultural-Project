<template>
  <div class="logout-container">
    <div class="logout-content">
      <el-icon class="logout-icon"><SwitchButton /></el-icon>
      <h2>正在退出登录...</h2>
      <p>请稍候，正在清理您的会话信息</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { SwitchButton } from '@element-plus/icons-vue';
import { auth } from '@/services/api';

const router = useRouter();

const handleLogout = async () => {
  try {
    // 调用后端退出登录接口
    await auth.logout();
  } catch (error) {
    console.error('退出登录API调用失败:', error);
    // API调用失败不阻止本地退出流程
  } finally {
    // 清理本地存储的认证信息
    localStorage.removeItem('admin-token');
    localStorage.removeItem('adminUser');
    localStorage.removeItem('rememberAdmin');
    
    // 显示成功消息
    ElMessage.success('已成功退出登录');
    
    // 延迟重定向到登录页，给用户时间看到提示
    setTimeout(() => {
      router.replace('/admin/login');
    }, 1500);
  }
};

onMounted(() => {
  // 组件挂载后立即执行退出登录
  handleLogout();
});
</script>

<style scoped>
.logout-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.logout-content {
  text-align: center;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 90%;
}

.logout-icon {
  font-size: 4rem;
  color: #6b46c1;
  margin-bottom: 1.5rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

p {
  color: #6b7280;
  font-size: 1rem;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .logout-content {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .logout-icon {
    font-size: 3rem;
  }
  
  h2 {
    font-size: 1.25rem;
  }
}
</style>