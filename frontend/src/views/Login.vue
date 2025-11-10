<template>
  <div class="login-page">
    <div class="login-container">
      <el-card class="login-card">
        <template #header>
          <div class="card-header">
            <h2>登录</h2>
          </div>
        </template>
        <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
          <el-form-item label="用户名/邮箱" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名或邮箱"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              style="width: 100%"
            >
              登录
            </el-button>
          </el-form-item>
          <el-form-item>
            <div class="register-link">
              还没有账号？
              <el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '../store'
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const store = useStore()
    const formRef = ref(null)
    const loading = ref(false)
    const form = reactive({
      username: '',
      password: ''
    })

    const rules = {
      username: [
        { required: true, message: '请输入用户名或邮箱', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 8, message: '密码至少8位', trigger: 'blur' }
      ]
    }

    const handleLogin = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          const result = await store.login(form.username, form.password)
          loading.value = false
          
          if (result.success) {
            ElMessage.success('登录成功')
            router.push('/')
          } else {
            ElMessage.error(result.error || '登录失败')
          }
        }
      })
    }

    return {
      formRef,
      form,
      rules,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.register-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-page {
    padding: 16px;
  }

  .login-container {
    max-width: 100%;
  }

  .login-card {
    border-radius: 8px;
  }

  .card-header h2 {
    font-size: 20px;
  }
}
</style>

