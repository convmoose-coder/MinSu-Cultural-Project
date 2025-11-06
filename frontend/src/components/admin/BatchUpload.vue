<template>
  <div class="batch-upload">
    <div class="upload-header">
      <h3>{{ title }}</h3>
      <button 
        @click="downloadTemplate" 
        class="template-btn"
        :disabled="isUploading"
      >
        下载模板
      </button>
    </div>
    
    <div 
      @click="triggerFileInput"
      class="upload-zone"
      :class="{ 'dragging': isDragging, 'has-file': selectedFile }"
      :disabled="isUploading"
    >
      <input
        ref="fileInput"
        type="file"
        @change="handleFileChange"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop"
        :accept=".csv,.xlsx,.xls"
        style="display: none"
      />
      
      <div v-if="!selectedFile" class="upload-placeholder">
        <div class="upload-icon">📁</div>
        <p>点击或拖拽文件到此处上传</p>
        <p class="upload-hint">支持 CSV、XLS、XLSX 格式，最大 10MB</p>
      </div>
      
      <div v-else class="file-preview">
        <div class="file-icon">
          {{ getFileIcon(selectedFile.name) }}
        </div>
        <div class="file-info">
          <div class="file-name">{{ selectedFile.name }}</div>
          <div class="file-size">{{ formatFileSize(selectedFile.size) }}</div>
        </div>
        <button @click.stop="removeFile" class="remove-btn" :disabled="isUploading">
          ✕
        </button>
      </div>
    </div>
    
    <div class="upload-footer">
      <div class="data-type-selector">
        <label for="data-type">数据类型：</label>
        <select id="data-type" v-model="dataType" :disabled="isUploading">
          <option value="culture">民族文化数据</option>
          <option value="festival">民族节日数据</option>
          <option value="custom">自定义数据</option>
        </select>
      </div>
      
      <button 
        @click="startUpload"
        class="upload-btn"
        :disabled="!selectedFile || isUploading"
      >
        {{ isUploading ? '上传中...' : '开始上传' }}
      </button>
    </div>
    
    <!-- 上传进度 -->
    <div v-if="isUploading" class="upload-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="progress-text">{{ progress }}%</div>
    </div>
    
    <!-- 上传结果 -->
    <div v-if="uploadResult" class="upload-result">
      <div :class="['result-header', uploadResult.success ? 'success' : 'error']">
        <span>{{ uploadResult.success ? '✅ 上传成功' : '❌ 上传失败' }}</span>
        <button @click="clearResult" class="clear-btn">✕</button>
      </div>
      <div class="result-content">
        <p>{{ uploadResult.message }}</p>
        
        <div v-if="uploadResult.data" class="result-stats">
          <div class="stat-item">
            <span class="stat-label">总记录数：</span>
            <span class="stat-value">{{ uploadResult.data.total }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">成功：</span>
            <span class="stat-value success">{{ uploadResult.data.success }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">失败：</span>
            <span class="stat-value error">{{ uploadResult.data.failed }}</span>
          </div>
        </div>
        
        <div v-if="uploadResult.data?.errors && uploadResult.data.errors.length > 0" class="error-details">
          <h4>错误详情：</h4>
          <div class="error-list">
            <div v-for="(error, index) in uploadResult.data.errors" :key="index" class="error-item">
              第 {{ error.row }} 行：{{ error.error }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import uploadService from '@/services/admin/uploadService';

interface Props {
  title?: string;
  defaultDataType?: string;
}

const props = withDefaults(defineProps<Props>(), {
  title: '批量数据上传',
  defaultDataType: 'culture'
});

const emit = defineEmits<{
  uploadSuccess: [result: any];
  uploadError: [error: any];
}>();

// 响应式数据
const fileInput = ref<HTMLInputElement>();
const selectedFile = ref<File | null>(null);
const dataType = ref(props.defaultDataType);
const isUploading = ref(false);
const isDragging = ref(false);
const progress = ref(0);
const uploadResult = ref<any>(null);

// 触发文件选择
const triggerFileInput = () => {
  if (!isUploading.value) {
    fileInput.value?.click();
  }
};

// 处理文件选择
const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    processFile(target.files[0]);
  }
};

// 处理拖放事件
const handleDragOver = () => {
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const handleDrop = (event: DragEvent) => {
  isDragging.value = false;
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    processFile(event.dataTransfer.files[0]);
  }
};

// 处理文件
const processFile = (file: File) => {
  // 验证文件
  const validation = uploadService.validateFile(file);
  if (!validation.valid) {
    alert(validation.error);
    return;
  }
  
  selectedFile.value = file;
  // 清除之前的上传结果
  uploadResult.value = null;
};

// 移除文件
const removeFile = () => {
  selectedFile.value = null;
  uploadResult.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

// 开始上传
const startUpload = async () => {
  if (!selectedFile.value || isUploading.value) return;
  
  isUploading.value = true;
  progress.value = 0;
  uploadResult.value = null;
  
  try {
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += Math.random() * 10;
      }
    }, 200);
    
    // 调用上传服务
    const result = await uploadService.batchUpload(selectedFile.value, dataType.value);
    
    clearInterval(progressInterval);
    progress.value = 100;
    uploadResult.value = result;
    
    // 触发成功事件
    emit('uploadSuccess', result);
  } catch (error) {
    uploadResult.value = {
      success: false,
      message: error instanceof Error ? error.message : '上传失败，请重试'
    };
    // 触发错误事件
    emit('uploadError', error);
  } finally {
    // 延迟重置上传状态，让用户有时间看到结果
    setTimeout(() => {
      isUploading.value = false;
      progress.value = 0;
    }, 500);
  }
};

// 清除上传结果
const clearResult = () => {
  uploadResult.value = null;
};

// 下载模板
const downloadTemplate = () => {
  uploadService.downloadTemplate(dataType.value);
};

// 获取文件图标
const getFileIcon = (filename: string) => {
  const extension = filename.toLowerCase().substring(filename.lastIndexOf('.'));
  if (extension === '.csv') return '📄';
  if (extension === '.xls' || extension === '.xlsx') return '📊';
  return '📁';
};

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
};
</script>

<style scoped>
.batch-upload {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.upload-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.template-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.template-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.template-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upload-zone {
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #f8fafc;
}

.upload-zone:hover:not(:disabled) {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.upload-zone.dragging {
  border-color: #3b82f6;
  background-color: #dbeafe;
}

.upload-zone.has-file {
  border-style: solid;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
}

.upload-placeholder .upload-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.upload-placeholder p {
  margin: 0 0 8px 0;
  color: #64748b;
  font-size: 1rem;
}

.upload-placeholder .upload-hint {
  font-size: 0.875rem;
  color: #94a3b8;
}

.file-preview {
  display: flex;
  align-items: center;
  width: 100%;
}

.file-icon {
  font-size: 2rem;
  margin-right: 16px;
}

.file-info {
  flex: 1;
  text-align: left;
}

.file-name {
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 4px;
}

.file-size {
  font-size: 0.875rem;
  color: #64748b;
}

.remove-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #64748b;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.remove-btn:hover:not(:disabled) {
  background-color: #fee2e2;
  color: #ef4444;
}

.remove-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upload-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.data-type-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.data-type-selector label {
  color: #334155;
  font-weight: 500;
}

.data-type-selector select {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background-color: white;
  font-size: 0.9rem;
  cursor: pointer;
}

.upload-btn {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.upload-btn:hover:not(:disabled) {
  background-color: #059669;
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.upload-progress {
  margin-top: 20px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background-color: #10b981;
  transition: width 0.3s;
}

.progress-text {
  text-align: center;
  font-size: 0.9rem;
  color: #64748b;
}

.upload-result {
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.result-header {
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.result-header.success {
  background-color: #dcfce7;
  color: #15803d;
}

.result-header.error {
  background-color: #fee2e2;
  color: #b91c1c;
}

.clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: inherit;
}

.result-content {
  padding: 16px;
  background-color: white;
}

.result-content p {
  margin: 0 0 16px 0;
  color: #334155;
}

.result-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  padding: 16px;
  background-color: #f8fafc;
  border-radius: 6px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
}

.stat-value.success {
  color: #10b981;
}

.stat-value.error {
  color: #ef4444;
}

.error-details h4 {
  margin: 0 0 12px 0;
  color: #b91c1c;
  font-size: 1rem;
}

.error-list {
  max-height: 200px;
  overflow-y: auto;
}

.error-item {
  padding: 8px 12px;
  margin-bottom: 4px;
  background-color: #fee2e2;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #b91c1c;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-header,
  .upload-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .upload-zone {
    padding: 24px;
  }
  
  .file-preview {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .file-info {
    text-align: center;
  }
}
</style>