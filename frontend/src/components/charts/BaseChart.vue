<!-- frontend/src/components/charts/BaseChart.vue -->
<template>
  <div 
    ref="chartRef" 
    :style="{
      width: width || '100%',
      height: height || '400px',
      ...customStyle
    }"
  ></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  options: {
    type: Object,
    required: true
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '400px'
  },
  theme: {
    type: String,
    default: 'light'
  },
  initOptions: {
    type: Object,
    default: () => ({})
  },
  autoResize: {
    type: Boolean,
    default: true
  },
  customStyle: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['chart-click', 'chart-ready'])

const chartRef = ref(null)
let chartInstance = null
let resizeObserver = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value, props.theme, props.initOptions)
  chartInstance.setOption(props.options)
  
  // 绑定事件
  chartInstance.on('click', (params) => {
    emit('chart-click', params)
  })
  
  emit('chart-ready', chartInstance)
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) return
  chartInstance.setOption(props.options, true)
}

// 自适应大小
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 监听选项变化
watch(
  () => props.options,
  () => {
    updateChart()
  },
  { deep: true }
)

onMounted(() => {
  initChart()
  
  // 自动调整大小
  if (props.autoResize) {
    resizeObserver = new ResizeObserver(handleResize)
    if (chartRef.value) {
      resizeObserver.observe(chartRef.value)
    }
  }
})

onBeforeUnmount(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})

// 暴露方法
defineExpose({
  getInstance: () => chartInstance,
  resize: handleResize,
  clear: () => {
    if (chartInstance) {
      chartInstance.clear()
    }
  }
})
</script>