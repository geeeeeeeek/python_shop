<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
        <a-button type="primary" @click="handleAdd">新增</a-button>
        <a-button @click="handleBatchDelete">批量删除</a-button>
        <a-input-search addon-before="商品" enter-button @search="onSearch" @change="onSearchChange" />
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
<!--        <span slot="cover" slot-scope="text">-->
<!--          <img :src="text" style="width: 40px;height: 60px;"/>-->
<!--        </span>-->
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleEdit(record)">编辑</a>
            <a @click="handleDelete(record)">删除</a>
          </a-space>
        </span>
      </a-table>
    </div>
  </div>
</template>

<script>
import {listApi, deleteApi, createApi} from '@/api/admin/thing'
import EditThing from '@/views/admin/model/edit-thing'

const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    width: 60
  },
  {
    title: '名称',
    dataIndex: 'title',
    key: 'title'
  },
  // {
  //   title: '封面',
  //   dataIndex: 'cover',
  //   key: 'cover',
  //   scopedSlots: { customRender: 'cover' }
  // },
  {
    title: '价格',
    dataIndex: 'price',
    key: 'price'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    customRender: (text) => text === '0' ? '上架' : '下架'
  },
  {
    title: '库存',
    dataIndex: 'repertory',
    key: 'repertory'
  },
  {
    title: '简介',
    dataIndex: 'description',
    key: 'description',
    customRender: (text) => text ? text.substring(0, 10) + '...' : '--'
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  name: 'Thing',
  data () {
    return {
      loading: false,
      selectedRowKeys: [],
      columns,
      data: [],
      keyword: undefined,
      pageSize: 10,
      page: 1
    }
  },
  methods: {
    getList () {
      this.loading = true
      listApi({
        keyword: this.keyword
      }).then(res => {
        this.loading = false
        res.data.forEach((item, index) => {
          item.index = index + 1
          if (item.cover) {
            item.cover = this.$BASE_URL + item.cover
          }
        })
        this.data = res.data
        console.log(res)
      }).catch(err => {
        this.$message.error(err.msg)
        this.loading = false
      })
    },
    onSearchChange (e) {
      this.keyword = e.target.value
    },
    onSearch (value) {
      this.getList()
    },
    rowSelection () {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          this.selectedRowKeys = selectedRowKeys
        }
      }
    },
    // async handleMockAdd () {
    //    // 模拟新增
    //   for (let i = 0; i < 30; i++) {
    //     const desc = '他既到了北京、上海等繁华都市，也抵达了黑龙江朗乡、新疆吐鲁番等疆界边陲。他走到中国大地上，与各种各样的人聊天，在上海人民公园英语角里练习口语的年轻人、想去做进出口生意的学生、刚刚经历过浩劫的知识分子……他用犀利幽默的口吻，一路吐槽不断，但也用冷静、理智的眼光，剖析中国人的性格，发现时代变迁下中国人的生活日常与思想变化。'
    //     const formData = new FormData()
    //     formData.append('title', '生活图书' + i)
    //     formData.append('description', desc)
    //     formData.append('author', '马丽丽'+i)
    //     formData.append('translator', '')
    //     formData.append('isbn', '97875327617' + i)
    //     formData.append('price', Math.floor(Math.random() * 100).toString())
    //     formData.append('press', '现代出版社')
    //     formData.append('layout', '平装')
    //     formData.append('page_count', Math.floor(Math.random() * 500).toString())
    //     formData.append('repertory', Math.floor(Math.random() * 100).toString())
    //     formData.append('status', '0')
    //     formData.append('pub_date', '2011-09-28')
    //
    //     await createApi(formData)
    //     console.log('finish '+i)
    //   }
    // },
    handleAdd () {
      this.$dialog(
        EditThing,
        {
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: '新增商品',
          width: '640px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
    },
    handleEdit (record) {
      this.$dialog(
        EditThing,
        {
          thing: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: '编辑商品',
          width: '640px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
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
