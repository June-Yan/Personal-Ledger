<template>
  <div class="category-view">
    <div class="header">
      <button class="back" @click="$router.back()">&lt; 返回</button>
      <h2>分类管理</h2>
      <span></span>
    </div>
    <div class="tabs">
      <button :class="{ active: activeType === 'expense' }" @click="activeType = 'expense'">支出</button>
      <button :class="{ active: activeType === 'income' }" @click="activeType = 'income'">收入</button>
    </div>
    <div class="list">
      <div v-for="cat in filtered" :key="cat.id" class="item">
        <span>{{ categoryIcon(cat.name) }} {{ cat.name }}</span>
        <button v-if="!cat.is_preset" class="del" @click="remove(cat.id)">删除</button>
      </div>
    </div>
    <div class="add-form">
      <input v-model="newName" placeholder="新分类名称" />
      <button @click="add" :disabled="!newName.trim()">添加</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCategoriesStore } from '../stores/categories'

const catStore = useCategoriesStore()
const activeType = ref<'expense' | 'income'>('expense')
const newName = ref('')

onMounted(() => catStore.fetchCategories())

const filtered = computed(() =>
  catStore.categories.filter(c => c.type === activeType.value).sort((a, b) => a.sort_order - b.sort_order)
)

const categoryIcon = (name: string) => {
  const map: Record<string, string> = { '餐饮': '🍜', '交通': '🚗', '购物': '🛍️', '娱乐': '🎮', '住房': '🏠', '收入': '💰' }
  return map[name] || '📄'
}

const add = async () => {
  try {
    await catStore.addCategory({ name: newName.value.trim(), type: activeType.value })
    newName.value = ''
  } catch (e: any) {
    alert(e.message)
  }
}

const remove = async (id: number) => {
  if (!confirm('确定删除该分类？如果分类下有账单，关联账单也会被删除。')) return
  try {
    await catStore.removeCategory(id, true)
  } catch (e: any) {
    alert(e.message)
  }
}
</script>

<style scoped>
.category-view { min-height: 100vh; background: #f5f5f5; }
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.back { background: none; border: none; color: #666; font-size: 14px; cursor: pointer; }
.header h2 { font-size: 16px; }
.tabs {
  display: flex;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.tabs button {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  font-size: 15px;
  color: #999;
  cursor: pointer;
}
.tabs button.active { color: #00bfa5; border-bottom: 2px solid #00bfa5; }
.list { background: #fff; margin: 12px; border-radius: 12px; overflow: hidden; }
.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #f5f5f5;
}
.item:last-child { border-bottom: none; }
.del {
  padding: 4px 12px;
  background: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}
.add-form {
  display: flex;
  gap: 8px;
  padding: 12px;
  background: #fff;
  margin: 0 12px;
  border-radius: 12px;
}
.add-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.add-form button {
  padding: 0 16px;
  background: #00bfa5;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.add-form button:disabled { background: #ccc; }
</style>
