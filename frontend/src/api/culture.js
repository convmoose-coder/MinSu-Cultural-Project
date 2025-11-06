// 民俗文化API
import apiClient from './index'

// 获取民俗文化列表
export function getFolkCultures(params = {}) {
  return apiClient.get('/folkcultures', { params })
}

// 获取民俗文化详情
export function getFolkCultureById(id) {
  return apiClient.get(`/folkcultures/${id}`)
}

// 搜索民俗文化
export function searchFolkCultures(params = {}) {
  return apiClient.get('/search', { params })
}

// 获取地区列表
export function getRegions(params = {}) {
  return apiClient.get('/regions', { params })
}

// 获取地区详情
export function getRegionById(id) {
  return apiClient.get(`/regions/${id}`)
}

// 获取地区民俗文化
export function getRegionCultures(regionId, params = {}) {
  return apiClient.get(`/region/${regionId}`, { params })
}