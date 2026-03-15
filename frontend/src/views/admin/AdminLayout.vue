<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <el-icon :size="22"><Monitor /></el-icon>
        <span>管理后台</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
        background-color="#1a1d29"
        text-color="#a3a6b5"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>概览</span>
        </el-menu-item>
        <el-menu-item index="/admin/evaluations">
          <el-icon><Document /></el-icon>
          <span>评估管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/weights">
          <el-icon><Setting /></el-icon>
          <span>权重设置</span>
        </el-menu-item>
      </el-menu>
      <div class="sidebar-footer">
        <el-button type="primary" plain size="small" @click="$router.push('/personal-center')" block>
          <el-icon><Back /></el-icon>
          返回个人中心
        </el-button>
      </div>
    </aside>
    <main class="admin-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Monitor, DataAnalysis, Document, User, Setting, Back } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f0f2f5;
}

.admin-sidebar {
  width: 220px;
  background: #1a1d29;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  height: 56px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid #2d3142;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  padding: 12px 0;
}

.sidebar-menu .el-menu-item {
  margin: 4px 12px;
  border-radius: 8px;
  height: 44px;
  line-height: 44px;
}

.sidebar-menu .el-menu-item.is-active {
  background: rgba(64, 158, 255, 0.15) !important;
  color: #409EFF;
}

.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid #2d3142;
}

.admin-main {
  flex: 1;
  overflow: auto;
  padding: 20px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 64px;
  }
  .sidebar-header span,
  .sidebar-menu .el-menu-item span {
    display: none;
  }
  .sidebar-footer .el-button span {
    display: none;
  }
}
</style>
