import request from './request'

export const getSystemStatsAPI = () => request.get('/admin/stats')

export const getUsersAPI = (params = {}) => request.get('/admin/users', { params })

export const createAdminUserAPI = (data) => request.post('/admin/users', data)

export const getAdminUserAPI = (id) => request.get(`/admin/users/${id}`)

export const updateAdminUserAPI = (id, data) => request.put(`/admin/users/${id}`, data)

export const deleteAdminUserAPI = (id) => request.delete(`/admin/users/${id}`)

export const getWeightsAPI = () => request.get('/admin/weights')

export const updateWeightsAPI = (weights) => request.put('/admin/weights', weights)

export const getRecentEvaluationsAPI = (params = {}) =>
  request.get('/evaluations', { params: { page: 1, pageSize: 10, ...params, scope: 'all' } })

export const getDashboardDataAPI = () => request.get('/admin/stats')
