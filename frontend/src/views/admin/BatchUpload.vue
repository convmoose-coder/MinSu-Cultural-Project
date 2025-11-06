<template>
  <div class="batch-upload-container">
    <h2 class="page-title">批量数据上传</h2>
    
    <el-card class="upload-card">
      <template #header>
        <div class="upload-header">
          <span class="header-title">上传文件</span>
          <div class="file-type-hint">支持格式: CSV, Excel (.xlsx)</div>
        </div>
      </template>
      
      <div 
        class="dropzone"
        :class="{ 'drag-over': isDragging }"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <div v-if="!selectedFile" class="upload-placeholder">
          <el-icon class="upload-icon"><UploadFilled /></el-icon>
          <p class="upload-text">拖拽文件到此处或点击选择文件</p>
          <p class="upload-subtext">最大支持10MB，支持CSV和Excel格式</p>
        </div>
        
        <div v-else class="file-info">
          <el-icon class="file-icon"><Document /></el-icon>
          <div class="file-details">
            <div class="file-name">{{ selectedFile.name }}</div>
            <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
          </div>
          <el-button 
            type="danger" 
            circle 
            size="small" 
            @click.stop="removeFile"
            class="remove-btn"
          >
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </div>
      
      <input 
        ref="fileInput"
        type="file" 
        class="file-input" 
        accept=".csv,.xlsx"
        @change="handleFileChange"
      >
      
      <div class="upload-options">
        <el-form :model="formData" label-width="80px">
          <div class="form-row">
            <el-form-item label="数据类型:">
              <el-select v-model="formData.dataType" placeholder="请选择数据类型">
                <el-option value="folk_culture" label="民俗文化" />
                <el-option value="region" label="地区信息" />
                <el-option value="festival" label="民族节日" />
                <el-option value="users" label="用户数据" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="上传方式:">
              <el-radio-group v-model="formData.uploadMode">
                <el-radio value="append">追加数据</el-radio>
                <el-radio value="replace">替换数据</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
          
          <el-form-item v-if="formData.dataType" label="字段映射:">
            <el-alert
              :title="getMappingInfo(formData.dataType)"
              type="info"
              :closable="false"
              show-icon
            />
          </el-form-item>
        </el-form>
      </div>
      
      <el-button 
        type="primary" 
        class="upload-btn" 
        :disabled="!selectedFile || isUploading"
        @click="uploadFile"
        :loading="isUploading"
        size="large"
      >
        <el-icon v-if="!isUploading"><Upload /></el-icon>
        <el-icon v-else><Loading /></el-icon>
        {{ isUploading ? '上传中...' : '开始上传' }}
      </el-button>
      
      <el-progress 
        v-if="uploadProgress > 0" 
        :percentage="uploadProgress" 
        :status="uploadProgress === 100 ? 'success' : 'primary'"
        :stroke-width="8"
        :show-text="true"
        class="progress-bar"
      />
    </el-card>
    
    <el-alert
      v-if="uploadStatus"
      :title="uploadStatus.message"
      :type="uploadStatus.type"
      :closable="true"
      show-icon
      @close="clearStatus"
      class="status-message"
    />
    
    <el-card v-if="uploadResults" class="results-card" shadow="hover">
      <template #header>
        <span>上传结果</span>
      </template>
      
      <div class="results-stats">
        <el-statistic title="成功导入" :value="uploadResults.successCount" :precision="0">
          <template #suffix>
            <el-icon><Check /></el-icon>
          </template>
        </el-statistic>
        
        <el-statistic v-if="uploadResults.warningCount" title="警告" :value="uploadResults.warningCount" :precision="0">
          <template #suffix>
            <el-icon><Warning /></el-icon>
          </template>
        </el-statistic>
        
        <el-statistic v-if="uploadResults.errorCount" title="失败" :value="uploadResults.errorCount" :precision="0">
          <template #suffix>
            <el-icon><Close /></el-icon>
          </template>
        </el-statistic>
      </div>
      
      <el-collapse v-if="uploadResults.errors && uploadResults.errors.length > 0">
        <el-collapse-item title="错误详情" name="errors">
          <el-table :data="errorTableData" border style="width: 100%">
            <el-table-column prop="row" label="行号" width="80" />
            <el-table-column prop="message" label="错误信息" />
          </el-table>
        </el-collapse-item>
      </el-collapse>
      
      <el-collapse v-if="uploadResults.warnings && uploadResults.warnings.length > 0">
        <el-collapse-item title="警告详情" name="warnings">
          <el-table :data="warningTableData" border style="width: 100%">
            <el-table-column prop="row" label="行号" width="80" />
            <el-table-column prop="message" label="警告信息" />
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-card>
    
    <el-card class="template-section" shadow="hover">
      <template #header>
        <span>下载模板</span>
      </template>
      
      <p class="template-desc">下载标准数据模板，按照格式填写后再上传</p>
      
      <el-divider>可用模板</el-divider>
      
      <div class="template-grid">
        <el-card 
          v-for="template in availableTemplates" 
          :key="template.id"
          class="template-item"
          shadow="hover"
        >
          <template #header>
            <div class="template-header">
              <el-icon v-if="template.format === 'CSV'" class="template-icon"><Document /></el-icon>
              <el-icon v-else class="template-icon"><Grid /></el-icon>
              <span>{{ template.name }}</span>
            </div>
          </template>
          
          <div class="template-meta">
            <span class="template-format">{{ template.format }}</span>
            <span class="template-fields">{{ template.fields.length }}个字段</span>
          </div>
          
          <el-button 
            type="info" 
            size="small" 
            class="download-btn"
            @click="downloadTemplate(template.type, template.format)"
          >
            <el-icon><Download /></el-icon>
            下载
          </el-button>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import axios from 'axios';
import { ElMessage, ElNotification } from 'element-plus';
import {
  UploadFilled,
  Upload,
  Close,
  Document,
  Grid,
  Download,
  Check,
  Warning,
  Loading
} from '@element-plus/icons-vue';

// 表单数据
const formData = ref({
  dataType: 'folk_culture',
  uploadMode: 'append'
});

// 响应式数据
const fileInput = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);
const isDragging = ref(false);
const isUploading = ref(false);
const uploadProgress = ref(0);
const uploadStatus = ref<{ type: 'success' | 'warning' | 'error' | 'info'; message: string } | null>(null);
const uploadResults = ref<any>(null);

// 可用模板配置
const availableTemplates = [
  { id: '1', type: 'folk_culture', name: '民俗文化数据模板', format: 'CSV', fields: getTemplateFields('folk_culture') },
  { id: '2', type: 'folk_culture', name: '民俗文化数据模板', format: 'Excel', fields: getTemplateFields('folk_culture') },
  { id: '3', type: 'region', name: '地区信息数据模板', format: 'CSV', fields: getTemplateFields('region') },
  { id: '4', type: 'region', name: '地区信息数据模板', format: 'Excel', fields: getTemplateFields('region') },
  { id: '5', type: 'festival', name: '民族节日数据模板', format: 'CSV', fields: getTemplateFields('festival') },
  { id: '6', type: 'festival', name: '民族节日数据模板', format: 'Excel', fields: getTemplateFields('festival') }
];

// 获取模板字段信息
function getTemplateFields(type: string) {
  const fieldsMap: Record<string, Array<{ name: string; required: boolean; description: string }>> = {
    folk_culture: [
      { name: 'name', required: true, description: '文化名称' },
      { name: 'category', required: true, description: '分类' },
      { name: 'region', required: true, description: '所属地区' },
      { name: 'description', required: false, description: '详细描述' },
      { name: 'history', required: false, description: '历史背景' },
      { name: 'features', required: false, description: '文化特色' },
      { name: 'images', required: false, description: '图片链接（多个用逗号分隔）' }
    ],
    region: [
      { name: 'name', required: true, description: '地区名称' },
      { name: 'level', required: true, description: '行政级别' },
      { name: 'parent', required: false, description: '上级地区' },
      { name: 'description', required: false, description: '地区描述' },
      { name: 'location', required: false, description: '地理位置' }
    ],
    festival: [
      { name: 'name', required: true, description: '节日名称' },
      { name: 'date', required: true, description: '日期（YYYY-MM-DD）' },
      { name: 'ethnic_group', required: true, description: '所属民族' },
      { name: 'region', required: false, description: '主要流行地区' },
      { name: 'description', required: false, description: '节日描述' },
      { name: 'customs', required: false, description: '传统习俗' }
    ]
  };
  
  return fieldsMap[type] || [];
}

// 获取映射信息
function getMappingInfo(type: string) {
  const mappingInfo: Record<string, string> = {
    folk_culture: '请确保CSV/Excel包含：name(必填), category(必填), region(必填), description, history, features, images',
    region: '请确保CSV/Excel包含：name(必填), level(必填), parent, description, location',
    festival: '请确保CSV/Excel包含：name(必填), date(必填, YYYY-MM-DD), ethnic_group(必填), region, description, customs'
  };
  
  return mappingInfo[type] || '请按照模板格式准备数据';
}

// 文件拖放处理
const handleDragOver = () => {
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const handleDrop = (e: DragEvent) => {
  isDragging.value = false;
  const files = e.dataTransfer?.files;
  if (files && files.length > 0) {
    processFile(files[0]);
  }
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (files && files.length > 0) {
    processFile(files[0]);
  }
};

// 文件处理和验证
const processFile = (file: File) => {
  // 验证文件类型
  const validExtensions = ['.csv', '.xlsx'];
  const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
  
  if (!validExtensions.includes(fileExtension)) {
    ElMessage.error('请上传CSV或Excel格式的文件');
    return;
  }
  
  // 验证文件大小（限制为10MB）
  const maxSize = 10 * 1024 * 1024; // 10MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过10MB');
    return;
  }
  
  selectedFile.value = file;
  uploadResults.value = null;
  uploadStatus.value = null;
  
  ElNotification({
    title: '文件已选择',
    message: `已选择文件: ${file.name}`,
    type: 'success',
    duration: 3000
  });
};

// 移除文件
const removeFile = () => {
  selectedFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  uploadProgress.value = 0;
  uploadResults.value = null;
  uploadStatus.value = null;
};

// 文件大小格式化
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// 上传文件
const uploadFile = async () => {
  if (!selectedFile.value) return;
  
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  formData.append('data_type', formData.value.dataType);
  formData.append('mode', formData.value.uploadMode);
  
  try {
    isUploading.value = true;
    uploadProgress.value = 0;
    
    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += Math.random() * 10;
      }
    }, 300);
    
    // 实际项目中替换为真实API调用
    // const response = await axios.post('/api/admin/batch-upload', formData, {
    //   headers: {
    //     'Content-Type': 'multipart/form-data'
    //   },
    //   onUploadProgress: (progressEvent) => {
    //     if (progressEvent.total) {
    //       uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
    //     }
    //   }
    // });
    
    // 模拟API响应
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    clearInterval(progressInterval);
    uploadProgress.value = 100;
    
    // 模拟响应数据
    const mockResponse = {
      successCount: Math.floor(Math.random() * 50) + 10,
      warningCount: Math.floor(Math.random() * 5),
      errorCount: Math.floor(Math.random() * 3),
      errors: [
        { row: 5, message: '缺少必填字段: name' },
        { row: 12, message: '日期格式不正确: 2024/13/45' }
      ].slice(0, Math.floor(Math.random() * 2)),
      warnings: [
        { row: 8, message: '建议补充描述信息' },
        { row: 15, message: '图片链接可能无效' }
      ].slice(0, Math.floor(Math.random() * 2))
    };
    
    uploadResults.value = mockResponse;
    uploadStatus.value = {
      type: mockResponse.errorCount > 0 ? 'warning' : 'success',
      message: mockResponse.errorCount > 0 
        ? `上传完成，但有 ${mockResponse.errorCount} 条数据导入失败` 
        : `上传成功！成功导入 ${mockResponse.successCount} 条数据`
    };
    
    ElNotification({
      title: uploadStatus.value.type === 'success' ? '上传成功' : '上传完成',
      message: uploadStatus.value.message,
      type: uploadStatus.value.type,
      duration: 5000
    });
    
  } catch (error) {
    console.error('Upload error:', error);
    uploadStatus.value = {
      type: 'error',
      message: error instanceof Error ? error.message : '上传失败，请重试'
    };
    
    ElNotification({
      title: '上传失败',
      message: uploadStatus.value.message,
      type: 'error',
      duration: 5000
    });
  } finally {
    isUploading.value = false;
  }
};

// 清除状态
const clearStatus = () => {
  uploadStatus.value = null;
};

// 下载模板
const downloadTemplate = async (type: string, format: string) => {
  try {
    ElMessage.info('正在准备下载模板...');
    
    // 实际项目中应该调用API下载模板
    // const response = await axios.get(`/api/admin/templates/${type}`, {
    //   params: { format: format.toLowerCase() },
    //   responseType: 'blob'
    // });
    
    // 模拟模板下载
    setTimeout(() => {
      ElMessage.success(`模板已开始下载: ${type}_template.${format.toLowerCase()}`);
      
      // 这里可以添加实际的下载逻辑
      // const url = window.URL.createObjectURL(new Blob([response.data]));
      // const link = document.createElement('a');
      // link.href = url;
      // link.setAttribute('download', `${type}_template.${format.toLowerCase()}`);
      // document.body.appendChild(link);
      // link.click();
      // link.remove();
      // window.URL.revokeObjectURL(url);
    }, 1000);
  } catch (error) {
    console.error('Download template error:', error);
    ElMessage.error('模板下载失败，请稍后重试');
  }
};

// 计算错误表格数据
const errorTableData = computed(() => {
  return uploadResults.value?.errors || [];
});

// 计算警告表格数据
const warningTableData = computed(() => {
  return uploadResults.value?.warnings || [];
});
</script>

<style scoped>
.batch-upload-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--el-text-color-primary);
}

.upload-card {
  margin-bottom: 24px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.3s ease;
}

.upload-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.file-type-hint {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.dropzone {
  border: 2px dashed var(--el-border-color);
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  background-color: var(--el-fill-color-blank);
  margin-bottom: 20px;
  position: relative;
}

.dropzone:hover,
.dropzone.drag-over {
  border-color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-icon {
  font-size: 48px;
  color: var(--el-color-primary);
  margin-bottom: 12px;
}

.upload-text {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.upload-subtext {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.file-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background-color: var(--el-color-info-light-9);
  border-radius: 6px;
  border: 1px solid var(--el-color-info-light-5);
}

.file-icon {
  font-size: 24px;
  color: var(--el-color-info);
  margin-right: 12px;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-name {
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin-bottom: 2px;
  font-size: 14px;
}

.file-size {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.remove-btn {
  margin-left: 8px;
}

.file-input {
  display: none;
}

.upload-options {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.upload-btn {
  width: 100%;
  margin-bottom: 16px;
}

.progress-bar {
  margin-top: 16px;
}

.status-message {
  margin-bottom: 24px;
  border-radius: 8px;
}

.results-card,
.template-section {
  margin-bottom: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.3s ease;
}

.results-card:hover,
.template-section:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.results-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.results-stats > :deep(.el-statistic) {
  flex: 1;
  min-width: 200px;
  text-align: center;
  padding: 16px;
  background-color: var(--el-fill-color-blank);
  border-radius: 8px;
  border: 1px solid var(--el-border-color);
}

.results-stats > :deep(.el-statistic__label) {
  font-size: 14px;
  margin-bottom: 8px;
  color: var(--el-text-color-secondary);
}

.results-stats > :deep(.el-statistic__value) {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.template-desc {
  margin-bottom: 16px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.template-item {
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

.template-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12) !important;
}

.template-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.template-icon {
  font-size: 18px;
  color: var(--el-color-info);
}

.template-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.download-btn {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .batch-upload-container {
    padding: 16px;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 12px;
  }
  
  .results-stats {
    gap: 12px;
  }
  
  .results-stats > :deep(.el-statistic) {
    min-width: 100%;
  }
  
  .template-grid {
    grid-template-columns: 1fr;
  }
  
  .upload-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .file-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .file-details {
    width: 100%;
  }
}
</style>