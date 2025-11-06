<template>
  <div class="file-uploader">
    <div class="uploader-header">
      <h3 class="uploader-title">{{ title || '文件上传' }}</h3>
      <div class="uploader-actions">
        <button 
          v-if="!isUploading" 
          class="clear-btn" 
          @click="clearAllFiles"
          :disabled="files.length === 0"
        >
          清空列表
        </button>
        <button 
          v-if="isUploading" 
          class="cancel-btn" 
          @click="cancelUpload"
        >
          取消上传
        </button>
        <button 
          v-if="!isUploading && files.length > 0" 
          class="upload-btn primary" 
          @click="startUpload"
        >
          开始上传
        </button>
      </div>
    </div>

    <!-- 上传区域 -->
    <div 
      class="upload-area" 
      :class="{ 'drag-over': isDragOver, 'dark': isDarkMode }"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input 
        ref="fileInput" 
        type="file" 
        class="file-input" 
        :multiple="multiple" 
        :accept="accept"
        @change="handleFileSelect"
        style="display: none"
      >
      
      <div class="upload-icon">{{ uploadIcon }}</div>
      <h4 class="upload-text">{{ isDragOver ? '释放文件以上传' : '点击或拖拽文件到此处上传' }}</h4>
      <p class="upload-hint">
        {{ acceptHint || '支持多种文件格式，最大文件大小50MB' }}
        <br>
        <span v-if="maxFiles > 1" class="file-limit">最多上传 {{ maxFiles }} 个文件</span>
      </p>
      <button class="browse-btn" @click.stop="triggerFileInput">
        浏览文件
      </button>
    </div>

    <!-- 上传进度 -->
    <div v-if="isUploading" class="upload-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
      </div>
      <div class="progress-info">
        <span class="progress-text">
          {{ uploadingFileName || '正在上传...' }} ({{ uploadProgress.toFixed(0) }}%)
        </span>
        <span class="progress-speed">{{ uploadSpeed }}/s</span>
      </div>
    </div>

    <!-- 文件列表 -->
    <div v-if="files.length > 0" class="file-list">
      <div class="list-header">
        <span class="header-name">文件名</span>
        <span class="header-size">大小</span>
        <span class="header-status">状态</span>
        <span class="header-action">操作</span>
      </div>
      
      <div 
        v-for="(file, index) in files" 
        :key="index"
        class="file-item"
        :class="{ 'error': file.error, 'success': file.uploaded, 'uploading': file.uploading }"
      >
        <div class="file-info">
          <span class="file-icon">{{ getFileIcon(file.type) }}</span>
          <div class="file-details">
            <span class="file-name" :title="file.name">{{ truncateFileName(file.name) }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
          </div>
        </div>
        
        <div class="file-status">
          <div v-if="file.uploading" class="status-uploading">
            <div class="mini-progress">
              <div class="mini-progress-fill" :style="{ width: file.progress + '%' }"></div>
            </div>
            <span class="progress-text">{{ file.progress.toFixed(0) }}%</span>
          </div>
          <span v-else-if="file.uploaded" class="status-success">✓ 上传成功</span>
          <span v-else-if="file.error" class="status-error">{{ file.error }}</span>
          <span v-else class="status-waiting">等待上传</span>
        </div>
        
        <div class="file-action">
          <button 
            v-if="!file.uploaded && !file.uploading"
            class="remove-btn"
            @click="removeFile(index)"
            title="移除"
          >
            ×
          </button>
          <button 
            v-else-if="file.uploaded"
            class="download-btn"
            @click="downloadFile(file)"
            title="下载"
          >
            ↓
          </button>
          <button 
            v-else-if="file.uploading"
            class="cancel-file-btn"
            @click="cancelFileUpload(index)"
            title="取消"
          >
            ■
          </button>
        </div>
      </div>
    </div>

    <!-- 成功提示 -->
    <div v-if="showSuccessMessage" class="success-message">
      <span class="success-icon">✓</span>
      <span class="success-text">{{ successMessage }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

// 定义属性
interface Props {
  title?: string;
  multiple?: boolean;
  accept?: string;
  acceptHint?: string;
  maxFiles?: number;
  maxFileSize?: number; // 单位MB
  endpoint?: string;
  autoUpload?: boolean;
  darkMode?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: '文件上传',
  multiple: true,
  accept: '*',
  acceptHint: '',
  maxFiles: 10,
  maxFileSize: 50,
  endpoint: '/api/upload',
  autoUpload: false,
  darkMode: false
});

// 定义事件
const emit = defineEmits<{
  'update:files': [files: FileUploadItem[]];
  'upload-start': [files: FileUploadItem[]];
  'upload-progress': [progress: number, file: FileUploadItem];
  'upload-success': [response: any, file: FileUploadItem];
  'upload-error': [error: string, file: FileUploadItem];
  'upload-complete': [results: UploadResult[]];
}>();

// 文件上传项接口
interface FileUploadItem {
  file: File;
  name: string;
  size: number;
  type: string;
  progress: number;
  uploaded: boolean;
  uploading: boolean;
  error?: string;
  response?: any;
  uploadStartTime?: number;
}

// 上传结果接口
interface UploadResult {
  file: File;
  success: boolean;
  response?: any;
  error?: string;
}

// 响应式数据
const fileInput = ref<HTMLInputElement | null>(null);
const files = ref<FileUploadItem[]>([]);
const isDragOver = ref(false);
const isUploading = ref(false);
const uploadProgress = ref(0);
const uploadingFileName = ref('');
const uploadSpeed = ref('0 KB');
const showSuccessMessage = ref(false);
const successMessage = ref('');
const currentUploads = ref<AbortController[]>([]);

// 计算属性
const isDarkMode = computed(() => props.darkMode);
const uploadIcon = computed(() => isDragOver.value ? '📁' : '📂');

// 方法
const triggerFileInput = () => {
  if (fileInput.value && !isUploading.value) {
    fileInput.value.click();
  }
};

const handleDragOver = () => {
  isDragOver.value = true;
};

const handleDragLeave = () => {
  isDragOver.value = false;
};

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false;
  const droppedFiles = event.dataTransfer?.files || new FileList();
  processFiles(droppedFiles);
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const selectedFiles = target.files || new FileList();
  processFiles(selectedFiles);
  // 重置input，允许再次选择相同的文件
  if (target) {
    target.value = '';
  }
};

const processFiles = (fileList: FileList) => {
  if (files.value.length >= props.maxFiles) {
    showError(`最多只能上传 ${props.maxFiles} 个文件`);
    return;
  }

  const remainingSlots = props.maxFiles - files.value.length;
  const newFiles: FileUploadItem[] = [];

  for (let i = 0; i < Math.min(fileList.length, remainingSlots); i++) {
    const file = fileList[i];
    
    // 检查文件大小
    if (file.size > props.maxFileSize * 1024 * 1024) {
      showError(`文件 "${file.name}" 超过最大允许大小 ${props.maxFileSize}MB`);
      continue;
    }

    // 检查文件是否已存在
    if (files.value.some(f => f.name === file.name && f.size === file.size)) {
      showError(`文件 "${file.name}" 已在列表中`);
      continue;
    }

    newFiles.push({
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      progress: 0,
      uploaded: false,
      uploading: false
    });
  }

  files.value = [...files.value, ...newFiles];
  emit('update:files', files.value);

  // 自动上传
  if (props.autoUpload && newFiles.length > 0) {
    startUpload();
  }
};

const startUpload = async () => {
  if (isUploading.value || files.value.filter(f => !f.uploaded && !f.error).length === 0) {
    return;
  }

  isUploading.value = true;
  const uploadResults: UploadResult[] = [];
  
  // 筛选未上传的文件
  const filesToUpload = files.value.filter(f => !f.uploaded && !f.error);
  emit('upload-start', filesToUpload);
  
  let totalProgress = 0;
  const totalFiles = filesToUpload.length;

  try {
    for (let i = 0; i < filesToUpload.length; i++) {
      const fileItem = filesToUpload[i];
      const index = files.value.findIndex(f => f === fileItem);
      
      if (index === -1) continue;
      
      files.value[index].uploading = true;
      files.value[index].uploadStartTime = Date.now();
      uploadingFileName.value = fileItem.name;
      
      // 创建上传控制器
      const controller = new AbortController();
      currentUploads.value.push(controller);
      
      try {
        // 模拟上传，实际项目中替换为真实API调用
        const response = await mockFileUpload(fileItem, index, controller.signal);
        
        files.value[index].uploaded = true;
        files.value[index].uploading = false;
        files.value[index].response = response;
        
        uploadResults.push({
          file: fileItem.file,
          success: true,
          response
        });
        
        emit('upload-success', response, fileItem);
      } catch (error: any) {
        if (error.name === 'AbortError') {
          files.value[index].uploading = false;
          uploadResults.push({
            file: fileItem.file,
            success: false,
            error: '上传已取消'
          });
        } else {
          files.value[index].uploading = false;
          files.value[index].error = error.message || '上传失败';
          
          uploadResults.push({
            file: fileItem.file,
            success: false,
            error: files.value[index].error
          });
          
          emit('upload-error', files.value[index].error, fileItem);
        }
      } finally {
        // 移除已完成的上传控制器
        currentUploads.value = currentUploads.value.filter(c => c !== controller);
        
        // 更新总进度
        totalProgress += 1;
        uploadProgress.value = Math.round((totalProgress / totalFiles) * 100);
      }
    }
  } finally {
    isUploading.value = false;
    uploadingFileName.value = '';
    uploadSpeed.value = '0 KB';
    
    emit('upload-complete', uploadResults);
    
    // 显示成功消息
    if (uploadResults.filter(r => r.success).length > 0) {
      showSuccess(`${uploadResults.filter(r => r.success).length} 个文件上传成功`);
    }
  }
};

// 模拟文件上传
const mockFileUpload = (fileItem: FileUploadItem, index: number, signal: AbortSignal): Promise<any> => {
  return new Promise((resolve, reject) => {
    let uploadedBytes = 0;
    const totalBytes = fileItem.size;
    const startTime = Date.now();
    
    // 检查信号是否已中止
    if (signal.aborted) {
      reject(new DOMException('Aborted', 'AbortError'));
      return;
    }
    
    // 监听中止信号
    const onAbort = () => {
      reject(new DOMException('Aborted', 'AbortError'));
    };
    signal.addEventListener('abort', onAbort);
    
    const uploadInterval = setInterval(() => {
      // 检查是否中止
      if (signal.aborted) {
        clearInterval(uploadInterval);
        signal.removeEventListener('abort', onAbort);
        return;
      }
      
      // 模拟上传进度
      const chunkSize = Math.min(totalBytes * 0.1, 1024 * 1024); // 每次上传10%或1MB
      uploadedBytes = Math.min(uploadedBytes + chunkSize, totalBytes);
      
      const progress = (uploadedBytes / totalBytes) * 100;
      files.value[index].progress = progress;
      
      // 计算上传速度
      const elapsedTime = (Date.now() - startTime) / 1000;
      const bytesPerSecond = uploadedBytes / elapsedTime;
      uploadSpeed.value = formatFileSize(bytesPerSecond);
      
      emit('upload-progress', progress, fileItem);
      
      // 完成上传
      if (uploadedBytes >= totalBytes) {
        clearInterval(uploadInterval);
        signal.removeEventListener('abort', onAbort);
        
        // 模拟服务器响应
        setTimeout(() => {
          resolve({
            url: `/uploads/${fileItem.name}`,
            id: `file-${Date.now()}`,
            filename: fileItem.name,
            size: fileItem.size
          });
        }, 200);
      }
    }, 100);
  });
};

const cancelUpload = () => {
  // 中止所有上传
  currentUploads.value.forEach(controller => controller.abort());
  currentUploads.value = [];
  
  // 更新文件状态
  files.value.forEach(file => {
    if (file.uploading) {
      file.uploading = false;
    }
  });
  
  isUploading.value = false;
  uploadProgress.value = 0;
  uploadingFileName.value = '';
  uploadSpeed.value = '0 KB';
};

const cancelFileUpload = (index: number) => {
  const file = files.value[index];
  if (file && file.uploading) {
    // 查找对应的上传控制器并中止
    if (currentUploads.value.length > 0) {
      const controller = currentUploads.value.shift();
      if (controller) controller.abort();
    }
    
    files.value[index].uploading = false;
  }
};

const removeFile = (index: number) => {
  files.value.splice(index, 1);
  emit('update:files', files.value);
};

const clearAllFiles = () => {
  if (isUploading.value) {
    cancelUpload();
  }
  files.value = [];
  emit('update:files', files.value);
};

const downloadFile = (file: FileUploadItem) => {
  // 实际项目中，这里应该使用服务器返回的URL进行下载
  if (file.response && file.response.url) {
    const link = document.createElement('a');
    link.href = file.response.url;
    link.download = file.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

// 工具函数
const getFileIcon = (fileType: string): string => {
  const type = fileType.split('/')[0];
  const ext = fileType.split('/')[1] || '';
  
  switch (type) {
    case 'image':
      return '🖼️';
    case 'video':
      return '🎬';
    case 'audio':
      return '🎵';
    case 'text':
      return '📄';
    case 'application':
      if (ext.includes('pdf')) return '📑';
      if (ext.includes('word') || ext.includes('document')) return '📝';
      if (ext.includes('excel') || ext.includes('sheet')) return '📊';
      if (ext.includes('zip') || ext.includes('compressed')) return '🗜️';
      return '📁';
    default:
      return '📄';
  }
};

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const truncateFileName = (name: string, maxLength = 20): string => {
  if (name.length <= maxLength) return name;
  
  const extension = name.substring(name.lastIndexOf('.'));
  const nameWithoutExt = name.substring(0, name.lastIndexOf('.'));
  
  return nameWithoutExt.substring(0, maxLength - extension.length - 3) + '...' + extension;
};

const showError = (message: string) => {
  // 实际项目中可以使用更复杂的错误提示组件
  alert(message);
};

const showSuccess = (message: string) => {
  successMessage.value = message;
  showSuccessMessage.value = true;
  
  setTimeout(() => {
    showSuccessMessage.value = false;
  }, 3000);
};

// 监听暗黑模式变化
watch(() => props.darkMode, (newVal) => {
  // 可以在这里添加暗黑模式相关的额外处理
});
</script>

<style scoped>
.file-uploader {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.file-uploader.dark {
  background-color: #1e293b;
  color: #f1f5f9;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

/* 头部样式 */
.uploader-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.file-uploader.dark .uploader-header {
  border-bottom-color: #334155;
}

.uploader-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.file-uploader.dark .uploader-title {
  color: #f1f5f9;
}

.uploader-actions {
  display: flex;
  gap: 10px;
}

/* 按钮基础样式 */
button {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  background-color: #ffffff;
  color: #475569;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.file-uploader.dark button {
  background-color: #334155;
  border-color: #475569;
  color: #cbd5e1;
}

button:hover:not(:disabled) {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}

.file-uploader.dark button:hover:not(:disabled) {
  background-color: #475569;
  border-color: #64748b;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button.primary {
  background-color: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

button.primary:hover:not(:disabled) {
  background-color: #2563eb;
  border-color: #2563eb;
}

/* 上传区域 */
.upload-area {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #f8fafc;
}

.file-uploader.dark .upload-area {
  border-color: #475569;
  background-color: #273449;
}

.upload-area.drag-over {
  border-color: #3b82f6;
  background-color: #eff6ff;
}

.file-uploader.dark .upload-area.drag-over {
  background-color: #1e3a8a;
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.upload-text {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 500;
  color: #334155;
}

.file-uploader.dark .upload-text {
  color: #f1f5f9;
}

.upload-hint {
  margin: 0 0 20px 0;
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.5;
}

.file-uploader.dark .upload-hint {
  color: #94a3b8;
}

.file-limit {
  font-weight: 500;
  color: #3b82f6;
}

.file-uploader.dark .file-limit {
  color: #60a5fa;
}

.browse-btn {
  background-color: #3b82f6;
  border-color: #3b82f6;
  color: white;
  padding: 10px 20px;
  font-weight: 500;
}

.browse-btn:hover {
  background-color: #2563eb;
  border-color: #2563eb;
}

/* 上传进度 */
.upload-progress {
  margin: 20px 0;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.file-uploader.dark .progress-bar {
  background-color: #334155;
}

.progress-fill {
  height: 100%;
  background-color: #3b82f6;
  border-radius: 3px;
  transition: width 0.2s ease;
}

.file-uploader.dark .progress-fill {
  background-color: #60a5fa;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #64748b;
}

.file-uploader.dark .progress-info {
  color: #94a3b8;
}

/* 文件列表 */
.file-list {
  margin-top: 20px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.file-uploader.dark .file-list {
  border-color: #334155;
}

.list-header {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 16px;
  padding: 12px 16px;
  background-color: #f8fafc;
  font-weight: 500;
  font-size: 0.9rem;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
}

.file-uploader.dark .list-header {
  background-color: #273449;
  color: #94a3b8;
  border-bottom-color: #334155;
}

.file-item {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 16px;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
  transition: background-color 0.2s ease;
}

.file-item:last-child {
  border-bottom: none;
}

.file-uploader.dark .file-item {
  border-bottom-color: #334155;
}

.file-item:hover {
  background-color: #f8fafc;
}

.file-uploader.dark .file-item:hover {
  background-color: #273449;
}

.file-item.error {
  background-color: #fef2f2;
}

.file-uploader.dark .file-item.error {
  background-color: #7f1d1d;
}

.file-item.success {
  background-color: #f0fdf4;
}

.file-uploader.dark .file-item.success {
  background-color: #166534;
}

.file-item.uploading {
  background-color: #f0f9ff;
}

.file-uploader.dark .file-item.uploading {
  background-color: #0c4a6e;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-icon {
  font-size: 1.2rem;
}

.file-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.file-name {
  font-size: 0.95rem;
  font-weight: 500;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 300px;
}

.file-uploader.dark .file-name {
  color: #f1f5f9;
}

.file-size {
  font-size: 0.8rem;
  color: #64748b;
}

.file-uploader.dark .file-size {
  color: #94a3b8;
}

.file-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
}

.status-uploading {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mini-progress {
  width: 80px;
  height: 4px;
  background-color: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.file-uploader.dark .mini-progress {
  background-color: #334155;
}

.mini-progress-fill {
  height: 100%;
  background-color: #3b82f6;
  border-radius: 2px;
}

.file-uploader.dark .mini-progress-fill {
  background-color: #60a5fa;
}

.status-success {
  color: #22c55e;
  font-weight: 500;
}

.status-error {
  color: #ef4444;
}

.status-waiting {
  color: #64748b;
}

.file-uploader.dark .status-waiting {
  color: #94a3b8;
}

.file-action {
  display: flex;
  gap: 4px;
}

.remove-btn,
.download-btn,
.cancel-file-btn {
  width: 28px;
  height: 28px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 1rem;
  line-height: 1;
}

.remove-btn {
  background-color: #fee2e2;
  border-color: #fecaca;
  color: #dc2626;
}

.remove-btn:hover {
  background-color: #fecaca;
  border-color: #fca5a5;
}

.download-btn {
  background-color: #dbeafe;
  border-color: #93c5fd;
  color: #2563eb;
}

.download-btn:hover {
  background-color: #93c5fd;
  border-color: #60a5fa;
}

.cancel-file-btn {
  background-color: #fde68a;
  border-color: #fcd34d;
  color: #d97706;
}

.cancel-file-btn:hover {
  background-color: #fcd34d;
  border-color: #fbbf24;
}

/* 成功提示 */
.success-message {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px;
  background-color: #dcfce7;
  border: 1px solid #bbf7d0;
  border-radius: 6px;
  color: #166534;
  font-size: 0.9rem;
  animation: slideIn 0.3s ease;
}

.file-uploader.dark .success-message {
  background-color: #166534;
  border-color: #15803d;
  color: #bbf7d0;
}

.success-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .file-uploader {
    padding: 16px;
  }
  
  .uploader-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .uploader-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .upload-area {
    padding: 30px 16px;
  }
  
  .upload-icon {
    font-size: 2.5rem;
  }
  
  .list-header,
  .file-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .file-info {
    justify-content: space-between;
  }
  
  .file-name {
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .uploader-actions {
    flex-wrap: wrap;
  }
  
  .upload-area {
    padding: 24px 12px;
  }
  
  .upload-icon {
    font-size: 2rem;
  }
  
  .file-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .file-name {
    max-width: 100%;
  }
}
</style>