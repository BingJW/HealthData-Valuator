<template>
  <div class="dashboard-wrap">
    <el-card class="welcome-card">
      <h2>欢迎回来，{{ userStore.userInfo?.username || '用户' }}</h2>
      <p class="sub">这里是您的个人中心仪表盘，可快速进入新建评估、查看历史或管理资料。</p>
    </el-card>
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">评估总数</div>
          <div class="stat-value">{{ stats.total_count ?? '—' }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">总估值（元）</div>
          <div class="stat-value">{{ formatNum(stats.total_value) }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">平均估值（元）</div>
          <div class="stat-value">{{ formatNum(stats.average_value) }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-card class="quick-actions">
      <template #header>
        <span>快捷操作</span>
      </template>
      <el-space wrap :size="16">
        <el-button type="primary" @click="$router.push('/data-input')">
          <el-icon><DocumentAdd /></el-icon>
          新建评估
        </el-button>
        <el-button @click="$router.push('/personal-center/evaluations')">
          <el-icon><Files /></el-icon>
          我的评估
        </el-button>
        <el-button @click="$router.push('/personal-center/profile')">
          <el-icon><User /></el-icon>
          个人资料
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { getEvaluationStatsAPI } from '@/api/evaluation'
import { DocumentAdd, Files, User } from '@element-plus/icons-vue'

const userStore = useUserStore()
const stats = ref({})

const formatNum = (v) => {
  if (v == null || v === '') return '—'
  const n = Number(v)
  if (isNaN(n)) return '—'
  return n.toLocaleString('zh-CN')
}

onMounted(async () => {
  try {
    const res = await getEvaluationStatsAPI()
    if (res?.data) stats.value = res.data
  } catch (e) {
    // 忽略，保持占位
  }
})
</script>

<style scoped>
.dashboard-wrap {
  max-width: 900px;
}
.welcome-card {
  margin-bottom: 20px;
}
.welcome-card h2 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  color: #2c3e50;
}
.welcome-card .sub {
  margin: 0;
  color: #666;
  font-size: 14px;
}
.stats-row {
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
}
.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #409eff;
}
.quick-actions :deep(.el-card__header) {
  font-weight: 600;
}
</style>
