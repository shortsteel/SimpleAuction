import { reactive, computed } from 'vue'
import api from '../api'

const state = reactive({
  token: localStorage.getItem('token') || null,
  userInfo: null
})

export function useStore() {
  const isAuthenticated = computed(() => !!state.token)

  const setToken = (token) => {
    state.token = token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUserInfo = (userInfo) => {
    state.userInfo = userInfo
  }

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password })
      setToken(response.data.token)
      setUserInfo(response.data.user)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || '登录失败'
      }
    }
  }

  const register = async (username, email, password) => {
    try {
      const response = await api.post('/auth/register', { username, email, password })
      setToken(response.data.token)
      setUserInfo(response.data.user)
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || '注册失败'
      }
    }
  }

  const checkAuth = async () => {
    // 从localStorage同步token到state
    const token = localStorage.getItem('token')
    if (token && token !== state.token) {
      state.token = token
    }
    
    if (!state.token) return
    
    try {
      const response = await api.get('/auth/me')
      setUserInfo(response.data)
    } catch (error) {
      // 如果验证失败，清除token
      if (error.response?.status === 401 || error.response?.status === 422) {
        setToken(null)
        setUserInfo(null)
      }
    }
  }

  const logout = () => {
    setToken(null)
    setUserInfo(null)
  }

  return {
    state,
    isAuthenticated,
    userInfo: computed(() => state.userInfo),
    setToken,
    login,
    register,
    checkAuth,
    logout
  }
}

