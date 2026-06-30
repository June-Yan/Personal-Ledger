import api from './index'
import type { ApiResponse, Bill } from '../types'

export interface BillListRes {
  items: Bill[];
  total: number;
  page: number;
  page_size: number;
}

export const getBills = (year: number, month: number, page = 1, pageSize = 20) =>
  api.get<ApiResponse<BillListRes>>('/bills', { params: { year, month, page, page_size: pageSize } })

export const createBill = (data: { amount: number; category_id: number; note?: string; bill_date: string }) =>
  api.post<ApiResponse<Bill>>('/bills', data)

export const updateBill = (id: number, data: { amount?: number; category_id?: number; note?: string; bill_date?: string }) =>
  api.put<ApiResponse<Bill>>(`/bills/${id}`, data)

export const deleteBill = (id: number) =>
  api.delete<ApiResponse<null>>(`/bills/${id}`)
