import { reactive, readonly } from 'vue'
import { folkCultureApi } from '@/api/culture'

// 状态对象
const state = reactive({
  folkCultures: [],
  currentCulture: null,
  regions: [],
  categories: [],
  loading: false,
  error: null
})

/**
 * 民俗文化Store
 * 提供全局状态管理和数据操作方法
 */
export const folkCultureStore = {
  // 获取只读状态
  get state() {
    return readonly(state)
  },

  /**
   * 加载所有民俗文化数据
   */
  async loadAllFolkCultures() {
    state.loading = true
    state.error = null
    
    try {
      const response = await folkCultureApi.getCultures()
      state.folkCultures = response.data
    } catch (err) {
      state.error = err
      console.error('加载民俗文化数据失败:', err)
    } finally {
      state.loading = false
    }
  },

  /**
   * 根据ID加载民俗文化详情
   * @param {number} id - 民俗文化ID
   */
  async loadFolkCultureById(id) {
    state.loading = true
    state.error = null
    
    try {
      const response = await folkCultureApi.getCultureById(id)
      state.currentCulture = response.data
    } catch (err) {
      state.error = err
      console.error(`加载ID为${id}的民俗文化详情失败:`, err)
    } finally {
      state.loading = false
    }
  },

  /**
   * 创建新的民俗文化记录
   * @param {Object} data - 民俗文化数据
   */
  async createNewFolkCulture(data) {
    state.loading = true
    state.error = null
    
    try {
      const result = await folkCultureApi.createCulture(data)
      // 创建成功后重新加载数据
      await this.loadAllFolkCultures()
      return result
    } catch (err) {
      state.error = err
      console.error('创建民俗文化记录失败:', err)
      throw err
    } finally {
      state.loading = false
    }
  },

  /**
   * 加载所有地区
   */
  async loadRegions() {
    try {
      const response = await folkCultureApi.getRegions()
      state.regions = response.data
    } catch (err) {
      console.error('加载地区数据失败:', err)
    }
  },

  /**
   * 加载所有分类
   */
  async loadCategories() {
    try {
      const response = await folkCultureApi.getCategories()
      state.categories = response.data
    } catch (err) {
      console.error('加载分类数据失败:', err)
    }
  },

  /**
   * 清除当前错误状态
   */
  clearError() {
    state.error = null
  },

  /**
   * 清除当前选中的民俗文化
   */
  clearCurrentCulture() {
    state.currentCulture = null
  }
}

export default folkCultureStore
