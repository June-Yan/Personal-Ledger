import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '../types'
import * as authApi from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref<User | null>(null)

  const setAuth = (t: string, u: User) => {
    token.value = t
    user.value = u
    localStorage.setItem('token', t)
  }

  const clearAuth = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  const isLoggedIn = () => !!token.value

  const logout = async () => {
    try { await authApi.logout() } catch {}
    clearAuth()
  }

  return { token, user, setAuth, clearAuth, isLoggedIn, logout }
})
