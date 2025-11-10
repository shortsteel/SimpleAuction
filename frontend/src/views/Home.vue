<template>
  <div class="home">
    <div class="container">
      <h1 class="page-title">拍卖列表</h1>
      
      <!-- 筛选和排序 -->
      <el-card class="filter-card">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" class="filter-item">
            <el-select v-model="filters.status" placeholder="筛选状态" clearable @change="loadAuctions" style="width: 100%">
              <el-option label="全部" value=""></el-option>
              <el-option label="进行中" value="active"></el-option>
              <el-option label="已结束" value="ended"></el-option>
              <el-option label="流拍" value="no_bid"></el-option>
            </el-select>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" class="filter-item">
            <el-select v-model="filters.orderBy" placeholder="排序方式" @change="loadAuctions" style="width: 100%">
              <el-option label="最新发布" value="created_at"></el-option>
              <el-option label="即将结束" value="end_time"></el-option>
            </el-select>
          </el-col>
          <el-col :xs="24" :sm="24" :md="8" class="filter-item">
            <el-button type="primary" @click="loadAuctions" :loading="loading" style="width: 100%">刷新</el-button>
          </el-col>
        </el-row>
      </el-card>

      <!-- 拍卖列表 -->
      <div v-loading="loading" class="auction-list">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="8" v-for="auction in auctions" :key="auction.id" class="auction-item">
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
                <div class="auction-seller">
                  <span class="seller-label">发布者：</span>
                  <span class="seller-name">{{ auction.seller_username || '未知' }}</span>
                </div>
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
                  <span class="time-left ended" v-else-if="auction.status === 'ended'">
                    已成交
                  </span>
                  <span class="time-left no-bid" v-else-if="auction.status === 'no_bid'">
                    无人出价
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 分页 -->
        <el-pagination
          v-if="pagination.total > 0"
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.per_page"
          :total="pagination.total"
          :page-sizes="[12, 24, 48]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
          class="pagination"
        />
      </div>

      <!-- 空状态 -->
      <el-empty v-if="!loading && auctions.length === 0" description="暂无拍卖"></el-empty>
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
  name: 'Home',
  components: {
    Picture
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const auctions = ref([])
    const filters = ref({
      status: '',
      orderBy: 'created_at'
    })
    const pagination = ref({
      page: 1,
      per_page: 12,
      total: 0
    })

    const loadAuctions = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.value.page,
          per_page: pagination.value.per_page,
          order_by: filters.value.orderBy
        }
        if (filters.value.status) {
          params.status = filters.value.status
        }
        const response = await api.get('/auctions', { params })
        auctions.value = response.data.auctions
        pagination.value = {
          page: response.data.pagination.page,
          per_page: response.data.pagination.per_page,
          total: response.data.pagination.total
        }
      } catch (error) {
        console.error('加载拍卖列表失败:', error)
        ElMessage.error('加载拍卖列表失败')
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
        'active': '🔥 进行中',
        'ended': '✅ 已结束',
        'no_bid': '❌ 流拍'
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

    const handleSizeChange = (size) => {
      pagination.value.per_page = size
      pagination.value.page = 1
      loadAuctions()
    }

    const handlePageChange = (page) => {
      pagination.value.page = page
      loadAuctions()
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
      filters,
      pagination,
      loadAuctions,
      goToDetail,
      getStatusType,
      getStatusText,
      formatTimeLeft,
      handleSizeChange,
      handlePageChange,
      handleImageError
    }
  }
}
</script>

<style scoped>
.home {
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

.filter-card {
  margin-bottom: 24px;
}

.filter-item {
  margin-bottom: 12px;
}

.auction-list {
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

.auction-seller {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}

.seller-label {
  color: #999;
  margin-right: 4px;
}

.seller-name {
  color: #333;
  font-weight: 500;
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

.time-left.ended {
  color: #67c23a;
  font-weight: 500;
}

.time-left.no-bid {
  color: #e6a23c;
  font-weight: 500;
}

.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-title {
    font-size: 24px;
    margin-bottom: 16px;
  }

  .filter-card {
    margin-bottom: 16px;
  }

  .filter-item {
    margin-bottom: 8px;
  }

  .filter-item:last-child {
    margin-bottom: 0;
  }

  .auction-item {
    margin-bottom: 16px;
  }

  .auction-image {
    height: 180px;
  }

  .auction-title {
    font-size: 16px;
  }

  .pagination {
    margin-top: 24px;
    padding: 12px;
  }

  /* 简化分页显示 */
  .pagination :deep(.el-pagination__sizes),
  .pagination :deep(.el-pagination__jump) {
    display: none;
  }
}

/* 平板适配 */
@media (min-width: 769px) and (max-width: 1024px) {
  .auction-image {
    height: 180px;
  }
}
</style>

