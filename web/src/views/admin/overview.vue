<template>

  <a-spin :spinning="showSpin">
    <div class="main">
      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="商品总数">
            <a-tag color="blue" slot="extra">总</a-tag>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.thing_count }}<span class="v-e">种</span></span>
                <a-icon type="profile" theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>本周新增 {{ data.thing_week_count }} 种</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="未付订单">
            <a-tag color="green" slot="extra">未付</a-tag>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.order_not_pay_count }}<span class="v-e">单</span></span>
                <a-icon type="carry-out"  theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>共 {{data.order_not_pay_p_count}} 人</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="已付订单">
            <a-tag color="blue" slot="extra">已付</a-tag>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.order_payed_count }}<span class="v-e">单</span></span>
                <a-icon type="interaction" theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>共 {{data.order_payed_p_count}} 人</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" title="取消订单">
            <a-tag color="green" slot="extra">取消</a-tag>

            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.order_cancel_count }}<span class="v-e">单</span></span>
                <a-icon type="bell" theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>共 {{data.order_cancel_p_count}} 人</span>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>

      <a-card title="最近一周访问量">
        <div style="height: 300px;" ref="visitChart"></div>
      </a-card>

      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门商品排名" style="flex:1;">
            <div style="height: 300px;" ref="barChart"></div>
          </a-card>
        </a-col>
        <a-col :sm="24" :md="24" :lg="12">
          <a-card title="热门分类比例" style="flex:1;">
            <div style="height: 300px;" ref="pieChart"></div>
          </a-card>
        </a-col>
      </a-row>

    </div>
  </a-spin>

</template>

<script>
import * as echarts from 'echarts'
import {listApi} from '@/api/admin/overview'
import storage from 'store'
import {ADMIN_TOKEN} from '@/store/constants'

export default {
  name: 'One',
  data () {
    return {
      showSpin: true,
      visitChart: undefined,
      barChart: undefined,
      pieChart: undefined,
      data: {
        order_rank_data: [],
        classification_rank_data: [],
        visit_data: []
      }
    }
  },
  mounted () {
    // this.$store.commit('SET_NAME', 'zhangsan')
    // this.$store.dispatch('Login', 'linxiaomei')

    // console.log(this.$store.state.user.name)
    // console.log(this.$store.getters.name)

    console.log(storage.get(ADMIN_TOKEN))
    this.list()
    const that = this
    window.onresize = function () { // resize
      that.visitChart.resize()
      that.barChart.resize()
      that.pieChart.resize()
    }
  },
  methods: {
    list () {
      listApi({}).then(res => {
        console.log(res.data)
        this.data = res.data
        this.initCharts()
        this.showSpin = false
      }).catch(err => {
        this.showSpin = false
        this.$message.error(err.msg || '获取失败！')
      })
    },
    initCharts () {
      const that = this
      setTimeout(function () {
        that.initVisitChart()
        that.initBarChart()
        that.initPieChart()
      }, 100)
    },
    initVisitChart () {
      let xData = []
      let uvData = []
      let pvData = []
      this.data.visit_data.forEach((item, index) => {
        xData.push(item.day)
        uvData.push(item.uv)
        pvData.push(item.pv)
      })
      this.visitChart = echarts.init(this.$refs.visitChart)
      let option = {
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['IP', 'visit'],
          top: '90%',
          left: 'center'
        },
        grid: {
          top: '30px',
          left: '20px',
          right: '20px',
          bottom: '40px',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            textStyle: {
              color: '#2F4F4F'
            }
          },
          axisLine: {
            lineStyle: {
              color: '#2F4F4F'
            }
          },
          // boundaryGap: false,
          data: xData
        },
        yAxis: {
          type: 'value',
          axisLine: {show: false},
          axisTick: {show: false},
          splitLine: {
            show: true, // 网格线
            lineStyle: {
              color: 'rgba(10, 10, 10, 0.1)',
              width: 1,
              type: 'solid'
            }
          }
        },
        series: [
          {
            name: 'IP',
            type: 'line',
            stack: 'Total',
            data: uvData
          },
          {
            name: 'visit',
            type: 'line',
            stack: 'Total',
            data: pvData
          }
        ]
      }
      this.visitChart.setOption(option)
    },
    initBarChart () {
      let xData = []
      let yData = []
      this.data.order_rank_data.forEach((item, index) => {
        xData.push(item.title)
        yData.push(item.count)
      })
      // const xData = ['遥远的救世主', '平凡的世界', '测试书籍12', '测试书籍13', '测试书籍14', '测试书籍15', '测试书籍16', '测试书籍17']
      // const yData = [220, 200, 180, 150, 130, 110, 100, 80]
      this.barChart = echarts.init(this.$refs.barChart)
      let option = {
        grid: {
          // 让图表占满容器
          top: '40px',
          left: '40px',
          right: '40px',
          bottom: '40px'
        },
        title: {
          text: '热门商品排名',
          textStyle: {
            color: '#aaa',
            fontStyle: 'normal',
            fontWeight: 'normal',
            fontSize: 18
          },
          x: 'center',
          y: 'top'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          data: xData,
          type: 'category',
          axisLabel: {
            rotate: 30, // 倾斜30度,
            textStyle: {
              color: '#2F4F4F'
            }
          },
          axisLine: {
            lineStyle: {
              color: '#2F4F4F'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {show: false},
          axisTick: {show: false},
          splitLine: {
            show: true, // 网格线
            lineStyle: {
              color: 'rgba(10, 10, 10, 0.1)',
              width: 1,
              type: 'solid'
            }
          }
        },
        series: [
          {
            data: yData,
            type: 'bar',
            itemStyle: {
              normal: {
                color: function (params) {
                  // 柱图颜色
                  return '#70B0EA'
                }
              }
            }
          }
        ]
      }
      this.barChart.setOption(option)
    },
    initPieChart () {
      let pieData = []
      this.data.classification_rank_data.forEach((item, index) => {
        pieData.push({name: item.title, value: item.count})
      })
      this.pieChart = echarts.init(this.$refs.pieChart)
      const option = {
        grid: {
          // 让图表占满容器
          top: '40px',
          left: '40px',
          right: '40px',
          bottom: '40px'
        },
        title: {
          text: '热门商品分类',
          textStyle: {
            color: '#aaa',
            fontStyle: 'normal',
            fontWeight: 'normal',
            fontSize: 18
          },
          x: 'center',
          y: 'top'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '90%',
          left: 'center'
        },
        series: [
          {
            name: '分类',
            type: 'pie',
            itemStyle: {
              normal: {
                color: function (params) {
                  const colorList = ['#70B0EA', '#B3A3DA', '#88DEE2', '#62C4C8', '#58A3A1']
                  let index = params.dataIndex
                  if (params.dataIndex >= colorList.length) {
                    index = params.dataIndex - colorList.length
                  }
                  return colorList[index]
                }
              }
            },
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: pieData
          }
        ]
      }
      this.pieChart.setOption(option)
    }
  }
}
</script>

<style lang="less" scoped>

.main {
  height: 100%;
  display: flex;
  gap:20px;
  flex-direction: column;

  .box {
    padding: 12px;
    display: flex;
    flex-direction: column;

    .box-top {
      display: flex;
      flex-direction: row;
      align-items: center;
    }
    .box-value {
      color: #000000;
      font-size: 32px;
      margin-right: 12px;
      .v-e {
        font-size: 14px;
      }
    }

    .box-bottom {
      margin-top: 24px;
      color: #000000d9;
    }
  }
}

</style>
