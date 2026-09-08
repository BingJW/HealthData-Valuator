<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h1>概览</h1>
      <p class="subtitle">系统数据与快捷入口</p>
    </div>

    <el-row :gutter="20" class="overview-cards">
      <el-col :xs="24" :sm="12" :md="6" v-for="card in overviewCards" :key="card.title">
        <el-card shadow="hover" class="stat-card" :style="{ borderLeft: `4px solid ${card.color}` }">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: card.color + '20' }">
              <el-icon :size="24" :color="card.color"><component :is="card.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-label">{{ card.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="14">
        <el-card class="recent-card" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>最近评估</h3>
              <router-link to="/admin/evaluations" class="link">全部 →</router-link>
            </div>
          </template>
          <el-table :data="recentList" v-loading="loading" stripe size="small">
            <el-table-column prop="name" label="名称" min-width="140" show-overflow-tooltip>
              <template #default="{ row }">
                <router-link :to="`/result/${row.id}`" class="link">{{ row.name }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="totalValue" label="总估值" width="110">
              <template #default="{ row }">{{ formatCurrency(row.totalValue) }}</template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewEvaluation(row.id)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!loading && recentList.length === 0" description="暂无评估" :image-size="60" />
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="10">
        <el-card class="quick-card" shadow="never">
          <template #header><h3>快捷操作</h3></template>
          <div class="actions-grid">
            <el-button type="primary" class="action-btn" @click="$router.push('/admin/evaluations')">
              <el-icon><Document /></el-icon>
              <span>评估管理</span>
            </el-button>
            <el-button class="action-btn" @click="$router.push('/admin/users')">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-button>
            <el-button class="action-btn" @click="$router.push('/admin/weights')">
              <el-icon><Setting /></el-icon>
              <span>权重设置</span>
            </el-button>
            <el-button class="action-btn" @click="initDemoData">
              <el-icon><MagicStick /></el-icon>
              <span>初始化演示数据</span>
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Document } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSystemStatsAPI } from '@/api/admin'
import { getEvaluationsAPI } from '@/api/evaluation'
import { initDemoDataAPI } from '@/api/demo'

const router = useRouter()
const loading = ref(false)
const overviewCards = ref([
  { title: '总用户数', value: '—', icon: 'User', color: '#409EFF' },
  { title: '总评估数', value: '—', icon: 'Document', color: '#67C23A' },
  { title: '总估值', value: '—', icon: 'Money', color: '#E6A23C' },
  { title: '平均估值', value: '—', icon: 'DataAnalysis', color: '#F56C6C' }
])
const recentList = ref([])

const formatCurrency = (v) =>
  new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY', minimumFractionDigits: 0 }).format(v || 0)
const getStatusType = (s) => ({ draft: 'info', completed: 'success', processing: 'warning', failed: 'danger' }[s] || 'info')
const getStatusText = (s) => ({ draft: '草稿', completed: '已完成', processing: '计算中', failed: '失败' }[s] || '—')

async function refreshData() {
  loading.value = true
  try {
    const [statsRes, listRes] = await Promise.all([
      getSystemStatsAPI(),
      getEvaluationsAPI({ page: 1, pageSize: 5, scope: 'all' })
    ])
    const d = statsRes?.data || {}
    overviewCards.value = [
      { title: '总用户数', value: String(d.total_users ?? '—'), icon: 'User', color: '#409EFF' },
      { title: '总评估数', value: String(d.total_evaluations ?? '—'), icon: 'Document', color: '#67C23A' },
      { title: '总估值', value: d.total_value != null ? `¥ ${Number(d.total_value).toLocaleString('zh-CN')}` : '—', icon: 'Money', color: '#E6A23C' },
      { title: '平均估值', value: d.average_value != null ? `¥ ${Number(d.average_value).toLocaleString('zh-CN')}` : '—', icon: 'DataAnalysis', color: '#F56C6C' }
    ]
    const list = listRes?.data?.list || []
    recentList.value = list.map((e) => ({
      id: e.id,
      name: e.name || '未命名',
      totalValue: e.totalValue ?? 0,
      status: e.status || 'completed'
    }))
  } catch (e) {
    ElMessage.error('加载失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

function viewEvaluation(id) {
  router.push(`/result/${id}`)
}

async function initDemoData() {
  try {
    await ElMessageBox.confirm('确定创建演示评估？需服务端启用演示模式，不会创建默认账号。', '确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await initDemoDataAPI()
    ElMessage.success('演示数据初始化成功')
    await refreshData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('初始化失败: ' + (e.response?.data?.detail || e.message))
  }
}

onMounted(() => refreshData())
</script>

<style scoped>
.admin-dashboard { max-width: 1100px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-header h1 { margin: 0 0 6px 0; font-size: 22px; color: #2c3e50; }
.subtitle { margin: 0; color: #666; font-size: 14px; }
.overview-cards { margin-bottom: 24px; }
.stat-card { transition: transform 0.2s, box-shadow 0.2s; }
.stat-card:hover { transform: translateY(-2px); }
.stat-content { display: flex; align-items: center; padding: 8px 0; }
.stat-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 14px; flex-shrink: 0; }
.stat-info { flex: 1; min-width: 0; }
.stat-value { font-size: 20px; font-weight: 600; color: #2c3e50; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.stat-label { font-size: 13px; color: #666; margin-top: 2px; }
.recent-card, .quick-card { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { margin: 0; font-size: 16px; }
.link { color: #409EFF; text-decoration: none; }
.link:hover { text-decoration: underline; }
.actions-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.action-btn { height: 72px; flex-direction: column; gap: 6px; }
.action-btn .el-icon { font-size: 22px; }
@media (max-width: 768px) { .actions-grid { grid-template-columns: 1fr; } }
</style>
