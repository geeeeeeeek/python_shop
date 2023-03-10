<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
        <a-input-search addon-before="查询" enter-button @search="onSearch" />
      </a-space>
    </div>
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
import {listApi} from '@/api/admin/op-log'

const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '请求方式',
    dataIndex: 're_method',
    key: 're_method',
    align: 'center'
  },
  {
    title: '请求URL',
    dataIndex: 're_url',
    key: 're_url',
    align: 'center'
  },
  // {
  //   title: '请求参数',
  //   dataIndex: 're_content',
  //   key: 're_content'
  // },
  {
    title: '操作IP',
    dataIndex: 're_ip',
    key: 're_ip',
    align: 'center'
  },
  {
    title: '操作时间',
    dataIndex: 're_time',
    key: 're_time',
    align: 'center'
  },
  {
    title: '耗时',
    dataIndex: 'access_time',
    key: 'access_time',
    align: 'center',
    customRender: (text) => text + 'ms'
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
    onSearch (value) {
      this.page = 1
      this.getList()
    },
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
    }
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
