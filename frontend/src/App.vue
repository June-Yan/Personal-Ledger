<template>
  <div id="app">
    <router-view />
    <BottomNav v-if="showNav" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import BottomNav from './components/BottomNav.vue'

const route = useRoute()
const showNav = computed(() => !route.meta.public && route.path !== '/login')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  color: #333;
}
#app {
  max-width: 480px;
  margin: 0 auto;
  min-height: 100vh;
  background: #f5f5f5;
  position: relative;
  padding-bottom: 60px;
}
</style>
