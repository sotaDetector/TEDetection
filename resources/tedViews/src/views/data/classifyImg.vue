<template>
  <div class="classify_container">
    <div class="query">
      <RadioGroup v-model="isLabeled" type="button" @on-change="changeQuery">
        <Radio :label="2">未标注图片</Radio>
        <Radio :label="1">已标注图片</Radio>
      </RadioGroup>
    </div>
    <div class="empty" v-if="isEmpty">
      暂无数据
    </div>
    <div class="img_box unselect" ondragstart="return false" v-if="!isEmpty">
      <img id="img" :src="imgSrc" alt="" ondragstart="return false" class="unselect" />
      <Icon class="left" type="ios-arrow-back" @click="previousImg()" />
      <Icon class="right" type="ios-arrow-forward" @click="nextImg()" />
    </div>
    <!-- 标注结果 -->
    <div class="result">
      <Button type="primary" icon="ios-arrow-back" size="small" @click="back" style="margin-right:40%;">返 回</Button>
      <div class="title">
        <Icon style="font-size:22px;margin-right:6px;" type="ios-menu" />
        <span style="margin-right:25px;">标注结果</span>
      </div>
      <div class="tip">请在右侧选择标签</div>
      <div v-if="dlName_result" style="font-size:30px;color:red;">{{dlName_result}}</div>
      <div v-else style="color:red">本图片暂未标注分类</div>
    </div>
    <!-- 添加标签 -->
    <div class="add_label">
      <div class="title">
        <Icon style="font-size:22px;margin-top:3px;margin-right:6px;" type="ios-menu" />
        <span style="margin-right:25px;">标签管理</span>
        <!-- <Button icon="ios-add-circle-outline" type="success" size="small" @click="addLabel">新增标签</Button> -->
        <Button type="success" size="small" @click="addLabel">新 增</Button>
      </div>
      <ul class="add">
        <li class="add_li" v-for="(item, idx) in labelList" :key="idx">
          <Input ref="labelInput" v-if="!item.edited" type="text" placeholder="标签名称" size="small" style="width:110px;margin-right:5px;" v-model="item.dlName"></Input>
          <span title="点击选择为标注结果" :style="{color: item._id==dlid_result?'red':'#fff','margin-right':'18px', 'cursor':'pointer'}" v-if="item.edited" @click="selectResult(item)">{{ item.dlName }}</span>
          <span v-if="item.edited" class="iconfont icon-bianji label_icon" style="font-size:18px;" @click="editLabel(idx)"></span>
          <Icon v-if="item._id" class="label_icon" type="ios-trash" @click="delLabel(item._id)" />
          <Icon v-if="!item.edited" class="label_icon" type="ios-cloud-upload" @click="saveLabel(item,idx)" />
        </li>
      </ul>
    </div>
    <!-- 图片列表 -->
    <img-list @chooseImg="chooseImg" @back="back" :taskType="1" @emptyImg="emptyImg" ref="imgList"></img-list>

    <!-- 模态框 -->
    <Modal class="sys_modal" v-model="modal_delete" class-name="vertical_modal" width="316">
      <div class="modal_body modal_body_delete">
        <p><img src="@/assets/img/warn_tip.png" alt="">
          您确定要删除该标签吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod(dlid)">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
  </div>
</template>
<script>

var s1, s2

import ImgList from '@/components/ImgList.vue'
export default {
  name: "ClassifyImg",
  components: {
    ImgList
  },
  mounted () {
    this.dsId = this.$route.params.id
    this.getLabelList()
  },
  data () {
    return {
      isLabeled: 2,
      imgSrc: '',
      dsId: '', // 数据集Id
      labelList: [],
      myLabelList: [],
      dlid: '',
      modal_delete: false,
      dlid_result: '',
      dlName_result: '',
      isEmpty: false
    };
  },
  methods: {
    emptyImg (e) {
      this.isEmpty = e
      this.dlName_result = ''
      this.dlid_result = ''
    },
    changeQuery (e) {
      this.$refs.imgList.changeQuery(e)
    },
    previousImg () {
      this.$refs.imgList.previousImg()
    },
    nextImg () {
      this.$refs.imgList.nextImg()
    },
    chooseImg (imgInfo, isChoose) {
      if(isChoose) {
        this.$Spin.show()
      }
      this.clearTime()
      this.imgSrc = imgInfo.ditFilePath

      this.ditId = imgInfo._id
      var path = '/classifyImg/' + this.dsId + '/' + this.ditId
      if(this.$route.path != path) {
        this.$router.push({ path })
      }
      this.initPage(imgInfo)
    },
    initPage (imgInfo) {
      $('.content-box').scrollLeft(0)

      // console.log(imgInfo)
      this.dlid_result = imgInfo.classifyLabel
      this.dlName_result = imgInfo.classifyLabelName

      var _this = this;
      var ratio = imgInfo.ditWidth / imgInfo.ditHeight

      s1 = setTimeout(() => {
        // 图片标注相关
        var imgBox = $(".img_box");
        var boxWidth = imgBox.width();
        var boxHeight = imgBox.height();
        var img = $("#img");
        // 设置图片宽高以适配屏幕
        if(ratio > 1) {
          img.width("100%");
          img.height(img.width() / ratio);

          if(img.height() > boxHeight) {
            img.height(boxHeight);
            img.width(img.height() * ratio);
          }
        } else {
          img.height("100%");
          img.width(img.height() * ratio);

          if(img.width() > boxWidth) {
            img.width("100%");
            img.height(img.width() / ratio);
          }
        }
        s2 = setTimeout(() => {
          this.$Spin.hide()
        }, 150);
      }, 200);
    },
    getLabelList () {
      let params = {
        dsId: this.dsId
      }
      // this.$Spin.show()
      this.$post('/dataLabel/getAllDataLabelByDsid', params).then(data => {
        // this.$Spin.hide()
        if(data.rs === 1) {
          this.myLabelList = [...data.data]
          this.labelList = data.data.map(item => {
            return {
              dlName: item.dlName,
              _id: item._id,
              edited: true
            }
          })
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    addLabel () {
      if(this.labelList.find(item => !item.dlName)) {
        this.$Message.error('请先输入当前标签')
        return false
      }
      this.labelList.push({
        dlName: '',
        edited: false
      });
      this.$nextTick(() => {
        var inputLength = this.labelList.filter(item => item.edited == false).length
        this.$refs.labelInput[inputLength - 1].focus()
      })
    },
    editLabel (idx) {
      if(!this.labelList[idx].edited) return false
      this.labelList[idx].edited = false
    },
    saveLabel (item, idx) {
      if(!item.dlName || item.edited) return false
      this.$set(this.labelList[idx], 'edited', true)

      if(!item._id) { // 新增
        var params = {
          dlName: item.dlName,
          dsId: this.dsId
        }
        var url = '/dataLabel/addDataLabel'
        var text = '添加'
      } else { // 修改
        var params = {
          dlid: item._id,
          updateClolumn: {
            dlName: item.dlName
          }
        }
        var url = '/dataLabel/updateDataLabel'
        var text = '修改'

      }

      this.$Spin.show()
      this.$post(url, params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.$Message.success(text + '成功')
          this.getLabelList()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    delLabel (id) {
      this.modal_delete = true
      this.dlid = id
    },
    deleteMethod (id) {
      this.$Spin.show()
      this.$post('/dataLabel/delDataLabel', { dlid: id }).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.modal_delete = false
          this.$Message.success('删除成功！')
          this.getLabelList()
          this.$refs.imgList.getImgs();
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    cancel () {
      this.modal_delete = false
    },
    selectResult (item) {
      if(this.isEmpty) return false
      this.dlid_result = item._id
      this.dlName_result = item.dlName
      this.submit()
    },
    submit () {
      if(!this.dlid_result) return false

      this.$Spin.show()
      this.$post('/clsImgDS/upClsImgItem', {
        dsId: this.dsId,
        clsimgid: this.ditId,
        classifyLabel: this.dlid_result
      }).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.modal_modify = false
          this.$Message.success('保存成功!');
          this.dlid_result = ''
          this.dlName_result = ''
          this.$refs.imgList.getImgs();
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    clearTime () {
      for(var i = 1; i <= 2; i++) {
        if('s' + i) {
          clearTimeout('s' + i)
        }
      }
    },
    back () {
      this.$router.push('/dataManage')
    }
  },
};
</script>
<style lang="scss">
* {
  box-sizing: border-box;
}
.classify_container {
  // width: 1200px;
  width: 100%;
  height: calc(100vh - 72px);
  margin: 0 auto;
  text-align: center;
  background: #333;
  position: relative;
  padding-top: 1px;
  .query {
    margin-top: 13px;
    .ivu-radio-group-button .ivu-radio-wrapper-checked {
      background: #8c0776;
      color: #fff;
    }
  }
  .empty {
    display: inline-block;
    padding-top: 200px;
    color: #ccc;
  }
  .unselect {
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    -khtml-user-select: none;
    user-select: none;
  }
  .img_box {
    // max-width: 710px;
    width: 52%;
    // height: 90%;
    height: 71%;
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    .left,
    .right {
      width: 32px;
      height: 68px;
      background: rgba(255, 255, 255, 0.3);
      position: absolute;
      top: 50%;
      margin-top: -34px;
      font-size: 30px;
      color: #fff;
      line-height: 64px;
      cursor: pointer;
    }
    .left {
      left: 0;
      border-radius: 6px 0 0 6px;
    }
    .right {
      right: 0;
      border-radius: 0 6px 6px 0;
    }
  }

  #img {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  #img:hover {
    // cursor: crosshair;
  }

  .active,
  .box {
    background: rgba(66, 104, 207, 0.3);
    position: absolute;
  }

  .box {
    border: 1px dashed rgb(66, 104, 207, 0.5);
    // border: 1px dashed rgba(94, 207, 66, 0.5);
    cursor: move;
  }
  .box span {
    // background: #aaa;
    font-size: 12px;
    background: rgba(0, 0, 0, 0.2);
    color: #fff;
    position: absolute;
    bottom: 0;
    left: 0;
  }

  .result,
  .add_label {
    // max-height: calc(100% - 110px);
    // overflow-y: auto;
    // padding-top: 20px;
    width: 22%;
    height: calc(100% - 32px);
  }

  .result {
    float: left;
    color: #fff;
    text-align: left;
    padding-left: 30px;
    // padding-top: 70px;
    .tip {
      margin: 20px 0;
    }
  }
  .add_label {
    float: right;
    .add {
      margin-right: 20px;
      max-height: calc(100% - 228px);
      overflow-y: auto;
      text-align: left;
      padding-left: 20px;
    }
  }
  // .choose {
  //   max-height: calc(100% - 165px);
  //   overflow-y: auto;
  // }

  /* 设置滚动条的样式 */
  .add::-webkit-scrollbar,
  .choose::-webkit-scrollbar {
    width: 12px;
  }
  /* 滚动槽 */
  .add::-webkit-scrollbar-track,
  .choose::-webkit-scrollbar-track {
    // -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    -webkit-box-shadow: inset 0 0 6px rgba(255, 255, 255, 0.2);
    border-radius: 10px;
  }
  /* 滚动条滑块 */
  .add::-webkit-scrollbar-thumb,
  .choose::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background: rgba(0, 0, 0, 0.1);
    // -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
    -webkit-box-shadow: inset 0 0 6px rgba(255, 0, 0, 0.8);
  }
  .delete {
    width: 16px;
    height: 16px;
    margin-left: 16px;
    vertical-align: middle;
    cursor: pointer;
  }
  .add_li,
  .cho_li {
    line-height: 40px;
    height: 40px;
    // vertical-align: middle;
  }
}
.label_icon {
  cursor: pointer;
  color: #ccc;
  font-size: 20px;
  margin: 0 5px;
}
.add_label {
  text-align: left;
}
.add_label .title,
.result .title {
  // width: 110px;
  // border-left: 3px solid #2d8cf0;
  line-height: 20px;
  margin: 20px 4px;
  color: #f0faff;
  font-size: 16px;
}
</style>
