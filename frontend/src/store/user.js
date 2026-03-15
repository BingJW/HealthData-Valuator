// frontend/src/store/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  loginAPI, 
  registerAPI, 
  getUserInfoAPI, 
  logoutAPI,  // 确保导入 logoutAPI
  updateUserInfoAPI 
} from '@/api/user'  // 或 '../api/user'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref({})
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.username === 'admin' || localStorage.getItem('isAdmin') === 'true')

  // 设置token
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  // 清除token
  const clearToken = () => {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('token')
    localStorage.removeItem('isAdmin')
  }

  // 登录
  const login = async (formData) => {
    try {
      const res = await loginAPI(formData)
      // 后端返回结构：{ code, data: { token, user_info } }
      if (res.code === 0 && res.data && res.data.token) {
        setToken(res.data.token)
        userInfo.value = res.data.user_info || {}
        const isAdminUser = (res.data.user_info?.username === 'admin')
        if (isAdminUser) localStorage.setItem('isAdmin', 'true')
        else localStorage.removeItem('isAdmin')
        ElMessage.success('登录成功')
        return res
      }
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }

  // 注册
  const register = async (formData) => {
    try {
      const res = await registerAPI(formData)
      ElMessage.success('注册成功，请登录')
      return res
    } catch (error) {
      console.error('注册失败:', error)
      throw error
    }
  }

  // 获取用户信息
  const getUserInfo = async () => {
    try {
      const res = await getUserInfoAPI()
      userInfo.value = res.data || {}
      return res
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // token可能失效，清除token
      if (error.response?.status === 401) {
        clearToken()
      }
      throw error
    }
  }

  // 更新用户信息
  const updateUserInfo = async (data) => {
    try {
      const res = await updateUserInfoAPI(data)
      userInfo.value = { ...userInfo.value, ...data }
      ElMessage.success('个人信息更新成功')
      return res
    } catch (error) {
      console.error('更新用户信息失败:', error)
      throw error
    }
  }

  // 退出登录 - 使用 logoutAPI
  const logout = async () => {
    try {
      await logoutAPI()  // 调用API退出登录
    } catch (error) {
      console.error('退出登录失败:', error)
      // 即使API调用失败，也要清除本地token
    } finally {
      clearToken()
      ElMessage.success('已退出登录')
      router.push('/login')
    }
  }

  // 检查token是否有效
  const checkToken = async () => {
    if (!token.value) return false
    
    try {
      await getUserInfo()
      return true
    } catch (error) {
      return false
    }
  }

  return {
    token,
    userInfo,
    isAuthenticated,
    isAdmin,
    
    // 方法
    setToken,
    clearToken,
    login,
    register,
    getUserInfo,
    logout,  // 确保导出logout方法
    updateUserInfo,
    checkToken
  }
})