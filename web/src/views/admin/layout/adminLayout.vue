<template>
  <a-layout id="components-layout-demo-custom-trigger">
    <a-layout-header style="background: #fff; padding: 0">
      <Header />
    </a-layout-header>
    <a-layout>
      <a-layout-sider v-model="collapsed" collapsible>
        <div class="logo" />
        <SiderBar/>
      </a-layout-sider>
      <a-layout-content :style="{ margin: '24px 16px', minHeight: '100px' }">
        <router-view/>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
import Header from '@/views/admin/components/header'
import SiderBar from '@/views/admin/components/siderBar'
export default {
  components: {
    SiderBar,
    Header
  },
  data () {
    return {
      collapsed: false
    }
  }
}
</script>
<style>

#components-layout-demo-custom-trigger {
  height: 100%;
}
#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 8px;
  margin: 16px;
}
</style>
