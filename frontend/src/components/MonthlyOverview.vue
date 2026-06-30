<template>
  <div class="overview">
    <div class="card income">
      <div class="label">收入合计</div>
      <div class="amount">¥ {{ income.toFixed(2) }}</div>
    </div>
    <div class="card expense">
      <div class="label">支出合计</div>
      <div class="amount">¥ {{ expense.toFixed(2) }}</div>
    </div>
    <div class="card balance">
      <div class="label">结余</div>
      <div class="amount" :class="{ negative: balance < 0 }">¥ {{ balance.toFixed(2) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ income: number; expense: number; balance: number }>()
</script>

<style scoped>
.overview {
  display: flex;
  gap: 8px;
  padding: 0 12px 12px;
}
.card {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.label {
  font-size: 12px;
  color: #999;
  margin-bottom: 6px;
}
.amount {
  font-size: 16px;
  font-weight: 600;
}
.income .amount { color: #52c41a; }
.expense .amount { color: #ff4d4f; }
.balance .amount { color: #1890ff; }
.balance .amount.negative { color: #ff4d4f; }
</style>
