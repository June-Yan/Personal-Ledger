<template>
  <div class="pie-chart">
    <div ref="chartRef" style="width: 100%; height: 240px;"></div>
    <div v-if="data.length === 0" class="empty">暂无支出数据</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import * as echarts from 'echarts'
import type { CategoryBreakdown } from '../types'

const props = defineProps<{ data: CategoryBreakdown[] }>()
const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const render = () => {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  if (props.data.length === 0) {
    chart.clear()
    return
  }
  chart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
    legend: { bottom: 0, left: 'center', itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 11 } },
    series: [{
      type: 'pie',
      radius: ['40%', '65%'],
      center: ['50%', '45%'],
      data: props.data.map(d => ({ name: d.category_name, value: d.amount })),
      label: { show: false },
      itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 2 }
    }]
  })
}

onMounted(render)
watch(() => props.data, render, { deep: true })
</script>

<style scoped>
.pie-chart {
  background: #fff;
  border-radius: 12px;
  margin: 0 12px 12px;
  position: relative;
}
.empty {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 14px;
}
</style>
