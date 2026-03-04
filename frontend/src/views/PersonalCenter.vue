<!-- frontend/src/views/PersonalCenter.vue -->
<template>
  <div class="personal-center-container">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="header-content">
        <div class="logo" @click="$router.push('/')">
          <h2>医疗数据资产价值计量器</h2>
        </div>
        <div class="user-info">
          <el-dropdown @command="handleCommand">
            <span class="user-name">
              {{ userInfo.username || '用户' }}
              <el-icon><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>

    <div class="main-content">
      <!-- 侧边栏 -->
      <el-aside class="sidebar" width="250px">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <el-icon><House /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          
          <el-menu-item index="new-evaluation">
            <el-icon><DocumentAdd /></el-icon>
            <span>新建评估</span>
          </el-menu-item>
          
          <el-sub-menu index="evaluations">
            <template #title>
              <el-icon><Files /></el-icon>
              <span>我的评估</span>
            </template>
            <el-menu-item index="evaluation-list">评估列表</el-menu-item>
            <el-menu-item index="evaluation-drafts">草稿箱</el-menu-item>
          </el-sub-menu>
          
          <el-menu-item index="profile">
            <el-icon><User /></el-icon>
            <span>个人资料</span>
          </el-menu-item>
          
          <el-menu-item index="help">
            <el-icon><QuestionFilled /></el-icon>
            <span>使用帮助</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="content">
        <router-view />
      </el-main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { 
  House, 
  DocumentAdd, 
  Files, 
  User, 
  QuestionFilled,
  ArrowDown 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 从store获取用户信息
const userInfo = computed(() => userStore.userInfo)

// 计算激活的菜单项
const activeMenu = computed(() => {
  const path = route.path
  if (path.includes('/data-input')) return 'new-evaluation'
  if (path.includes('/result/')) return 'evaluation-list'
  if (path.includes('/profile')) return 'profile'
  return 'dashboard'
})

onMounted(async () => {
  // 如果没有用户信息，尝试获取
  if (!userInfo.value.username) {
    await userStore.getUserInfo()
  }
})

const handleMenuSelect = (index) => {
  switch (index) {
    case 'dashboard':
      router.push('/personal-center')
      break
    case 'new-evaluation':
      router.push('/data-input')
      break
    case 'evaluation-list':
      router.push('/personal-center/evaluations')
      break
    case 'profile':
      router.push('/personal-center/profile')
      break
    case 'help':
      ElMessage.info('帮助文档正在建设中...')
      break
  }
}

const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      router.push('/personal-center/profile')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await userStore.logout()
      } catch (error) {
        // 用户取消
      }
      break
  }
}
</script>

<style scoped>
.personal-center-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #2c3e50;
  color: white;
  padding: 0 20px;
}

.header-content {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.logo {
  cursor: pointer;
}

.logo h2 {
  margin: 0;
  font-size: 1.5rem;
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-name {
  cursor: pointer;
  color: white;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

.user-name:hover {
  color: #409EFF;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background-color: #f5f5f5;
  border-right: 1px solid #e6e6e6;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.content {
  padding: 20px;
  background-color: #f9f9f9;
  overflow-y: auto;
}

:deep(.el-menu-item.is-active) {
  background-color: #ecf5ff;
  color: #409EFF;
}

:deep(.el-sub-menu__title:hover) {
  background-color: #f5f5f5;
}
</style>