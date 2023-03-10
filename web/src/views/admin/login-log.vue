<template>
  <div class="page-view">
    <div class="table-wrap" ref="tableWrap">
      <a-table
        size="middle"
        rowKey="id"
        bordered
        :loading="loading"
        :columns="columns"
        :data-source="data"
        :scroll="{ x: 'max-content' }"
        :pagination="{
          size: 'default',
          current: page,
          pageSize: pageSize,
          onChange: (current) => page = current,
          pageSizeOptions: ['10', '20', '30', '40'],
          showSizeChanger: true,
          showTotal: (total) => `共${total}条数据`
        }"
      >
      </a-table>
    </div>
  </div>
</template>

<script>
import {listApi} from '@/api/admin/login-log'

const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '用户',
    dataIndex: 'username',
    key: 'username',
    align: 'center'
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    key: 'ip',
    align: 'center'
  },
  {
    title: 'User-Agent',
    dataIndex: 'ua',
    key: 'ua',
    align: 'center'
  },
  {
    title: '登录时间',
    dataIndex: 'log_time',
    key: 'log_time',
    align: 'center'
  }
]

export default {
  name: 'LoginLog',
  data () {
    return {
      loading: false,
      selectedRowKeys: [],
      columns,
      data: [],
      pageSize: 10,
      page: 1
    }
  },
  methods: {
    getList () {
      this.loading = true
      listApi().then(res => {
        this.loading = false
        res.data.forEach((item, index) => {
          item.index = index + 1
        })
        this.data = res.data
        console.log(res)
      })
    },
  },
  mounted () {
    this.getList()
  }
}
</script>

<style lang="less" scoped>
.table-wrap {
  flex: 1;
}
.page-view {
  min-height: 100%;
  background: #FFF;
  padding: 24px;
  display: flex;
  flex-direction: column;
}
.table-operation {
  height: 50px;
  text-align: right;
}
</style>
