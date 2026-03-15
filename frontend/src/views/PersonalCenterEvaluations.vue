<template>
  <div class="evaluations-wrap">
    <el-card>
      <template #header>
        <span>我的评估</span>
        <el-button type="primary" size="small" style="float: right" @click="$router.push('/data-input')">
          新建评估
        </el-button>
      </template>
      <el-table v-loading="loading" :data="list" stripe>
        <el-table-column prop="name" label="评估名称" min-width="160" />
        <el-table-column prop="totalValue" label="总估值（元）" width="140">
          <template #default="{ row }">{{ formatNum(row.totalValue) }}</template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180">
          <template #default="{ row }">{{ formatDate(row.createdAt) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : 'info'" size="small">
              {{ row.status === 'completed' ? '已完成' : row.status || '已完成' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="$router.push('/result/' + row.id)">查看报告</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-if="total > pageSize"
        class="mt-4"
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="onPageChange"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEvaluationsAPI } from '@/api/evaluation'

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

const formatNum = (v) => (v != null && !isNaN(Number(v)) ? Number(v).toLocaleString('zh-CN') : '—')
const formatDate = (s) => {
  if (!s) return '—'
  try {
    return new Date(s).toLocaleString('zh-CN')
  } catch {
    return s
  }
}

const load = async () => {
  loading.value = true
  try {
    const res = await getEvaluationsAPI({ page: page.value, pageSize: pageSize.value })
    if (res?.data) {
      list.value = res.data.list || []
      total.value = res.data.total ?? 0
    }
  } catch (e) {
    list.value = []
  } finally {
    loading.value = false
  }
}

const onPageChange = (p) => {
  page.value = p
  load()
}

onMounted(load)
</script>

<style scoped>
.evaluations-wrap {
  max-width: 1000px;
}
.mt-4 {
  margin-top: 16px;
}
</style>
