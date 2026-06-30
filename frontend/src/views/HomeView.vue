<template>
  <div class="home-view">
    <div class="top-bar">
      <span class="logo">💰 个人记账本</span>
    </div>
    <MonthSwitcher v-model:year="year" v-model:month="month" />
    <MonthlyOverview :income="summary.income_total" :expense="summary.expense_total" :balance="summary.balance" />
    <div class="section-title">分类支出占比</div>
    <CategoryPieChart :data="breakdown" />
    <div class="section-title">最近账单 <router-link to="/bills" class="more">查看全部</router-link></div>
    <div class="recent-bills">
      <div v-for="bill in recentBills" :key="bill.id" class="bill-item">
        <div class="icon">{{ categoryIcon(bill.category_name) }}</div>
        <div class="info">
          <div class="name">{{ bill.category_name }} <small v-if="bill.note">{{ bill.note }}</small></div>
          <div class="date">{{ bill.bill_date }}</div>
        </div>
        <div class="amount" :class="bill.category_type">{{ bill.category_type === 'income' ? '+' : '-' }}¥{{ bill.amount.toFixed(2) }}</div>
      </div>
      <div v-if="recentBills.length === 0" class="empty">当前月份无账单记录</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import MonthSwitcher from '../components/MonthSwitcher.vue'
import MonthlyOverview from '../components/MonthlyOverview.vue'
import CategoryPieChart from '../components/CategoryPieChart.vue'
import { useBillsStore } from '../stores/bills'
import { useCategoriesStore } from '../stores/categories'
import * as reportsApi from '../api/reports'
import type { MonthlySummary, CategoryBreakdown } from '../types'

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)
const billsStore = useBillsStore()
const catStore = useCategoriesStore()

const summary = ref<MonthlySummary>({ income_total: 0, expense_total: 0, balance: 0 })
const breakdown = ref<CategoryBreakdown[]>([])

const recentBills = computed(() => billsStore.bills.slice(0, 5))

const categoryIcon = (name: string) => {
  const map: Record<string, string> = { '餐饮': '🍜', '交通': '🚗', '购物': '🛍️', '娱乐': '🎮', '住房': '🏠', '收入': '💰', '工资': '💼' }
  return map[name] || '📄'
}

const loadData = async () => {
  await billsStore.fetchBills(year.value, month.value, 1)
  await catStore.fetchCategories()
  const s = await reportsApi.getMonthlySummary(year.value, month.value) as any
  summary.value = s.data
  const b = await reportsApi.getCategoryBreakdown(year.value, month.value) as any
  breakdown.value = b.data
}

watch([year, month], loadData, { immediate: true })
</script>

<style scoped>
.home-view { padding-bottom: 16px; }
.top-bar {
  background: #00bfa5;
  color: #fff;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 600;
}
.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px 8px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}
.more {
  font-size: 12px;
  color: #00bfa5;
  text-decoration: none;
}
.recent-bills {
  background: #fff;
  margin: 0 12px;
  border-radius: 12px;
  overflow: hidden;
}
.bill-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f5f5f5;
}
.bill-item:last-child { border-bottom: none; }
.icon { font-size: 24px; margin-right: 12px; }
.info { flex: 1; }
.name { font-size: 14px; color: #333; }
.name small { color: #999; margin-left: 4px; }
.date { font-size: 12px; color: #999; margin-top: 2px; }
.amount { font-size: 14px; font-weight: 600; }
.amount.income { color: #52c41a; }
.amount.expense { color: #ff4d4f; }
.empty { text-align: center; padding: 24px; color: #999; font-size: 14px; }
</style>
