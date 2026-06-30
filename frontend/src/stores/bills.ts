import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Bill } from '../types'
import * as billsApi from '../api/bills'

export const useBillsStore = defineStore('bills', () => {
  const bills = ref<Bill[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(20)

  const fetchBills = async (year: number, month: number, p = 1) => {
    const res = await billsApi.getBills(year, month, p, pageSize.value) as any
    if (p === 1) {
      bills.value = res.data.items
    } else {
      bills.value.push(...res.data.items)
    }
    total.value = res.data.total
    page.value = p
  }

  const addBill = async (data: { amount: number; category_id: number; note?: string; bill_date: string }) => {
    const res = await billsApi.createBill(data) as any
    bills.value.unshift(res.data)
    total.value++
    return res.data
  }

  const updateBillItem = async (id: number, data: { amount?: number; category_id?: number; note?: string; bill_date?: string }) => {
    const res = await billsApi.updateBill(id, data) as any
    const idx = bills.value.findIndex(b => b.id === id)
    if (idx !== -1) bills.value[idx] = res.data
    return res.data
  }

  const removeBill = async (id: number) => {
    await billsApi.deleteBill(id)
    bills.value = bills.value.filter(b => b.id !== id)
    total.value--
  }

  return { bills, total, page, pageSize, fetchBills, addBill, updateBillItem, removeBill }
})
