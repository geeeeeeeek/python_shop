<template>
  <div class="list-content">
    <a-radio-group v-model="checkedValue" style="width: 100%;">
      <div class="address-item flex-view" v-for="(item,index) in addressData" @click="checkItem(index)">
        <a-radio :value="index"></a-radio>
        <div class="infos">
          <div class="name-box">
            <span class="name">{{item.name}}</span>
            <span class="tel">{{item.mobile}}</span>
          </div>
          <p class="address-box">{{item.desc}}</p>
        </div>
      </div>
    </a-radio-group>
    <div class="no-data" style="display: none;">暂无地址</div>
  </div>
</template>

<script>
import {createApi, listApi, updateApi} from '@/api/index/address'

export default {
  data () {
    return {
      checkedValue: undefined,
      addressData: []
    }
  },
  created () {
    this.listAddressData()
  },
  methods: {
    checkItem(index) {
      this.checkedValue = index
    },
    listAddressData () {
      let userId = this.$store.state.user.userId
      listApi({userId: userId}).then(res => {
        this.addressData = res.data
      }).catch(err => {
        console.log(err)
      })
    },
    onOk () {
      console.log(this.checkedValue)
      console.log(this.addressData[this.checkedValue])
      return new Promise((resolve, reject) => {
        if(this.checkedValue >= 0) {
          const formData = new FormData()
          formData.append('name', this.addressData[this.checkedValue].name)
          formData.append('mobile', this.addressData[this.checkedValue].mobile)
          formData.append('desc', this.addressData[this.checkedValue].desc)
          resolve(formData)
        } else {
          reject(new Error('fail'))
          this.$message.warn('请选择地址')
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
progress {
  vertical-align: baseline;
}

.flex-view {
  display: flex;
}

input, textarea {
  outline: none;
  border-style: none;
}

button {
  padding: 0;
}

.content-list {
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    //line-height: 24px;
    height: 48px;
    margin-bottom: 20px;
    border-bottom: 1px solid #cedce4;
  }
  .add-new-btn {
    color: #4684e2;
    font-size: 14px;
    float: right;
    font-weight: 400;
    cursor: pointer;
  }
}

.address-item {
  cursor: pointer;
  background: #f7f9fb;
  border-radius: 4px;
  margin-bottom: 12px;
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  //justify-content: space-between;
  padding: 16px;

  .name-box {
    margin-left: 12px;
    color: #152844;
    font-weight: 500;
    font-size: 14px;
    line-height: 22px;
    height: 22px;
  }

  .name {
    margin-right: 16px;
  }

  .address-box {
    margin-left: 12px;
    color: #484848;
    font-size: 14px;
    line-height: 22px;
    height: 22px;
    margin-top: 4px;
  }

  .btns {
    font-size: 14px;
    cursor: pointer;
    height: 22px;
    line-height: 22px;
  }

  .edit {
    color: #4684e2;
    margin-right: 24px;
  }

  .delete {
    color: #f62a2a;
  }

  .default-box {
    margin-top: 4px;
    font-size: 0;

    img {
      position: relative;
      top: -1px;
      width: 16px;
      height: 16px;
      margin-right: 4px;
      vertical-align: middle;
    }

    span {
      color: #6f6f6f;
      font-size: 14px;
      vertical-align: middle;
    }
  }
}
</style>
