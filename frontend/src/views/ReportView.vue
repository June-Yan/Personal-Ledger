<template>
  <div class="report-view">
    <div class="top-bar">
      <h2>报表</h2>
    </div>
    <MonthSwitcher v-model:year="year" v-model:month="month" />
    <MonthlyOverview :income="summary.income_total" :expense="summary.expense_total" :balance="summary.balance" />
    <div class="section-title">分类支出占比</div>
    <CategoryPieChart :data="breakdown" />
    <div class="section-title">支出明细</div>
    <div class="breakdown-list">
      <div v-for="item in breakdown" :key="item.category_id" class="item">
        <span class="name">{{ item.category_name }}</span>
        <div class="bar-wrap">
          <div class="bar" :style="{ width: item.percentage + '%' }"></div>
        </div>
        <span class="amount">¥{{ item.amount.toFixed(2) }}</span>
        <span class="pct">{{ item.percentage }}%</span>
      </div>
      <div v-if="breakdown.length === 0" class="empty">暂无支出数据</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import MonthSwitcher from '../components/MonthSwitcher.vue'
import MonthlyOverview from '../components/MonthlyOverview.vue'
import CategoryPieChart from '../components/CategoryPieChart.vue'
import * as reportsApi from '../api/reports'
import type { MonthlySummary, CategoryBreakdown } from '../types'

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)

const summary = ref<MonthlySummary>({ income_total: 0, expense_total: 0, balance: 0 })
const breakdown = ref<CategoryBreakdown[]>([])

const load = async () => {
  const s = await reportsApi.getMonthlySummary(year.value, month.value) as any
  summary.value = s.data
  const b = await reportsApi.getCategoryBreakdown(year.value, month.value) as any
  breakdown.value = b.data
}

watch([year, month], load, { immediate: true })
</script>

<style scoped>
.report-view { padding-bottom: 16px; }
.top-bar { background: #00bfa5; color: #fff; padding: 12px 16px; font-size: 16px; font-weight: 600; }
.section-title { padding: 12px 16px 8px; font-size: 14px; font-weight: 600; }
.breakdown-list { background: #fff; margin: 0 12px; border-radius: 12px; padding: 8px 16px; }
.item { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
.item:last-child { border-bottom: none; }
.name { width: 60px; font-size: 13px; color: #666; }
.bar-wrap { flex: 1; height: 8px; background: #f0f0f0; border-radius: 4px; margin: 0 8px; overflow: hidden; }
.bar { height: 100%; background: #00bfa5; border-radius: 4px; }
.amount { width: 80px; text-align: right; font-size: 13px; color: #333; }
.pct { width: 48px; text-align: right; font-size: 12px; color: #999; }
.empty { text-align: center; padding: 24px; color: #999; }
</style>
