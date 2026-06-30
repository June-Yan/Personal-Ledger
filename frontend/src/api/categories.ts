import api from './index'
import type { ApiResponse, Category } from '../types'

export const getCategories = () =>
  api.get<ApiResponse<Category[]>>('/categories')

export const createCategory = (data: { name: string; type: 'income' | 'expense'; icon?: string; sort_order?: number }) =>
  api.post<ApiResponse<Category>>('/categories', data)

export const updateCategory = (id: number, data: { name?: string; icon?: string; sort_order?: number }) =>
  api.put<ApiResponse<Category>>(`/categories/${id}`, data)

export const deleteCategory = (id: number, confirm = false) =>
  api.delete<ApiResponse<null>>(`/categories/${id}?confirm=${confirm}`)
