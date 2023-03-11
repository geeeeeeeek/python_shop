<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
<!--        <a-button type="primary" @click="handleAdd">模拟借书</a-button>-->
      </a-space>
    </div>
    <div class="table-wrap" ref="tableWrap">
      <a-table
        size="middle"
        rowKey="id"
        :loading="loading"
        :columns="columns"
        :data-source="data"
        :scroll="{ x: 'max-content' }"
        :row-selection="rowSelection()"
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
        <span slot="status" slot-scope="text">
          <a-tag :color="text === '1'? '#2db7f5':'#87d068'">
            {{text === '1'? '借出':'已还'}}
          </a-tag>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a :disabled="record.status === '2'" @click="handleReturn(record)">还书</a>
            <a :disabled="record.delayed || record.status === '2'" @click="handleDelay(record)">延期</a>
          </a-space>
        </span>
      </a-table>
    </div>
  </div>
</template>

<script>
import {listApi, createApi, updateApi, returnThingApi, delayApi} from '@/api/admin/borrow'

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
    title: '商品',
    dataIndex: 'title',
    key: 'title',
    align: 'center'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    filters: [
      {text: '借出', value: '1'},
      {text: '已还', value: '2'}
    ],
    onFilter: (value, record) => record.status.includes(value),
    // customRender: (text) => text === '1' ? '借出' : '已还'
    scopedSlots: {customRender: 'status'}
  },
  {
    title: '借出时间',
    dataIndex: 'borrow_time',
    key: 'borrow_time',
    align: 'center'
  },
  {
    title: '应还时间',
    dataIndex: 'expect_time',
    key: 'expect_time',
    align: 'center'
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: {customRender: 'operation'}
  }
]

export default {
  name: 'Borrow',
  data() {
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
    getList() {
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
    rowSelection() {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          this.selectedRowKeys = selectedRowKeys
        }
      }
    },
    // 还书
    handleReturn(record) {
      const that = this
      this.$confirm({
        title: '确定还书?',
        onOk() {
          returnThingApi({
            id: record.id
          }, {
            thing: record.thing,
            status: '2'
          }).then(res => {
            that.$message.success('还书成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '还书失败')
          })
        }
      })
    },
    // 延期
    handleDelay (record) {
      const that = this
      this.$confirm({
        title: '确定延期?',
        content: '延期30天',
        onOk () {
          delayApi({
            id: record.id
          }, {}).then(res => {
            that.$message.success('延期成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '延期失败')
          })
        }
      })
    }
  },
  mounted() {
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
