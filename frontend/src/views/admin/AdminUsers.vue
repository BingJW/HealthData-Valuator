<template>
  <div class="admin-users">
    <div class="page-header">
      <h1>用户管理</h1>
      <p class="subtitle">管理员对用户进行增删改查</p>
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
            <el-button type="success" @click="openCreate"><el-icon><Plus /></el-icon> 新增用户</el-button>
          </div>
        </div>
      </template>

      <el-table :data="list" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="hospital" label="医院" min-width="140" show-overflow-tooltip />
        <el-table-column prop="phone" label="手机" width="130">
          <template #default="{ row }">{{ row.phone || '—' }}</template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="160" show-overflow-tooltip>
          <template #default="{ row }">{{ row.email || '—' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" :disabled="row.username === 'admin'" @click="remove(row)">删除</el-button>
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

    <el-dialog v-model="createVisible" title="新增用户" width="480px" destroy-on-close @closed="resetCreateForm">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="createForm.username" placeholder="3-20 位" maxlength="20" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="createForm.password" type="password" show-password placeholder="至少 6 位" />
        </el-form-item>
        <el-form-item label="医院" prop="hospital">
          <el-input v-model="createForm.hospital" placeholder="选填" />
        </el-form-item>
        <el-form-item label="手机" prop="phone">
          <el-input v-model="createForm.phone" placeholder="选填" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="createForm.email" placeholder="选填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitCreate">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="editVisible" title="编辑用户" width="480px" destroy-on-close>
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="医院" prop="hospital">
          <el-input v-model="editForm.hospital" />
        </el-form-item>
        <el-form-item label="手机" prop="phone">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="新密码" prop="password">
          <el-input v-model="editForm.password" type="password" show-password placeholder="不修改请留空" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getUsersAPI,
  createAdminUserAPI,
  getAdminUserAPI,
  updateAdminUserAPI,
  deleteAdminUserAPI
} from '@/api/admin'

const loading = ref(false)
const submitting = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const keyword = ref('')

const createVisible = ref(false)
const createFormRef = ref()
const createForm = reactive({ username: '', password: '', hospital: '', phone: '', email: '' })
const createRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '至少 6 位', trigger: 'blur' }
  ]
}

const editVisible = ref(false)
const editFormRef = ref()
const editForm = reactive({ id: null, username: '', hospital: '', phone: '', email: '', password: '' })
const editRules = {}

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

function resetCreateForm() {
  createForm.username = ''
  createForm.password = ''
  createForm.hospital = ''
  createForm.phone = ''
  createForm.email = ''
}

function openCreate() {
  resetCreateForm()
  createVisible.value = true
}

async function submitCreate() {
  try {
    await createFormRef.value?.validate()
  } catch {
    return
  }
  submitting.value = true
  try {
    await createAdminUserAPI({
      username: createForm.username.trim(),
      password: createForm.password,
      hospital: createForm.hospital || '',
      phone: createForm.phone || '',
      email: createForm.email || ''
    })
    ElMessage.success('已创建')
    createVisible.value = false
    fetchList()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  } finally {
    submitting.value = false
  }
}

async function openEdit(row) {
  try {
    const res = await getAdminUserAPI(row.id)
    const d = res?.data || {}
    editForm.id = d.id
    editForm.username = d.username
    editForm.hospital = d.hospital || ''
    editForm.phone = d.phone || ''
    editForm.email = d.email || ''
    editForm.password = ''
    editVisible.value = true
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '加载失败')
  }
}

async function submitEdit() {
  try {
    await editFormRef.value?.validate()
  } catch {
    return
  }
  submitting.value = true
  try {
    const body = {
      hospital: editForm.hospital,
      phone: editForm.phone,
      email: editForm.email
    }
    if (editForm.password?.trim()) body.password = editForm.password
    await updateAdminUserAPI(editForm.id, body)
    ElMessage.success('已保存')
    editVisible.value = false
    fetchList()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    submitting.value = false
  }
}

async function remove(row) {
  if (row.username === 'admin') return
  try {
    await ElMessageBox.confirm(`确定删除用户「${row.username}」？`, '删除确认', { type: 'warning' })
    await deleteAdminUserAPI(row.id)
    ElMessage.success('已删除')
    fetchList()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(e.response?.data?.detail || '删除失败')
  }
}

watch(keyword, () => { page.value = 1; fetchList() })

onMounted(() => fetchList())
</script>

<style scoped>
.admin-users { max-width: 1100px; margin: 0 auto; }
.page-header { margin-bottom: 20px; }
.page-header h1 { margin: 0 0 6px 0; font-size: 22px; color: #2c3e50; }
.subtitle { margin: 0; color: #666; font-size: 14px; }
.card-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.card-header h3 { margin: 0; font-size: 16px; }
.header-actions { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.pagination-wrap { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
