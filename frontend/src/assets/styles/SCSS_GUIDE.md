# SCSS变量和混合器使用指南

## 颜色变量

### 主色调
- `$primary-color`: #4A90E2 (主蓝色)
- `$secondary-color`: #50E3C2 (次绿色)
- `$accent-color`: #F5A623 (强调橙色)

### 中性色
- `$gray-100` 到 `$gray-900`: 灰色系列
- `$black`: #000000
- `$white`: #FFFFFF

### 文字颜色
- `$text-primary`: #333333 (主要文字)
- `$text-secondary`: #666666 (次要文字)
- `$text-inverse`: #FFFFFF (反色文字)

### 背景颜色
- `$bg-primary`: #FFFFFF (主要背景)
- `$bg-secondary`: #F8F9FA (次要背景)
- `$bg-accent`: #F0F8FF (强调背景)

### 状态颜色
- `$success`: #2ECC71 (成功)
- `$warning`: #F39C12 (警告)
- `$danger`: #E74C3C (危险)
- `$info`: #3498DB (信息)

### 民族特色颜色
- `$traditional-red`: #C8102E (传统红色)
- `$traditional-gold`: #FFD700 (传统金色)
- `$traditional-blue`: #1E4A8B (传统蓝色)

## 间距变量
- `$spacing-xs`: 0.25rem
- `$spacing-sm`: 0.5rem
- `$spacing-md`: 1rem
- `$spacing-lg`: 1.5rem
- `$spacing-xl`: 2rem
- `$spacing-xxl`: 3rem

## 断点变量
- `$breakpoint-sm`: 576px
- `$breakpoint-md`: 768px
- `$breakpoint-lg`: 992px
- `$breakpoint-xl`: 1200px
- `$breakpoint-xxl`: 1400px

## 混合器 (Mixins)

### 布局相关
- `@mixin flex-center`: 居中对齐
- `@mixin flex-between`: 两端对齐
- `@mixin flex-column`: 垂直排列
- `@mixin absolute-center`: 绝对居中
- `@mixin absolute-full`: 全屏定位

### 文本相关
- `@mixin text-ellipsis`: 文本省略
- `@mixin text-ellipsis-multiline($lines)`: 多行文本省略

### 响应式设计
- `@mixin responsive($breakpoint)`: 响应式断点

### 民族特色装饰
- `@mixin chinese-pattern($opacity: 0.1)`: 中国传统图案背景

### 卡片样式
- `@mixin card($hover: false)`: 卡片样式

### 按钮样式
- `@mixin button($theme: primary)`: 按钮样式

### 主题应用
- `@mixin theme($theme)`: 应用主题
- `@mixin theme-surface($theme)`: 应用表面主题
- `@mixin theme-primary($theme)`: 应用主色主题
- `@mixin theme-secondary($theme)`: 应用次色主题
- `@mixin theme-accent($theme)`: 应用强调色主题

## 使用示例

### 颜色使用
```scss
.my-component {
  color: $text-primary;
  background-color: $bg-secondary;
}
```

### 混合器使用
```scss
.card {
  @include card(true);
  
  .title {
    @include text-ellipsis;
  }
}
```

### 响应式设计
```scss
.responsive-element {
  @include responsive(md) {
    padding: $spacing-lg;
  }
}
```