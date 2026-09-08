<!-- frontend/src/views/ResultDisplay.vue -->
<template>
  <div class="result-container" v-loading="loading">
    <!-- 主报告卡片 -->
    <el-card ref="reportCardRef" class="result-card" v-if="!loading && evaluationResult">
      <!-- 报告头部 -->
      <div class="report-header">
        <div class="header-left">
          <h1>医疗数据资产价值评估报告</h1>
          <div class="header-info">
            <span class="report-id">报告编号: {{ evaluationResult.reportId || 'N/A' }}</span>
            <el-tag 
              :type="getStatusType(evaluationResult.status)" 
              size="small"
              class="status-tag"
            >
              {{ getStatusText(evaluationResult.status) }}
            </el-tag>
          </div>
        </div>
        <div class="header-right">
          <div class="hospital-info">
            <h3>{{ evaluationResult.hospital || '未指定医院' }}</h3>
            <p class="evaluation-time">评估时间: {{ formatDate(evaluationResult.createdAt) }}</p>
            <p class="evaluation-name" v-if="evaluationResult.name">评估名称: {{ evaluationResult.name }}</p>
          </div>
        </div>
      </div>

      <!-- 总估值卡片 -->
      <div class="total-value-section">
        <el-card class="total-card" shadow="hover">
          <div class="total-content">
            <div class="total-label">数据资产总估值</div>
            <div class="total-amount">{{ formatCurrency(evaluationResult.totalValue) }}</div>
            <div class="total-description">
              基于9大类成本指标直接相加 | 评估有效期至: {{ getExpiryDate(evaluationResult.createdAt) }}
            </div>
            <div class="calculation-method">
              <el-tooltip 
                content="总估值 = Σ(各项成本金额)，采用直接相加的计算方法"
                placement="top"
              >
                <el-icon><InfoFilled /></el-icon>
                <span>计算方法: 直接相加</span>
              </el-tooltip>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 成本构成分析 -->
      <div class="cost-breakdown-section">
        <h2><el-icon><PieChart /></el-icon> 成本构成分析</h2>
        <div class="breakdown-grid">
          <el-card 
            v-for="category in evaluationResult.categories" 
            :key="category.id"
            class="category-card"
            :data-category="category.id"
            shadow="never"
            :style="{ borderLeft: `4px solid ${getCategoryColor(category.id)}` }"
            @click="focusCategory(category.id)"
          >
            <template #header>
              <div class="category-header">
                <span class="category-number">{{ category.id }}</span>
                <h3>{{ category.name }}</h3>
              </div>
            </template>
            <div class="category-content">
              <div class="category-value-row">
                <div class="category-value">{{ formatCurrency(category.value) }}</div>
                <div class="category-percentage" :style="{ color: getCategoryColor(category.id) }">
                  占比: {{ calculatePercentage(category.value) }}%
                </div>
              </div>
              <el-progress 
                :percentage="calculatePercentage(category.value)" 
                :color="getCategoryColor(category.id)"
                :show-text="false"
              />
              <div class="category-details" v-if="category.details && category.details.length > 0">
                <div 
                  v-for="detail in category.details.slice(0, 3)" 
                  :key="detail.itemName"
                  class="detail-item"
                >
                  <span class="detail-name">{{ detail.itemName }}</span>
                  <span class="detail-value">{{ formatCurrency(detail.amount) }}</span>
                </div>
                <div v-if="category.details.length > 3" class="more-details">
                  <el-button link size="small" @click.stop="showCategoryDetails(category)">
                    查看更多 {{ category.details.length - 3 }} 项
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 详细数据表格 -->
      <div class="detailed-table-section">
        <div class="table-header">
          <h2><el-icon><Document /></el-icon> 详细成本明细</h2>
          <div class="table-actions">
            <el-button :icon="Download" @click="exportToExcel" size="small">导出Excel</el-button>
            <el-button :icon="CopyDocument" @click="copyTableData" size="small">复制数据</el-button>
          </div>
        </div>
        
        <p class="table-scroll-hint">左右滑动表格可查看全部内容和操作</p>
      <el-table
          :data="evaluationResult.details" 
          stripe
          border
          style="width: 100%"
          :row-class-name="tableRowClassName"
          @row-click="handleRowClick"
        >
          <el-table-column type="index" label="序号" width="60" align="center" :fixed="!isMobile" />
          
          <el-table-column prop="categoryName" label="成本类别" width="180" :fixed="!isMobile">
            <template #default="{ row }">
              <div class="category-cell">
                <span 
                  class="category-color-dot" 
                  :style="{ backgroundColor: getCategoryColor(row.categoryId) }"
                ></span>
                <span>{{ row.categoryName }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="itemName" label="成本项目" width="250">
            <template #default="{ row }">
              <div class="item-name-cell">
                <span>{{ row.itemName }}</span>
                <el-tooltip 
                  v-if="row.description" 
                  :content="row.description" 
                  placement="top"
                >
                  <el-icon class="item-hint"><QuestionFilled /></el-icon>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="amount" label="金额" width="150" sortable>
            <template #default="{ row }">
              <div class="amount-cell">
                {{ formatCurrency(row.amount) }}
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="percentage" label="占比" width="100" sortable>
            <template #default="{ row }">
              <div class="percentage-cell">
                {{ row.percentage.toFixed(2) }}%
                <el-progress 
                  :percentage="row.percentage" 
                  :show-text="false" 
                  :stroke-width="6"
                  style="margin-top: 5px;"
                />
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="120" :fixed="isMobile ? false : 'right'">
            <template #default="{ row }">
              <el-button 
                link 
                size="small" 
                @click.stop="viewItemDetail(row)"
              >
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <table class="print-table">
          <thead><tr><th>成本类别</th><th>成本项目</th><th>金额（元）</th><th>占比</th></tr></thead>
          <tbody><tr v-for="(item, index) in evaluationResult.details" :key="index"><td>{{ item.categoryName }}</td><td>{{ item.itemName }}</td><td>{{ formatCurrency(item.amount) }}</td><td>{{ item.percentage }}%</td></tr></tbody>
        </table>
        
        <div class="table-summary">
          <div class="summary-item">
            <span class="summary-label">总项目数:</span>
            <span class="summary-value">{{ evaluationResult.details?.length || 0 }} 项</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">总金额:</span>
            <span class="summary-value">
              {{ formatCurrency(evaluationResult.totalValue) }}
            </span>
          </div>
          <div class="summary-item">
            <span class="summary-label">最大单项:</span>
            <span class="summary-value">
              {{ getMaxItem()?.itemName || '-' }}
              ({{ formatCurrency(getMaxItem()?.amount || 0) }})
            </span>
          </div>
        </div>
      </div>

      <!-- 专家建议与说明 -->
      <div class="expert-advice-section">
        <h2><el-icon><ChatLineRound /></el-icon> 计算说明与建议</h2>
        <el-card class="advice-card">
          <div class="advice-content">
            <div class="advice-item">
              <el-icon color="#409EFF"><InfoFilled /></el-icon>
              <div class="advice-text">
                <h4>计算方法说明</h4>
                <p>本次评估采用<b>直接相加法</b>计算总估值，即：将9大类成本下的所有细项金额直接求和。这是最基础、最透明的计算方式，便于理解和核对。</p>
              </div>
            </div>
            <div class="advice-item">
              <el-icon color="#67C23A"><ChatLineRound /></el-icon>
              <div class="advice-text">
                <h4>结果解读建议</h4>
                <p>重点关注<b>占比最高</b>的成本类别，这代表了您医院在数据资产管理中的主要投入方向。可结合"成本构成分析"中的百分比数据进行深入分析。</p>
              </div>
            </div>
            <div class="advice-item">
              <el-icon color="#E6A23C"><Warning /></el-icon>
              <div class="advice-text">
                <h4>注意事项</h4>
                <p>直接相加法未考虑不同成本项对数据资产价值的差异化贡献。如需更精确的评估，可联系管理员启用加权计算功能。</p>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 操作按钮区域 -->
      <div class="action-buttons">
        <el-button-group class="primary-actions">
          <el-button 
            type="primary" 
            :icon="Printer" 
            @click="printReport"
            size="large"
          >
            打印报告
          </el-button>
          <el-button 
            type="success" 
            :icon="Download" 
            @click="exportPDF"
            size="large"
          >
            导出PDF报告
          </el-button>
          <el-button 
            type="warning" 
            :icon="Share" 
            @click="shareReport"
            size="large"
          >
            分享报告
          </el-button>
        </el-button-group>
        
        <el-button-group class="secondary-actions">
          <el-button 
            :icon="Edit" 
            @click="editEvaluation"
            size="large"
          >
            重新编辑
          </el-button>
          <el-button 
            :icon="CopyDocument" 
            @click="duplicateEvaluation"
            size="large"
          >
            复制评估
          </el-button>
          <el-button 
            :icon="Delete" 
            @click="deleteEvaluation"
            size="large"
            v-if="evaluationResult.status === 'draft'"
          >
            删除草稿
          </el-button>
          <el-button 
            :icon="Back" 
            @click="goBack"
            size="large"
          >
            返回列表
          </el-button>
        </el-button-group>
      </div>

      <!-- 报告页脚 -->
      <div class="report-footer">
        <p class="footer-disclaimer">
          <el-icon><Warning /></el-icon>
          免责声明：本报告基于您提供的数据，采用直接相加法进行计算，结果仅供参考。实际数据资产价值可能因市场变化、技术发展等因素而有所不同。
        </p>
        <p class="footer-contact">
          如有疑问或需要专业咨询，请联系: contact@datavaluecal.com | 400-xxx-xxxx
        </p>
        <p class="footer-generated">
          报告生成时间: {{ new Date().toLocaleString('zh-CN') }} | 系统版本: V1.0 | 计算方式: 直接相加
        </p>
      </div>
    </el-card>

    <!-- 加载状态 -->
    <div v-else-if="loading" class="loading-state">
      <el-skeleton :rows="10" animated />
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <el-empty description="未找到评估结果">
        <template #image>
          <el-icon :size="100" color="#909399"><Files /></el-icon>
        </template>
        <p>可能的原因：评估已被删除、ID不正确或您没有查看权限</p>
        <div class="empty-actions">
          <el-button type="primary" @click="goBack">返回评估列表</el-button>
          <el-button @click="$router.push('/data-input')">创建新评估</el-button>
        </div>
      </el-empty>
    </div>

    <!-- 类别详情对话框 -->
    <el-dialog
      v-model="showCategoryDialog"
      :title="selectedCategory ? selectedCategory.name + ' - 详细成本' : ''"
      width="600px"
    >
      <el-table
        :data="selectedCategory?.details || []" 
        size="small"
        stripe
      >
        <el-table-column prop="itemName" label="成本项目" />
        <el-table-column prop="amount" label="金额" width="120">
          <template #default="{ row }">{{ formatCurrency(row.amount) }}</template>
        </el-table-column>
        <el-table-column prop="percentage" label="占比" width="100">
          <template #default="{ row }">{{ row.percentage.toFixed(2) }}%</template>
        </el-table-column>
      </el-table>
      <template #footer>
        <el-button @click="showCategoryDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 项目详情对话框 -->
    <el-dialog
      v-model="showItemDialog"
      :title="selectedItem ? selectedItem.itemName + ' - 详情' : ''"
      width="500px"
    >
      <div v-if="selectedItem" class="item-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="所属类别">
            {{ selectedItem.categoryName }}
          </el-descriptions-item>
          <el-descriptions-item label="金额">
            {{ formatCurrency(selectedItem.amount) }}
          </el-descriptions-item>
          <el-descriptions-item label="占总比">
            {{ selectedItem.percentage.toFixed(2) }}%
          </el-descriptions-item>
        </el-descriptions>
        <div class="item-description" v-if="selectedItem.description">
          <h4>项目说明:</h4>
          <p>{{ selectedItem.description }}</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="showItemDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 分享对话框：仅复制链接 -->
    <el-dialog
      v-model="showShareDialog"
      title="复制报告访问链接"
      width="400px"
    >
      <p>此链接需要登录，仅报告所属账号或管理员可查看。向其他人提供报告请导出 PDF。</p>
      <div class="share-link" v-if="shareLink">
        <el-input v-model="shareLink" readonly>
          <template #append>
            <el-button :icon="CopyDocument" @click="copyToClipboard(shareLink)">复制链接</el-button>
          </template>
        </el-input>
      </div>
      <template #footer>
        <el-button @click="showShareDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { csvCell, copyText } from '@/utils/export'
import { useResponsive } from '@/utils/responsive'
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  getEvaluationResultAPI, 
  deleteEvaluationAPI,
  duplicateEvaluationAPI 
} from '@/api/evaluation'
import { 
  Printer, 
  Download, 
  Edit, 
  Back,
  Share,
  Delete,
  CopyDocument,
  InfoFilled,
  QuestionFilled,
  Warning,
  ChatLineRound,
  Document,
  Files,
  PieChart
} from '@element-plus/icons-vue'
import { 
  ElMessage, 
  ElLoading, 
  ElMessageBox
} from 'element-plus'

const { isMobile } = useResponsive()

const route = useRoute()
const router = useRouter()

// 状态管理
const loading = ref(true)
const evaluationResult = ref(null)
const showCategoryDialog = ref(false)
const showItemDialog = ref(false)
const showShareDialog = ref(false)
const selectedCategory = ref(null)
const selectedItem = ref(null)
const shareLink = ref('')

// 类别颜色映射
const categoryColors = [
  '#409EFF', // 1. 数据战略与治理成本
  '#67C23A', // 2. 数据获取与采集成本
  '#E6A23C', // 3. 数据存储与备份成本
  '#F56C6C', // 4. 数据处理与加工成本
  '#909399', // 5. 数据应用与分析成本
  '#FF85C0', // 6. 数据流通与共享成本
  '#9B59B6', // 7. 数据安全、隐私与合规成本
  '#1ABC9C', // 8. 数据归档与销毁成本
  '#2C3E50'  // 9. 数据全流程人力成本
]


const loadEvaluationResult = async () => {
  loading.value = true
  const loadingInstance = ElLoading.service({ 
    lock: true, 
    text: '加载评估结果中...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  try {
    const id = route.params.id
    if (!id) {
      ElMessage.error('无效的评估ID')
      router.push('/personal-center')
      return
    }

    // 调用API获取评估结果
    const response = await getEvaluationResultAPI(id)
    
    if (response.data) {
      evaluationResult.value = response.data
    } else {
      throw new Error('报告数据为空')
    }
  } catch (error) {
    evaluationResult.value = null
    ElMessage.error('加载评估结果失败: ' + (error.response?.data?.detail || error.message || '网络错误'))
  } finally {
    loading.value = false
    loadingInstance.close()
  }
}

onMounted(loadEvaluationResult)
watch(() => route.params.id, loadEvaluationResult)

// 格式化货币
const formatCurrency = (value) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value || 0)
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知日期'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取类别颜色
const getCategoryColor = (categoryId) => {
  return categoryColors[categoryId - 1] || '#909399'
}

// 计算百分比
const calculatePercentage = (value) => {
  if (!evaluationResult.value || !evaluationResult.value.totalValue) return 0
  return Number(((value / evaluationResult.value.totalValue) * 100).toFixed(2))
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

// 获取过期日期（评估后1年）
const getExpiryDate = (createdAt) => {
  if (!createdAt) return '未设置'
  const date = new Date(createdAt)
  date.setFullYear(date.getFullYear() + 1)
  return date.toLocaleDateString('zh-CN')
}

// 表格行类名
const tableRowClassName = ({ row }) => {
  if (row.amount > evaluationResult.value?.totalValue * 0.1) {
    return 'highlight-row'
  }
  return ''
}

// 处理行点击
const handleRowClick = (row) => {
  viewItemDetail(row)
}

// 查看项目详情
const viewItemDetail = (item) => {
  selectedItem.value = item
  showItemDialog.value = true
}

// 获取最大金额项目
const getMaxItem = () => {
  if (!evaluationResult.value?.details) return null
  return evaluationResult.value.details.reduce((max, item) => {
    return item.amount > max.amount ? item : max
  }, { amount: 0 })
}

// 聚焦类别
const focusCategory = (categoryId) => {
  const element = document.querySelector(`.category-card[data-category="${categoryId}"]`)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    element.classList.add('focus-animation')
    setTimeout(() => {
      element.classList.remove('focus-animation')
    }, 1000)
  }
}

// 显示类别详情
const showCategoryDetails = (category) => {
  selectedCategory.value = category
  showCategoryDialog.value = true
}

// 打印报告（浏览器打印，可另存为 PDF）
const printReport = () => {
  window.print()
}

// 导出 PDF：打开打印对话框，用户选择“另存为 PDF”
const exportPDF = () => {
  ElMessage.info('请在弹出的打印窗口中选择“另存为 PDF”或目标打印机')
  window.print()
}

// 分享报告
const shareReport = () => {
  shareLink.value = window.location.href
  showShareDialog.value = true
}

// 导出到 Excel（CSV，UTF-8 带 BOM，Excel 可直接打开）
const exportToExcel = () => {
  const r = evaluationResult.value
  if (!r) {
    ElMessage.warning('暂无数据可导出')
    return
  }
  const rows = []
  rows.push(['医疗数据资产价值评估报告'])
  rows.push(['报告编号', r.reportId || ''])
  rows.push(['评估名称', r.name || ''])
  rows.push(['医院', r.hospital || ''])
  rows.push(['评估时间', r.createdAt ? new Date(r.createdAt).toLocaleString('zh-CN') : ''])
  rows.push(['总估值（元）', r.totalValue ?? ''])
  rows.push([])
  rows.push(['成本类别汇总'])
  rows.push(['序号', '类别名称', '金额（元）', '占比(%)'])
  ;(r.categories || []).forEach((c, i) => {
    rows.push([i + 1, c.name, c.value ?? '', (r.totalValue ? ((c.value / r.totalValue) * 100).toFixed(2) : '')])
  })
  rows.push([])
  rows.push(['详细成本明细'])
  rows.push(['序号', '成本类别', '成本项目', '金额（元）', '占比(%)'])
  ;(r.details || []).forEach((d, i) => {
    rows.push([i + 1, d.categoryName, d.itemName, d.amount ?? '', (d.percentage ?? '').toString()])
  })
  const BOM = '\uFEFF'
  const csv = BOM + rows.map(row => row.map(csvCell).join(',')).join('\r\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `评估报告_${(r.name || r.reportId || 'export').replace(/[/\\?*:]/g, '_')}_${Date.now()}.csv`
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('已导出为 CSV，可用 Excel 打开')
}

// 复制表格数据
const copyTableData = () => {
  if (!evaluationResult.value?.details) {
    ElMessage.warning('没有可复制的数据')
    return
  }
  
  const headers = ['类别', '项目', '金额', '占比']
  const data = evaluationResult.value.details.map(item => [
    item.categoryName,
    item.itemName,
    formatCurrency(item.amount),
    `${item.percentage.toFixed(2)}%`
  ])
  
  const text = [headers, ...data]
    .map(row => row.join('\t'))
    .join('\n')
  
  copyText(text)
    .then(() => ElMessage.success('表格数据已复制到剪贴板'))
    .catch(() => ElMessage.error('复制失败'))
}

// 复制到剪贴板
const copyToClipboard = (text) => {
  copyText(text)
    .then(() => ElMessage.success('链接已复制到剪贴板'))
    .catch(() => ElMessage.error('复制失败'))
}

// 重新编辑
const editEvaluation = () => {
  router.push(`/data-input?edit=${route.params.id}`)
}

// 复制评估
const duplicateEvaluation = async () => {
  try {
    const response = await duplicateEvaluationAPI(route.params.id)
    if (response.data && response.data.id) {
      ElMessage.success('评估复制成功')
      router.push(`/result/${response.data.id}`)
    }
  } catch (error) {
    ElMessage.error('复制失败: ' + (error.response?.data?.message || '网络错误'))
  }
}

// 删除评估
const deleteEvaluation = async () => {
  try {
    await ElMessageBox.confirm('确定要删除此评估吗？此操作不可恢复。', '警告', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    })
    
    await deleteEvaluationAPI(route.params.id)
    ElMessage.success('评估已删除')
    router.push('/personal-center')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败: ' + (error.response?.data?.message || '网络错误'))
    }
  }
}

// 返回上一页
const goBack = () => {
  router.push('/personal-center')
}

</script>

<style scoped>
.result-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.result-card {
  max-width: 1400px;
  margin: 0 auto;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 报告头部样式 */
.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 0;
  border-bottom: 1px solid #e6e6e6;
  margin-bottom: 30px;
}

.header-left h1 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 28px;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.report-id {
  color: #666;
  font-size: 14px;
}

.status-tag {
  font-size: 12px;
}

.hospital-info h3 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 18px;
  text-align: right;
}

.evaluation-time, .evaluation-name {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
  text-align: right;
}

/* 总估值卡片样式 */
.total-value-section {
  margin: 30px 0;
}

.total-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.total-content {
  padding: 30px;
  text-align: center;
}

.total-label {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 10px;
}

.total-amount {
  font-size: 48px;
  font-weight: bold;
  margin: 20px 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.total-description {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 15px;
}

.calculation-method {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  cursor: help;
}

.calculation-method:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 成本构成分析样式 */
.cost-breakdown-section h2 {
  color: #2c3e50;
  margin: 40px 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.breakdown-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.category-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e6e6e6;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.category-card.focus-animation {
  animation: pulse 1s;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(64, 158, 255, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(64, 158, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(64, 158, 255, 0); }
}

.category-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-number {
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

.category-header h3 {
  margin: 0;
  flex: 1;
  font-size: 16px;
  color: #333;
}

.category-content {
  padding: 15px 0;
}

.category-value-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.category-value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.category-percentage {
  font-size: 14px;
  font-weight: bold;
}

.category-details {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  font-size: 12px;
}

.detail-name {
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 70%;
}

.detail-value {
  color: #333;
  font-weight: 500;
}

.more-details {
  text-align: center;
  padding-top: 5px;
}

/* 详细表格样式 */
.detailed-table-section {
  margin: 40px 0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h2 {
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.category-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-color-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.item-name-cell {
  display: flex;
  align-items: center;
  gap: 5px;
}

.item-hint {
  color: #999;
  cursor: help;
}

.amount-cell {
  font-weight: 500;
  color: #333;
}

.percentage-cell {
  font-weight: 500;
}

.table-summary {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e6e6e6;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.summary-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.summary-value {
  font-weight: bold;
  color: #333;
}

/* 专家建议样式 */
.expert-advice-section h2 {
  color: #2c3e50;
  margin: 40px 0 20px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.advice-card {
  border: 1px solid #e6e6e6;
}

.advice-content {
  padding: 20px;
}

.advice-item {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.advice-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.advice-item .el-icon {
  font-size: 20px;
  margin-top: 3px;
  flex-shrink: 0;
}

.advice-text h4 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
}

.advice-text p {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.advice-actions {
  margin-top: 10px;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 40px 0;
  padding: 30px 0;
  border-top: 1px solid #e6e6e6;
  border-bottom: 1px solid #e6e6e6;
}

.primary-actions, .secondary-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

/* 报告页脚样式 */
.report-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e6e6e6;
  text-align: center;
  color: #666;
  font-size: 12px;
}

.footer-disclaimer {
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.footer-contact, .footer-generated {
  margin: 5px 0;
}

/* 加载状态样式 */
.loading-state {
  padding: 50px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 空状态样式 */
.empty-state {
  padding: 100px 20px;
  text-align: center;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.empty-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

/* 分享对话框样式 */
.share-link {
  margin: 0;
}

/* 项目详情对话框样式 */
.item-detail {
  padding: 10px 0;
}

.item-description {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.item-description h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.item-description p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .report-header {
    flex-direction: column;
    gap: 20px;
  }
  
  .hospital-info {
    text-align: left;
  }
  
  .hospital-info h3,
  .evaluation-time,
  .evaluation-name {
    text-align: left;
  }
  
  .total-amount {
    font-size: 36px;
  }
  
  .breakdown-grid {
    grid-template-columns: 1fr;
  }
  
  .primary-actions,
  .secondary-actions {
    flex-direction: column;
  }
  
  .primary-actions .el-button,
  .secondary-actions .el-button {
    width: 100%;
  }
  
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .table-actions {
    width: 100%;
    justify-content: flex-start;
  }
}

</style>

<style>
.print-table { display: none; }
@media print {
  body * { visibility: hidden; }
  .result-container, .result-container * { visibility: visible; }
  .result-container { position: absolute; left: 0; top: 0; width: 100%; padding: 0 !important; background: white; }
  .result-card { box-shadow: none !important; border: 0; }
  .result-container .primary-actions, .result-container .secondary-actions,
  .result-container .table-actions, .result-container .table-scroll-hint,
  .result-container .detailed-table-section .el-table, .el-overlay { display: none !important; }
  .print-table { display: table; width: 100%; border-collapse: collapse; font-size: 10pt; }
  .print-table th, .print-table td { border: 1px solid #999; padding: 6px; overflow-wrap: anywhere; }
  .print-table tr { break-inside: avoid; }
}
/* 全局表格样式 */
.highlight-row {
  background-color: #f0f9ff !important;
}

.highlight-row:hover > td {
  background-color: #e8f4ff !important;
}
</style>