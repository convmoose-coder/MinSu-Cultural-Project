<template>
  <AdminLayout>
    <div class="dashboard-container">
      <h2 class="page-title">仪表盘概览</h2>
      
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-icon users-icon">👥</div>
          <div class="stat-content">
            <div class="stat-number">{{ userCount }}</div>
            <div class="stat-label">用户数量</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon data-icon">📊</div>
          <div class="stat-content">
            <div class="stat-number">{{ dataCount }}</div>
            <div class="stat-label">数据条目</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon upload-icon">📤</div>
          <div class="stat-content">
            <div class="stat-number">{{ uploadCount }}</div>
            <div class="stat-label">上传次数</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon views-icon">👁️</div>
          <div class="stat-content">
            <div class="stat-number">{{ viewCount }}</div>
            <div class="stat-label">访问量</div>
          </div>
        </div>
      </div>
      
      <div class="recent-activity">
        <h3>最近活动</h3>
        <div v-if="loading" class="loading-placeholder">加载中...</div>
        <div v-else class="activity-list">
          <div v-if="recentActivities.length === 0" class="no-activities">暂无活动记录</div>
          <div 
            v-for="activity in recentActivities" 
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon">
              {{ activity.type === 'upload' ? '📤' : 
                 activity.type === 'user' ? '👥' : '⚙️' }}
            </div>
            <div class="activity-content">
              <div class="activity-text">{{ activity.text }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import AdminLayout from '@/components/admin/AdminLayout.vue';
import { dashboard } from '@/services/api';

// 统计数据
const userCount = ref(0);
const dataCount = ref(0);
const uploadCount = ref(0);
const viewCount = ref(0);
const recentActivities = ref([]);
const loading = ref(true);

// 从API获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    loading.value = true;
    const response = await dashboard.getDashboardData();
    
    // 更新统计数据
    userCount.value = response.stats.userCount;
    dataCount.value = response.stats.dataCount;
    uploadCount.value = response.stats.uploadCount;
    viewCount.value = response.stats.viewCount;
    recentActivities.value = response.recentActivities;
    
  } catch (error) {
    console.error('获取仪表盘数据失败:', error);
    ElMessage.error('获取数据失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>
.dashboard-container {
  max-width: 100%;
}

.page-title {
  color: #1e293b;
  margin-bottom: 24px;
  font-size: 1.8rem;
  font-weight: 600;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 2.5rem;
  margin-right: 16px;
  padding: 12px;
  background-color: #f1f5f9;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.recent-activity {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.recent-activity h3 {
  color: #1e293b;
  margin-bottom: 16px;
  font-size: 1.2rem;
  font-weight: 600;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 12px;
  border-radius: 8px;
  background-color: #f8fafc;
}

.activity-icon {
  font-size: 1.2rem;
  margin-right: 12px;
  padding: 8px;
  background-color: white;
  border-radius: 50%;
  min-width: 36px;
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #1e293b;
  font-weight: 500;
  margin-bottom: 4px;
}

.activity-time {
  color: #94a3b8;
  font-size: 0.85rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>