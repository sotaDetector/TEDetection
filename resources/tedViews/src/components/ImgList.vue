<template>
  <div class="container">
    <div class="left" @click="clickLeft">
      <Icon type="ios-arrow-back" />
    </div>
    <div class="img_list">
      <!-- <ul class="list">
        <li @click="chooseImg()" v-for="(item,idx) in 15" :key="idx"><img src="@/assets/img/美女.jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/timg (1).jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/timg (2).jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/timg (3).jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/white.jpg" alt="" /></li>
      </ul> -->
      <ul class="list" v-if="imgList.length">
        <li :class="{'actived': idx==activeIdx}" @click="chooseImg(item,idx,true)" v-for="(item,idx) in imgList" :key="item._id">
          <img :src="item.ditFilePath" alt="" />
          <Icon type="md-close-circle" class="del" @click.stop.prevent="delImg(item._id)" />
        </li>
      </ul>
    </div>
    <div class="right" @click="clickRight">
      <Icon type="ios-arrow-forward" />
    </div>

    <Page style="margin-top:10px;" size="small" :total="total" :page-size='pagesize' @on-change="handleChange" show-total show-elevator></Page>
    <!-- 模态框 -->
    <Modal class="sys_modal" v-model="modal_delete" class-name="vertical_modal" width="316">
      <div class="modal_body modal_body_delete">
        <p><img src="@/assets/img/warn_tip.png" alt="">
          您确定要删除该图片吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod(ditId)">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
  </div>
</template>

<script>

export default {
  data () {
    return {
      ditId: '',
      modal_delete: false,
      activeIdx: 0,
      total: 0,// 初始化信息总条数
      pageNow: 1,
      pagesize: 20,// 每页显示多少条
      isLabeled: 2, // 未标注
      imgList: [
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (3).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (3).jpg"),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require("@/assets/img/timg (2).jpg"),
        // require("@/assets/img/timg (1).jpg"),
        // require("@/assets/img/timg (3).jpg"),
        // require("@/assets/img/timg (3).jpg"),
        // require("@/assets/img/white.jpg"),
        // require("@/assets/img/timg (2).jpg"),
      ],
    }
  },
  mounted () {
    this.getImgs(true)
    console.log(this.taskType)
  },
  props: {
    taskType: Number
  },
  methods: {
    changeQuery (isLabeled) {
      this.isLabeled = isLabeled
      this.ditId = ''
      this.activeIdx = 0
      this.pageNow = 1
      this.getImgs()
    },
    getImgs (isInit) {
      var type = this.taskType
      var id = parseInt(this.$route.params.id)
      var url = ''
      var params = {
        pageSize: this.pagesize,
        pageIndex: this.pageNow,
        dsId: id
      }
      if(type == 1) { // 图像分类
        url = '/clsImgDS/getClsImgItemList'
        params.isLabeled = this.isLabeled
      } else if(type == 2) { // 目标检测
        url = '/dsc/getImageItemList'
      }

      this.$Spin.show()
      this.$post(url, params).then(data => {
        if(data.rs === 1) {
          var pageData = data.pageData

          // 最后一页删除了最后一个数据之后，往回退一页
          if(pageData.page > pageData.totalPages && !pageData.dataList.length && type == 2) { // 图片分类-未标注或已标注图片数量都有可能为0
            this.reset()
            return false
          }

          this.imgList = pageData.dataList
          this.total = pageData.totalCount;//总数
          this.chosePage = pageData.page;//选择页
          this.pageNow = pageData.page;//当前页

          if(isInit) {
            var ditId = this.$route.params.ditId
            if(ditId) {
              this.activeIdx = this.imgList.findIndex(item => item._id == ditId)
            }
          }

          if(type == 1) {
            if(!this.imgList.length) { // 图片分类-未标注或已标注图片数量都有可能为0
              this.$Spin.hide()
              this.$emit('emptyImg', true)
              return false
            } else {
              this.$emit('emptyImg', false)
            }
          }

          var index = this.imgList[this.activeIdx] ? this.activeIdx : 0
          this.activeIdx = index
          this.chooseImg(this.imgList[index], this.activeIdx)

          setTimeout(() => {
            $('.list').width($('.list li').length * 80)
            this.listWidth = $('.list').width()
            this.boxWidth = $('.img_list').width()
            this.$Spin.hide()
          }, 200);

        } else {
          this.$Spin.hide()
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    //分页
    handleChange (page) {
      this.pageNow = page;//赋值当前页
      this.activeIdx = 0
      this.getImgs();
      setTimeout(() => {
        $('.list').css({ left: 0 })
      }, 200);
    },
    reset () {
      this.pageNow = this.pageNow - 1
      if(this.pageNow == 0) {
        this.$emit('back')
        return false
      }
      this.getImgs()
    },
    delImg (id) {
      this.modal_delete = true
      this.ditId = id
    },
    deleteMethod () {
      var url = this.taskType == 1 ? '/clsImgDS/delClsImgItem' : '/dsc/delImageItem'
      var params = this.taskType == 1 ? { clsimgid: this.ditId } : { ditId: this.ditId }

      this.$Spin.show()
      this.$post(url, params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.modal_delete = false
          this.$Message.success('删除成功')
          this.getImgs()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    chooseImg (item, idx, isChoose) {
      this.activeIdx = idx
      this.$emit('chooseImg', item, isChoose)
    },
    previousImg () {
      if(this.activeIdx == 0) return false
      this.activeIdx -= 1
      this.$emit('chooseImg', this.imgList[this.activeIdx], true)
    },
    nextImg () {
      if(this.activeIdx == this.imgList.length - 1) return false
      this.activeIdx += 1
      this.$emit('chooseImg', this.imgList[this.activeIdx], true)
    },
    clickLeft () {
      var left = $('.list').position().left
      left += 500
      if(left >= 0) {
        $('.list').animate({ left: 0 })
        return false
      }
      $('.list').animate({ left: left + 'px' })
    },
    clickRight () {
      var left = $('.list').position().left
      left -= 500
      if(left <= this.boxWidth - this.listWidth) {
        $('.list').animate({ left: (this.boxWidth - this.listWidth) + 'px' })
        return false
      }
      $('.list').animate({ left: left + 'px' })
    },
    cancel () {
      this.modal_delete = false
    },
  }
}
</script>

<style lang="scss" scoped>
.container {
  width: 100%;
  color: #fff;
  height: 110px;
  position: absolute;
  bottom: 10px;
  left: 0;
  padding: 5px 60px 0;
}
.img_list {
  width: calc(100% - 40px);
  margin: 0 auto;
  overflow: hidden;
  position: relative;
  height: 70px;
  padding-top: 10px;
}
.list {
  display: flex;
  // justify-content: center;
  // width: calc(100% - 40px);
  position: relative;
  left: 0;
  width: auto;
}
.list li {
  width: 60px;
  height: 60px;
  margin: 0 10px;
  cursor: pointer;
  flex: none;
  position: relative;
  &.actived {
    border: 2px solid rgb(94, 207, 66);
  }
  img {
    width: 100%;
    height: 100%;
  }
  .del {
    color: #ff2842;
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 18px;
  }
}
.right,
.left {
  cursor: pointer;
  width: 60px;
  height: 60px;
  color: #fff;
  font-size: 30px;
  line-height: 60px;
  text-align: center;
  background: rgba(255, 255, 255, 0.3);
  position: absolute;
  top: 15px;
}
.left {
  left: 0;
}
.right {
  right: 0;
}
</style>