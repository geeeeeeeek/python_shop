<template>
  <div>
    <Header/>
    <section class="cart-page flex-view">
    <div class="left-flex">
      <div class="title flex-view">
        <h3>订单明细</h3>
      </div>
      <div class="cart-list-view">
        <div class="list-th flex-view">
          <span class="line-1">商品名称</span>
          <span class="line-2">价格</span>
          <span class="line-5">数量</span>
          <span class="line-6">操作</span>
        </div>
        <div class="list">
          <div class="items flex-view">
            <div class="book flex-view">
              <img src="https://file.ituring.com.cn/SmallCover/2212c21242c05ebc49f3">
              <h2>{{title}}</h2>
            </div>
            <div class="pay">¥{{price}}</div>
            <a-input-number v-model="count" :min="1" :max="10" @change="onCountChange"/>
            <img src="@/assets/images/delete-icon.svg" class="delete">
          </div>
        </div>
      </div>
      <div class="title flex-view">
        <h3>备注</h3>
      </div>
      <textarea :value="remark" placeholder="输入备注信息，100字以内" class="remark">
    </textarea>
    </div>
    <div class="right-flex">
      <div class="title flex-view">
        <h3>收货地址</h3>
        <span class="click-txt" @click="handleSelectAddress" v-if="receiver_address">选择地址</span>
      </div>
      <div class="address-view">
        <div class="info" style="">
          <span>收件人：</span>
          <span class="name">{{receiver_name}}
          </span>
          <span class="tel">{{receiver_phone}}
          </span>
        </div>
        <div class="address" v-if="receiver_address"> {{receiver_address}}</div>
        <div class="info" v-else>
          <span>目前暂无地址信息，请</span>
          <span class="info-blue" @click="handleCreateAddress">新建地址</span>
        </div>
      </div>
      <div class="title flex-view">
        <h3>结算</h3>
        <span class="click-txt">价格</span>
      </div>
      <div class="price-view">
        <div class="price-item flex-view">
          <div class="item-name">商品总价</div>
          <div class="price-txt">¥{{this.amount}}</div>
        </div>
        <div class="price-item flex-view">
          <div class="item-name">商品优惠</div>
          <div class="price-txt">¥0</div>
        </div>
        <div class="price-item flex-view">
          <div class="item-name">商品折扣</div>
          <div class="price-txt">¥0</div>
        </div>
        <div class="total-price-view flex-view">
          <span>合计</span>
          <div class="price">
            <span class="font-big">¥{{this.amount}}</span>
          </div>
        </div>
        <div class="btns-view">
          <button class="btn buy">返回</button>
          <button class="btn pay jiesuan" @click="handleJiesuan()">结算</button>
        </div>
      </div>
    </div>
  </section>
  </div>
</template>

<script>
import Header from '@/views/index/components/header'
import Footer from '@/views/index/components/footer'
import AddAddress from '@/views/index/modal/add-address'
import SelectAddress from '@/views/index/modal/select-address'
import {createApi} from '@/api/index/order'
import {listApi as listAddressListApi} from '@/api/index/address'

export default {
  components: {
    Footer,
    Header
  },
  data () {
    return {
      id: undefined,
      title: undefined,
      price: undefined,
      remark: undefined,
      count: 1,
      amount: undefined,
      receiver_name: undefined,
      receiver_phone: undefined,
      receiver_address: undefined
    }
  },
  mounted () {
    this.id = this.$route.query.id
    this.title = this.$route.query.title
    this.price = this.$route.query.price
    this.amount = this.price

    this.listAddressData()
  },
  methods: {
    onCountChange(value){
      this.amount = this.price * value
    },
    listAddressData () {
      let userId = this.$store.state.user.userId
      listAddressListApi({userId: userId}).then(res => {

        if (res.data.length > 0) {
          this.receiver_name = res.data[0].name
          this.receiver_phone = res.data[0].mobile
          this.receiver_address = res.data[0].desc
          res.data.forEach(item => {
            if (item.default) {
              this.receiver_name = item.name
              this.receiver_phone = item.mobile
              this.receiver_address = item.desc
            }
          })
        }
      }).catch(err => {
        console.log(err)
      })
    },

    handleSelectAddress () {
      this.$dialog(
        SelectAddress,
        {
          on: {
            ok: form => {
              console.log(form)
              this.receiver_name = form.get('name')
              this.receiver_phone = form.get('mobile')
              this.receiver_address = form.get('desc')
            }
          }
        },
        {
          title: '选择地址',
          width: '480px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
    },
    handleCreateAddress () {
      this.$dialog(
        AddAddress,
        {
          on: {
            ok: form => {
              console.log(form)
              this.receiver_name = form.get('name')
              this.receiver_phone = form.get('mobile')
              this.receiver_address = form.get('desc')
            }
          }
        },
        {
          title: '新增地址',
          width: '480px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
    },
    handleJiesuan () {
      const formData = new FormData()
      let userId = this.$store.state.user.userId
      if (!userId) {
        this.$message.warn('请先登录！')
        return
      }
      if (!this.receiver_name) {
        this.$message.warn('请选择地址！')
        return
      }
      formData.append('user', userId)
      formData.append('thing', this.id)
      formData.append('count', this.count)
      if (this.remark){
        formData.append('remark', this.remark)
      }
      formData.append('receiver_name', this.receiver_name)
      formData.append('receiver_phone', this.receiver_phone)
      formData.append('receiver_address', this.receiver_address)
      console.log(formData)
      createApi(formData).then(res => {
        this.$message.success('请支付订单')
        this.$router.push({'name': 'pay', query: {'amount': this.amount}})
      }).catch(err => {
        this.$message.error(err.msg || '失败')
      })
    }

  }
}
</script>

<style scoped lang="less">

.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.cart-page {
  width: 1024px;
  min-height: 50vh;
  margin: 100px auto;
}

.left-flex {
  -webkit-box-flex: 17;
  -ms-flex: 17;
  flex: 17;
  padding-right: 20px;
}

.title {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;

  h3 {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    height: 26px;
    line-height: 26px;
    margin: 0;
  }
}

.cart-list-view {
  margin: 4px 0 40px;

  .list-th {
    height: 42px;
    line-height: 42px;
    border-bottom: 1px solid #cedce4;
    color: #152844;
    font-size: 14px;

    .line-1 {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      margin-right: 20px;
    }

    .line-2, .pc-style .cart-list-view .list-th .line-3, .pc-style .cart-list-view .list-th .line-4 {
      width: 65px;
      margin-right: 20px;
    }

    .line-5 {
      width: 80px;
      margin-right: 40px;
    }

    .line-6 {
      width: 28px;
    }
  }
}

.items {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  margin-top: 20px;

  .book {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-right: 20px;
    cursor: pointer;

    img {
      width: 48px;
      margin-right: 16px;
      border-radius: 4px;
    }

    h2 {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      font-size: 14px;
      line-height: 22px;
      color: #152844;
    }
  }

  .type {
    width: 65px;
    margin-right: 20px;
    color: #152844;
    font-size: 14px;
  }

  .pay {
    color: #ff8a00;
    font-weight: 600;
    font-size: 16px;
    width: 65px;
    margin-right: 20px;
  }

  .num-box {
    width: 80px;
    margin-right: 43px;
    border-radius: 4px;
    border: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 32px;
    padding: 0 4px;
  }

  .delete {
    margin-left: 36px;
    width: 24px;
    cursor: pointer;
  }
}

.mb-24 {
  margin-bottom: 24px;
}

.show-txt {
  color: #ff8a00;
  font-size: 14px;
}

.remark {
  width: 100%;
  background: #f6f9fb;
  border: 0;
  border-radius: 4px;
  padding: 6px 12px;
  //color: #152844;
  margin-top: 16px;
  resize: none;
  height: 56px;
  line-height: 22px;
}

.right-flex {
  -webkit-box-flex: 8;
  -ms-flex: 8;
  flex: 8;
  padding-left: 24px;
  border-left: 1px solid #cedce4;
}

.click-txt {
  color: #4684e2;
  font-size: 14px;
  cursor: pointer;
}

.address-view {
  margin: 12px 0 24px;

  .info {
    color: #909090;
    font-size: 14px;
    .info-blue {
      cursor: pointer;
      color: #4684e2;
    }
  }

  .name {
    color: #152844;
    font-weight: 500;
  }

  .tel {
    color: #152844;
    float: right;
  }

  .address {
    color: #152844;
    margin-top: 4px;
  }
}

.price-view {
  overflow: hidden;
  margin-top: 16px;

  .price-item {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;

    .item-name {
      color: #152844;
    }

    .price-txt {
      font-weight: 500;
      color: #ff8a00;
    }
  }

  .total-price-view {
    margin-top: 12px;
    border-top: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: flex-start;
    padding-top: 10px;
    color: #152844;
    font-weight: 500;

    .price {
      color: #ff8a00;
      font-size: 16px;
      height: 36px;
      line-height: 36px;
    }
  }

  .btns-view {
    margin-top: 24px;
    text-align: right;

    .buy {
      background: #fff;
      color: #4684e2;
    }

    .jiesuan {
      cursor: pointer;
      background: #4684e2;
      color: #fff;
    }

    .btn {
      cursor: pointer;
      width: 96px;
      height: 36px;
      line-height: 33px;
      margin-left: 16px;
      text-align: center;
      border-radius: 32px;
      border: 1px solid #4684e2;
      font-size: 16px;
      outline: none;
    }
  }

}

</style>
