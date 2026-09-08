import request from './request'
export const loginAPI = data => request.post('/auth/login', data)
export const registerAPI = data => request.post('/auth/register', data)
export const getUserInfoAPI = () => request.get('/user/info')
export const updateUserInfoAPI = data => request.put('/user/info', data)
export const logoutAPI = () => request.post('/auth/logout')
