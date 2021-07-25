<template>
  <div>
    <div class="container_title">
      <!-- 面包屑 -->
      <Breadcrumb>
        <BreadcrumbItem>训练统计</BreadcrumbItem>
      </Breadcrumb>
      <div class="info">
        <span style="margin-right:30px;">模型名称：{{$route.query.dmName}}</span>
        <span>模型版本：{{$route.query.dmtvName}}</span>
      </div>
      <!-- 操作按钮 -->
      <div class="ops_btn">
        <Button type="primary" icon="ios-arrow-back" size="small" @click="back">返 回</Button>
      </div>
    </div>
    <Collapse v-model="value1">
      <Panel name="1">
        <span class="panel_title">metrics</span>
        <div slot="content">
          <div class="box clear-fix">
            <div class="chart" v-for="(item,idx) in 4" :key="idx" :id="'main'+idx"></div>
          </div>
        </div>
      </Panel>
      <Panel name="2">
        <span class="panel_title">train</span>
        <div slot="content">
          <div class="box clear-fix">
            <div class="chart" v-for="(item,idx) in 3" :key="idx" :id="'main'+(idx+4)"></div>
          </div>
        </div>
      </Panel>
      <Panel name="3">
        <span class="panel_title">val</span>
        <div slot="content">
          <div class="box clear-fix">
            <div class="chart" v-for="(item,idx) in 3" :key="idx" :id="'main'+(idx+7)"></div>
          </div>
        </div>
      </Panel>
      <Panel name="4">
        <span class="panel_title">x</span>
        <div slot="content">
          <div class="box clear-fix">
            <div class="chart" v-for="(item,idx) in 3" :key="idx" :id="'main'+(idx+10)"></div>
          </div>
        </div>
      </Panel>
    </Collapse>
  </div>
</template>

<script>
var echarts = require('echarts')

export default {
  data () {
    return {
      value1: ['1', '2', '3', '4'],
      charts: {},
      init: true,
      timer: null,
      dmtvName: '',
      dmName: ''
    }
  },
  mounted () {
    this.dmtvid = parseInt(this.$route.params.id)
    // this.dmtvName = this.$route.dmtvName
    // this.dmName = this.$route.dmName
    this.getStatistics()
    this.setTimer()
  },
  destroyed () {
    clearInterval(this.timer)
  },
  methods: {
    initChart () {
      for(var i = 0; i < 13; i++) {
        var myChart = 'myChart' + i
        this.charts[myChart] = echarts.init(document.getElementById('main' + i))
      }
      this.setOption()
    },
    setOption () {
      for(var i = 0; i < 13; i++) {
        // 绘制图表
        var str = ''
        var arr = this.statisticsList[i].statisName.split('_')
        arr.splice(0, 1)
        if(arr.length > 1) {
          str = arr.join('_')
        } else {
          str = arr[0]
        }

        this.charts['myChart' + i].setOption({
          title: {
            text: str,
            textStyle: {
              fontSize: '16px',
              color: '#8c0776'
            }
          },
          grid: {
            left: '1%',
            right: '1%',
            bottom: '10%',
            containLabel: true,
          },
          tooltip: {
            trigger: 'axis',
            formatter: function (param) {
              param = param[0];
              return param.axisValue + '：' + param.value.toFixed(4)
            }
          },
          xAxis: {
            type: 'category',
            data: this.statisticsList[i].statisValue.map((item, idx) => idx + 1),
            minorTick: {
              show: true
            },
            splitLine: {
              lineStyle: {
                color: '#999'
              }
            },
            minorSplitLine: {
              show: true,
              lineStyle: {
                color: '#ddd'
              }
            }
          },
          yAxis: {
            type: 'value',
            splitLine: {
              lineStyle: {
                color: '#999'
              }
            },
          },
          series: [{
            data: this.statisticsList[i].statisValue,
            type: 'line',
            smooth: true
          }]
        });
      }
    },
    getStatistics () {
      let params = {
        dmtvid: this.dmtvid
      }
      // if(this.init) {
      this.$Spin.show()
      // }
      this.$post('/dmTrainStatis/getTrainStatistics', params).then(data => {
        // if(this.init) {
        this.$Spin.hide()
        // }
        if(data.rs === 1) {
          this.statisticsList = data.dataList;
          if(this.init) {
            setTimeout(() => {
              this.initChart()
              this.init = false
            }, 200);
          } else {
            this.setOption()
          }
          // this.total = data.pageData.totalCount;//总数
          // this.chosePage = data.pageData.page;//选择页
          // this.pageNow = data.pageData.page;//当前页
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    setTimer () {
      this.timer = setInterval(() => {
        if(this.value1.length != 4) {
          this.value1 = ['1', '2', '3', '4']
        }
        this.getStatistics()
      }, 2 * 60 * 1000)
    },
    back () {
      this.$router.go(-1)
    }
  }
}
</script>

<style lang="scss" scoped>
#main {
  width: 200px;
  height: 200px;
}
.chart {
  width: 280px;
  height: 280px;
  float: left;
  margin: 0 15px;
}
.panel_title {
  font-size: 18px;
  color: #8c0776;
}
</style>