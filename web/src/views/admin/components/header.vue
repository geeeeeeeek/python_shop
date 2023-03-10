<template>
  <div class="header">
    <img class="header-logo" src="@/assets/images/front-logo.png">
    <span class="header-title">图书后台管理系统</span>
    <div class="empty"></div>
    <span>管理员[{{$store.state.user.adminUserName}}]</span>
    <a class="header-quit" @click="handleLogout">退出</a>
  </div>
</template>

<script>
export default {
  name: 'Header',
  data () {
    return {
      username: ''
    }
  },
  mounted () {
    // this.username = this.$store.state.user.adminUserName
  },
  methods: {
    handleLogout () {
      this.$store.dispatch('AdminLogout').then(res => {
        this.$router.push({path: '/admin-login'})
      })
    }
  }
}
</script>
<style lang="less" scoped>

.header {
  display: flex;
  flex-direction: row;
  align-items: center; // 垂直居中
  padding-left: 24px;
  padding-right: 24px;

  .header-logo {
    width: 32px;
    height: 32px;
    cursor: pointer;
  }

  .header-title {
    margin-left: 16px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
  }

  .empty {
    flex:1;
  }

  .header-quit {
    margin-left: 12px;
  }
}
</style>
