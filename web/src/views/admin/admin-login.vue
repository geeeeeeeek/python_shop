<template>
  <div id="userLayout">
    <div class="user-layout-header">
      <img class="logo" src="@/assets/images/front-logo.png" alt="">
      <span>商城后台管理系统</span>
    </div>
    <div class="container">
      <div class="main">
        <div class="main_right">
          <h2 class="sys_title">管理员登录</h2>
          <a-form-model
            ref="loginForm"
            :model="loginForm"
            :rules="rules"
            :hideRequiredMark="true"
          >
            <a-form-model-item prop="username" label="账号" :colon="false">
              <a-input
                size="large"
                placeholder="请输入登录账号"
                v-model="loginForm.username"
                @pressEnter="handleSubmit">
                <a-icon slot="prefix" type="user" />
              </a-input>
            </a-form-model-item>
            <a-form-model-item prop="password" label="密码" :colon="false">
              <a-input
                size="large"
                type="password"
                placeholder="请输入登录密码"
                v-model="loginForm.password"
                @pressEnter="handleSubmit">
                <a-icon slot="prefix" type="lock" />
              </a-input>
            </a-form-model-item>
            <a-form-model-item style="padding-top: 24px">
              <a-button
                class="login-button"
                type="primary"
                :loading="loginBtn"
                size="large"
                block
                @click="handleSubmit"
              >
                登录
              </a-button>
            </a-form-model-item>
          </a-form-model>
          <div class="error-tip">{{ loginError }}</div>
        </div>
      </div>

    </div>
    <footer class="footer">
      <div class="copyright">
        <span></span>
      </div>
    </footer>
  </div>

</template>

<script>
import { mapActions } from 'vuex'

export default {
  components: {
    // TextField
  },
  data () {
    this.imgUrl = './config/images/login_title.png'
    // this.config = config
    return {
      loginBtn: false,
      loginError: '',
      checked: false,
      loginForm: {
        username: undefined,
        password: undefined
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ...mapActions(['AdminLogin']),
    handleSubmit () {
      this.loginError = ''
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loginBtn = true
          this.handleLogin()
        } else {
          return false
        }
      })
    },
    handleLogin () {
      this.AdminLogin({
        username: this.loginForm.username,
        password: this.loginForm.password
      }).then(() => {
        this.loginSuccess()
      }).catch(error => {
        this.requestFailed(error)
      })
    },
    loginSuccess () {
      this.loginBtn = false
      this.$router.push({ path: '/admin' })
      this.$message.success('登录成功！')
      // satoken
    },
    requestFailed (err) {
      this.loginBtn = false
      this.$message.error(err.msg)
    }
  }
}
</script>

<style lang="less" scoped>
@import url(~@/style/_var.less);

#userLayout {
  position: relative;
  height: 100vh;
  .user-layout-header {
    height: 80px;
    padding: 0 24px;
    color: @heading-color;
    font-size: 28px;
    font-weight: bold;
    line-height: 80px;
    .logo {
      width: 40px;
      height: 40px;
      margin-right: 8px;
      margin-top: -4px;
    }
  }
  .container {
    height: calc(100vh - 160px);
    background-image: url('~@/assets/images/login.png');
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;

    .main {
      position: absolute;
      right: 80px;
      top: 50%;
      display: flex;
      transform: translate(0, -50%);
      border-radius: 8px;
      overflow: hidden;

      .main_right {
        background: #ffffff;
        padding: 24px;
        width: 420px;
        user-select: none;

        .sys_title {
          font-size: 24px;
          color: @heading-color;
          font-weight: bold;
          user-select: none;
          padding-bottom: 8px;
        }
        /deep/ .ant-form-item label {
          font-weight: bold;
        }

        .flex {
          align-items: center;
          display: flex;
          justify-content: space-between;
        }
        .forget_password {
          cursor: pointer;
        }
        .login-button {
          background: linear-gradient(128deg,#00aaeb, #00c1cd 59%, #0ac2b0 100%);
        }
      }
      .error-tip {
        color: @error-color;
        text-align: center;
      }
    }
  }
  .footer {
    height: 80px;
  }
}

</style>
