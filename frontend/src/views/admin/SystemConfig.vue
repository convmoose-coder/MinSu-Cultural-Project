<template>
  <AdminLayout>
    <div class="system-config-container">
      <h2 class="page-title">系统配置</h2>
      
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 站点设置 -->
        <el-tab-pane label="站点设置" name="site">
          <el-form ref="siteFormRef" :model="siteForm" :rules="siteRules" label-width="120px">
            <el-form-item label="站点名称" prop="siteName">
              <el-input v-model="siteForm.siteName" placeholder="请输入站点名称" style="width: 300px;"></el-input>
            </el-form-item>
            
            <el-form-item label="站点描述" prop="siteDescription">
              <el-input 
                v-model="siteForm.siteDescription" 
                type="textarea" 
                :rows="3" 
                placeholder="请输入站点描述"
                style="width: 400px;"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="站点关键词" prop="siteKeywords">
              <el-input 
                v-model="siteForm.siteKeywords" 
                placeholder="请输入关键词，用逗号分隔"
                style="width: 400px;"
              ></el-input>
            </el-form-item>
            
            <el-form-item label="站点Logo" prop="siteLogo">
              <el-upload
                class="avatar-uploader"
                action="#"
                :show-file-list="false"
                :before-upload="beforeLogoUpload"
                :http-request="handleLogoUpload"
              >
                <img v-if="siteForm.siteLogo" :src="siteForm.siteLogo" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSiteConfig">保存设置</el-button>
              <el-button @click="resetSiteConfig">重置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 主题配置 -->
        <el-tab-pane label="主题配置" name="theme">
          <div class="theme-config">
            <h3>主题颜色</h3>
            <div class="color-picker-group">
              <div class="color-item">
                <span>主色调：</span>
                <el-color-picker v-model="themeForm.primaryColor" />
                <span class="color-value">{{ themeForm.primaryColor }}</span>
              </div>
              
              <div class="color-item">
                <span>成功色：</span>
                <el-color-picker v-model="themeForm.successColor" />
                <span class="color-value">{{ themeForm.successColor }}</span>
              </div>
              
              <div class="color-item">
                <span>警告色：</span>
                <el-color-picker v-model="themeForm.warningColor" />
                <span class="color-value">{{ themeForm.warningColor }}</span>
              </div>
              
              <div class="color-item">
                <span>危险色：</span>
                <el-color-picker v-model="themeForm.dangerColor" />
                <span class="color-value">{{ themeForm.dangerColor }}</span>
              </div>
            </div>
            
            <h3>布局设置</h3>
            <div class="layout-config">
              <el-form label-width="100px">
                <el-form-item label="导航模式">
                  <el-radio-group v-model="themeForm.navMode">
                    <el-radio label="sidebar">侧边栏</el-radio>
                    <el-radio label="top">顶部导航</el-radio>
                    <el-radio label="mix">混合模式</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="主题模式">
                  <el-radio-group v-model="themeForm.themeMode">
                    <el-radio label="light">浅色</el-radio>
                    <el-radio label="dark">深色</el-radio>
                    <el-radio label="auto">自动</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="固定头部">
                  <el-switch v-model="themeForm.fixedHeader" />
                </el-form-item>
                
                <el-form-item label="固定侧边栏">
                  <el-switch v-model="themeForm.fixedSidebar" />
                </el-form-item>
              </el-form>
            </div>
            
            <el-button type="primary" @click="saveThemeConfig">保存主题配置</el-button>
            <el-button @click="resetThemeConfig">重置主题</el-button>
          </div>
        </el-tab-pane>
        
        <!-- 系统设置 -->
        <el-tab-pane label="系统设置" name="system">
          <el-form label-width="150px">
            <el-form-item label="用户注册">
              <el-switch v-model="systemForm.allowRegister" />
              <span class="tip-text">允许用户注册账号</span>
            </el-form-item>
            
            <el-form-item label="评论功能">
              <el-switch v-model="systemForm.enableComment" />
              <span class="tip-text">启用文章评论功能</span>
            </el-form-item>
            
            <el-form-item label="文件上传大小">
              <el-input-number 
                v-model="systemForm.maxUploadSize" 
                :min="1" 
                :max="100" 
                controls-position="right"
              />
              <span class="tip-text">MB</span>
            </el-form-item>
            
            <el-form-item label="缓存时间">
              <el-input-number 
                v-model="systemForm.cacheTime" 
                :min="0" 
                :max="1440" 
                controls-position="right"
              />
              <span class="tip-text">分钟（0表示不缓存）</span>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSystemConfig">保存系统设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'

// 激活的标签页
const activeTab = ref('site')

// 站点设置表单
const siteFormRef = ref()
const siteForm = reactive({
  siteName: '民俗文化展示系统',
  siteDescription: '展示和传播中国传统民俗文化的平台',
  siteKeywords: '民俗,文化,传统,节日,艺术',
  siteLogo: ''
})

// 主题配置表单
const themeForm = reactive({
  primaryColor: '#409EFF',
  successColor: '#67C23A',
  warningColor: '#E6A23C',
  dangerColor: '#F56C6C',
  navMode: 'sidebar',
  themeMode: 'light',
  fixedHeader: true,
  fixedSidebar: true
})

// 系统设置表单
const systemForm = reactive({
  allowRegister: true,
  enableComment: true,
  maxUploadSize: 10,
  cacheTime: 30
})

// 表单验证规则
const siteRules = {
  siteName: [
    { required: true, message: '请输入站点名称', trigger: 'blur' }
  ],
  siteDescription: [
    { required: true, message: '请输入站点描述', trigger: 'blur' }
  ]
}

// 上传Logo前的验证
const beforeLogoUpload = (file: File) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('Logo必须是 JPG 或 PNG 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('Logo大小不能超过 2MB!')
    return false
  }
  return true
}

// 处理Logo上传
const handleLogoUpload = async (options: any) => {
  try {
    // 模拟上传过程
    const file = options.file
    const reader = new FileReader()
    reader.onload = (e) => {
      siteForm.siteLogo = e.target?.result as string
      ElMessage.success('Logo上传成功')
    }
    reader.readAsDataURL(file)
  } catch (error) {
    ElMessage.error('Logo上传失败')
  }
}

// 保存站点设置
const saveSiteConfig = async () => {
  try {
    await siteFormRef.value.validate()
    // 模拟保存到后端
    ElMessage.success('站点设置保存成功')
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

// 重置站点设置
const resetSiteConfig = () => {
  ElMessageBox.confirm('确定要重置站点设置吗？', '提示', {
    type: 'warning'
  }).then(() => {
    Object.assign(siteForm, {
      siteName: '民俗文化展示系统',
      siteDescription: '展示和传播中国传统民俗文化的平台',
      siteKeywords: '民俗,文化,传统,节日,艺术',
      siteLogo: ''
    })
    ElMessage.success('站点设置已重置')
  })
}

// 保存主题配置
const saveThemeConfig = () => {
  ElMessage.success('主题配置保存成功')
}

// 重置主题配置
const resetThemeConfig = () => {
  Object.assign(themeForm, {
    primaryColor: '#409EFF',
    successColor: '#67C23A',
    warningColor: '#E6A23C',
    dangerColor: '#F56C6C',
    navMode: 'sidebar',
    themeMode: 'light',
    fixedHeader: true,
    fixedSidebar: true
  })
  ElMessage.success('主题配置已重置')
}

// 保存系统设置
const saveSystemConfig = () => {
  ElMessage.success('系统设置保存成功')
}

onMounted(() => {
  // 加载配置数据
  loadConfigData()
})

// 加载配置数据
const loadConfigData = async () => {
  // 模拟从后端加载配置数据
  try {
    // 这里可以调用API获取配置数据
  } catch (error) {
    console.error('加载配置数据失败:', error)
  }
}
</script>

<style scoped>
.system-config-container {
  max-width: 100%;
  padding: 20px;
}

.page-title {
  color: #1e293b;
  margin-bottom: 24px;
  font-size: 1.8rem;
  font-weight: 600;
}

.theme-config h3 {
  margin: 20px 0 15px 0;
  color: #1e293b;
  font-size: 1.1rem;
}

.color-picker-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-value {
  font-family: monospace;
  color: #64748b;
}

.layout-config {
  margin-bottom: 20px;
}

.tip-text {
  margin-left: 10px;
  color: #64748b;
  font-size: 0.9rem;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
  width: 120px;
  height: 120px;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  text-align: center;
  line-height: 120px;
}

.avatar {
  width: 120px;
  height: 120px;
  display: block;
}
</style>