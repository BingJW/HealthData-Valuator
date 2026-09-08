// src/api/evaluation.js
import request from './request'

/**
 * 获取所有评估指标
 * @returns {Promise}
 */
export const getIndicatorsAPI = () => {
  return request.get('/indicators')
}

/**
 * 创建新评估
 * @param {Object} data - 评估数据
 * @returns {Promise}
 */
export const createEvaluationAPI = (data) => {
  return request.post('/evaluations', data)
}

/**
 * 获取评估列表
 * @param {Object} params - 查询参数 {page, pageSize, status, keyword}
 * @returns {Promise}
 */
export const getEvaluationsAPI = (params = {}) => {
  return request.get('/evaluations', { params })
}

/**
 * 获取评估详情
 * @param {String|Number} id - 评估ID
 * @returns {Promise}
 */
export const getEvaluationDetailAPI = (id) => {
  return request.get(`/evaluations/${id}`)
}

/**
 * 更新评估数据
 * @param {String|Number} id - 评估ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export const updateEvaluationAPI = (id, data) => {
  return request.put(`/evaluations/${id}`, data)
}

/**
 * 删除评估
 * @param {String|Number} id - 评估ID
 * @returns {Promise}
 */
export const deleteEvaluationAPI = (id) => {
  return request.delete(`/evaluations/${id}`)
}

/**
 * 提交评估进行计算
 * @param {String|Number} id - 评估ID
 * @returns {Promise}
 */
export const submitEvaluationAPI = (id) => {
  return request.post(`/evaluations/${id}/submit`)
}

/**
 * 获取评估结果
 * @param {String|Number} id - 评估ID
 * @returns {Promise}
 */
export const getEvaluationResultAPI = (id) => {
  return request.get(`/evaluations/${id}/result`)
}

/**
 * 复制评估
 * @param {String|Number} id - 评估ID
 * @returns {Promise}
 */
export const duplicateEvaluationAPI = (id) => {
  return request.post(`/evaluations/${id}/duplicate`)
}

/**
 * 获取评估统计数据
 * @returns {Promise}
 */
export const getEvaluationStatsAPI = () => {
  return request.get('/evaluations/stats')
}
