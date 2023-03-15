<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="评论内容" prop="content">
          <a-input placeholder="请输入" v-model="form.content"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="商品id" prop="thing">
          <a-input placeholder="请输入" v-model="form.thing"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="用户id" prop="user">
          <a-input placeholder="请输入" v-model="form.user"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/comment'

export default {
  name: 'EditComment',
  props: {
  },
  data () {
    return {
      form: {
      },
      rules: {
        content: [{ required: true, message: '请输入评论内容', trigger: 'change' }]
      }
    }
  },
  created () {
    // if (this.modifyFlag) {
    //   this.form = this.tag
    // }
  },
  methods: {
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        this.$refs.myform.validate(valid => {
          if (valid) {
            createApi(this.form).then(res => {
              console.log(res)
              resolve(true)
            }).catch(err => {
              this.$message.error(err.msg || '新建失败')
              reject(new Error('新建失败'))
            })
          }
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
