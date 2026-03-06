<!-- frontend/src/components/DemoDataPanel.vue -->
<template>
  <el-dialog
    v-model="visible"
    title="演示数据管理"
    width="600px"
    :before-close="handleClose"
  >
    <el-tabs v-model="activeTab">
      <el-tab-pane label="数据初始化" name="init">
        <div class="demo-info">
          <el-alert
            title="演示数据说明"
            type="info"
            :closable="false"
            description="初始化演示数据将清空现有数据，创建3个测试用户和3个评估示例。"
            class="mb-4"
          />
          
          <el-descriptions :column="1" border>
            <el-descriptions-item label="测试用户">
              <el-tag type="success" class="mr-2">admin / admin123</el-tag>
              <el-tag class="mr-2">doctor_zhang / password123</el-tag>
              <el-tag type="warning">nurse_li / password123</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="评估示例">
              1. 2023年度数据资产评估 (125万元)<br>
              2. 急诊科数据专项评估 (85万元)<br>
              3. 医疗影像数据评估 (210万元)
            </el-descriptions-item>
          </el-descriptions>
          
          <div class="mt-6 text-center">
            <el-button
              type="primary"
              :loading="loading.init"
              @click="handleInitDemoData"
              size="large"
            >
              <el-icon><Refresh /></el-icon>
              初始化演示数据
            </el-button>
          </div>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="数据统计" name="stats">
        <div v-if="stats" class="stats-grid">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon users">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_users }}</div>
                <div class="stat-label">总用户数</div>
              </div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon evaluations">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.total_evaluations }}</div>
                <div class="stat-label">总评估数</div>
              </div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon value">
                <el-icon><Money /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ formatCurrency(stats.total_value) }}</div>
                <div class="stat-label">总估值</div>
              </div>
            </div>
          </el-card>
          
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-icon avg">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ formatCurrency(stats.average_value) }}</div>
                <div class="stat-label">平均估值</div>
              </div>
            </div>
          </el-card>
        </div>
        
        <div v-else class="loading-state">
          <el-skeleton :rows="4" animated />
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="handleClose">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { 
  Refresh, 
  User, 
  Document, 
  Money, 
  TrendCharts 
} from '@element-plus/icons-vue'
import { initDemoDataAPI, getDemoStatsAPI } from '@/api/demo'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'data-initialized'])

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const activeTab = ref('init')
const loading = reactive({
  init: false,
  stats: false
})
const stats = ref(null)

// 格式化货币
const formatCurrency = (value) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value || 0)
}

// 获取统计数据
const fetchStats = async () => {
  loading.stats = true
  try {
    const res = await getDemoStatsAPI()
    stats.value = res.data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  } finally {
    loading.stats = false
  }
}

// 初始化演示数据
const handleInitDemoData = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要初始化演示数据吗？现有数据将被清空。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    loading.init = true
    const res = await initDemoDataAPI()
    
    ElMessage.success(res.message || '演示数据初始化成功')
    emit('data-initialized')
    activeTab.value = 'stats'
    await fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('初始化失败: ' + (error.response?.data?.message || error.message))
    }
  } finally {
    loading.init = false
  }
}

// 关闭对话框
const handleClose = () => {
  visible.value = false
}

// 标签切换时刷新统计数据
watch(activeTab, (newTab) => {
  if (newTab === 'stats' && !stats.value) {
    fetchStats()
  }
})

onMounted(() => {
  if (visible.value && activeTab.value === 'stats') {
    fetchStats()
  }
})
</script>

<style scoped>
.demo-info {
  padding: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 0.5rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 24px;
}

.stat-icon.users {
  background-color: #e6f4ff;
  color: #409eff;
}

.stat-icon.evaluations {
  background-color: #f0f9eb;
  color: #67c23a;
}

.stat-icon.value {
  background-color: #fef0f0;
  color: #f56c6c;
}

.stat-icon.avg {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
}

.loading-state {
  padding: 2rem 0;
}

:deep(.el-descriptions__label) {
  width: 100px;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

.mt-6 {
  margin-top: 1.5rem;
}
</style>