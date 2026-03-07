<!-- frontend/src/views/admin/Dashboard.vue -->
<template>
  <div class="admin-dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1><el-icon><Monitor /></el-icon> 管理员看板</h1>
      <p class="subtitle">系统运行状态与数据概览</p>
    </div>

    <!-- 系统概览卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :xs="24" :sm="12" :md="6" v-for="card in overviewCards" :key="card.title">
        <el-card shadow="hover" class="stat-card" :style="{ borderLeft: `4px solid ${card.color}` }">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: card.color + '20' }">
              <el-icon :size="24" :color="card.color">
                <component :is="card.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-label">{{ card.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 两列布局 -->
    <el-row :gutter="20" class="dashboard-content">
      <!-- 左列：评估统计 -->
      <el-col :xs="24" :lg="16">
        <!-- 最近评估列表 -->
        <el-card class="recent-evaluations" shadow="never">
          <template #header>
            <div class="card-header">
              <h3><el-icon><Clock /></el-icon> 最近评估</h3>
              <div class="header-actions">
                <!-- 搜索和操作区域 -->
                <div class="search-actions-row">
                  <!-- 医院搜索框 -->
                  <el-input
                    v-model="hospitalSearch"
                    placeholder="按医院名称搜索"
                    clearable
                    class="search-input"
                    @input="handleHospitalSearch"
                    @clear="handleSearchClear"
                  >
                    <template #prefix>
                      <el-icon><Search /></el-icon>
                    </template>
                  </el-input>
                  
                  <!-- 操作按钮组 -->
                  <div class="action-buttons">
                    <!-- 高级筛选 -->
                    <el-dropdown @command="handleAdvancedFilter" trigger="click">
                      <el-button>
                        <el-icon><Filter /></el-icon>
                        筛选
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item command="all">显示全部</el-dropdown-item>
                          <el-dropdown-item command="completed" divided>仅显示已完成</el-dropdown-item>
                          <el-dropdown-item command="processing">仅显示计算中</el-dropdown-item>
                          <el-dropdown-item command="draft">仅显示草稿</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                    
                    <!-- 刷新按钮 -->
                    <el-button type="primary" @click="refreshData">
                      <el-icon><Refresh /></el-icon> 刷新
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 搜索统计 -->
            <div v-if="showSearchInfo" class="search-info">
              <el-tag type="info" size="small" class="mr-2">
                共找到 {{ filteredEvaluations.length }} 条记录
              </el-tag>
              <el-tag v-if="hospitalSearch" type="primary" size="small" closable @close="clearHospitalSearch">
                医院: {{ hospitalSearch }}
              </el-tag>
              <el-tag v-if="currentStatusFilter !== 'all'" :type="getStatusType(currentStatusFilter)" size="small" closable @close="clearStatusFilter">
                状态: {{ getStatusText(currentStatusFilter) }}
              </el-tag>
            </div>
          </template>
          
          <!-- 评估表格 -->
          <el-table 
            :data="paginatedEvaluations" 
            stripe
            style="width: 100%"
            v-loading="loading.evaluations"
            :default-sort="{ prop: 'createdAt', order: 'descending' }"
            @sort-change="handleSortChange"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="评估名称" width="200">
              <template #default="{ row }">
                <router-link :to="`/result/${row.id}`" class="evaluation-link">
                  {{ row.name }}
                </router-link>
              </template>
            </el-table-column>
            <el-table-column prop="hospital" label="医院" width="150">
              <template #header>
                <div class="column-header">
                  <span>医院</span>
                  <el-icon v-if="hospitalSearch" color="#409EFF" style="margin-left: 4px;">
                    <Search />
                  </el-icon>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="totalValue" label="总估值" width="120" sortable>
              <template #default="{ row }">
                {{ formatCurrency(row.totalValue) }}
              </template>
            </el-table-column>
            <el-table-column prop="createdAt" label="创建时间" width="180" sortable>
              <template #default="{ row }">
                {{ formatDateTime(row.createdAt) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100" sortable>
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button-group>
                  <el-button 
                    type="primary" 
                    text
                    size="small"
                    @click="viewEvaluation(row.id)"
                  >
                    查看
                  </el-button>
                  <el-button 
                    type="danger" 
                    text
                    size="small"
                    @click="deleteEvaluation(row.id)"
                    v-if="row.status === 'draft'"
                  >
                    删除
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 分页 -->
          <div class="pagination-container" v-if="filteredEvaluations.length > 0">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[5, 10, 20, 50]"
              :total="filteredEvaluations.length"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
          
          <!-- 空状态 -->
          <div v-if="filteredEvaluations.length === 0" class="empty-state">
            <el-empty description="未找到匹配的评估记录">
              <template #image>
                <el-icon :size="60" color="#909399">
                  <Search />
                </el-icon>
              </template>
              <p v-if="hospitalSearch">没有找到医院名称包含 "{{ hospitalSearch }}" 的评估记录</p>
              <p v-else-if="currentStatusFilter !== 'all'">没有找到状态为 "{{ getStatusText(currentStatusFilter) }}" 的评估记录</p>
              <p v-else>暂无评估数据</p>
              <div class="empty-actions">
                <el-button @click="clearAllFilters">清除所有筛选条件</el-button>
                <el-button type="primary" @click="refreshData">刷新数据</el-button>
              </div>
            </el-empty>
          </div>
        </el-card>

        <!-- 成本类别分布 -->
        <el-card class="category-distribution" shadow="never">
          <template #header>
            <h3><el-icon><PieChart /></el-icon> 成本类别分布</h3>
          </template>
          
          <div class="distribution-content">
            <div class="chart-container">
              <div class="chart-placeholder">
                <el-icon :size="60" color="#409EFF"><DataAnalysis /></el-icon>
                <p>成本分布图表（二期功能）</p>
              </div>
            </div>
            <div class="distribution-list">
              <div 
                v-for="category in categories" 
                :key="category.id"
                class="category-item"
              >
                <div class="category-info">
                  <span class="category-badge">{{ category.id }}</span>
                  <span class="category-name">{{ category.name }}</span>
                </div>
                <div class="category-stats">
                  <span class="category-value">{{ formatCurrency(category.value) }}</span>
                  <span class="category-percentage">{{ category.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右列：系统信息 -->
      <el-col :xs="24" :lg="8">
        <!-- 系统状态 -->
        <el-card class="system-status" shadow="never">
          <template #header>
            <h3><el-icon><Setting /></el-icon> 系统状态</h3>
          </template>
          
          <div class="status-list">
            <div class="status-item" v-for="item in systemStatus" :key="item.label">
              <div class="status-label">
                <el-icon :color="item.color"><component :is="item.icon" /></el-icon>
                <span>{{ item.label }}</span>
              </div>
              <div class="status-value">
                <el-tag :type="item.statusType" size="small">
                  {{ item.value }}
                </el-tag>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 快速操作 -->
        <el-card class="quick-actions" shadow="never">
          <template #header>
            <h3><el-icon><Operation /></el-icon> 快速操作</h3>
          </template>
          
          <div class="actions-grid">
            <el-button 
              type="primary" 
              class="action-btn" 
              @click="gotoWeightSetting"
            >
              <el-icon><Setting /></el-icon>
              权重设置
            </el-button>
            
            <el-button 
              class="action-btn"
              @click="initDemoData"
            >
              <el-icon><MagicStick /></el-icon>
              初始化演示数据
            </el-button>
            
            <el-button 
              class="action-btn"
              @click="exportSystemLogs"
            >
              <el-icon><Download /></el-icon>
              导出系统日志
            </el-button>
            
            <el-button 
              class="action-btn"
              @click="clearSystemCache"
            >
              <el-icon><Delete /></el-icon>
              清理缓存
            </el-button>
          </div>
        </el-card>

        <!-- 用户增长趋势 -->
        <el-card class="user-growth" shadow="never">
          <template #header>
            <h3><el-icon><User /></el-icon> 用户增长</h3>
          </template>
          
          <div class="growth-chart">
            <div class="chart-placeholder">
              <el-icon :size="60" color="#67C23A"><TrendCharts /></el-icon>
              <p>用户增长图表（二期功能）</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统公告 -->
    <el-card class="system-notice" shadow="never">
      <template #header>
        <h3><el-icon><Bell /></el-icon> 系统公告</h3>
      </template>
      
      <div class="notice-content">
        <el-timeline>
          <el-timeline-item
            v-for="notice in systemNotices"
            :key="notice.id"
            :timestamp="notice.time"
            :type="notice.type"
            :hollow="true"
          >
            <div class="notice-item">
              <h4>{{ notice.title }}</h4>
              <p>{{ notice.content }}</p>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Monitor, 
  User, 
  Document, 
  Money, 
  Clock,
  Refresh,
  PieChart,
  Setting,
  Operation,
  Download,
  Delete,
  Bell,
  MagicStick,
  DataAnalysis,
  TrendCharts,
  Search,
  Filter
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 搜索相关状态
const hospitalSearch = ref('')
const currentStatusFilter = ref('all')
const currentSort = ref({ prop: 'createdAt', order: 'descending' })
const currentPage = ref(1)
const pageSize = ref(5)

// 加载状态
const loading = reactive({
  evaluations: false,
  system: false
})

// 系统概览卡片数据
const overviewCards = ref([
  {
    title: '总用户数',
    value: '156',
    icon: 'User',
    color: '#409EFF',
    trend: '+12%'
  },
  {
    title: '总评估数',
    value: '234',
    icon: 'Document',
    color: '#67C23A',
    trend: '+8%'
  },
  {
    title: '总估值',
    value: '¥ 1,256万',
    icon: 'Money',
    color: '#E6A23C',
    trend: '+15%'
  },
  {
    title: '平均估值',
    value: '¥ 53.7万',
    icon: 'TrendCharts',
    color: '#F56C6C',
    trend: '+5%'
  }
])

// 所有评估数据
const allEvaluations = ref([
  {
    id: '1',
    name: '2023年度数据资产评估',
    hospital: '北京协和医院',
    totalValue: 1250000,
    createdAt: '2023-12-15T10:30:00',
    status: 'completed'
  },
  {
    id: '2',
    name: '急诊科数据专项评估',
    hospital: '上海瑞金医院',
    totalValue: 850000,
    createdAt: '2023-11-20T14:15:00',
    status: 'completed'
  },
  {
    id: '3',
    name: '医疗影像数据评估',
    hospital: '广州中山医院',
    totalValue: 2100000,
    createdAt: '2023-10-10T09:45:00',
    status: 'completed'
  },
  {
    id: '4',
    name: '2024年Q1数据资产盘点',
    hospital: '北京协和医院',
    totalValue: 980000,
    createdAt: '2024-03-01T11:20:00',
    status: 'processing'
  },
  {
    id: '5',
    name: '门诊数据价值分析',
    hospital: '上海华山医院',
    totalValue: 670000,
    createdAt: '2024-02-15T16:45:00',
    status: 'completed'
  },
  {
    id: '6',
    name: '住院部数据质量评估',
    hospital: '北京协和医院',
    totalValue: 320000,
    createdAt: '2024-01-20T09:30:00',
    status: 'completed'
  },
  {
    id: '7',
    name: '临床研究数据资产评估',
    hospital: '上海瑞金医院',
    totalValue: 540000,
    createdAt: '2024-01-15T14:20:00',
    status: 'completed'
  },
  {
    id: '8',
    name: '医院运营数据分析评估',
    hospital: '广州中山医院',
    totalValue: 890000,
    createdAt: '2023-12-28T16:00:00',
    status: 'completed'
  },
  {
    id: '9',
    name: '药品管理数据价值评估',
    hospital: '北京协和医院',
    totalValue: 410000,
    createdAt: '2023-12-10T10:15:00',
    status: 'draft'
  },
  {
    id: '10',
    name: '医疗设备数据价值评估',
    hospital: '上海华山医院',
    totalValue: 720000,
    createdAt: '2023-11-25T15:30:00',
    status: 'completed'
  }
])

// 成本类别分布
const categories = ref([
  { id: 1, name: '数据战略与治理成本', value: 50000, percentage: 4.0 },
  { id: 2, name: '数据获取与采集成本', value: 120000, percentage: 9.6 },
  { id: 3, name: '数据存储与备份成本', value: 80000, percentage: 6.4 },
  { id: 4, name: '数据处理与加工成本', value: 150000, percentage: 12.0 },
  { id: 5, name: '数据应用与分析成本', value: 200000, percentage: 16.0 },
  { id: 6, name: '数据流通与共享成本', value: 30000, percentage: 2.4 },
  { id: 7, name: '数据安全、隐私与合规成本', value: 60000, percentage: 4.8 },
  { id: 8, name: '数据归档与销毁成本', value: 25000, percentage: 2.0 },
  { id: 9, name: '数据全流程人力成本', value: 180000, percentage: 14.4 }
])

// 系统状态
const systemStatus = ref([
  { label: '后端服务', value: '运行正常', icon: 'Monitor', color: '#67C23A', statusType: 'success' },
  { label: '数据库', value: '连接正常', icon: 'DataBoard', color: '#67C23A', statusType: 'success' },
  { label: 'API响应', value: '平均 120ms', icon: 'Timer', color: '#E6A23C', statusType: 'warning' },
  { label: '系统负载', value: '42%', icon: 'Cpu', color: '#67C23A', statusType: 'success' },
  { label: '磁盘空间', value: '78% 已用', icon: 'HardDisk', color: '#F56C6C', statusType: 'danger' },
  { label: '最后备份', value: '2024-03-10', icon: 'Finished', color: '#67C23A', statusType: 'success' }
])

// 系统公告
const systemNotices = ref([
  {
    id: 1,
    title: '系统升级通知',
    content: '计划于本周末进行系统维护，预计停机2小时。',
    time: '2024-03-15 10:00',
    type: 'primary'
  },
  {
    id: 2,
    title: '新功能上线',
    content: '数据可视化功能已上线，支持雷达图和柱状图展示。',
    time: '2024-03-10 14:30',
    type: 'success'
  },
  {
    id: 3,
    title: '权重设置更新',
    content: '管理员现在可以动态调整9大类指标的权重系数。',
    time: '2024-03-05 09:15',
    type: 'warning'
  }
])

// 计算属性
// 过滤后的评估数据
const filteredEvaluations = computed(() => {
  let filtered = [...allEvaluations.value]
  
  // 按医院名称搜索
  if (hospitalSearch.value) {
    const searchTerm = hospitalSearch.value.toLowerCase()
    filtered = filtered.filter(item => 
      item.hospital.toLowerCase().includes(searchTerm)
    )
  }
  
  // 按状态筛选
  if (currentStatusFilter.value !== 'all') {
    filtered = filtered.filter(item => item.status === currentStatusFilter.value)
  }
  
  // 排序
  if (currentSort.value.prop) {
    const prop = currentSort.value.prop
    const order = currentSort.value.order
    
    filtered.sort((a, b) => {
      let aVal = a[prop]
      let bVal = b[prop]
      
      // 处理特殊字段
      if (prop === 'createdAt') {
        aVal = new Date(aVal).getTime()
        bVal = new Date(bVal).getTime()
      }
      
      if (aVal < bVal) return order === 'ascending' ? -1 : 1
      if (aVal > bVal) return order === 'ascending' ? 1 : -1
      return 0
    })
  }
  
  return filtered
})

// 分页后的数据
const paginatedEvaluations = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredEvaluations.value.slice(start, end)
})

// 是否显示搜索信息
const showSearchInfo = computed(() => {
  return hospitalSearch.value || currentStatusFilter.value !== 'all'
})

// 格式化货币
const formatCurrency = (value) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value || 0)
}

// 格式化日期时间
const formatDateTime = (dateString) => {
  if (!dateString) return '未知日期'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).replace(/\//g, '/')
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'draft': 'info',
    'completed': 'success',
    'processing': 'warning',
    'failed': 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    'draft': '草稿',
    'completed': '已完成',
    'processing': '计算中',
    'failed': '计算失败'
  }
  return texts[status] || '未知'
}

// 查看评估详情
const viewEvaluation = (id) => {
  router.push(`/result/${id}`)
}

// 删除评估
const deleteEvaluation = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条评估记录吗？此操作不可恢复。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    const index = allEvaluations.value.findIndex(item => item.id === id)
    if (index !== -1) {
      allEvaluations.value.splice(index, 1)
      ElMessage.success('评估记录已删除')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + error.message)
    }
  }
}

// 刷新数据
const refreshData = async () => {
  loading.evaluations = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    loading.evaluations = false
  }
}

// 处理医院搜索
const handleHospitalSearch = () => {
  currentPage.value = 1 // 重置到第一页
}

// 清除医院搜索
const clearHospitalSearch = () => {
  hospitalSearch.value = ''
  currentPage.value = 1
}

// 处理高级筛选
const handleAdvancedFilter = (command) => {
  currentStatusFilter.value = command
  currentPage.value = 1
}

// 清除状态筛选
const clearStatusFilter = () => {
  currentStatusFilter.value = 'all'
  currentPage.value = 1
}

// 清除所有筛选条件
const clearAllFilters = () => {
  hospitalSearch.value = ''
  currentStatusFilter.value = 'all'
  currentPage.value = 1
}

// 处理排序变化
const handleSortChange = ({ prop, order }) => {
  currentSort.value = { prop, order }
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

// 处理当前页变化
const handleCurrentChange = (val) => {
  currentPage.value = val
}

// 处理搜索清空
const handleSearchClear = () => {
  currentPage.value = 1
}

// 跳转到权重设置
const gotoWeightSetting = () => {
  router.push('/admin/weights')
}

// 初始化演示数据
const initDemoData = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要初始化演示数据吗？这将创建测试用户和评估数据。',
      '初始化演示数据',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    ElMessage.success('演示数据初始化成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('初始化失败: ' + error.message)
    }
  }
}

// 导出系统日志
const exportSystemLogs = async () => {
  try {
    ElMessage.info('系统日志导出功能开发中...')
  } catch (error) {
    ElMessage.error('导出失败: ' + error.message)
  }
}

// 清理系统缓存
const clearSystemCache = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清理系统缓存吗？这可能会影响系统性能。',
      '清理缓存',
      {
        confirmButtonText: '确定清理',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    ElMessage.success('系统缓存清理完成')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清理失败: ' + error.message)
    }
  }
}

// 组件挂载时加载数据
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e6e6e6;
}

.page-header h1 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 28px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-header .subtitle {
  margin: 0;
  color: #666;
  font-size: 16px;
}

/* 概览卡片样式 */
.overview-cards {
  margin-bottom: 30px;
}

.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  line-height: 1.2;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stat-label {
  font-size: 14px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 内容区域 */
.dashboard-content {
  margin-bottom: 30px;
}

/* 卡片公共样式 */
.recent-evaluations,
.category-distribution,
.system-status,
.quick-actions,
.user-growth,
.system-notice {
  margin-bottom: 20px;
  border-radius: 8px;
  border: 1px solid #e6e6e6;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
  margin-bottom: 16px;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 搜索和操作行 */
.search-actions-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 10px;
}

.search-input {
  flex: 1;
  max-width: 300px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

/* 搜索信息 */
.search-info {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.mr-2 {
  margin-right: 8px;
}

/* 表头样式 */
.column-header {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 评估链接 */
.evaluation-link {
  color: #409EFF;
  text-decoration: none;
  transition: color 0.3s;
}

.evaluation-link:hover {
  color: #3375b9;
  text-decoration: underline;
}

/* 分页容器 */
.pagination-container {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: center;
}

/* 空状态 */
.empty-state {
  padding: 40px 0;
  text-align: center;
}

.empty-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* 成本分布 */
.distribution-content {
  display: flex;
  gap: 30px;
}

.chart-container {
  flex: 1;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.chart-placeholder {
  text-align: center;
  color: #999;
}

.chart-placeholder p {
  margin-top: 10px;
  font-size: 14px;
}

.distribution-list {
  flex: 1;
  max-width: 300px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.category-item:last-child {
  border-bottom: none;
}

.category-info {
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
  background-color: #409EFF;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
}

.category-name {
  font-size: 14px;
  color: #333;
}

.category-stats {
  text-align: right;
}

.category-value {
  display: block;
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.category-percentage {
  display: block;
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

/* 系统状态 */
.status-list {
  padding: 10px 0;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #333;
}

.status-value {
  font-weight: 500;
}

/* 快速操作 */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-btn {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  white-space: normal;
  line-height: 1.4;
}

.action-btn .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

/* 用户增长 */
.growth-chart {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  border-radius: 8px;
}

/* 系统公告 */
.notice-content {
  padding: 10px 0;
}

.notice-item h4 {
  margin: 0 0 6px 0;
  font-size: 16px;
  color: #333;
}

.notice-item p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .distribution-content {
    flex-direction: column;
  }
  
  .distribution-list {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 10px;
  }
  
  .overview-cards .el-col {
    margin-bottom: 15px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .search-actions-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    max-width: 100%;
  }
  
  .action-buttons {
    justify-content: flex-start;
  }
}
</style>