<template>
  <div>
    <h2>管理后台首页</h2>
    <p>欢迎使用乘灼管理后台系统</p>
    
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <h3>乘灼文化总数</h3>
          <p>128</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <h3>本月新增</h3>
          <p>12</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <h3>待审核内容</h3>
          <p>5</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
// 这里可以添加首页组件的逻辑
</script>

<style scoped>
.el-row {
  margin-top: 20px;
}

.el-card {
  text-align: center;
}
</style>