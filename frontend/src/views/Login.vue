<!-- frontend/src/views/Login.vue -->
<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>用户登录</h2>
          <p>欢迎使用医疗数据资产价值计量器</p>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="80px"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
            size="large"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <div class="form-actions">
            <el-button
              type="primary"
              :loading="loading"
              @click="handleLogin"
              size="large"
              style="width: 100%"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </div>
        </el-form-item>
        
        <div class="form-footer">
          <span>还没有账号？</span>
          <el-button link type="primary" @click="$router.push('/register')">立即注册</el-button>
        </div>
        <p class="login-tip">管理员账号：admin / admin123（首次打开登录页时已自动初始化）</p>
        <div class="form-footer">
          <el-button link @click="$router.push('/')">返回首页</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'
import { initDemoDataAPI } from '@/api/demo'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref()

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
  ]
}

const loading = ref(false)

onMounted(async () => {
  try {
    await initDemoDataAPI()
  } catch {
    // 忽略（可能已初始化或后端未启动）
  }
})

const handleLogin = async () => {
  // 表单验证
  if (!loginFormRef.value) return
  const valid = await loginFormRef.value.validate()
  if (!valid) return

  loading.value = true
  try {
    await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    const redirect = router.currentRoute.value.query.redirect || (userStore.isAdmin ? '/admin' : '/personal-center')
    router.push(redirect)
  } catch (error) {
    const msg = error.response?.data?.detail || error.response?.data?.message || '用户名或密码错误'
    ElMessage.error(typeof msg === 'string' ? msg : '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

// 自动填充测试数据（开发环境用）
if (process.env.NODE_ENV === 'development') {
  loginForm.username = 'testuser'
  loginForm.password = 'password123'
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.card-header {
  text-align: center;
  padding: 20px 0;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 24px;
}

.card-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.login-form {
  padding: 20px 0;
}

.form-actions {
  width: 100%;
}

.form-footer {
  margin-top: 20px;
  text-align: center;
  color: #666;
  font-size: 14px;
}

.form-footer .el-button {
  margin-left: 5px;
}

.login-tip {
  margin: 12px 0 0 0;
  font-size: 12px;
  color: #909399;
  text-align: center;
}
</style>