<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="横幅图片">
          <a-upload-dragger
            name="file"
            accept="image/*"
            :multiple="false"
            :before-upload="beforeUpload"
          >
            <p class="ant-upload-drag-icon">
              <template v-if="imageUrl">
                <img :src="imageUrl"  style="width: 100px;height: 50px;"/>
              </template>
              <template v-else>
                <a-icon type="inbox" />
              </template>
            </p>
            <p class="ant-upload-text">
              请选择要上传的横幅图片
            </p>
          </a-upload-dragger>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="关联商品" prop="thing">
          <a-select placeholder="请选择" allowClear v-model="form.thing">
            <template v-for="item in thingData">
              <a-select-option :key="item.id" :value="item.id">{{item.title}}</a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/banner'
import {listApi as listThingApi} from '@/api/admin/thing'

export default {
  name: 'EditBanner',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    banner: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      thing: undefined,
      imageUrl: undefined,
      form: {
      },
      thingData: [],
      rules: {
        thing: [{ required: true, message: '请选择商品', trigger: 'change' }]
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.banner
      this.imageUrl = this.banner.image
      this.form.image = undefined
    }
    this.getThingList()
  },
  methods: {
    beforeUpload (file) {
      // 改文件名
      const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
      const copyFile = new File([file], fileName)
      console.log(copyFile)
      this.form.image = copyFile
      return false
    },
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        const formData = new FormData()
        if (this.form.image) {
          formData.append('image', this.form.image)
        }
        if (this.form.thing) {
          formData.append('thing', this.form.thing)
        }
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.banner.id
              }, formData).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '更新失败')
                reject(new Error('更新失败'))
              })
            } else {
              // 新增接口
              createApi(formData).then(res => {
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
    },
    getThingList () {
      listThingApi().then(res => {
        this.thingData = res.data
      }).catch(err => {
        this.$message.error(err.msg || '查询失败')
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
