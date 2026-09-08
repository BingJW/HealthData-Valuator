<!-- frontend/src/components/charts/RadarChart.vue -->
<template>
  <BaseChart
    ref="chartRef"
    :options="options"
    :width="width"
    :height="height"
    :theme="theme"
    @chart-click="handleChartClick"
  />
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseChart from './BaseChart.vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(item => 
        item && typeof item === 'object' && 
        'name' in item && 'value' in item
      )
    }
  },
  title: {
    type: String,
    default: '成本分布雷达图'
  },
  indicators: {
    type: Array,
    default: () => [
      { name: '数据战略与治理', max: 100 },
      { name: '数据获取与采集', max: 100 },
      { name: '数据存储与备份', max: 100 },
      { name: '数据处理与加工', max: 100 },
      { name: '数据应用与分析', max: 100 },
      { name: '数据流通与共享', max: 100 },
      { name: '数据安全隐私合规', max: 100 },
      { name: '数据归档与销毁', max: 100 },
      { name: '数据全流程人力', max: 100 }
    ]
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '500px'
  },
  theme: {
    type: String,
    default: 'light'
  },
  showLegend: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['item-click'])

const chartRef = ref(null)

// 计算选项
const options = computed(() => {
  return {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        return `${params.name}: ${params.value}%`
      }
    },
    legend: props.showLegend ? {
      type: 'scroll',
      bottom: 10,
      data: props.data.map(item => item.name)
    } : null,
    radar: {
      indicator: props.indicators,
      shape: 'circle',
      splitNumber: 5,
      axisName: {
        color: '#333',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: [
            'rgba(64, 158, 255, 0.1)',
            'rgba(64, 158, 255, 0.2)',
            'rgba(64, 158, 255, 0.4)',
            'rgba(64, 158, 255, 0.6)',
            'rgba(64, 158, 255, 0.8)'
          ]
        }
      },
      splitArea: {
        show: false
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(64, 158, 255, 0.3)'
        }
      }
    },
    series: [
      {
        name: props.title,
        type: 'radar',
        data: props.data,
        symbolSize: 6,
        lineStyle: {
          width: 2
        },
        label: {
          show: true,
          formatter: (params) => {
            return `${params.value}%`
          }
        },
        areaStyle: {
          opacity: 0.1
        },
        emphasis: {
          lineStyle: {
            width: 3
          },
          areaStyle: {
            opacity: 0.3
          }
        }
      }
    ],
    color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
  }
})

// 处理点击事件
const handleChartClick = (params) => {
  emit('item-click', params)
}

// 暴露方法
defineExpose({
  resize: () => {
    if (chartRef.value && chartRef.value.getInstance()) {
      chartRef.value.getInstance().resize()
    }
  }
})
</script>