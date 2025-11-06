<template>
  <AdminLayout>
    <div class="content-config-container">
      <h2 class="page-title">内容配置</h2>
      
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 分类管理 -->
        <el-tab-pane label="分类管理" name="categories">
          <div class="category-management">
            <div class="toolbar">
              <el-button type="primary" @click="handleAddCategory">
                <el-icon><Plus /></el-icon>
                添加分类
              </el-button>
              
              <el-button type="warning" @click="handleSortCategories">
                <el-icon><Sort /></el-icon>
                排序分类
              </el-button>
            </div>
            
            <el-table 
              :data="categoryList" 
              style="width: 100%"
              border
              row-key="id"
            >
              <el-table-column prop="id" label="ID" width="80" />
              
              <el-table-column prop="name" label="分类名称" min-width="150" />
              
              <el-table-column prop="slug" label="标识符" min-width="120">
                <template #default="scope">
                  <el-tag size="small">{{ scope.row.slug }}</el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="description" label="描述" min-width="200" />
              
              <el-table-column prop="sortOrder" label="排序" width="80" />
              
              <el-table-column prop="status" label="状态" width="80">
                <template #default="scope">
                  <el-switch 
                    v-model="scope.row.status" 
                    :active-value="true" 
                    :inactive-value="false"
                    @change="handleToggleCategoryStatus(scope.row)"
                  />
                </template>
              </el-table-column>
              
              <el-table-column prop="createdAt" label="创建时间" width="160">
                <template #default="scope">
                  {{ formatDate(scope.row.createdAt) }}
                </template>
              </el-table-column>
              
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="handleEditCategory(scope.row)"
                  >
                    编辑
                  </el-button>
                  
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="handleDeleteCategory(scope.row)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        
        <!-- 标签管理 -->
        <el-tab-pane label="标签管理" name="tags">
          <div class="tag-management">
            <div class="toolbar">
              <el-input 
                v-model="tagSearchQuery" 
                placeholder="搜索标签名称" 
                prefix-icon="Search"
                clearable
                style="width: 300px;"
                @clear="handleTagSearch"
                @keyup.enter="handleTagSearch"
              />
              
              <el-button type="primary" @click="handleAddTag">
                <el-icon><Plus /></el-icon>
                添加标签
              </el-button>
              
              <el-button type="warning" @click="handleBatchTagOperation">
                <el-icon><Operation /></el-icon>
                批量操作
              </el-button>
            </div>
            
            <div class="tag-cloud">
              <el-tag 
                v-for="tag in tagList" 
                :key="tag.id"
                :type="getTagType(tag.usageCount)"
                size="large"
                closable
                @close="handleDeleteTag(tag)"
                @click="handleEditTag(tag)"
                style="margin: 5px; cursor: pointer;"
              >
                {{ tag.name }} ({{ tag.usageCount }})
              </el-tag>
            </div>
            
            <div class="pagination-wrapper">
              <el-pagination
                v-model:current-page="tagCurrentPage"
                v-model:page-size="tagPageSize"
                :page-sizes="[20, 50, 100, 200]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="tagTotal"
                @size-change="handleTagSizeChange"
                @current-change="handleTagCurrentChange"
              />
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 内容设置 -->
        <el-tab-pane label="内容设置" name="settings">
          <div class="content-settings">
            <el-form label-width="150px">
              <el-form-item label="内容审核">
                <el-switch v-model="contentSettings.requireApproval" />
                <span class="tip-text">新发布的内容需要审核后才能显示</span>
              </el-form-item>
              
              <el-form-item label="评论审核">
                <el-switch v-model="contentSettings.commentApproval" />
                <span class="tip-text">新发布的评论需要审核后才能显示</span>
              </el-form-item>
              
              <el-form-item label="内容分页大小">
                <el-input-number 
                  v-model="contentSettings.pageSize" 
                  :min="5" 
                  :max="50" 
                  controls-position="right"
                />
                <span class="tip-text">条/页</span>
              </el-form-item>
              
              <el-form-item label="热门内容标准">
                <el-input-number 
                  v-model="contentSettings.hotThreshold" 
                  :min="10" 
                  :max="1000" 
                  controls-position="right"
                />
                <span class="tip-text">浏览量达到此数值的内容标记为热门</span>
              </el-form-item>
              
              <el-form-item label="自动保存间隔">
                <el-input-number 
                  v-model="contentSettings.autoSaveInterval" 
                  :min="1" 
                  :max="10" 
                  controls-position="right"
                />
                <span class="tip-text">分钟</span>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="saveContentSettings">保存设置</el-button>
                <el-button @click="resetContentSettings">重置设置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
      
      <!-- 分类编辑对话框 -->
      <el-dialog 
        v-model="categoryDialogVisible" 
        :title="categoryDialogTitle" 
        width="500px"
        :close-on-click-modal="false"
      >
        <el-form 
          ref="categoryFormRef" 
          :model="categoryForm" 
          :rules="categoryRules"
          label-width="80px"
        >
          <el-form-item label="分类名称" prop="name">
            <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
          </el-form-item>
          
          <el-form-item label="标识符" prop="slug">
            <el-input v-model="categoryForm.slug" placeholder="请输入标识符（英文）" />
          </el-form-item>
          
          <el-form-item label="描述" prop="description">
            <el-input 
              v-model="categoryForm.description" 
              type="textarea" 
              :rows="3"
              placeholder="请输入分类描述"
            />
          </el-form-item>
          
          <el-form-item label="排序" prop="sortOrder">
            <el-input-number 
              v-model="categoryForm.sortOrder" 
              :min="1" 
              :max="999" 
              controls-position="right"
            />
          </el-form-item>
          
          <el-form-item label="状态" prop="status">
            <el-switch v-model="categoryForm.status" />
            <span class="tip-text">{{ categoryForm.status ? '启用' : '禁用' }}</span>
          </el-form-item>
        </el-form>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="categoryDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleCategorySubmit">确定</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 标签编辑对话框 -->
      <el-dialog 
        v-model="tagDialogVisible" 
        :title="tagDialogTitle" 
        width="400px"
        :close-on-click-modal="false"
      >
        <el-form 
          ref="tagFormRef" 
          :model="tagForm" 
          :rules="tagRules"
          label-width="80px"
        >
          <el-form-item label="标签名称" prop="name">
            <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
          </el-form-item>
          
          <el-form-item label="描述" prop="description">
            <el-input 
              v-model="tagForm.description" 
              type="textarea" 
              :rows="2"
              placeholder="请输入标签描述（可选）"
            />
          </el-form-item>
        </el-form>
        
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="tagDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleTagSubmit">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Sort, Search, Operation } from '@element-plus/icons-vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'

// 激活的标签页
const activeTab = ref('categories')

// 分类管理
const categoryList = ref([])
const categoryDialogVisible = ref(false)
const categoryDialogTitle = ref('添加分类')
const categoryFormRef = ref()
const isCategoryEdit = ref(false)

// 分类表单数据
const categoryForm = reactive({
  id: '',
  name: '',
  slug: '',
  description: '',
  sortOrder: 1,
  status: true
})

// 分类验证规则
const categoryRules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入标识符', trigger: 'blur' },
    { pattern: /^[a-z0-9-]+$/, message: '标识符只能包含小写字母、数字和横线', trigger: 'blur' }
  ]
}

// 标签管理
const tagList = ref([])
const tagSearchQuery = ref('')
const tagCurrentPage = ref(1)
const tagPageSize = ref(20)
const tagTotal = ref(0)
const tagDialogVisible = ref(false)
const tagDialogTitle = ref('添加标签')
const tagFormRef = ref()
const isTagEdit = ref(false)

// 标签表单数据
const tagForm = reactive({
  id: '',
  name: '',
  description: ''
})

// 标签验证规则
const tagRules = {
  name: [
    { required: true, message: '请输入标签名称', trigger: 'blur' }
  ]
}

// 内容设置
const contentSettings = reactive({
  requireApproval: true,
  commentApproval: false,
  pageSize: 20,
  hotThreshold: 100,
  autoSaveInterval: 3
})

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

// 获取标签类型（根据使用次数）
const getTagType = (usageCount: number) => {
  if (usageCount > 100) return 'danger'
  if (usageCount > 50) return 'warning'
  if (usageCount > 20) return 'primary'
  return 'info'
}

// 分类管理方法
const handleAddCategory = () => {
  isCategoryEdit.value = false
  categoryDialogTitle.value = '添加分类'
  Object.assign(categoryForm, {
    id: '',
    name: '',
    slug: '',
    description: '',
    sortOrder: categoryList.value.length + 1,
    status: true
  })
  categoryDialogVisible.value = true
}

const handleEditCategory = (category: any) => {
  isCategoryEdit.value = true
  categoryDialogTitle.value = '编辑分类'
  Object.assign(categoryForm, { ...category })
  categoryDialogVisible.value = true
}

const handleCategorySubmit = async () => {
  try {
    await categoryFormRef.value.validate()
    
    if (isCategoryEdit.value) {
      ElMessage.success('分类更新成功')
    } else {
      ElMessage.success('分类添加成功')
    }
    
    categoryDialogVisible.value = false
    loadCategories()
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

const handleToggleCategoryStatus = async (category: any) => {
  try {
    // 模拟API调用
    ElMessage.success(`分类${category.status ? '启用' : '禁用'}成功`)
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDeleteCategory = async (category: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类 "${category.name}" 吗？此操作不可恢复。`,
      '警告',
      { type: 'warning' }
    )
    
    ElMessage.success('分类删除成功')
    loadCategories()
  } catch (error) {
    // 用户取消操作
  }
}

const handleSortCategories = () => {
  ElMessage.info('排序功能开发中...')
}

// 标签管理方法
const handleAddTag = () => {
  isTagEdit.value = false
  tagDialogTitle.value = '添加标签'
  Object.assign(tagForm, {
    id: '',
    name: '',
    description: ''
  })
  tagDialogVisible.value = true
}

const handleEditTag = (tag: any) => {
  isTagEdit.value = true
  tagDialogTitle.value = '编辑标签'
  Object.assign(tagForm, { ...tag })
  tagDialogVisible.value = true
}

const handleTagSubmit = async () => {
  try {
    await tagFormRef.value.validate()
    
    if (isTagEdit.value) {
      ElMessage.success('标签更新成功')
    } else {
      ElMessage.success('标签添加成功')
    }
    
    tagDialogVisible.value = false
    loadTags()
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

const handleDeleteTag = async (tag: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除标签 "${tag.name}" 吗？`,
      '提示',
      { type: 'warning' }
    )
    
    ElMessage.success('标签删除成功')
    loadTags()
  } catch (error) {
    // 用户取消操作
  }
}

const handleTagSearch = () => {
  tagCurrentPage.value = 1
  loadTags()
}

const handleBatchTagOperation = () => {
  ElMessage.info('批量操作功能开发中...')
}

const handleTagSizeChange = (size: number) => {
  tagPageSize.value = size
  tagCurrentPage.value = 1
  loadTags()
}

const handleTagCurrentChange = (page: number) => {
  tagCurrentPage.value = page
  loadTags()
}

// 内容设置方法
const saveContentSettings = () => {
  ElMessage.success('内容设置保存成功')
}

const resetContentSettings = () => {
  Object.assign(contentSettings, {
    requireApproval: true,
    commentApproval: false,
    pageSize: 20,
    hotThreshold: 100,
    autoSaveInterval: 3
  })
  ElMessage.success('内容设置已重置')
}

// 加载数据方法
const loadCategories = async () => {
  // 模拟数据
  categoryList.value = [
    {
      id: 1,
      name: '传统节日',
      slug: 'festival',
      description: '中国传统节日文化',
      sortOrder: 1,
      status: true,
      createdAt: '2024-01-01T00:00:00'
    },
    {
      id: 2,
      name: '民间艺术',
      slug: 'art',
      description: '民间艺术表演和技艺',
      sortOrder: 2,
      status: true,
      createdAt: '2024-01-02T00:00:00'
    }
  ]
}

const loadTags = async () => {
  // 模拟数据
  tagList.value = [
    { id: 1, name: '春节', description: '中国传统节日', usageCount: 156 },
    { id: 2, name: '剪纸', description: '民间艺术', usageCount: 89 },
    { id: 3, name: '舞龙', description: '传统表演', usageCount: 67 },
    { id: 4, name: '元宵节', description: '传统节日', usageCount: 45 },
    { id: 5, name: '刺绣', description: '手工艺', usageCount: 34 }
  ]
  tagTotal.value = 5
}

onMounted(() => {
  loadCategories()
  loadTags()
})
</script>

<style scoped>
.content-config-container {
  max-width: 100%;
  padding: 20px;
}

.page-title {
  color: #1e293b;
  margin-bottom: 24px;
  font-size: 1.8rem;
  font-weight: 600;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.tag-cloud {
  min-height: 200px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  margin-bottom: 20px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.tip-text {
  margin-left: 10px;
  color: #64748b;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .toolbar > * {
    width: 100%;
  }
}
</style>