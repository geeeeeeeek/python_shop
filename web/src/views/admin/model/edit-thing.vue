<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="商品名称" prop="title">
          <a-input placeholder="请输入" v-model="form.title"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="12">
        <a-form-model-item label="分类" prop="classification">
          <a-tree-select
            v-model="form.classification"
            style="width: 100%"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            placeholder="请选择"
            allow-clear
            tree-default-expand-all
          >
            <template v-for="item1 in cData">
              <a-tree-select-node :key="item1.key" :value="item1.key" :title="item1.name">
                <template v-for="item2 in item1.children">
                  <a-tree-select-node :key="item2.key" :value="item2.key" :title="item2.name"></a-tree-select-node>
                </template>
              </a-tree-select-node>
            </template>
          </a-tree-select>
        </a-form-model-item>
      </a-col>
      <a-col span="12">
        <a-form-model-item label="标签">
          <a-select mode="multiple" placeholder="请选择" allowClear v-model="form.tag">
            <template v-for="item in tagData">
              <a-select-option :key="item.id" :value="item.id">{{item.title}}</a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="封面">
          <a-upload-dragger
            name="file"
            accept="image/*"
            :multiple="false"
            :before-upload="beforeUpload"
          >
            <p class="ant-upload-drag-icon">
              <template v-if="coverUrl">
                <img :src="coverUrl"  style="width: 60px;height: 80px;"/>
              </template>
              <template v-else>
                <a-icon type="inbox" />
              </template>
            </p>
            <p class="ant-upload-text">
              请选择要上传的封面图片
            </p>
          </a-upload-dragger>
        </a-form-model-item>
      </a-col>

      <a-col span="24">
        <a-form-model-item label="内容简介">
          <a-textarea placeholder="请输入" v-model="form.description"></a-textarea>
        </a-form-model-item>
      </a-col>
      <a-col span="12">
        <a-form-model-item label="定价" prop="price">
          <a-input-number  placeholder="请输入" :min="0" v-model="form.price" style="width: 100%;"></a-input-number>
        </a-form-model-item>
      </a-col>
      <a-col span="12">
        <a-form-model-item label="状态" prop="status">
          <a-select placeholder="请选择" allowClear v-model="form.status">
            <a-select-option key="0" value="0">上架</a-select-option>
            <a-select-option key="1" value="1">下架</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="12">
        <a-form-model-item label="库存" prop="repertory">
          <a-input-number placeholder="请输入" :min="0" v-model="form.repertory" style="width: 100%;"></a-input-number>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/thing'
import {listApi as listClassificationApi} from '@/api/admin/classification'
import {listApi as listTagApi} from '@/api/admin/tag'

export default {
  name: 'EditThing',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    thing: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      coverUrl: undefined,
      form: {
        layout: undefined
      },
      rules: {
        title: [{ required: true, message: '请输入名称', trigger: 'change' }],
        classification: [{ required: true, message: '请选择分类', trigger: 'change' }],
        repertory: [{ required: true, message: '请输入库存', trigger: 'change' }],
        price: [{ required: true, message: '请输入定价', trigger: 'change' }],
        status: [{ required: true, message: '请选择状态', trigger: 'change' }]
      },
      cData: [],
      tagData: []
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.thing
      this.coverUrl = this.form.cover
      this.form.cover = undefined
      this.form.classification = this.thing.classification || undefined
      this.form.tag = this.thing.tag || undefined
    }
    this.getCDataList()
    this.getTagDataList()
  },
  methods: {
    beforeUpload (file) {
      // 改文件名
      const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
      const copyFile = new File([file], fileName)
      console.log(copyFile)
      this.form.cover = copyFile
      return false
    },
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        const formData = new FormData()
        formData.append('title', this.form.title)
        if (this.form.classification) {
          formData.append('classification', this.form.classification)
        }
        if (this.form.tag) {
          this.form.tag.forEach(function (value) {
            formData.append('tag', value)
          })
        }
        if (this.form.cover) {
          formData.append('cover', this.form.cover)
        }
        formData.append('description', this.form.description || '')
        formData.append('price', this.form.price || '')
        if (this.form.repertory >= 0) {
          formData.append('repertory', this.form.repertory)
        }
        if (this.form.status) {
          formData.append('status', this.form.status)
        }
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.thing.id
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
    getCDataList () {
      listClassificationApi().then(res => {
        this.loading = false
        this.cData = res.data
      })
    },
    getTagDataList () {
      listTagApi().then(res => {
        this.loading = false
        res.data.forEach((item, index) => {
          item.index = index + 1
        })
        this.tagData = res.data
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
