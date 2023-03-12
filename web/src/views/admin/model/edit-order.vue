<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="商品" prop="thing">
          <a-select placeholder="请选择" allowClear v-model="form.thing">
            <template v-for="item in thingData">
              <a-select-option :key="item.id" :value="item.id">{{item.title}}</a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="用户" prop="user">
          <a-select placeholder="请选择" allowClear v-model="form.user">
            <template v-for="item in userData">
              <a-select-option :key="item.id" :value="item.id">{{item.username}}</a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="状态" prop="status">
          <a-select placeholder="请选择" allowClear v-model="form.status">
            <a-select-option key="1" value="1">借出</a-select-option>
            <a-select-option key="2" value="2">还入</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/order'

export default {
  name: 'EditOrder',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    order: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      form: {
      },
      rules: {
        thing: [{ required: true, message: '请选择商品', trigger: 'change' }]
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.tag
    }
  },
  methods: {
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.tag.id
              }, this.form).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '更新失败')
                reject(new Error('更新失败'))
              })
            } else {
              // 新增接口
              createApi(this.form).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '新建失败')
                reject(new Error('新建失败'))
              })
            }
          }
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
