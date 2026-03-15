<template>
  <div class="admin-users">
    <div class="page-header">
      <h1>用户管理</h1>
      <p class="subtitle">查看系统注册用户列表</p>
    </div>

    <el-card shadow="never" class="table-card">
      <template #header>
        <div class="card-header">
          <h3>用户列表</h3>
          <div class="header-actions">
            <el-input
              v-model="keyword"
              placeholder="用户名 / 医院"
              clearable
              style="width: 220px"
              @keyup.enter="fetchList"
            >
              <template #prefix><el-icon><Search /></el-icon></template>
            </el-input>
            <el-button type="primary" @click="fetchList"><el-icon><Refresh /></el-icon> 刷新</el-button>
          </div>
        </div>
      </template>

      <el-table :data="list" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="hospital" label="医院" min-width="160" show-overflow-tooltip />
        <el-table-column prop="phone" label="手机" width="130">
          <template #default="{ row }">{{ row.phone || '—' }}</template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">{{ row.email || '—' }}</template>
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
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getUsersAPI } from '@/api/admin'

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const keyword = ref('')

async function fetchList() {
  loading.value = true
  try {
    const res = await getUsersAPI({ page: page.value, pageSize: pageSize.value, keyword: keyword.value || undefined })
    const data = res?.data || {}
    list.value = data.list || []
    total.value = data.total ?? 0
  } catch (e) {
    ElMessage.error('加载失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

watch(keyword, () => { page.value = 1; fetchList() })

onMounted(() => fetchList())
</script>

<style scoped>
.admin-users { max-width: 1000px; margin: 0 auto; }
.page-header { margin-bottom: 20px; }
.page-header h1 { margin: 0 0 6px 0; font-size: 22px; color: #2c3e50; }
.subtitle { margin: 0; color: #666; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.card-header h3 { margin: 0; font-size: 16px; }
.header-actions { display: flex; align-items: center; gap: 10px; }
.pagination-wrap { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
