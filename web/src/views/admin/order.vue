<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
<!--        <a-button type="primary" @click="handleMockAdd">模拟新增</a-button>-->
        <a-button @click="handleBatchDelete">批量删除</a-button>
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
            {{text === '1'? '待支付': text === '2'? '已支付':'已取消'}}
          </a-tag>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleCancel(record)">取消</a>
            <a @click="handleDelete(record)">删除</a>
          </a-space>
        </span>
      </a-table>
    </div>
  </div>
</template>

<script>
import {listApi, createApi, updateApi, cancelOrderApi, delayApi, deleteApi} from '@/api/admin/order'

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
    align: 'center',
    customRender: (text) => text ? text.substring(0, 10) + '...' : '--'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    scopedSlots: {customRender: 'status'}
  },
  {
    title: '订单时间',
    dataIndex: 'order_time',
    key: 'order_time',
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
  name: 'Order',
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
    rowSelection () {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          this.selectedRowKeys = selectedRowKeys
        }
      }
    },
    handleMockAdd () {
      createApi({
        thing: 1,
        user: 2,
        count: 1
      }).then(res => {
        this.getList()
      }).catch(err => {

      })
    },
    // 取消
    handleCancel (record) {
      const that = this
      this.$confirm({
        title: '确定取消?',
        onOk () {
          cancelOrderApi({
            id: record.id
          }).then(res => {
            that.$message.success('取消成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '取消失败')
          })
        }
      })
    },
    // 删除
    handleDelete (record) {
      const that = this
      this.$confirm({
        title: '确定删除?',
        onOk () {
          deleteApi({
            ids: record.id
          }).then(res => {
            that.$message.success('删除成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '删除失败')
          })
        }
      })
    },
    // 批量删除
    handleBatchDelete () {
      console.log(this.selectedRowKeys)
      if (this.selectedRowKeys.length <= 0) {
        this.$message.warn('请勾选删除项')
        return
      }
      const that = this
      this.$confirm({
        title: '确定删除?',
        onOk () {
          deleteApi({
            ids: that.selectedRowKeys.join(',')
          }).then(res => {
            that.$message.success('删除成功')
            that.selectedRowKeys = []
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '删除失败')
          })
        }
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
