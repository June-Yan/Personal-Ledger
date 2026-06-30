<template>
  <div class="profile-view">
    <div class="top-bar">
      <h2>我的</h2>
    </div>
    <div class="user-card">
      <div class="avatar">👤</div>
      <div class="email">{{ auth.user?.email || '未登录' }}</div>
    </div>
    <div class="menu">
      <router-link to="/categories" class="menu-item">
        <span>🏷️ 分类管理</span>
        <span class="arrow">&gt;</span>
      </router-link>
      <div class="menu-item" @click="handleLogout">
        <span>🚪 退出登录</span>
        <span class="arrow">&gt;</span>
      </div>
      <div class="menu-item danger" @click="handleDelete">
        <span>🗑️ 注销账户</span>
        <span class="arrow">&gt;</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import * as authApi from '../api/auth'

const router = useRouter()
const auth = useAuthStore()

const handleLogout = async () => {
  await auth.logout()
  router.push('/login')
}

const handleDelete = async () => {
  if (!confirm('注销账户将删除所有数据，确定继续？')) return
  try {
    await authApi.deleteAccount()
    auth.clearAuth()
    router.push('/login')
  } catch (e: any) {
    alert(e.message)
  }
}
</script>

<style scoped>
.profile-view { padding-bottom: 16px; }
.top-bar { background: #00bfa5; color: #fff; padding: 12px 16px; font-size: 16px; font-weight: 600; }
.user-card {
  background: #fff;
  margin: 12px;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
}
.avatar { font-size: 48px; margin-bottom: 8px; }
.email { font-size: 14px; color: #666; }
.menu { background: #fff; margin: 0 12px; border-radius: 12px; overflow: hidden; }
.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  text-decoration: none;
  color: #333;
}
.menu-item:last-child { border-bottom: none; }
.arrow { color: #ccc; }
.danger { color: #ff4d4f; }
</style>
