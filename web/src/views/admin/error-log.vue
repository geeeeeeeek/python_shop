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
import {listApi} from '@/api/admin/error-log'

const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '请求方式',
    dataIndex: 'method',
    key: 'method',
    align: 'center'
  },
  {
    title: '请求URL',
    dataIndex: 'url',
    key: 'url',
    align: 'center'
  },
  {
    title: '异常信息',
    dataIndex: 'content',
    key: 'content'
  },
  {
    title: '操作IP',
    dataIndex: 'ip',
    key: 'ip',
    align: 'center'
  },
  {
    title: '操作时间',
    dataIndex: 'log_time',
    key: 'log_time',
    align: 'center'
  }
]

export default {
  name: 'ErrorLog',
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
