<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="角色名称" prop="title">
          <a-input placeholder="请输入" v-model="form.title"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="备注">
          <a-input placeholder="请输入" v-model="form.remark"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/role'

export default {
  name: 'EditRole',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    role: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      form: {
      },
      rules: {
        title: [{ required: true, message: '请输入名称', trigger: 'change' }]
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.role
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
                id: this.role.id
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
