import api from './index'
import type { ApiResponse, User } from '../types'

export interface LoginRes {
  token: string;
  user: User;
}

export const sendCode = (email: string) =>
  api.post<ApiResponse<null>>('/auth/send-code', { email })

export const register = (email: string, password: string, code: string) =>
  api.post<ApiResponse<LoginRes>>('/auth/register', { email, password, code })

export const loginPassword = (email: string, password: string) =>
  api.post<ApiResponse<LoginRes>>('/auth/login/password', { email, password })

export const loginCode = (email: string, code: string) =>
  api.post<ApiResponse<LoginRes>>('/auth/login/code', { email, code })

export const logout = () =>
  api.post<ApiResponse<null>>('/auth/logout')

export const deleteAccount = () =>
  api.delete<ApiResponse<null>>('/auth/account')
