<template>
  <div class="my-bids">
    <div class="container">
      <h1 class="page-title">我的竞拍</h1>
      
      <el-card v-loading="loading" class="bids-card">
        <div v-if="bids.length > 0" class="bids-list">
          <el-table :data="bids" style="width: 100%">
            <el-table-column prop="title" label="拍卖标的" width="300">
              <template #default="scope">
                <div class="auction-title-cell" @click="goToDetail(scope.row.auction_id)">
                  <span class="title-text">{{ scope.row.title }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="我的出价" width="150">
              <template #default="scope">
                <span class="bid-amount">¥{{ scope.row.amount.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="current_price" label="当前最高价" width="150">
              <template #default="scope">
                <span class="current-price">¥{{ scope.row.current_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="is_highest" label="状态" width="120">
              <template #default="scope">
                <el-tag v-if="scope.row.is_highest && scope.row.status === 'active'" type="success" size="small">
                  领先中
                </el-tag>
                <el-tag v-else-if="scope.row.status === 'active'" type="warning" size="small">
                  已出价
                </el-tag>
                <el-tag v-else-if="scope.row.status === 'ended'" type="info" size="small">
                  已结束
                </el-tag>
                <el-tag v-else type="danger" size="small">
                  已流拍
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="time_left" label="剩余时间" width="200">
              <template #default="scope">
                <span v-if="scope.row.status === 'active' && scope.row.time_left > 0">
                  {{ formatTimeLeft(scope.row.time_left) }}
                </span>
                <span v-else-if="scope.row.status === 'ended'">
                  已结束
                </span>
                <span v-else>
                  已流拍
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="出价时间" width="180">
              <template #default="scope">
                {{ formatDateTime(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click="goToDetail(scope.row.auction_id)"
                >
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-empty v-else description="您还没有参与任何竞拍"></el-empty>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'

export default {
  name: 'MyBids',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const bids = ref([])

    const loadBids = async () => {
      loading.value = true
      try {
        const response = await api.get('/auctions/my/bids')
        bids.value = response.data.bids
      } catch (error) {
        ElMessage.error('加载我的竞拍失败')
      } finally {
        loading.value = false
      }
    }

    const goToDetail = (id) => {
      router.push(`/auction/${id}`)
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

    const formatDateTime = (dateTime) => {
      return new Date(dateTime).toLocaleString('zh-CN')
    }

    onMounted(() => {
      loadBids()
    })

    return {
      loading,
      bids,
      loadBids,
      goToDetail,
      formatTimeLeft,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.my-bids {
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

.bids-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.auction-title-cell {
  cursor: pointer;
  color: #667eea;
  transition: color 0.3s;
}

.auction-title-cell:hover {
  color: #764ba2;
  text-decoration: underline;
}

.title-text {
  font-weight: 500;
}

.bid-amount {
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
}

.current-price {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}
</style>

