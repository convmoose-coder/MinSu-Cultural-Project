import { ref, onMounted } from 'vue'

/**
 * 数据获取自定义Hook
 * 封装异步数据获取逻辑，提供加载状态和错误处理
 * @param {Function} fetchFn - 数据获取函数
 * @param {Array} deps - 依赖数组，当这些值变化时重新获取数据
 * @returns {Object} { data, loading, error, refetch }
 */
export function useDataFetching(fetchFn, deps = []) {
  // 响应式状态
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // 数据获取函数
  const fetchData = async () => {
    // 重置状态
    loading.value = true
    error.value = null
    
    try {
      // 执行数据获取
      const result = await fetchFn()
      data.value = result
    } catch (err) {
      // 捕获错误
      error.value = err
      console.error('数据获取失败:', err)
    } finally {
      // 无论成功失败，都设置loading为false
      loading.value = false
    }
  }

  // 重新获取数据的方法
  const refetch = () => fetchData()

  // 组件挂载时获取数据
  onMounted(() => {
    fetchData()
  })

  return {
    data,
    loading,
    error,
    refetch
  }
}

/**
 * 延迟执行函数
 * @param {number} ms - 延迟毫秒数
 * @returns {Promise}
 */
export function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
