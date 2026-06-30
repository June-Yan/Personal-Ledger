<template>
  <div class="add-bill-view">
    <div class="header">
      <button class="back" @click="$router.back()">&lt; 返回</button>
      <h2>{{ isEdit ? '编辑账单' : '记一笔' }}</h2>
      <span></span>
    </div>
    <div class="form">
      <div class="amount-field">
        <span class="prefix">¥</span>
        <input v-model="form.amount" type="number" step="0.01" placeholder="0.00" />
      </div>
      <div class="type-toggle">
        <button :class="{ active: form.type === 'expense' }" @click="form.type = 'expense'">支出</button>
        <button :class="{ active: form.type === 'income' }" @click="form.type = 'income'">收入</button>
      </div>
      <div class="field">
        <label>分类</label>
        <div class="category-grid">
          <button
            v-for="cat in currentCategories"
            :key="cat.id"
            :class="{ active: form.category_id === cat.id }"
            @click="form.category_id = cat.id"
          >
            <span class="cat-icon">{{ categoryIcon(cat.name) }}</span>
            <span class="cat-name">{{ cat.name }}</span>
          </button>
        </div>
      </div>
      <div class="field">
        <label>日期</label>
        <input v-model="form.bill_date" type="date" />
      </div>
      <div class="field">
        <label>备注</label>
        <input v-model="form.note" type="text" placeholder="选填" maxlength="200" />
      </div>
      <button class="save" :disabled="!canSave" @click="save">{{ isEdit ? '保存修改' : '保存' }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBillsStore } from '../stores/bills'
import { useCategoriesStore } from '../stores/categories'

const route = useRoute()
const router = useRouter()
const billsStore = useBillsStore()
const catStore = useCategoriesStore()

const isEdit = computed(() => !!route.query.id)

const form = ref({
  amount: '',
  type: 'expense' as 'income' | 'expense',
  category_id: 0,
  bill_date: new Date().toISOString().slice(0, 10),
  note: ''
})

const currentCategories = computed(() =>
  form.value.type === 'expense' ? catStore.expenseCategories : catStore.incomeCategories
)

const canSave = computed(() => {
  const amt = parseFloat(form.value.amount)
  return !isNaN(amt) && amt > 0 && form.value.category_id > 0
})

const categoryIcon = (name: string) => {
  const map: Record<string, string> = { '餐饮': '🍜', '交通': '🚗', '购物': '🛍️', '娱乐': '🎮', '住房': '🏠', '收入': '💰', '工资': '💼' }
  return map[name] || '📄'
}

onMounted(async () => {
  await catStore.fetchCategories()
  if (isEdit.value) {
    const bill = billsStore.bills.find(b => b.id === Number(route.query.id))
    if (bill) {
      form.value.amount = String(bill.amount)
      form.value.type = bill.category_type
      form.value.category_id = bill.category_id
      form.value.bill_date = bill.bill_date
      form.value.note = bill.note || ''
    }
  } else if (currentCategories.value.length > 0) {
    form.value.category_id = currentCategories.value[0].id
  }
})

const save = async () => {
  const data = {
    amount: parseFloat(parseFloat(form.value.amount).toFixed(2)),
    category_id: form.value.category_id,
    note: form.value.note || undefined,
    bill_date: form.value.bill_date
  }
  try {
    if (isEdit.value) {
      await billsStore.updateBillItem(Number(route.query.id), data)
    } else {
      await billsStore.addBill(data)
    }
    router.push('/')
  } catch (e: any) {
    alert(e.message)
  }
}
</script>

<style scoped>
.add-bill-view {
  min-height: 100vh;
  background: #fff;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
}
.back {
  background: none;
  border: none;
  color: #666;
  font-size: 14px;
  cursor: pointer;
}
.header h2 { font-size: 16px; }
.form { padding: 16px; }
.amount-field {
  display: flex;
  align-items: center;
  border-bottom: 2px solid #00bfa5;
  padding: 12px 0;
  margin-bottom: 16px;
}
.prefix {
  font-size: 24px;
  color: #333;
  margin-right: 8px;
}
.amount-field input {
  flex: 1;
  border: none;
  font-size: 32px;
  outline: none;
}
.type-toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.type-toggle button {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
}
.type-toggle button.active {
  border-color: #00bfa5;
  background: #e6f9f6;
  color: #00bfa5;
}
.field { margin-bottom: 16px; }
.field label {
  display: block;
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}
.field input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
}
.category-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}
.category-grid button {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 4px;
  border: 1px solid #eee;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
}
.category-grid button.active {
  border-color: #00bfa5;
  background: #e6f9f6;
}
.cat-icon { font-size: 20px; margin-bottom: 4px; }
.cat-name { font-size: 12px; color: #666; }
.save {
  width: 100%;
  padding: 14px;
  background: #00bfa5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
}
.save:disabled { background: #ccc; }
</style>
