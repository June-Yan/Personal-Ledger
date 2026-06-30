<template>
  <nav class="bottom-nav">
    <router-link to="/" :class="{ active: route.path === '/' }">
      <span class="icon">🏠</span>
      <span class="label">首页</span>
    </router-link>
    <router-link to="/bills" :class="{ active: route.path === '/bills' }">
      <span class="icon">📋</span>
      <span class="label">账单</span>
    </router-link>
    <router-link to="/add" class="center-btn">
      <span class="plus">+</span>
    </router-link>
    <router-link to="/reports" :class="{ active: route.path === '/reports' }">
      <span class="icon">📊</span>
      <span class="label">报表</span>
    </router-link>
    <router-link to="/profile" :class="{ active: route.path === '/profile' }">
      <span class="icon">👤</span>
      <span class="label">我的</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 480px;
  height: 56px;
  background: #fff;
  border-top: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 100;
}
.bottom-nav a {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #999;
  font-size: 11px;
  flex: 1;
}
.bottom-nav a.active {
  color: #00bfa5;
}
.icon {
  font-size: 20px;
  line-height: 1;
  margin-bottom: 2px;
}
.center-btn {
  position: relative;
  top: -16px;
}
.plus {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: #00bfa5;
  color: #fff;
  border-radius: 50%;
  font-size: 28px;
  box-shadow: 0 2px 8px rgba(0,191,165,0.4);
}
</style>
