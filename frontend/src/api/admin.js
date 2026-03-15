import request from './request'

export const getSystemStatsAPI = () => request.get('/admin/stats')

export const getUsersAPI = (params = {}) => request.get('/admin/users', { params })

export const getWeightsAPI = () => request.get('/admin/weights')

export const updateWeightsAPI = (weights) => request.put('/admin/weights', weights)

export const getRecentEvaluationsAPI = (params = {}) =>
  request.get('/evaluations', { params: { page: 1, pageSize: 10, ...params } })

export const getDashboardDataAPI = () => request.get('/admin/stats')
