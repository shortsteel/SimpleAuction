<template>
  <div class="my-bids">
    <div class="container">
      <h1 class="page-title">我的竞拍</h1>
      
      <el-card v-loading="loading" class="bids-card">
        <div v-if="bids.length > 0" class="bids-header">
          <el-radio-group v-model="viewMode" class="view-switcher">
            <el-radio-button label="time">按时间顺序</el-radio-button>
            <el-radio-button label="group">按拍卖标的</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 时间顺序视图 -->
        <div v-if="bids.length > 0 && viewMode === 'time'" class="bids-list">
          <el-table :data="bids" style="width: 100%">
            <el-table-column prop="title" label="拍卖标的" width="100">
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
            <el-table-column prop="is_highest" label="状态" width="140">
              <template #default="scope">
                <el-tag v-if="scope.row.is_highest && scope.row.status === 'active'" type="success" size="small">
                  🏆 领先中
                </el-tag>
                <el-tag v-else-if="scope.row.status === 'active'" type="warning" size="small">
                  💰 已出价
                </el-tag>
                <el-tag v-else-if="scope.row.status === 'ended' && scope.row.is_winner" type="success" size="small">
                  ✅ 已中标
                </el-tag>
                <el-tag v-else-if="scope.row.status === 'ended'" type="info" size="small">
                  未中标
                </el-tag>
                <el-tag v-else-if="scope.row.status === 'no_bid'" type="warning" size="small">
                  ❌ 已流拍
                </el-tag>
                <el-tag v-else type="info" size="small">
                  已结束
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
                <span v-else-if="scope.row.status === 'no_bid'">
                  已流拍
                </span>
                <span v-else>
                  已结束
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
        
        <!-- 分组视图 -->
        <div v-if="bids.length > 0 && viewMode === 'group'" class="grouped-bids">
          <div v-for="group in groupedBids" :key="group.auction_id" class="auction-group">
            <div class="group-header" @click="goToDetail(group.auction_id)">
              <div class="group-title">
                <span class="title-text">{{ group.title }}</span>
                <el-tag v-if="group.status === 'active'" type="success" size="small" class="status-tag">
                  🔥 进行中
                </el-tag>
                <el-tag v-else-if="group.status === 'ended'" type="info" size="small" class="status-tag">
                  ✅ 已结束
                </el-tag>
                <el-tag v-else-if="group.status === 'no_bid'" type="warning" size="small" class="status-tag">
                  ❌ 已流拍
                </el-tag>
                <el-tag v-else type="info" size="small" class="status-tag">
                  已结束
                </el-tag>
              </div>
              <div class="group-info">
                <span class="info-item">当前最高价: <strong>¥{{ group.current_price.toFixed(2) }}</strong></span>
                <span v-if="group.status === 'active' && group.time_left > 0" class="info-item">
                  剩余时间: {{ formatTimeLeft(group.time_left) }}
                </span>
              </div>
            </div>
            <div class="group-bids">
              <el-table :data="group.bids" style="width: 100%">
                <el-table-column prop="amount" label="我的出价" width="150">
                  <template #default="scope">
                    <span class="bid-amount">¥{{ scope.row.amount.toFixed(2) }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="is_highest" label="状态" width="140">
                  <template #default="scope">
                    <el-tag v-if="scope.row.is_highest && group.status === 'active'" type="success" size="small">
                      🏆 领先中
                    </el-tag>
                    <el-tag v-else-if="group.status === 'active'" type="warning" size="small">
                      💰 已出价
                    </el-tag>
                    <el-tag v-else-if="group.status === 'ended' && scope.row.is_winner" type="success" size="small">
                      ✅ 已中标
                    </el-tag>
                    <el-tag v-else-if="group.status === 'ended'" type="info" size="small">
                      未中标
                    </el-tag>
                    <el-tag v-else-if="group.status === 'no_bid'" type="warning" size="small">
                      ❌ 已流拍
                    </el-tag>
                    <el-tag v-else type="info" size="small">
                      已结束
                    </el-tag>
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
                      @click="goToDetail(group.auction_id)"
                    >
                      查看详情
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </div>
        
        <el-empty v-if="bids.length === 0" description="您还没有参与任何竞拍"></el-empty>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'

export default {
  name: 'MyBids',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const bids = ref([])
    const viewMode = ref('time')

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

    // 按拍卖标的分组
    const groupedBids = computed(() => {
      const groups = {}
      
      bids.value.forEach(bid => {
        const key = bid.auction_id
        if (!groups[key]) {
          groups[key] = {
            auction_id: bid.auction_id,
            title: bid.title,
            status: bid.status,
            current_price: bid.current_price,
            time_left: bid.time_left,
            bids: []
          }
        }
        groups[key].bids.push(bid)
      })
      
      // 将对象转换为数组，并按每个组的最新出价时间排序
      return Object.values(groups).map(group => {
        // 对每个组内的出价按时间降序、金额降序排序
        group.bids.sort((a, b) => {
          const timeDiff = new Date(b.created_at) - new Date(a.created_at)
          if (timeDiff !== 0) return timeDiff
          return b.amount - a.amount
        })
        return group
      }).sort((a, b) => {
        // 按组内最新出价时间降序排序
        const aLatest = new Date(a.bids[0].created_at)
        const bLatest = new Date(b.bids[0].created_at)
        return bLatest - aLatest
      })
    })

    onMounted(() => {
      loadBids()
    })

    return {
      loading,
      bids,
      viewMode,
      groupedBids,
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

.bids-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.view-switcher {
  margin-bottom: 0;
}

.grouped-bids {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.auction-group {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  background: #fafafa;
}

.group-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 20px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.group-header:hover {
  opacity: 0.9;
}

.group-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.group-title .title-text {
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}

.status-tag {
  margin-left: auto;
}

.group-info {
  display: flex;
  gap: 24px;
  font-size: 14px;
  opacity: 0.95;
}

.info-item {
  display: flex;
  align-items: center;
}

.group-bids {
  background: white;
  padding: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-title {
    font-size: 24px;
    margin-bottom: 16px;
  }

  .bids-card {
    padding: 16px;
    border-radius: 8px;
  }

  .bids-header {
    margin-bottom: 16px;
  }

  /* 表格在移动端优化 */
  .bids-list :deep(.el-table) {
    font-size: 13px;
  }

  .bids-list :deep(.el-table th),
  .bids-list :deep(.el-table td) {
    padding: 8px 5px;
  }

  /* 隐藏部分列以适应小屏幕 */
  .bids-list :deep(.el-table__column--selection),
  .bids-list :deep(.el-table th:nth-child(3)),
  .bids-list :deep(.el-table td:nth-child(3)) {
    display: none;
  }

  /* 分组视图优化 */
  .group-header {
    padding: 12px 16px;
  }

  .group-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .group-title .title-text {
    font-size: 16px;
  }

  .status-tag {
    margin-left: 0;
  }

  .group-info {
    flex-direction: column;
    gap: 8px;
    font-size: 13px;
  }

  /* 分组内的表格 */
  .group-bids :deep(.el-table) {
    font-size: 13px;
  }

  .group-bids :deep(.el-table th),
  .group-bids :deep(.el-table td) {
    padding: 8px 5px;
  }
}

/* 平板适配 */
@media (min-width: 769px) and (max-width: 1024px) {
  .bids-list :deep(.el-table) {
    font-size: 14px;
  }
}
</style>

