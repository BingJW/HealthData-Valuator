<template>
  <div class="drafts-wrap">
    <el-card>
      <template #header>
        <span>草稿箱</span>
        <span class="header-tip">草稿仅保存在本机，清除浏览器数据会丢失</span>
      </template>
      <template v-if="draft">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="评估名称">{{ draft.evaluationName || '未命名' }}</el-descriptions-item>
          <el-descriptions-item label="说明">{{ draft.description || '—' }}</el-descriptions-item>
          <el-descriptions-item label="保存时间">{{ formatDate(draft.__savedAt) }}</el-descriptions-item>
        </el-descriptions>
        <div class="actions">
          <el-button type="primary" @click="$router.push('/data-input')">继续编辑</el-button>
          <el-button type="danger" plain @click="handleDelete">删除草稿</el-button>
        </div>
      </template>
      <el-empty v-else description="暂无草稿" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
const userStore = useUserStore()
const draftKey = () => `evaluationDraft:${userStore.userInfo.username}`
import { ElMessage, ElMessageBox } from 'element-plus'

const draft = ref(null)

const formatDate = (v) => {
  if (!v) return '—'
  try {
    const d = typeof v === 'number' ? new Date(v) : new Date(v)
    return d.toLocaleString('zh-CN')
  } catch {
    return '—'
  }
}

const loadDraft = async () => {
  try {
    if (!userStore.userInfo.username) await userStore.getUserInfo()
    const raw = localStorage.getItem(draftKey())
    if (raw) {
      const data = JSON.parse(raw)
      draft.value = data
    } else {
      draft.value = null
    }
  } catch {
    draft.value = null
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定删除该草稿？删除后无法恢复。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    localStorage.removeItem(draftKey())
    draft.value = null
    ElMessage.success('草稿已删除')
  } catch {
    // 取消
  }
}

onMounted(loadDraft)
</script>

<style scoped>
.drafts-wrap {
  max-width: 600px;
}
.header-tip {
  font-size: 12px;
  color: #909399;
  margin-left: 12px;
}
.actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}
</style>
