<template>
  <div class="auction-detail">
    <div class="container" v-loading="loading">
      <el-button @click="$router.back()" class="back-btn" type="text">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>

      <div v-if="auction" class="detail-content">
        <el-row :gutter="24">
          <!-- 左侧：图片和基本信息 -->
          <el-col :span="16">
            <el-card class="image-card">
              <div class="auction-images">
                <el-image
                  v-if="auction.images && auction.images.length > 0"
                  :src="currentImage"
                  fit="contain"
                  class="main-image"
                />
                <div v-else class="no-image">
                  <el-icon :size="120"><Picture /></el-icon>
                  <p>暂无图片</p>
                </div>
              </div>
              <div v-if="auction.images && auction.images.length > 1" class="image-thumbs">
                <el-image
                  v-for="(img, index) in auction.images"
                  :key="index"
                  :src="img"
                  fit="cover"
                  class="thumb-image"
                  :class="{ active: currentImage === img }"
                  @click="currentImage = img"
                />
              </div>
            </el-card>

            <el-card class="description-card">
              <h2>{{ auction.title }}</h2>
              <p class="description">{{ auction.description }}</p>
            </el-card>

            <el-card class="bid-history-card">
              <template #header>
                <h3>出价历史</h3>
              </template>
              <el-table :data="auction.bid_history" style="width: 100%">
                <el-table-column prop="amount" label="出价金额" width="150">
                  <template #default="scope">
                    <span class="bid-amount">¥{{ scope.row.amount.toFixed(2) }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="bidder" label="出价者" width="150" />
                <el-table-column prop="created_at" label="出价时间" />
              </el-table>
              <el-empty v-if="auction.bid_history.length === 0" description="暂无出价记录"></el-empty>
            </el-card>
          </el-col>

          <!-- 右侧：出价区域 -->
          <el-col :span="8">
            <el-card class="bid-card">
              <div class="price-info">
                <div class="price-item">
                  <span class="price-label">起拍价</span>
                  <span class="price-value">¥{{ auction.starting_price.toFixed(2) }}</span>
                </div>
                <div class="price-item current">
                  <span class="price-label">当前最高价</span>
                  <span class="price-value">¥{{ auction.current_price.toFixed(2) }}</span>
                </div>
                <div v-if="auction.current_bidder" class="bidder-info">
                  <span class="bidder-label">当前最高出价者：</span>
                  <span class="bidder-name">{{ auction.current_bidder.username }}</span>
                </div>
              </div>

              <el-divider />

              <div class="time-info">
                <el-tag :type="auction.status === 'active' ? 'success' : 'info'" size="large">
                  {{ getStatusText(auction.status) }}
                </el-tag>
                <div v-if="auction.status === 'active'" class="time-left">
                  <p>剩余时间：</p>
                  <p class="time-value">{{ formatTimeLeft(auction.time_left) }}</p>
                </div>
                <div v-else class="time-left">
                  <p>结束时间：{{ formatDateTime(auction.end_time) }}</p>
                </div>
              </div>

              <el-divider />

              <!-- 出价区域 -->
              <div v-if="auction.status === 'active' && canBid" class="bid-section">
                <el-form :model="bidForm" :rules="bidRules" ref="bidFormRef">
                  <el-form-item prop="amount">
                    <el-input-number
                      v-model="bidForm.amount"
                      :min="auction.current_price + 0.01"
                      :precision="2"
                      :step="1"
                      placeholder="请输入出价金额"
                      style="width: 100%"
                      size="large"
                    />
                    <p class="hint">最低出价：¥{{ (auction.current_price + 0.01).toFixed(2) }}</p>
                  </el-form-item>
                  <el-form-item>
                    <el-button
                      type="primary"
                      size="large"
                      :loading="bidding"
                      @click="handleBid"
                      style="width: 100%"
                    >
                      立即出价
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>

              <div v-else-if="!canBid && auction.status === 'active'" class="bid-section">
                <el-alert
                  :title="isOwner ? '不能对自己的拍卖出价' : '请先登录'"
                  type="warning"
                  :closable="false"
                />
              </div>

              <div v-else class="bid-section">
                <el-alert
                  :title="'拍卖已' + getStatusText(auction.status)"
                  type="info"
                  :closable="false"
                />
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from '../store'
import api from '../api'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Picture } from '@element-plus/icons-vue'

export default {
  name: 'AuctionDetail',
  components: {
    ArrowLeft,
    Picture
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const store = useStore()
    const loading = ref(false)
    const bidding = ref(false)
    const auction = ref(null)
    const currentImage = ref('')
    const bidForm = ref({
      amount: null
    })
    const bidFormRef = ref(null)
    let timer = null

    const isAuthenticated = computed(() => store.isAuthenticated)
    const userInfo = computed(() => store.userInfo)
    const isOwner = computed(() => auction.value && userInfo.value && auction.value.seller_id === userInfo.value.id)
    const canBid = computed(() => isAuthenticated.value && !isOwner.value)

    const bidRules = {
      amount: [
        { required: true, message: '请输入出价金额', trigger: 'blur' }
      ]
    }

    const loadAuction = async () => {
      loading.value = true
      try {
        const response = await api.get(`/auctions/${route.params.id}`)
        auction.value = response.data
        if (auction.value.images && auction.value.images.length > 0) {
          currentImage.value = auction.value.images[0]
        }
        if (canBid.value && auction.value.status === 'active') {
          bidForm.value.amount = auction.value.current_price + 0.01
        }
      } catch (error) {
        ElMessage.error('加载拍卖详情失败')
        router.push('/')
      } finally {
        loading.value = false
      }
    }

    const handleBid = async () => {
      if (!bidFormRef.value) return
      
      await bidFormRef.value.validate(async (valid) => {
        if (valid) {
          bidding.value = true
          try {
            await api.post(`/auctions/${route.params.id}/bids`, {
              amount: bidForm.value.amount
            })
            ElMessage.success('出价成功！')
            await loadAuction()
            bidForm.value.amount = auction.value.current_price + 0.01
          } catch (error) {
            ElMessage.error(error.response?.data?.error || '出价失败')
          } finally {
            bidding.value = false
          }
        }
      })
    }

    const getStatusText = (status) => {
      const texts = {
        'active': '进行中',
        'ended': '已结束',
        'no_bid': '流拍'
      }
      return texts[status] || status
    }

    const formatTimeLeft = (seconds) => {
      if (seconds <= 0) return '已结束'
      const days = Math.floor(seconds / 86400)
      const hours = Math.floor((seconds % 86400) / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      if (days > 0) return `${days}天${hours}小时${minutes}分钟`
      if (hours > 0) return `${hours}小时${minutes}分钟${secs}秒`
      return `${minutes}分钟${secs}秒`
    }

    const formatDateTime = (dateTime) => {
      return new Date(dateTime).toLocaleString('zh-CN')
    }

    const updateTimer = () => {
      if (auction.value && auction.value.status === 'active') {
        timer = setInterval(() => {
          if (auction.value.time_left > 0) {
            auction.value.time_left--
          } else {
            auction.value.status = 'ended'
            clearInterval(timer)
          }
        }, 1000)
      }
    }

    onMounted(() => {
      loadAuction()
      updateTimer()
    })

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer)
      }
    })

    return {
      loading,
      bidding,
      auction,
      currentImage,
      bidForm,
      bidFormRef,
      bidRules,
      isAuthenticated,
      userInfo,
      isOwner,
      canBid,
      handleBid,
      getStatusText,
      formatTimeLeft,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.auction-detail {
  min-height: calc(100vh - 64px);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.back-btn {
  margin-bottom: 24px;
  color: white;
  font-size: 16px;
}

.detail-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
}

.image-card {
  margin-bottom: 24px;
}

.auction-images {
  margin-bottom: 16px;
}

.main-image {
  width: 100%;
  height: 500px;
  border-radius: 8px;
  background: #f5f5f5;
}

.no-image {
  width: 100%;
  height: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #ccc;
  background: #f5f5f5;
  border-radius: 8px;
}

.image-thumbs {
  display: flex;
  gap: 12px;
  overflow-x: auto;
}

.thumb-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.thumb-image.active {
  border-color: #667eea;
}

.description-card {
  margin-bottom: 24px;
}

.description-card h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.description {
  font-size: 16px;
  color: #666;
  line-height: 1.8;
  white-space: pre-wrap;
}

.bid-history-card h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.bid-amount {
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
}

.bid-card {
  position: sticky;
  top: 24px;
}

.price-info {
  margin-bottom: 16px;
}

.price-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.price-item.current {
  border-bottom: 2px solid #667eea;
}

.price-label {
  font-size: 14px;
  color: #666;
}

.price-value {
  font-size: 24px;
  font-weight: 600;
  color: #667eea;
}

.bidder-info {
  margin-top: 12px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 14px;
}

.bidder-label {
  color: #666;
}

.bidder-name {
  color: #333;
  font-weight: 600;
}

.time-info {
  text-align: center;
  margin-bottom: 16px;
}

.time-left {
  margin-top: 16px;
}

.time-left p {
  margin: 8px 0;
  color: #666;
}

.time-value {
  font-size: 20px;
  font-weight: 600;
  color: #667eea;
}

.bid-section {
  margin-top: 16px;
}

.hint {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}
</style>

