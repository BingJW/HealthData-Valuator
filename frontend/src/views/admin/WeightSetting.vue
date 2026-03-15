<!-- frontend/src/views/admin/WeightSetting.vue -->
<template>
  <div class="weight-setting-container">
    <el-card class="header-card">
      <template #header>
        <div class="header-content">
          <div>
            <h2>权重设置</h2>
            <p>调整9大类成本指标的权重系数，影响总估值计算</p>
          </div>
          <el-button type="primary" plain @click="$router.push('/admin/dashboard')">返回概览</el-button>
        </div>
      </template>
      
      <el-alert
        title="权重说明"
        type="info"
        :closable="false"
        class="mb-4"
      >
        <p>• 权重系数会影响总估值的计算结果（总估值 = Σ(金额 × 权重)）</p>
        <p>• 默认权重为1.0，表示对原始金额不做调整</p>
        <p>• 权重大于1.0会增加该类别的价值贡献</p>
        <p>• 权重小于1.0会减少该类别的价值贡献</p>
      </el-alert>
    </el-card>
    
    <el-row :gutter="20" class="mt-6">
      <el-col :xs="24" :md="16">
        <el-card class="weights-card">
          <template #header>
            <div class="card-header">
              <h3>权重配置</h3>
              <div class="header-actions">
                <el-button @click="resetToDefault" :loading="loading.reset">
                  <el-icon><Refresh /></el-icon>
                  重置默认
                </el-button>
                <el-button 
                  type="primary" 
                  @click="saveWeights" 
                  :loading="loading.save"
                  :disabled="!hasChanges"
                >
                  <el-icon><Check /></el-icon>
                  保存更改
                </el-button>
              </div>
            </div>
          </template>
          
          <el-table 
            :data="weightsList" 
            stripe
            class="weights-table"
          >
            <el-table-column label="成本类别" width="180">
              <template #default="{ row }">
                <div class="category-cell">
                  <span class="category-badge">{{ row.id }}</span>
                  <span class="category-name">{{ row.name }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="当前权重" width="150">
              <template #default="{ row }">
                <el-tag 
                  :type="getWeightTagType(row.weight)"
                  size="large"
                  class="weight-tag"
                >
                  {{ row.weight.toFixed(2) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="权重调整">
              <template #default="{ row }">
                <div class="weight-control">
                  <el-slider
                    v-model="row.weight"
                    :min="0.1"
                    :max="3"
                    :step="0.1"
                    :show-input="true"
                    :format-tooltip="formatTooltip"
                    @change="handleWeightChange(row)"
                  />
                  <div class="weight-hints">
                    <span class="hint low" :class="{ active: row.weight < 1 }">低</span>
                    <span class="hint normal" :class="{ active: row.weight === 1 }">正常</span>
                    <span class="hint high" :class="{ active: row.weight > 1 }">高</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="影响系数" width="120">
              <template #default="{ row }">
                <div class="impact-factor">
                  {{ calculateImpact(row.weight) }}
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :md="8">
        <el-card class="preview-card">
          <template #header>
            <h3>权重分布预览</h3>
          </template>
          
          <div class="preview-content">
            <div class="chart-container">
              <BaseChart
                ref="previewChartRef"
                :options="previewOptions"
                height="300px"
              />
            </div>
            
            <div class="stats-summary">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="平均权重">
                  {{ avgWeight.toFixed(2) }}
                </el-descriptions-item>
                <el-descriptions-item label="最大权重">
                  {{ maxWeight.toFixed(2) }} ({{ maxWeightCategory }})
                </el-descriptions-item>
                <el-descriptions-item label="最小权重">
                  {{ minWeight.toFixed(2) }} ({{ minWeightCategory }})
                </el-descriptions-item>
                <el-descriptions-item label="总调整系数">
                  {{ totalImpact.toFixed(2) }}x
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useAdminStore } from '@/store/admin'
import { Refresh, Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useResponsive } from '@/utils/responsive'
import BaseChart from '@/components/charts/BaseChart.vue'

const adminStore = useAdminStore()
const previewChartRef = ref(null)

// 9大类成本类别定义
const categories = [
  { id: 1, name: '数据战略与治理成本' },
  { id: 2, name: '数据获取与采集成本' },
  { id: 3, name: '数据存储与备份成本' },
  { id: 4, name: '数据处理与加工成本' },
  { id: 5, name: '数据应用与分析成本' },
  { id: 6, name: '数据流通与共享成本' },
  { id: 7, name: '数据安全、隐私与合规成本' },
  { id: 8, name: '数据归档与销毁成本' },
  { id: 9, name: '数据全流程人力成本' }
]

// 加载状态
const loading = reactive({
  save: false,
  reset: false
})

// 权重列表
const weightsList = reactive([])

// 原始权重备份
const originalWeights = ref({})

// 计算统计信息
const avgWeight = computed(() => {
  if (weightsList.length === 0) return 0
  const sum = weightsList.reduce((total, item) => total + item.weight, 0)
  return sum / weightsList.length
})

const maxWeight = computed(() => {
  if (weightsList.length === 0) return 0
  return Math.max(...weightsList.map(item => item.weight))
})

const minWeight = computed(() => {
  if (weightsList.length === 0) return 0
  return Math.min(...weightsList.map(item => item.weight))
})

const maxWeightCategory = computed(() => {
  const item = weightsList.find(item => item.weight === maxWeight.value)
  return item ? item.name : ''
})

const minWeightCategory = computed(() => {
  const item = weightsList.find(item => item.weight === minWeight.value)
  return item ? item.name : ''
})

const totalImpact = computed(() => {
  return weightsList.reduce((total, item) => total + item.weight, 0)
})

// 检查是否有更改
const hasChanges = computed(() => {
  if (weightsList.length === 0) return false
  
  for (const item of weightsList) {
    const original = originalWeights.value[item.id]
    if (original === undefined || Math.abs(item.weight - original) > 0.01) {
      return true
    }
  }
  return false
})

// 获取权重标签类型
const getWeightTagType = (weight) => {
  if (weight < 0.8) return 'info'
  if (weight < 1.2) return ''
  if (weight < 1.8) return 'warning'
  return 'danger'
}

// 格式化工具提示
const formatTooltip = (value) => {
  return value.toFixed(1)
}

// 计算影响系数
const calculateImpact = (weight) => {
  if (weight < 1) return `-${(1 - weight) * 100}%`
  if (weight > 1) return `+${(weight - 1) * 100}%`
  return '0%'
}

// 处理权重变化
const handleWeightChange = (row) => {
  // 更新预览图表
  if (previewChartRef.value && previewChartRef.value.getInstance()) {
    previewChartRef.value.getInstance().setOption(previewOptions.value, true)
  }
}

// 重置为默认
const resetToDefault = () => {
  loading.reset = true
  try {
    weightsList.forEach(item => {
      item.weight = 1.0
    })
    
    // 备份当前权重
    backupCurrentWeights()
    
    ElMessage.success('已重置为默认权重')
  } finally {
    loading.reset = false
  }
}

// 保存权重
const saveWeights = async () => {
  loading.save = true
  try {
    const weights = {}
    weightsList.forEach(item => {
      weights[item.id] = item.weight
    })
    
    await adminStore.updateWeights(weights)
    
    // 更新备份
    backupCurrentWeights()
    
    ElMessage.success('权重设置保存成功')
  } catch (error) {
    ElMessage.error('保存失败: ' + (error.response?.data?.message || error.message))
  } finally {
    loading.save = false
  }
}

// 备份当前权重
const backupCurrentWeights = () => {
  originalWeights.value = {}
  weightsList.forEach(item => {
    originalWeights.value[item.id] = item.weight
  })
}

// 预览图表选项
const previewOptions = computed(() => {
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params) => {
        const param = params[0]
        return `${param.name}: ${param.value.toFixed(2)}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: weightsList.map(item => item.name),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 3,
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#eee'
        }
      }
    },
    series: [
      {
        name: '权重',
        type: 'bar',
        data: weightsList.map(item => item.weight),
        itemStyle: {
          color: (params) => {
            const weight = params.data
            if (weight < 0.8) return '#91cc75'
            if (weight < 1.2) return '#5470c6'
            if (weight < 1.8) return '#fac858'
            return '#ee6666'
          }
        },
        markLine: {
          silent: true,
          lineStyle: {
            color: '#999',
            type: 'dashed'
          },
          data: [
            {
              yAxis: 1,
              name: '默认权重'
            }
          ],
          label: {
            formatter: '默认: 1.0',
            position: 'end'
          }
        }
      }
    ]
  }
})

// 初始化
onMounted(async () => {
  try {
    // 获取当前权重
    await adminStore.fetchWeights()
    
    // 初始化权重列表
    categories.forEach(category => {
      const weight = adminStore.weights[category.id] || 1.0
      weightsList.push({
        id: category.id,
        name: category.name,
        weight: weight
      })
    })
    
    // 备份初始权重
    backupCurrentWeights()
  } catch (error) {
    console.error('初始化权重设置失败:', error)
  }
})

// 监听窗口大小变化
const { width } = useResponsive()
watch(width, () => {
  if (previewChartRef.value && previewChartRef.value.getInstance()) {
    previewChartRef.value.getInstance().resize()
  }
})
</script>

<style scoped>
.weight-setting-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.header-content h2 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 24px;
}

.header-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.weights-table {
  margin-top: 10px;
}

.category-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #409eff;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
}

.category-name {
  font-weight: 500;
}

.weight-tag {
  font-family: 'Courier New', monospace;
  font-weight: bold;
}

.weight-control {
  padding: 5px 0;
}

.weight-hints {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.weight-hints .hint {
  padding: 2px 8px;
  border-radius: 4px;
  transition: all 0.3s;
}

.weight-hints .hint.active {
  background-color: #409eff;
  color: white;
}

.weight-hints .hint.low.active {
  background-color: #91cc75;
}

.weight-hints .hint.normal.active {
  background-color: #5470c6;
}

.weight-hints .hint.high.active {
  background-color: #ee6666;
}

.impact-factor {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  text-align: center;
}

.preview-content {
  padding: 10px 0;
}

.chart-container {
  height: 300px;
  margin-bottom: 20px;
}

.stats-summary {
  margin-top: 20px;
}

:deep(.el-descriptions__label) {
  width: 120px;
}

:deep(.el-descriptions__content) {
  font-weight: 500;
}

.mt-6 {
  margin-top: 24px;
}

.mb-4 {
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions .el-button {
    flex: 1;
  }
}
</style>