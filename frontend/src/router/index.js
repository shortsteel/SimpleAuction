import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AuctionDetail from '../views/AuctionDetail.vue'
import CreateAuction from '../views/CreateAuction.vue'
import MyAuctions from '../views/MyAuctions.vue'
import MyBids from '../views/MyBids.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/auction/:id',
    name: 'AuctionDetail',
    component: AuctionDetail
  },
  {
    path: '/create',
    name: 'CreateAuction',
    component: CreateAuction,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-auctions',
    name: 'MyAuctions',
    component: MyAuctions,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-bids',
    name: 'MyBids',
    component: MyBids,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    // 如果需要认证但没有token，跳转到登录页
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    // 如果已登录，访问登录/注册页时跳转到首页
    next('/')
  } else {
    next()
  }
})

export default router

