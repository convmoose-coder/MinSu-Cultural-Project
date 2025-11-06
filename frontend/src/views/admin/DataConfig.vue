<template>
  <AdminLayout>
    <div class="data-config-container">
      <h2 class="page-title">数据配置</h2>
      
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 数据导入 -->
        <el-tab-pane label="数据导入" name="import">
          <div class="import-section">
            <h3>数据导入</h3>
            <p class="section-description">支持从Excel、CSV文件导入民俗文化数据</p>
            
            <div class="import-options">
              <el-card class="import-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>Excel导入</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>支持.xlsx格式文件，包含以下字段：</p>
                  <ul class="field-list">
                    <li>名称 (name)</li>
                    <li>分类 (category)</li>
                    <li>地区 (region)</li>
                    <li>描述 (description)</li>
                    <li>图片URL (image_url)</li>
                  </ul>
                  
                  <el-upload
                    class="upload-demo"
                    action="#"
                    :show-file-list="false"
                    :before-upload="beforeExcelUpload"
                    :http-request="handleExcelImport"
                    accept=".xlsx,.xls"
                  >
                    <el-button type="primary">
                      <el-icon><Upload /></el-icon>
                      选择Excel文件
                    </el-button>
                  </el-upload>
                </div>
              </el-card>
              
              <el-card class="import-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>CSV导入</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>支持.csv格式文件，UTF-8编码：</p>
                  <ul class="field-list">
                    <li>名称 (name)</li>
                    <li>分类 (category)</li>
                    <li>地区 (region)</li>
                    <li>描述 (description)</li>
                    <li>图片URL (image_url)</li>
                  </ul>
                  
                  <el-upload
                    class="upload-demo"
                    action="#"
                    :show-file-list="false"
                    :before-upload="beforeCSVUpload"
                    :http-request="handleCSVImport"
                    accept=".csv"
                  >
                    <el-button type="primary">
                      <el-icon><Upload /></el-icon>
                      选择CSV文件
                    </el-button>
                  </el-upload>
                </div>
              </el-card>
            </div>
            
            <!-- 导入进度 -->
            <div v-if="importProgress.visible" class="import-progress">
              <h4>导入进度</h4>
              <el-progress 
                :percentage="importProgress.percentage" 
                :status="importProgress.status"
                :stroke-width="8"
              />
              <p class="progress-text">{{ importProgress.message }}</p>
              
              <div v-if="importResult" class="import-result">
                <el-alert
                  :title="importResult.title"
                  :type="importResult.type"
                  :description="importResult.description"
                  show-icon
                  closable
                />
              </div>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 数据导出 -->
        <el-tab-pane label="数据导出" name="export">
          <div class="export-section">
            <h3>数据导出</h3>
            <p class="section-description">导出民俗文化数据到不同格式文件</p>
            
            <div class="export-options">
              <el-card class="export-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>Excel导出</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>导出为.xlsx格式文件，包含完整数据字段</p>
                  
                  <el-form label-width="100px">
                    <el-form-item label="导出范围">
                      <el-radio-group v-model="exportSettings.range">
                        <el-radio label="all">全部数据</el-radio>
                        <el-radio label="selected">选中分类</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    
                    <el-form-item v-if="exportSettings.range === 'selected'" label="选择分类">
                      <el-select v-model="exportSettings.categories" multiple placeholder="请选择分类">
                        <el-option 
                          v-for="category in categories" 
                          :key="category.id" 
                          :label="category.name" 
                          :value="category.id"
                        />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="包含图片">
                      <el-switch v-model="exportSettings.includeImages" />
                    </el-form-item>
                  </el-form>
                  
                  <el-button type="success" @click="handleExcelExport">
                    <el-icon><Download /></el-icon>
                    导出Excel
                  </el-button>
                </div>
              </el-card>
              
              <el-card class="export-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>JSON导出</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>导出为JSON格式文件，适合数据迁移</p>
                  
                  <el-button type="primary" @click="handleJSONExport">
                    <el-icon><Download /></el-icon>
                    导出JSON
                  </el-button>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 数据备份 -->
        <el-tab-pane label="数据备份" name="backup">
          <div class="backup-section">
            <h3>数据备份与恢复</h3>
            <p class="section-description">定期备份系统数据，防止数据丢失</p>
            
            <div class="backup-actions">
              <el-button type="primary" @click="handleManualBackup">
                <el-icon><CloudUpload /></el-icon>
                立即备份
              </el-button>
              
              <el-button type="success" @click="handleRestoreBackup">
                <el-icon><Refresh /></el-icon>
                恢复备份
              </el-button>
              
              <el-button type="warning" @click="handleBackupSettings">
                <el-icon><Setting /></el-icon>
                备份设置
              </el-button>
            </div>
            
            <!-- 备份列表 -->
            <div class="backup-list">
              <h4>备份记录</h4>
              <el-table :data="backupList" style="width: 100%" border>
                <el-table-column prop="filename" label="文件名" min-width="200" />
                <el-table-column prop="size" label="大小" width="100" />
                <el-table-column prop="createdAt" label="创建时间" width="180" />
                <el-table-column label="操作" width="200" fixed="right">
                  <template #default="scope">
                    <el-button 
                      type="primary" 
                      size="small" 
                      @click="handleDownloadBackup(scope.row)"
                    >
                      下载
                    </el-button>
                    <el-button 
                      type="success" 
                      size="small" 
                      @click="handleRestoreFromBackup(scope.row)"
                    >
                      恢复
                    </el-button>
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click="handleDeleteBackup(scope.row)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            
            <!-- 备份设置 -->
            <div class="backup-settings">
              <h4>自动备份设置</h4>
              <el-form label-width="120px">
                <el-form-item label="自动备份">
                  <el-switch v-model="backupSettings.autoBackup" />
                  <span class="tip-text">启用自动备份功能</span>
                </el-form-item>
                
                <el-form-item v-if="backupSettings.autoBackup" label="备份频率">
                  <el-select v-model="backupSettings.frequency" placeholder="请选择备份频率">
                    <el-option label="每天" value="daily" />
                    <el-option label="每周" value="weekly" />
                    <el-option label="每月" value="monthly" />
                  </el-select>
                </el-form-item>
                
                <el-form-item v-if="backupSettings.autoBackup" label="保留数量">
                  <el-input-number 
                    v-model="backupSettings.keepCount" 
                    :min="1" 
                    :max="50" 
                    controls-position="right"
                  />
                  <span class="tip-text">个备份文件</span>
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="saveBackupSettings">保存设置</el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 数据清理 -->
        <el-tab-pane label="数据清理" name="cleanup">
          <div class="cleanup-section">
            <h3>数据清理与优化</h3>
            <p class="section-description">清理无用数据，优化系统性能</p>
            
            <div class="cleanup-options">
              <el-card class="cleanup-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Delete /></el-icon>
                    <span>临时文件清理</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>清理系统生成的临时文件和缓存</p>
                  <el-button type="warning" @click="handleCleanTempFiles">
                    <el-icon><Delete /></el-icon>
                    清理临时文件
                  </el-button>
                </div>
              </el-card>
              
              <el-card class="cleanup-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><DataBoard /></el-icon>
                    <span>数据库优化</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>优化数据库性能，清理碎片数据</p>
                  <el-button type="primary" @click="handleOptimizeDatabase">
                    <el-icon><DataBoard /></el-icon>
                    优化数据库
                  </el-button>
                </div>
              </el-card>
              
              <el-card class="cleanup-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><User /></el-icon>
                    <span>用户数据清理</span>
                  </div>
                </template>
                
                <div class="card-content">
                  <p>清理长时间未登录的用户数据</p>
                  <el-button type="danger" @click="handleCleanUserData">
                    <el-icon><User /></el-icon>
                    清理用户数据
                  </el-button>
                </div>
              </el-card>
            </div>
            
            <!-- 清理统计 -->
            <div class="cleanup-stats">
              <h4>清理统计</h4>
              <el-descriptions :column="3" border>
                <el-descriptions-item label="临时文件">2.5 MB</el-descriptions-item>
                <el-descriptions-item label="数据库碎片">15.2 MB</el-descriptions-item>
                <el-descriptions-item label="未活跃用户">3 个</el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Document, Upload, Download, CloudUpload, Refresh, 
  Setting, Delete, DataBoard, User 
} from '@element-plus/icons-vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'

// 激活的标签页
const activeTab = ref('import')

// 导入相关数据
const importProgress = reactive({
  visible: false,
  percentage: 0,
  status: 'success',
  message: ''
})

const importResult = ref(null)

// 导出设置
const exportSettings = reactive({
  range: 'all',
  categories: [],
  includeImages: true
})

// 备份设置
const backupSettings = reactive({
  autoBackup: true,
  frequency: 'daily',
  keepCount: 10
})

// 分类数据
const categories = ref([
  { id: 1, name: '传统节日' },
  { id: 2, name: '民间艺术' },
  { id: 3, name: '民俗礼仪' }
])

// 备份列表
const backupList = ref([
  {
    filename: 'backup_20240115.sql',
    size: '2.3 MB',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    filename: 'backup_20240114.sql',
    size: '2.1 MB',
    createdAt: '2024-01-14 10:30:00'
  }
])

// 导入方法
const beforeExcelUpload = (file: File) => {
  const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                  file.type === 'application/vnd.ms-excel'
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isExcel) {
    ElMessage.error('请上传Excel文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }
  return true
}

const beforeCSVUpload = (file: File) => {
  const isCSV = file.type === 'text/csv' || file.name.endsWith('.csv')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isCSV) {
    ElMessage.error('请上传CSV文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('文件大小不能超过 5MB!')
    return false
  }
  return true
}

const handleExcelImport = async (options: any) => {
  importProgress.visible = true
  importProgress.percentage = 0
  importProgress.message = '开始导入Excel文件...'
  
  try {
    // 模拟导入过程
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200))
      importProgress.percentage = i
      importProgress.message = `正在导入数据... ${i}%`
    }
    
    importProgress.message = '导入完成'
    importResult.value = {
      title: '导入成功',
      type: 'success',
      description: '成功导入 25 条民俗文化数据'
    }
    
    ElMessage.success('Excel文件导入成功')
  } catch (error) {
    importProgress.status = 'exception'
    importProgress.message = '导入失败'
    importResult.value = {
      title: '导入失败',
      type: 'error',
      description: '导入过程中出现错误'
    }
    ElMessage.error('导入失败')
  }
}

const handleCSVImport = async (options: any) => {
  // 类似Excel导入逻辑
  ElMessage.info('CSV导入功能开发中...')
}

// 导出方法
const handleExcelExport = () => {
  ElMessage.success('开始导出Excel文件...')
  // 模拟导出过程
  setTimeout(() => {
    ElMessage.success('Excel文件导出成功')
  }, 2000)
}

const handleJSONExport = () => {
  ElMessage.success('开始导出JSON文件...')
  // 模拟导出过程
  setTimeout(() => {
    ElMessage.success('JSON文件导出成功')
  }, 2000)
}

// 备份方法
const handleManualBackup = () => {
  ElMessage.info('开始创建备份...')
  // 模拟备份过程
  setTimeout(() => {
    ElMessage.success('备份创建成功')
  }, 3000)
}

const handleRestoreBackup = () => {
  ElMessage.info('恢复备份功能开发中...')
}

const handleBackupSettings = () => {
  ElMessage.info('备份设置功能开发中...')
}

const handleDownloadBackup = (backup: any) => {
  ElMessage.success(`开始下载备份文件: ${backup.filename}`)
}

const handleRestoreFromBackup = (backup: any) => {
  ElMessageBox.confirm(
    `确定要从备份文件 "${backup.filename}" 恢复数据吗？此操作将覆盖现有数据。`,
    '警告',
    { type: 'warning' }
  ).then(() => {
    ElMessage.success('开始恢复备份...')
  })
}

const handleDeleteBackup = (backup: any) => {
  ElMessageBox.confirm(
    `确定要删除备份文件 "${backup.filename}" 吗？`,
    '提示',
    { type: 'warning' }
  ).then(() => {
    ElMessage.success('备份文件删除成功')
  })
}

const saveBackupSettings = () => {
  ElMessage.success('备份设置保存成功')
}

// 清理方法
const handleCleanTempFiles = () => {
  ElMessage.success('临时文件清理完成')
}

const handleOptimizeDatabase = () => {
  ElMessage.success('数据库优化完成')
}

const handleCleanUserData = () => {
  ElMessageBox.confirm(
    '确定要清理长时间未登录的用户数据吗？此操作不可恢复。',
    '警告',
    { type: 'warning' }
  ).then(() => {
    ElMessage.success('用户数据清理完成')
  })
}

onMounted(() => {
  // 初始化数据
})
</script>

<style scoped>
.data-config-container {
  max-width: 100%;
  padding: 20px;
}

.page-title {
  color: #1e293b;
  margin-bottom: 24px;
  font-size: 1.8rem;
  font-weight: 600;
}

.section-description {
  color: #64748b;
  margin-bottom: 20px;
}

.import-options,
.export-options,
.cleanup-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.import-card,
.export-card,
.cleanup-card {
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.card-content {
  min-height: 200px;
}

.field-list {
  margin: 10px 0;
  padding-left: 20px;
  color: #64748b;
}

.import-progress {
  margin-top: 30px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
}

.progress-text {
  margin-top: 10px;
  text-align: center;
  color: #64748b;
}

.import-result {
  margin-top: 20px;
}

.backup-actions {
  margin-bottom: 30px;
  display: flex;
  gap: 10px;
}

.backup-list {
  margin-bottom: 30px;
}

.backup-settings {
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
}

.cleanup-stats {
  margin-top: 30px;
}

.tip-text {
  margin-left: 10px;
  color: #64748b;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .import-options,
  .export-options,
  .cleanup-options {
    grid-template-columns: 1fr;
  }
  
  .backup-actions {
    flex-direction: column;
  }
}
</style>