<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo">
            <h2>🏛️ 乐拍拍</h2>
          </div>
          
          <!-- 桌面端导航 -->
          <div class="nav-menu desktop-nav">
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

          <!-- 桌面端用户信息 -->
          <div class="user-info desktop-user">
            <el-dropdown v-if="isAuthenticated" @command="handleCommand">
              <span class="user-dropdown">
                <span class="username">{{ userInfo?.username || '请登录' }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <div v-else class="auth-buttons">
              <el-button @click="$router.push('/login')" type="primary" size="small">登录</el-button>
              <el-button @click="$router.push('/register')" size="small">注册</el-button>
            </div>
          </div>

          <!-- 移动端汉堡菜单 -->
          <div class="mobile-menu-btn" @click="toggleMobileMenu">
            <el-icon :size="24"><Menu /></el-icon>
          </div>
        </div>
      </el-header>

      <!-- 移动端抽屉菜单 -->
      <el-drawer
        v-model="mobileMenuVisible"
        direction="rtl"
        size="70%"
        :show-close="false"
      >
        <template #header>
          <div class="mobile-drawer-header">
            <span class="drawer-title">🏛️ 乐拍拍</span>
          </div>
        </template>
        <div class="mobile-menu-content">
          <!-- 用户信息 -->
          <div class="mobile-user-info">
            <div v-if="isAuthenticated" class="user-profile">
              <div class="avatar-circle">{{ userInfo?.username?.charAt(0) || 'U' }}</div>
              <span class="mobile-username">{{ userInfo?.username || '用户' }}</span>
            </div>
            <div v-else class="mobile-auth-buttons">
              <el-button @click="goToPage('/login')" type="primary" size="large">登录</el-button>
              <el-button @click="goToPage('/register')" size="large">注册</el-button>
            </div>
          </div>
          
          <el-divider />

          <!-- 导航菜单 -->
          <el-menu
            :default-active="activeMenu"
            class="mobile-nav-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/create" v-if="isAuthenticated">
              <el-icon><Plus /></el-icon>
              <span>发布拍卖</span>
            </el-menu-item>
            <el-menu-item index="/my-auctions" v-if="isAuthenticated">
              <el-icon><Goods /></el-icon>
              <span>我的拍卖</span>
            </el-menu-item>
            <el-menu-item index="/my-bids" v-if="isAuthenticated">
              <el-icon><PriceTag /></el-icon>
              <span>我的竞拍</span>
            </el-menu-item>
          </el-menu>

          <el-divider v-if="isAuthenticated" />

          <!-- 退出登录 -->
          <div v-if="isAuthenticated" class="mobile-logout">
            <el-button @click="handleLogout" type="danger" plain style="width: 100%">
              <el-icon><SwitchButton /></el-icon>
              <span>退出登录</span>
            </el-button>
          </div>
        </div>
      </el-drawer>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from './store'
import { ArrowDown, Menu, HomeFilled, Plus, Goods, PriceTag, SwitchButton } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    ArrowDown,
    Menu,
    HomeFilled,
    Plus,
    Goods,
    PriceTag,
    SwitchButton
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const store = useStore()
    const mobileMenuVisible = ref(false)

    // store.isAuthenticated 本身已经是 computed，直接使用即可
    const isAuthenticated = store.isAuthenticated
    const userInfo = store.userInfo

    const activeMenu = computed(() => route.path)

    const handleCommand = (command) => {
      if (command === 'logout') {
        store.logout()
        router.push('/')
      }
    }

    const toggleMobileMenu = () => {
      mobileMenuVisible.value = !mobileMenuVisible.value
    }

    const handleMenuSelect = (index) => {
      router.push(index)
      mobileMenuVisible.value = false
    }

    const goToPage = (path) => {
      router.push(path)
      mobileMenuVisible.value = false
    }

    const handleLogout = () => {
      store.logout()
      router.push('/')
      mobileMenuVisible.value = false
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
      mobileMenuVisible,
      handleCommand,
      toggleMobileMenu,
      handleMenuSelect,
      goToPage,
      handleLogout
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
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  width: 100%;
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
  width: 100%;
  justify-content: center;
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

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.el-main {
  padding: 24px;
  min-height: calc(100vh - 64px);
  margin-top: 64px;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background 0.3s;
}

.mobile-menu-btn:hover {
  background: #f5f5f5;
}

/* 移动端抽屉内容 */
.mobile-drawer-header {
  font-size: 20px;
  font-weight: 600;
  color: #667eea;
}

.drawer-title {
  font-size: 20px;
  font-weight: 600;
}

.mobile-menu-content {
  padding: 0 12px;
}

.mobile-user-info {
  padding: 12px 0;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 600;
}

.mobile-username {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.mobile-auth-buttons {
  display: flex;
  flex-direction: row;
  gap: 12px;
  width: 100%;
}

.mobile-auth-buttons .el-button {
  width: 100%;
}

.mobile-nav-menu {
  border: none;
}

.mobile-logout {
  padding: 12px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }

  .logo h2 {
    font-size: 18px;
  }

  /* 隐藏桌面端导航 */
  .desktop-nav,
  .desktop-user {
    display: none !important;
  }

  /* 显示移动端菜单按钮 */
  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .el-main {
    padding: 16px;
    margin-top: 64px;
  }
}

/* 平板适配 */
@media (min-width: 769px) and (max-width: 1024px) {
  .header-content {
    padding: 0 20px;
  }

  .header-menu {
    font-size: 14px;
  }

  .el-main {
    padding: 20px;
  }
}

/* 大屏适配 */
@media (min-width: 1025px) {
  .mobile-menu-btn {
    display: none;
  }
}
</style>

