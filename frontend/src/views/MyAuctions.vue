<template>
  <div class="my-auctions">
    <div class="container">
      <h1 class="page-title">我的拍卖</h1>
      
      <el-card v-loading="loading" class="auctions-card">
        <div v-if="auctions.length > 0" class="auctions-list">
          <el-row :gutter="20">
            <el-col :span="8" v-for="auction in auctions" :key="auction.id" class="auction-item">
              <el-card class="auction-card" @click="goToDetail(auction.id)" shadow="hover">
                <div class="auction-image">
                  <img v-if="auction.images && auction.images.length > 0" 
                       :src="auction.images[0]" 
                       alt="拍卖图片"
                       @error="handleImageError">
                  <div v-else class="no-image">
                    <el-icon :size="60"><Picture /></el-icon>
                  </div>
                </div>
                <div class="auction-info">
                  <h3 class="auction-title">{{ auction.title }}</h3>
                  <p class="auction-description">{{ auction.description }}</p>
                  <div class="auction-stats">
                    <div class="stat-item">
                      <span class="stat-label">当前价：</span>
                      <span class="stat-value price">¥{{ auction.current_price.toFixed(2) }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">竞拍者：</span>
                      <span class="stat-value">{{ auction.bidder_count }}人</span>
                    </div>
                  </div>
                  <div class="auction-meta">
                    <el-tag :type="getStatusType(auction.status)" size="small">
                      {{ getStatusText(auction.status) }}
                    </el-tag>
                    <span class="time-left" v-if="auction.status === 'active'">
                      {{ formatTimeLeft(auction.time_left) }}
                    </span>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        <el-empty v-else description="您还没有发布任何拍卖"></el-empty>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'

export default {
  name: 'MyAuctions',
  components: {
    Picture
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const auctions = ref([])

    const loadAuctions = async () => {
      loading.value = true
      try {
        const response = await api.get('/auctions/my/listings')
        auctions.value = response.data.auctions
      } catch (error) {
        ElMessage.error('加载我的拍卖失败')
      } finally {
        loading.value = false
      }
    }

    const goToDetail = (id) => {
      router.push(`/auction/${id}`)
    }

    const getStatusType = (status) => {
      const types = {
        'active': 'success',
        'ended': 'info',
        'no_bid': 'warning'
      }
      return types[status] || 'info'
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
      if (days > 0) return `${days}天${hours}小时`
      if (hours > 0) return `${hours}小时${minutes}分钟`
      return `${minutes}分钟`
    }

    const handleImageError = (e) => {
      e.target.style.display = 'none'
      e.target.parentElement.querySelector('.no-image').style.display = 'flex'
    }

    onMounted(() => {
      loadAuctions()
    })

    return {
      loading,
      auctions,
      loadAuctions,
      goToDetail,
      getStatusType,
      getStatusText,
      formatTimeLeft,
      handleImageError
    }
  }
}
</script>

<style scoped>
.my-auctions {
  min-height: calc(100vh - 64px);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  color: white;
  margin-bottom: 24px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.auctions-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.auctions-list {
  min-height: 400px;
}

.auction-item {
  margin-bottom: 24px;
}

.auction-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.auction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.auction-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 16px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auction-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: #ccc;
}

.auction-info {
  padding: 0 8px;
}

.auction-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.auction-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.auction-stats {
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.stat-label {
  color: #666;
}

.stat-value {
  color: #333;
  font-weight: 600;
}

.price {
  color: #667eea;
  font-size: 18px;
}

.auction-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time-left {
  font-size: 12px;
  color: #999;
}
</style>

