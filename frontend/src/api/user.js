// frontend/src/api/user.js
import request from './request'

/**
 * 用户登录
 * @param {Object} data - 登录数据 {username, password}
 * @returns {Promise}
 */
export const loginAPI = (data) => {
  return request.post('/auth/login', data)
}

/**
 * 用户注册
 * @param {Object} data - 注册数据 {username, password, hospital, phone, email}
 * @returns {Promise}
 */
export const registerAPI = (data) => {
  return request.post('/auth/register', data)
}

/**
 * 获取用户信息
 * @returns {Promise}
 */
export const getUserInfoAPI = () => {
  return request.get('/user/info')
}

/**
 * 更新用户信息
 * @param {Object} data - 用户信息
 * @returns {Promise}
 */
export const updateUserInfoAPI = (data) => {
  return request.put('/user/info', data)
}

/**
 * 修改密码
 * @param {Object} data - 密码数据 {oldPassword, newPassword}
 * @returns {Promise}
 */
export const changePasswordAPI = (data) => {
  return request.post('/user/change-password', data)
}

/**
 * 退出登录 - 修复的关键：添加这个函数
 * @returns {Promise}
 */
export const logoutAPI = () => {
  return request.post('/auth/logout')
}

/**
 * 发送重置密码邮件
 * @param {Object} data - 邮箱数据 {email}
 * @returns {Promise}
 */
export const forgotPasswordAPI = (data) => {
  return request.post('/auth/forgot-password', data)
}

/**
 * 重置密码
 * @param {Object} data - 重置密码数据 {token, newPassword}
 * @returns {Promise}
 */
export const resetPasswordAPI = (data) => {
  return request.post('/auth/reset-password', data)
}