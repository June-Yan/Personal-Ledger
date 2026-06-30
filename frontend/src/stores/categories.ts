import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Category } from '../types'
import * as catApi from '../api/categories'

export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])

  const expenseCategories = computed(() => categories.value.filter(c => c.type === 'expense'))
  const incomeCategories = computed(() => categories.value.filter(c => c.type === 'income'))

  const fetchCategories = async () => {
    const res = await catApi.getCategories() as any
    categories.value = res.data
  }

  const addCategory = async (data: { name: string; type: 'income' | 'expense'; icon?: string; sort_order?: number }) => {
    const res = await catApi.createCategory(data) as any
    categories.value.push(res.data)
    return res.data
  }

  const updateCategoryItem = async (id: number, data: { name?: string; icon?: string; sort_order?: number }) => {
    const res = await catApi.updateCategory(id, data) as any
    const idx = categories.value.findIndex(c => c.id === id)
    if (idx !== -1) categories.value[idx] = res.data
    return res.data
  }

  const removeCategory = async (id: number, confirm = false) => {
    await catApi.deleteCategory(id, confirm)
    categories.value = categories.value.filter(c => c.id !== id)
  }

  return { categories, expenseCategories, incomeCategories, fetchCategories, addCategory, updateCategoryItem, removeCategory }
})
