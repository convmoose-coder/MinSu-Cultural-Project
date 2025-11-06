<template>
  <admin-layout>
    <template #header>
      <div class="page-header">
        <h1>民俗文化管理</h1>
        <el-button type="primary" @click="handleAddCulture">
          <el-icon><Plus /></el-icon>
          添加文化信息
        </el-button>
      </div>
    </template>
    
    <div class="content-wrapper">
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索名称或描述" 
          prefix-icon="el-icon-search"
          clearable
          style="width: 300px;"
        ></el-input>
        
        <el-select 
          v-model="categoryFilter" 
          placeholder="选择分类" 
          clearable
          style="width: 180px; margin-left: 10px;"
        >
          <el-option 
            v-for="category in categories" 
            :key="category.value" 
            :label="category.label" 
            :value="category.value"
          ></el-option>
        </el-select>
        
        <el-button 
          type="default" 
          @click="handleSearch"
          style="margin-left: 10px;"
        >
          搜索
        </el-button>
        
        <el-button 
          type="default" 
          @click="handleReset"
          style="margin-left: 10px;"
        >
          重置
        </el-button>
      </div>
      
      <!-- 数据表格 -->
      <el-table 
        v-loading="loading" 
        :data="cultureData" 
        style="width: 100%"
        border
        row-key="id"
      >
        <el-table-column prop="id" label="ID" width="80" fixed></el-table-column>
        <el-table-column prop="name" label="名称" min-width="180"></el-table-column>
        <el-table-column prop="category" label="分类" width="120"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="280">
          <template #default="scope">
            <div class="text-ellipsis" :title="scope.row.description">
              {{ scope.row.description }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="region" label="地区" width="120"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              @click="handleEditCulture(scope.row)"
              style="margin-right: 5px;"
            >
              编辑
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDeleteCulture(scope.row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form 
        ref="formRef" 
        :model="formData" 
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        
        <el-form-item label="分类" prop="category">
          <el-select v-model="formData.category" placeholder="请选择分类">
            <el-option 
              v-for="category in categories" 
              :key="category.value" 
              :label="category.label" 
              :value="category.value"
            ></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="地区" prop="region">
          <el-input v-model="formData.region" placeholder="请输入地区"></el-input>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="formData.description" 
            placeholder="请输入描述"
            type="textarea"
            :rows="4"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-switch v-model="formData.status"></el-switch>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </admin-layout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import AdminLayout from '@/components/admin/AdminLayout.vue';
import { folkCulture } from '@/services/api';

// 表格数据
const cultureData = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const total = ref(0);

// 搜索筛选条件
const searchQuery = ref('');
const categoryFilter = ref('');

// 分类数据
const categories = ref([
  { label: '传统节日', value: 'festival' },
  { label: '民间艺术', value: 'art' },
  { label: '民俗礼仪', value: 'ritual' },
  { label: '传统工艺', value: 'craft' },
  { label: '民间文学', value: 'literature' }
]);

// 对话框
const dialogVisible = ref(false);
const dialogTitle = ref('添加文化信息');
const formRef = ref();

// 表单数据
const formData = reactive({
  id: '',
  name: '',
  category: '',
  region: '',
  description: '',
  status: true
});

// 表单验证规则
const formRules = reactive({
  name: [
    { required: true, message: '请输入名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度在 2 到 100 个字符之间', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  region: [
    { required: true, message: '请输入地区', trigger: 'blur' },
    { min: 2, max: 50, message: '地区长度在 2 到 50 个字符之间', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' }
  ]
});

// 获取数据
const fetchData = async () => {
  try {
    loading.value = true;
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      category: categoryFilter.value
    };
    
    const response = await folkCulture.getCultures(params);
    cultureData.value = response?.data || [];
    total.value = response?.total || 0;
  } catch (error) {
    console.error('获取数据失败:', error);
    ElMessage.error('获取数据失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

// 搜索
const handleSearch = () => {
  currentPage.value = 1;
  fetchData();
};

// 重置
const handleReset = () => {
  searchQuery.value = '';
  categoryFilter.value = '';
  currentPage.value = 1;
  fetchData();
};

// 分页大小变化
const handleSizeChange = (size) => {
  pageSize.value = size;
  fetchData();
};

// 当前页码变化
const handleCurrentChange = (current) => {
  currentPage.value = current;
  fetchData();
};

// 添加文化信息
const handleAddCulture = () => {
  dialogTitle.value = '添加文化信息';
  formData.id = '';
  formData.name = '';
  formData.category = '';
  formData.region = '';
  formData.description = '';
  formData.status = true;
  dialogVisible.value = true;
};

// 编辑文化信息
const handleEditCulture = async (row) => {
  try {
    const response = await folkCulture.getCultureDetail(row.id);
    const data = response?.data || {};
    
    dialogTitle.value = '编辑文化信息';
    formData.id = data.id || '';
    formData.name = data.name || '';
    formData.category = data.category || '';
    formData.region = data.region || '';
    formData.description = data.description || '';
    formData.status = data.status !== undefined ? data.status : true;
    
    dialogVisible.value = true;
  } catch (error) {
    console.error('获取详情失败:', error);
    ElMessage.error('获取详情失败');
  }
};

// 删除文化信息
const handleDeleteCulture = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条数据吗？此操作不可撤销。',
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );
    
    await folkCulture.deleteCulture(id);
    ElMessage.success('删除成功');
    fetchData();
  } catch (error) {
    // 用户取消删除会抛出错误，不处理
    if (error !== 'cancel') {
      console.error('删除失败:', error);
      ElMessage.error('删除失败');
    }
  }
};

// 提交表单
const handleSubmit = async () => {
  formRef.value?.validate(async (valid) => {
    if (!valid) return;
    
    try {
      if (formData.id) {
        // 更新
        await folkCulture.updateCulture(formData.id, formData);
        ElMessage.success('更新成功');
      } else {
        // 创建
        await folkCulture.createCulture(formData);
        ElMessage.success('创建成功');
      }
      
      dialogVisible.value = false;
      fetchData();
    } catch (error) {
      console.error('提交失败:', error);
      ElMessage.error('操作失败，请稍后重试');
    }
  });
};

// 初始加载
onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #1f2937;
}

.content-wrapper {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-filter {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .search-filter {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-filter .el-input,
  .search-filter .el-select {
    width: 100%;
    margin-left: 0 !important;
  }
  
  .pagination-wrapper {
    justify-content: center;
  }
}
</style>