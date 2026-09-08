<template>
  <div class="admin-evaluations">
    <div class="page-header">
      <h1>评估管理</h1>
      <p class="subtitle">查看、编辑、删除全部评估记录</p>
    </div>

    <el-card shadow="never" class="table-card">
      <template #header>
        <div class="card-header">
          <h3>评估列表</h3>
          <div class="header-actions">
            <el-input
              v-model="keyword"
              placeholder="按名称搜索"
              clearable
              style="width: 200px"
              @keyup.enter="fetchList"
            >
              <template #prefix><el-icon><Search /></el-icon></template>
            </el-input>
            <el-select v-model="statusFilter" placeholder="状态" clearable style="width: 120px" @change="fetchList">
              <el-option label="全部" value="" />
              <el-option label="已完成" value="completed" />
              <el-option label="计算中" value="processing" />
              <el-option label="草稿" value="draft" />
              <el-option label="失败" value="failed" />
            </el-select>
            <el-button type="primary" @click="fetchList"><el-icon><Refresh /></el-icon> 刷新</el-button>
            <el-button @click="$router.push('/data-input')"><el-icon><Plus /></el-icon> 新建评估</el-button>
          </div>
        </div>
      </template>

      <p class="table-scroll-hint">左右滑动表格可查看全部内容和操作</p>
      <el-table
        :data="list"
        v-loading="loading"
        stripe
        style="width: 100%"
        :default-sort="{ prop: 'createdAt', order: 'descending' }"
      >
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="评估名称" min-width="180">
          <template #default="{ row }">
            <router-link :to="`/result/${row.id}`" class="link">{{ row.name }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="备注" width="140" show-overflow-tooltip>
          <template #default="{ row }">{{ row.description || '—' }}</template>
        </el-table-column>
        <el-table-column prop="totalValue" label="总估值" width="130" sortable>
          <template #default="{ row }">{{ formatCurrency(row.totalValue) }}</template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="170" sortable>
          <template #default="{ row }">{{ formatDateTime(row.createdAt) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" :fixed="isMobile ? false : 'right'">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="view(row.id)">查看</el-button>
            <el-button type="primary" link size="small" @click="edit(row.id)">编辑</el-button>
            <el-button type="danger" link size="small" @click="duplicateRow(row.id)">复制</el-button>
            <el-button type="danger" link size="small" @click="remove(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="fetchList"
          @current-change="fetchList"
        />
      </div>
    </el-card>

    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value">{{ total }}</div>
          <div class="stat-label">评估总数</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value">{{ formatCurrency(stats.totalValue) }}</div>
          <div class="stat-label">总估值</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value">{{ formatCurrency(stats.averageValue) }}</div>
          <div class="stat-label">平均估值</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useResponsive } from '@/utils/responsive'
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSystemStatsAPI } from '@/api/admin'
import { getEvaluationsAPI, deleteEvaluationAPI, duplicateEvaluationAPI } from '@/api/evaluation'

const { isMobile } = useResponsive()

const router = useRouter()
const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const keyword = ref('')
const statusFilter = ref('')
const stats = reactive({ totalValue: 0, averageValue: 0 })

const formatCurrency = (v) =>
  new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY', minimumFractionDigits: 0 }).format(v || 0)
const formatDateTime = (s) =>
  s ? new Date(s).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false }) : '—'
const statusType = (s) => ({ draft: 'info', completed: 'success', processing: 'warning', failed: 'danger' }[s] || 'info')
const statusText = (s) => ({ draft: '草稿', completed: '已完成', processing: '计算中', failed: '失败' }[s] || s || '—')

async function fetchList() {
  loading.value = true
  try {
    const res = await getEvaluationsAPI({
      scope: 'all',
      page: page.value,
      pageSize: pageSize.value,
      keyword: keyword.value || undefined,
      status: statusFilter.value || undefined
    })
    const data = res?.data || {}
    list.value = (data.list || []).map((e) => ({
      id: e.id,
      name: e.name || '未命名',
      description: e.description,
      totalValue: e.totalValue ?? 0,
      createdAt: e.createdAt || '',
      status: e.status || 'completed'
    }))
    total.value = data.total ?? 0
  } catch (e) {
    ElMessage.error('加载失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

async function fetchStats() {
  try {
    const res = await getSystemStatsAPI()
    const d = res?.data || {}
    stats.totalValue = d.total_value ?? 0
    stats.averageValue = d.average_value ?? 0
  } catch (error) { ElMessage.error(error.response?.data?.detail || '统计数据加载失败') }
}

function view(id) {
  router.push(`/result/${id}`)
}

function edit(id) {
  router.push(`/data-input?edit=${id}`)
}

async function duplicateRow(id) {
  try {
    await duplicateEvaluationAPI(id)
    ElMessage.success('已复制')
    fetchList()
    fetchStats()
  } catch (e) {
    ElMessage.error('复制失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function remove(id) {
  try {
    await ElMessageBox.confirm('确定删除该评估？此操作不可恢复。', '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteEvaluationAPI(id)
    ElMessage.success('已删除')
    fetchList()
    fetchStats()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败: ' + (e.response?.data?.detail || e.message))
  }
}

watch([keyword, statusFilter], () => { page.value = 1; fetchList() })

onMounted(() => {
  fetchList()
  fetchStats()
})
</script>

<style scoped>
.admin-evaluations { max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 20px; }
.page-header h1 { margin: 0 0 6px 0; font-size: 22px; color: #2c3e50; }
.subtitle { margin: 0; color: #666; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.card-header h3 { margin: 0; font-size: 16px; }
.header-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.link { color: #409EFF; text-decoration: none; }
.link:hover { text-decoration: underline; }
.pagination-wrap { margin-top: 16px; display: flex; justify-content: flex-end; }
.stats-row { margin-top: 20px; }
.stat-card { text-align: center; }
.stat-value { font-size: 20px; font-weight: 600; color: #2c3e50; }
.stat-label { font-size: 13px; color: #666; margin-top: 4px; }

@media (max-width: 768px) {
  .header-actions { width: 100%; flex-wrap: wrap; gap: 8px; }
  .header-actions > .el-input, .header-actions > .el-select { width: 100% !important; }
  .header-actions .el-button { margin-left: 0; }
  .pagination-wrap { justify-content: center; }
  .card-header { flex-wrap: wrap; gap: 12px; }
  .weight-setting-container { padding: 0; }
}

</style>
