<template>
  <div class="month-switcher">
    <button @click="prevMonth">&lt;</button>
    <span>{{ year }}年{{ month }}月</span>
    <button @click="nextMonth" :disabled="isCurrentMonth">&gt;</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ year: number; month: number }>()
const emit = defineEmits(['update:year', 'update:month'])

const isCurrentMonth = computed(() => {
  const now = new Date()
  return props.year === now.getFullYear() && props.month === now.getMonth() + 1
})

const prevMonth = () => {
  let y = props.year, m = props.month - 1
  if (m < 1) { m = 12; y-- }
  emit('update:year', y)
  emit('update:month', m)
}

const nextMonth = () => {
  if (isCurrentMonth.value) return
  let y = props.year, m = props.month + 1
  if (m > 12) { m = 1; y++ }
  emit('update:year', y)
  emit('update:month', m)
}
</script>

<style scoped>
.month-switcher {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 12px;
  font-size: 18px;
  font-weight: 600;
}
.month-switcher button {
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  padding: 4px 12px;
}
.month-switcher button:disabled {
  color: #ccc;
}
</style>
