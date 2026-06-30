<template>
  <div class="login-page">
    <div class="header">
      <div class="logo">💰</div>
      <h1>个人记账本</h1>
    </div>
    <div class="tabs">
      <button :class="{ active: tab === 'login' }" @click="tab = 'login'">登录</button>
      <button :class="{ active: tab === 'register' }" @click="tab = 'register'">注册</button>
    </div>

    <div v-if="tab === 'login'" class="form">
      <div class="segment">
        <button :class="{ active: loginMode === 'password' }" @click="loginMode = 'password'">密码登录</button>
        <button :class="{ active: loginMode === 'code' }" @click="loginMode = 'code'">验证码登录</button>
      </div>
      <input v-model="form.email" type="email" placeholder="邮箱" />
      <input v-if="loginMode === 'password'" v-model="form.password" type="password" placeholder="密码" />
      <div v-else class="code-row">
        <input v-model="form.code" type="text" placeholder="验证码" maxlength="6" />
        <button class="code-btn" :disabled="codeTimer > 0" @click="sendCode">{{ codeTimer > 0 ? `${codeTimer}s` : '获取验证码' }}</button>
      </div>
      <button class="submit" @click="handleLogin">登录</button>
    </div>

    <div v-else class="form">
      <input v-model="form.email" type="email" placeholder="邮箱" />
      <div class="code-row">
        <input v-model="form.code" type="text" placeholder="验证码" maxlength="6" />
        <button class="code-btn" :disabled="codeTimer > 0" @click="sendCode">{{ codeTimer > 0 ? `${codeTimer}s` : '获取验证码' }}</button>
      </div>
      <input v-model="form.password" type="password" placeholder="密码（至少6位）" />
      <button class="submit" @click="handleRegister">注册</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import * as authApi from '../api/auth'

const router = useRouter()
const auth = useAuthStore()
const tab = ref<'login' | 'register'>('login')
const loginMode = ref<'password' | 'code'>('password')
const codeTimer = ref(0)

const form = reactive({ email: '', password: '', code: '' })

let timer: any
const startTimer = () => {
  codeTimer.value = 60
  timer = setInterval(() => {
    codeTimer.value--
    if (codeTimer.value <= 0) clearInterval(timer)
  }, 1000)
}

const sendCode = async () => {
  if (!form.email) return alert('请输入邮箱')
  try {
    await authApi.sendCode(form.email)
    startTimer()
    alert('验证码已发送（开发环境固定为 123456）')
  } catch (e: any) {
    alert(e.message)
  }
}

const handleLogin = async () => {
  if (!form.email) return alert('请输入邮箱')
  try {
    let res: any
    if (loginMode.value === 'password') {
      res = await authApi.loginPassword(form.email, form.password)
    } else {
      res = await authApi.loginCode(form.email, form.code)
    }
    auth.setAuth(res.data.token, res.data.user)
    router.push('/')
  } catch (e: any) {
    alert(e.message)
  }
}

const handleRegister = async () => {
  if (!form.email || !form.password || !form.code) return alert('请填写完整信息')
  if (form.password.length < 6) return alert('密码至少6位')
  try {
    const res: any = await authApi.register(form.email, form.password, form.code)
    auth.setAuth(res.data.token, res.data.user)
    router.push('/')
  } catch (e: any) {
    alert(e.message)
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #fff;
  padding: 40px 24px;
}
.header {
  text-align: center;
  margin-bottom: 32px;
}
.logo {
  font-size: 56px;
  margin-bottom: 8px;
}
h1 {
  font-size: 22px;
  color: #333;
}
.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  margin-bottom: 24px;
}
.tabs button {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  font-size: 16px;
  color: #999;
  cursor: pointer;
}
.tabs button.active {
  color: #00bfa5;
  border-bottom: 2px solid #00bfa5;
}
.segment {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.segment button {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.segment button.active {
  border-color: #00bfa5;
  color: #00bfa5;
}
.form input {
  width: 100%;
  padding: 12px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
}
.code-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.code-row input {
  flex: 1;
  margin-bottom: 0;
}
.code-btn {
  padding: 0 16px;
  background: #00bfa5;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
}
.code-btn:disabled {
  background: #ccc;
}
.submit {
  width: 100%;
  padding: 14px;
  background: #00bfa5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 8px;
}
</style>
