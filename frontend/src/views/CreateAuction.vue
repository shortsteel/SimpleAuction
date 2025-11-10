<template>
  <div class="create-auction">
    <div class="container">
      <h1 class="page-title">发布拍卖</h1>
      
      <el-card class="form-card">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
          <el-form-item label="标的名称" prop="title">
            <el-input
              v-model="form.title"
              placeholder="请输入标的名称"
              size="large"
              maxlength="100"
              show-word-limit
            />
          </el-form-item>
          
          <el-form-item label="标的描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="6"
              placeholder="请输入标的描述"
              maxlength="1000"
              show-word-limit
            />
          </el-form-item>
          
          <el-form-item label="起拍价" prop="starting_price">
            <el-input-number
              v-model="form.starting_price"
              :min="0.01"
              :precision="2"
              :step="1"
              placeholder="请输入起拍价"
              size="large"
              style="width: 100%"
            />
            <p class="hint">起拍价必须大于0</p>
          </el-form-item>
          
          <el-form-item label="最低加价幅度" prop="min_increment">
            <el-input-number
              v-model="form.min_increment"
              :min="0.01"
              :precision="2"
              :step="0.01"
              placeholder="请输入最低加价幅度"
              size="large"
              style="width: 100%"
            />
            <p class="hint">每次出价必须至少增加此金额，默认为0.01</p>
          </el-form-item>
          
          <el-form-item label="拍卖结束时间" prop="end_time">
            <el-date-picker
              v-model="form.end_time"
              type="datetime"
              placeholder="选择拍卖结束时间"
              size="large"
              style="width: 100%"
              :disabled-date="disabledDate"
              :disabled-time="disabledTime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DDTHH:mm:ss"
            />
            <div class="time-shortcuts">
              <el-button size="small" @click="setEndTime(1)">1小时后</el-button>
              <el-button size="small" @click="setEndTime(3)">3小时后</el-button>
              <el-button size="small" @click="setEndTime(6)" >6小时后</el-button>
              <el-button size="small" @click="setEndTime(12)">12小时后</el-button>
              <el-button size="small" @click="setEndTime(24)">1天后</el-button>
              <el-button size="small" @click="setEndTime(72)">3天后</el-button>
              <el-button size="small" @click="setEndTime(168)">7天后</el-button>
            </div>
            <p class="hint">结束时间必须至少在未来1小时后，默认6小时</p>
          </el-form-item>
          
          <el-form-item label="标的图片" prop="images">
            <el-upload
              v-model:file-list="fileList"
              action="#"
              list-type="picture-card"
              :auto-upload="false"
              :limit="5"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :on-change="handleChange"
              :before-upload="beforeUpload"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
            <p class="hint">最多上传5张图片，每张图片不超过2MB</p>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="submitting"
              @click="handleSubmit"
            >
              发布拍卖
            </el-button>
            <el-button size="large" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

export default {
  name: 'CreateAuction',
  components: {
    Plus
  },
  setup() {
    const router = useRouter()
    const formRef = ref(null)
    const submitting = ref(false)
    const fileList = ref([])
    const form = reactive({
      title: '',
      description: '',
      starting_price: null,
      min_increment: 0.01,
      end_time: '',
      images: []
    })

    // 将Date对象格式化为本地时间字符串 YYYY-MM-DDTHH:mm:ss
    const formatLocalDateTime = (date) => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`
    }

    // 初始化默认结束时间为6小时后
    const initDefaultEndTime = () => {
      const now = new Date()
      const defaultEndTime = new Date(now.getTime() + 6 * 3600000) // 6小时后
      form.end_time = formatLocalDateTime(defaultEndTime)
    }

    // 设置结束时间的快捷方法
    const setEndTime = (hours) => {
      const now = new Date()
      const endTime = new Date(now.getTime() + hours * 3600000)
      form.end_time = formatLocalDateTime(endTime)
    }

    onMounted(() => {
      initDefaultEndTime()
    })

    const rules = {
      title: [
        { required: true, message: '请输入标的名称', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '请输入标的描述', trigger: 'blur' }
      ],
      starting_price: [
        { required: true, message: '请输入起拍价', trigger: 'blur' },
        { type: 'number', min: 0.01, message: '起拍价必须大于0', trigger: 'blur' }
      ],
      min_increment: [
        { required: true, message: '请输入最低加价幅度', trigger: 'blur' },
        { type: 'number', min: 0.01, message: '最低加价幅度必须大于0', trigger: 'blur' }
      ],
      end_time: [
        { required: true, message: '请选择拍卖结束时间', trigger: 'blur' }
      ]
    }

    const disabledDate = (time) => {
      // 只能选择今天及以后的日期
      return time.getTime() < Date.now() - 8.64e7
    }

    const disabledTime = (time) => {
      // 如果选择的是今天，则禁用今天之前的时间
      const now = new Date()
      const selectedDate = new Date(time)
      if (selectedDate.toDateString() === now.toDateString()) {
        const oneHourLater = new Date(now.getTime() + 3600000)
        return {
          disabledHours: () => {
            const hours = []
            for (let i = 0; i < oneHourLater.getHours(); i++) {
              hours.push(i)
            }
            return hours
          },
          disabledMinutes: (hour) => {
            if (hour === oneHourLater.getHours()) {
              const minutes = []
              for (let i = 0; i <= oneHourLater.getMinutes(); i++) {
                minutes.push(i)
              }
              return minutes
            }
            return []
          }
        }
      }
      return {}
    }

    const handlePreview = (file) => {
      // 预览图片
      console.log('Preview:', file)
    }

    const handleRemove = (file) => {
      const index = fileList.value.findIndex(item => item.uid === file.uid)
      if (index > -1) {
        fileList.value.splice(index, 1)
        form.images.splice(index, 1)
      }
    }

    const handleChange = (file) => {
      // 将文件转换为base64
      const reader = new FileReader()
      reader.onload = (e) => {
        if (!form.images.includes(e.target.result)) {
          form.images.push(e.target.result)
        }
      }
      reader.readAsDataURL(file.raw)
    }

    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isImage) {
        ElMessage.error('只能上传图片文件')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过2MB')
        return false
      }
      return false // 阻止自动上传
    }

    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          // 验证结束时间
          const endTime = new Date(form.end_time)
          const now = new Date()
          const oneHourLater = new Date(now.getTime() + 3600000)
          
          if (endTime <= oneHourLater) {
            ElMessage.error('拍卖结束时间必须至少在未来1小时后')
            return
          }

          submitting.value = true
          try {
            const response = await api.post('/auctions', {
              title: form.title,
              description: form.description,
              starting_price: form.starting_price,
              min_increment: form.min_increment,
              end_time: form.end_time,
              images: form.images
            })
            ElMessage.success('发布成功！')
            router.push(`/auction/${response.data.auction.id}`)
          } catch (error) {
            ElMessage.error(error.response?.data?.error || '发布失败')
          } finally {
            submitting.value = false
          }
        }
      })
    }

    const handleReset = () => {
      formRef.value?.resetFields()
      fileList.value = []
      form.images = []
    }

    return {
      formRef,
      form,
      rules,
      submitting,
      fileList,
      disabledDate,
      disabledTime,
      setEndTime,
      handlePreview,
      handleRemove,
      handleChange,
      beforeUpload,
      handleSubmit,
      handleReset
    }
  }
}
</script>

<style scoped>
.create-auction {
  min-height: calc(100vh - 64px);
}

.container {
  max-width: 800px;
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

.form-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.hint {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  margin-bottom: 0;
}

.time-shortcuts {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>

