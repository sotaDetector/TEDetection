<template>
  <div class="validate_container">
    <div class="container_title">
      <!-- 面包屑 -->
      <Breadcrumb>
        <BreadcrumbItem>模型校验</BreadcrumbItem>
      </Breadcrumb>
      <!-- 操作按钮 -->
      <div class="ops_btn">
        <Button type="primary" icon="ios-arrow-back" size="small" @click="back">返 回</Button>
      </div>
    </div>

    <div class="container_info">
      <div class="container_box clear-fix">
        <div class="info">
          <span style="margin-right:30px;">模型名称：{{$route.query.dmName}}</span>
          <span>模型版本：{{$route.query.dmtvName}}</span>
        </div>
        <div class="open" v-if="isOpenShow">
          <Button type="primary" size="small" :loading="opening" @click="openValidate">{{openText}}</Button>
        </div>

        <Tabs v-model="tabName" v-if="!isOpenShow" @on-click="changeType">
          <TabPane label="图片检测" icon="ios-image-outline">
            <div class="validate_content clear-fix">
              <div class="left">
                <Upload type="drag" action="//jsonplaceholder.typicode.com/posts/" :show-upload-list="false" class="drag" accept=".png, .jpg, .jpeg, .bmp, .tif, .tiff, .dng" :before-upload="handleUpload">
                  <div class="innner" style="height:100%;position:relative;background:#f7f7f7;display:flex;justify-content:center;align-items:center;flex-direction:column">
                    <img v-if="mediaSrc" class="media" :src="mediaSrc">
                    <Icon type="ios-image-outline" size="52" style="color:#8c0776"></Icon>
                    <p class="tip">点击 <span class="font">添加图片</span> 或 <span class="font">拖曳图片</span> 至此处</p>
                    <p class="tip">图片类型为jpg, png, bmp, jpeg, tif, tiff, dng，图片大小限制在<span class="font">4M</span>内。</p>
                  </div>
                </Upload>
              </div>
              <div class="right">
                <div class="threshold">
                  <span style="font-size:12px;">调整阈值</span>
                  <Slider v-model="threshold" @on-change="changeThreshold" :min="0" :max="1" :step="0.01" style="width:65%;margin: 0 18px"></Slider>
                  {{threshold}}
                </div>
                <div class="predict">
                  <div class="header">
                    <span>预测标签</span>
                    <span style="margin-left:42%;">置信度 > {{this.threshold | percent}}</span>
                  </div>
                  <ul class="label_box">
                    <li class="no_data" v-if="!resultList.length">没有满足条件的识别结果</li>
                    <li class="label" v-for="(item,idx) in resultList" :key="idx" :style="{color: 'rgb('+item.color.join()+')', 'font-size': '16px'}">{{item.label}}</li>
                  </ul>
                </div>
              </div>
            </div>
          </TabPane>
          <TabPane label="视频检测" icon="ios-film-outline">
            <div class="validate_content clear-fix">
              <div class="left">
                <Upload type="drag" action="//jsonplaceholder.typicode.com/posts/" :show-upload-list="false" class="drag" accept=".mov, .avi, .mp4, .mpg, .mpeg, .m4v, .wmv, .mkv" :before-upload="handleUpload">
                  <div class="innner" style="height:100%;position:relative;background:#f7f7f7;display:flex;justify-content:center;align-items:center;flex-direction:column">
                    <!-- <img v-if="mediaSrc" class="media" :src="mediaSrc"> -->
                    <img v-if="mediaSrc" class="media" :src="mediaSrc">
                    <Icon type="ios-film-outline" size="52" style="color:#8c0776"></Icon>
                    <p class="tip">点击 <span class="font">添加视频</span> 或 <span class="font">拖曳视频</span></p>
                    <p class="tip">图片类型为mov, avi, mp4, mpg, mpeg, m4v, wmv, mkv，视频大小限制在<span class="font">30M</span>内。</p>
                  </div>
                </Upload>
              </div>
              <div class="right">
                <div class="threshold">
                  <span style="font-size:12px;">调整阈值</span>
                  <Slider v-model="threshold" @on-change="changeThreshold" :min="0" :max="1" :step="0.01" style="width:65%;margin: 0 18px"></Slider>
                  {{threshold}}
                </div>
              </div>
            </div>
          </TabPane>
          <TabPane label="直播流检测" icon="ios-videocam-outline">
            <div class="validate_content clear-fix">
              <div class="left">
                <img v-if="mediaSrc" class="media" :src="mediaSrc">
              </div>
              <div class="right">
                <div class="threshold">
                  <span style="font-size:12px;">调整阈值</span>
                  <Slider v-model="threshold" @on-change="changeThreshold" :min="0" :max="1" :step="0.01" style="width:65%;margin: 0 18px"></Slider>
                  {{threshold}}
                </div>
                <div class="link_url">
                  <span style="margin-top:10px;font-size:12px;margin-right:18px">直播地址</span>
                  <Input style="width:75%;" v-model="source" placeholder="请输入直播地址"></Input>
                </div>
                <Button type="primary" size="small" :loading="waiting" @click="startDetect" style="margin-top:40px;" :disabled="sessionIdForClose!='' ||  source==''">开始检测</Button>
                <Button size="small" type="primary" ghost @click="stopDetect" style="margin-top:40px;margin-left:25px;" :disabled="!sessionIdForClose">关闭检测</Button>
              </div>
            </div>
          </TabPane>
          <!-- <TabPane label="摄像头检测" icon="ios-ionitron-outline">标签四的内容</TabPane> -->
          <TabPane label="摄像头检测" icon="ios-locate-outline">
            <div class="validate_content clear-fix">
              <div class="left">
                <img v-if="mediaSrc" class="media" :src="mediaSrc">
                <!-- <img src="http://47.111.130.154:8200/videoDetect/getVideoStream?videoPlayId=12" alt="" class="media"> -->
              </div>
              <div class="right">
                <div class="threshold">
                  <span style="font-size:12px;">调整阈值</span>
                  <Slider v-model="threshold" @on-change="changeThreshold" :min="0" :max="1" :step="0.01" style="width:65%;margin: 0 18px"></Slider>
                  {{threshold}}
                </div>
                <div v-if="deviceList.length && !deviceList[0].deviceName" style="margin-top:100px;text-align:center;color:#ccc;">暂未连接任何摄像设备</div>
                <div class="link_url" v-if="deviceList[0] && deviceList[0].deviceName">
                  <span style="margin-top:10px;font-size:12px;margin-right:18px">选择摄像设备</span>
                  <Select style="width:75%;" v-model="source" placeholder="请选择摄像设备">
                    <Option v-for="item in deviceList" :value="item.deviceIndex" :key="item.deviceIndex">{{item.deviceName}}</Option>
                  </Select>
                </div>
                <Button v-if="deviceList[0] && deviceList[0].deviceName" type="primary" size="small" :loading="waiting" @click="startDetect" style="margin-top:40px;" :disabled="sessionIdForClose!='' || source==''">开启摄像头检测</Button>
                <Button v-if="deviceList[0] && deviceList[0].deviceName" size="small" type="primary" ghost @click="stopDetect" style="margin-top:40px;margin-left:25px;" :disabled="!sessionIdForClose">关闭摄像头检测</Button>
              </div>
            </div>
          </TabPane>
        </Tabs>

      </div>
    </div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      tabName: 0,
      serviceSessionId: '',
      threshold: 0.3,
      file: '',
      mediaSrc: '',
      opening: false,
      openText: '启动模型校验服务',
      isOpenShow: true,
      resultList: [],
      source: '',
      waiting: false,
      defaultSource: '',
      deviceList: [],
      sessionIdForClose: '', // 开启 摄像头检测/直播流检测，返回此id，关闭后置空
      timer: null,
      sessionIdsList: []

    }
  },
  mounted () {
    this.dmtvid = parseInt(this.$route.params.id)
  },
  destroyed () {
    if(this.sessionIdForClose) {
      this.stopDetect()
    }
    clearInterval(this.timer)
  },
  methods: {
    openValidate () {
      this.opening = true
      this.openText = '启动中（约 5 分钟）'

      this.$Spin.show()
      var params = {
        dmtvid: this.dmtvid
      }

      this.$post('/detectService/launchDetectService', params).then(data => {
        this.$Spin.hide()
        this.opening = false
        this.openText = '启动模型校验服务'
        if(data.rs === 1) {
          this.serviceSessionId = data.serviceSessionId
          this.sessionIdsList.push(data.serviceSessionId)
          this.isOpenShow = false
          this.setTimer()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    changeType (e) {
      if(this.sessionIdForClose) {
        this.stopDetect()
      }

      this.threshold = 0.3
      this.file = ''
      this.mediaSrc = ''
      this.source = '' // 直播流地址或摄像头设备
      this.sessionIdForClose = ''
      this.resultList = [] // 图片检测结果标签列表

      if(e == 2) { // 直播流
        this.getDefaultSource()
      }

      if(e == 3) { // 摄像头
        this.getCameraDeviceList()
      }
    },
    getDefaultSource () {
      this.$Spin.show()
      var params = {}
      this.$post('/cameraStreamVal/getSampleStreamUrl', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.defaultSource = data.data[0]
          this.source = this.defaultSource
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    getCameraDeviceList () {
      this.$Spin.show()
      var params = {}
      this.$post('/cameraStreamVal/getCameraDeviceList', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.deviceList = data.data
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    handleUpload (file) {
      let type = '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
      var str = this.tabName == 0 ? '|jpg|png|jpeg|bmp|tif|tiff|dng' : '|mov|avi|mp4|mpg|mpeg|m4v|wmv|mkv'
      var size = this.tabName == 0 ? 4 : 30
      let rs = str.indexOf(type) !== -1;
      if(!rs) {
        this.$Message.error("请上传正确的文件格式！");
        return false;
      }
      if(file.size > 1024 * 1024 * size) {
        this.$Message.error("文件大小不能超过 " + size + " M！");
        return false;
      }

      this.file = file
      var src = window.URL.createObjectURL(file)
      this.mediaSrc = src
      if(this.tabName == 0) {
        this.uploadImg()
      } else if(this.tabName == 1) {
        this.uploadVideo()
      }
      return false
    },
    uploadImg () {
      this.$Spin.show()
      var fd = new FormData()
      fd.append('detectedImage', this.file)
      fd.append('threshold', this.threshold)
      fd.append('serviceSessionId', this.serviceSessionId)

      this.$post_('/imageDetect/getSingleImageDetectResult', fd).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.mediaSrc = data.imagePath
          this.resultList = data.detectResult.length && data.detectResult[0].detectObject
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    uploadVideo () {
      this.$Spin.show()
      var fd = new FormData()
      fd.append('detectVideo', this.file)
      fd.append('threshold', this.threshold)
      fd.append('serviceSessionId', this.serviceSessionId)

      this.$post_('/videoDetect/getVideoDetectResult', fd).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.mediaSrc = data.videoPlayUrl
          // setTimeout(() => {
          //   $('.media').attr('src', data.videoPlayUrl)
          // }, 300);
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    changeThreshold () {
      if(this.file) {
        this.tabName == 0 ? this.uploadImg() : this.uploadVideo()
      }
    },
    startDetect () {
      var str = this.tabName == 2 ? '直播地址不能为空' : '请选择摄像设备'
      var url = this.tabName == 2 ? '/cameraStreamVal/startLiveStreamDetect' : '/cameraStreamVal/startNativeCameraDetect'
      if(!this.source) {
        this.$Message.error(str)
        return false
      }
      this.waiting = true

      this.$Spin.show()
      var params = {
        dmtvid: this.dmtvid,
        threshold: this.threshold,
        source: this.source
      }

      this.$post(url, params).then(data => {
        this.$Spin.hide()
        this.waiting = false
        if(data.rs == 1) {
          // this.mediaSrc = 'http://47.111.130.154:8200/videoDetect/getVideoStream?videoPlayId=12'
          this.mediaSrc = data.videoPlayUrl
          this.sessionIdForClose = data.serviceSessionId
          this.sessionIdsList.push(data.serviceSessionId)
          clearInterval(this.timer)
          this.setTimer()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },

    stopDetect () {
      this.$Spin.show()
      var params = {
        serviceSessionId: this.sessionIdForClose
      }

      this.$post('/cameraStreamVal/stopDetectService', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          // this.$Message.success('摄像头检测已关闭')
          this.sessionIdForClose = ''
          this.sessionIdsList.pop()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    sendHeartbeat () {
      var params = {
        sessionIds: this.sessionIdsList.join(',')
      }
      this.$post('/heartBeat/sendDetectHeartbeat', params).then(data => {
        if(data.rs === 1) {

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
        this.sendHeartbeat()
      }, 20 * 1000);
    },
    back () {
      this.$router.go(-1)
    }
  }
}
</script>

<style lang="scss">
.validate_container {
  .info {
    height: 50px;
  }
  .tip {
    color: rgb(182, 181, 181);
    font-size: 12px;
    margin-top: 10px;
    .font {
      color: #8c0776;
    }
  }
  .left,
  .right {
    float: left;
  }
  .left {
    width: 60%;
    height: 435px;
    background: #f7f7f7;
    position: relative;
    .ivu-upload-drag {
      height: 100%;
    }
    .drag {
      height: 100%;
    }
    .media {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
    }
  }
  .right {
    width: 32%;
    margin-left: 5%;
    .threshold {
      display: flex;
      align-items: center;
    }
    .predict {
      border: 1px solid #eee;
      border-radius: 3px;
      margin-top: 10px;
      .header {
        height: 48px;
        line-height: 48px;
        background: #f7f7f7;
        padding-left: 20px;
        font-size: 12px;
      }
      .label_box {
        height: 340px;
        overflow-y: auto;
        padding: 10px;
      }
      .no_data {
        color: #ccc;
        font-size: 12px;
        margin-top: 140px;
        text-align: center;
      }
    }
    .link_url {
      margin-top: 20px;
    }
  }
}
</style>