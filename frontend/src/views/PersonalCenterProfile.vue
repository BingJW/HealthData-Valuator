<template>
  <div class="profile-wrap">
    <el-card>
      <template #header><span>个人资料</span></template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">{{ userStore.userInfo?.username || '—' }}</el-descriptions-item>
        <el-descriptions-item label="医院">{{ userStore.userInfo?.hospital || '—' }}</el-descriptions-item>
        <el-descriptions-item label="手机">{{ userStore.userInfo?.phone || '—' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ userStore.userInfo?.email || '—' }}</el-descriptions-item>
      </el-descriptions>
      <p class="tip">如需修改资料，请联系管理员或在后端扩展「更新用户信息」功能。</p>
    </el-card>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
</script>

<style scoped>
.profile-wrap {
  max-width: 600px;
}
.tip {
  margin-top: 16px;
  color: #909399;
  font-size: 13px;
}
</style>
