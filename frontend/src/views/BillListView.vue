<template>
  <div class="bill-list-view">
    <div class="top-bar">
      <h2>账单管理</h2>
    </div>
    <div class="filter-bar">
      <select v-model="filterType">
        <option value="">全部类型</option>
        <option value="expense">支出</option>
        <option value="income">收入</option>
      </select>
    </div>
    <button class="add-btn" @click="$router.push('/add')">+ 新增账单</button>
    <div class="bill-list">
      <div v-for="bill in filteredBills" :key="bill.id" class="bill-item" @click="editBill(bill)">
        <div class="icon">{{ categoryIcon(bill.category_name) }}</div>
        <div class="info">
          <div class="name">{{ bill.category_name }} <small v-if="bill.note">{{ bill.note }}</small></div>
          <div class="date">{{ bill.bill_date }}</div>
        </div>
        <div class="right">
          <div class="amount" :class="bill.category_type">{{ bill.category_type === 'income' ? '+' : '' }}¥{{ bill.amount.toFixed(2) }}</div>
          <button class="del" @click.stop="delBill(bill.id)">删除</button>
        </div>
      </div>
      <div v-if="filteredBills.length === 0" class="empty">暂无账单</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBillsStore } from '../stores/bills'
import type { Bill } from '../types'

const router = useRouter()
const billsStore = useBillsStore()
const filterType = ref('')

const now = new Date()
const year = now.getFullYear()
const month = now.getMonth() + 1

onMounted(() => billsStore.fetchBills(year, month))

const filteredBills = computed(() => {
  if (!filterType.value) return billsStore.bills
  return billsStore.bills.filter(b => b.category_type === filterType.value)
})

const categoryIcon = (name: string) => {
  const map: Record<string, string> = { '餐饮': '🍜', '交通': '🚗', '购物': '🛍️', '娱乐': '🎮', '住房': '🏠', '收入': '💰', '工资': '💼' }
  return map[name] || '📄'
}

const editBill = (bill: Bill) => {
  router.push({ path: '/add', query: { id: bill.id } })
}

const delBill = async (id: number) => {
  if (!confirm('确定删除该账单？')) return
  await billsStore.removeBill(id)
}
</script>

<style scoped>
.bill-list-view { padding: 0 12px 16px; }
.top-bar { padding: 12px 0; }
.top-bar h2 { font-size: 18px; }
.filter-bar { margin-bottom: 12px; }
.filter-bar select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  font-size: 14px;
}
.add-btn {
  width: 100%;
  padding: 12px;
  background: #00bfa5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  margin-bottom: 12px;
}
.bill-list { background: #fff; border-radius: 12px; overflow: hidden; }
.bill-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
}
.bill-item:last-child { border-bottom: none; }
.icon { font-size: 24px; margin-right: 12px; }
.info { flex: 1; }
.name { font-size: 14px; color: #333; }
.name small { color: #999; margin-left: 4px; }
.date { font-size: 12px; color: #999; margin-top: 2px; }
.right { text-align: right; }
.amount { font-size: 14px; font-weight: 600; }
.amount.income { color: #52c41a; }
.amount.expense { color: #ff4d4f; }
.del {
  margin-top: 4px;
  padding: 2px 8px;
  background: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}
.empty { text-align: center; padding: 24px; color: #999; }
</style>
