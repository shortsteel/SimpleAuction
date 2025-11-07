import axios from 'axios'
import router from '../router'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
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
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理认证错误（401和422都可能是认证问题）
    if (error.response?.status === 401 || error.response?.status === 422) {
      // 清除token
      localStorage.removeItem('token')
      // 如果不在登录页面，则跳转到登录页
      if (router.currentRoute.value.path !== '/login' && router.currentRoute.value.path !== '/register') {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

export default api

