// frontend/src/api/request.js
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useUserStore } from '@/store/user'

// 创建axios实例
const request = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 添加token到请求头
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (Array.isArray(error.response?.data?.detail)) {
      error.response.data.detail = error.response.data.detail.map(item => item.msg).join('；')
    }
    
    if (typeof error.response?.data?.detail === 'string') error.response.data.message = error.response.data.detail
    // 如果是401错误（未授权），清除token并跳转到登录页
    if (error.response && error.response.status === 401) {
      useUserStore().clearToken()
      if (router.currentRoute.value.path !== '/login') {
        ElMessage.error('登录已过期，请重新登录')
        router.push({ path: '/login', query: { redirect: router.currentRoute.value.fullPath } })
      }
    }
    
    return Promise.reject(error)
  }
)

export default request