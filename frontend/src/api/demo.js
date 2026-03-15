import request from './request'

/** 获取演示/统计数据（复用 admin 统计） */
export const getDemoStatsAPI = () => request.get('/admin/stats')

/** 初始化演示数据（用户与评估示例） */
export const initDemoDataAPI = () => request.post('/demo/init')
