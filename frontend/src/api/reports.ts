import api from './index'
import type { ApiResponse, MonthlySummary, CategoryBreakdown } from '../types'

export const getMonthlySummary = (year: number, month: number) =>
  api.get<ApiResponse<MonthlySummary>>('/reports/monthly-summary', { params: { year, month } })

export const getCategoryBreakdown = (year: number, month: number) =>
  api.get<ApiResponse<CategoryBreakdown[]>>('/reports/category-breakdown', { params: { year, month } })
