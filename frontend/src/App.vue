<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo">
            <h2>🏛️ 简单拍卖系统</h2>
          </div>
          <div class="nav-menu">
            <el-menu
              mode="horizontal"
              :default-active="activeMenu"
              router
              class="header-menu"
            >
              <el-menu-item index="/">首页</el-menu-item>
              <el-menu-item index="/create" v-if="isAuthenticated">发布拍卖</el-menu-item>
              <el-menu-item index="/my-auctions" v-if="isAuthenticated">我的拍卖</el-menu-item>
              <el-menu-item index="/my-bids" v-if="isAuthenticated">我的竞拍</el-menu-item>
            </el-menu>
          </div>
          <div class="user-info">
            <el-dropdown v-if="isAuthenticated" @command="handleCommand">
              <span class="user-dropdown">
                <el-avatar :size="32" :style="{ backgroundColor: '#667eea' }">
                  {{ userInfo?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span class="username">{{ userInfo?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-button v-else @click="$router.push('/login')" type="primary">登录</el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from './store'
import { ArrowDown } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    ArrowDown
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const store = useStore()

    const isAuthenticated = computed(() => store.isAuthenticated)
    const userInfo = computed(() => store.userInfo)

    const activeMenu = computed(() => route.path)

    const handleCommand = (command) => {
      if (command === 'logout') {
        store.logout()
        router.push('/')
      }
    }

    onMounted(() => {
      // 检查token并获取用户信息
      const token = localStorage.getItem('token')
      if (token) {
        // 先同步token到store
        store.setToken(token)
        // 然后验证token并获取用户信息
        store.checkAuth()
      }
    })

    return {
      isAuthenticated,
      userInfo,
      activeMenu,
      handleCommand
    }
  }
}
</script>

<style scoped>
#app {
  min-height: 100vh;
}

.el-header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 64px !important;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.logo h2 {
  margin: 0;
  color: #667eea;
  font-size: 20px;
}

.nav-menu {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-menu {
  border-bottom: none;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.3s;
}

.user-dropdown:hover {
  background: #f5f5f5;
}

.username {
  margin: 0 8px;
  font-size: 14px;
  color: #333;
}

.el-main {
  padding: 24px;
  min-height: calc(100vh - 64px);
}
</style>

