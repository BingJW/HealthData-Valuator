// frontend/src/store/admin.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { 
  getSystemStatsAPI, 
  getWeightsAPI,
  updateWeightsAPI,
  getDashboardDataAPI
} from '@/api/admin'

export const useAdminStore = defineStore('admin', () => {
  const systemStats = ref({})
  const recentEvaluations = ref([])
  const weights = ref({})
  const dashboardData = ref({})

  // 获取系统统计数据
  const fetchSystemStats = async () => {
    try {
      const res = await getSystemStatsAPI()
      systemStats.value = res.data
      return res
    } catch (error) {
      console.error('获取系统统计失败:', error)
      throw error
    }
  }

  // 获取权重设置
  const fetchWeights = async () => {
    try {
      const res = await getWeightsAPI()
      weights.value = res.data
      return res
    } catch (error) {
      console.error('获取权重失败:', error)
      throw error
    }
  }

  // 更新权重
  const updateWeights = async (newWeights) => {
    try {
      const res = await updateWeightsAPI(newWeights)
      weights.value = newWeights
      return res
    } catch (error) {
      console.error('更新权重失败:', error)
      throw error
    }
  }

  // 获取仪表盘数据
  const fetchDashboardData = async () => {
    try {
      const res = await getDashboardDataAPI()
      dashboardData.value = res.data
      return res
    } catch (error) {
      console.error('获取仪表盘数据失败:', error)
      throw error
    }
  }

  return {
    systemStats,
    recentEvaluations,
    weights,
    dashboardData,
    fetchSystemStats,
    fetchWeights,
    updateWeights,
    fetchDashboardData
  }
})