<template>
  <div class="container">
    <div class="img_box unselect" ondragstart="return false">
      <img id="img" :src="imgSrc" alt="" ondragstart="return false" class="unselect" />
    </div>
    <!-- 添加标签 -->
    <div class="add_label">
      <Button type="primary" icon="ios-arrow-back" size="small" @click="back" style="margin-left:20px;">返 回</Button>
      <div class="title">
        <Icon style="font-size:22px;margin-top:3px;margin-right:6px;margin-left:20px;" type="ios-menu" />
        <span style="margin-right:25px;">标签管理</span>
        <!-- <Button icon="ios-add-circle-outline" type="success" size="small" @click="addLabel">新增标签</Button> -->
        <Button type="success" size="small" @click="addLabel">新 增</Button>
      </div>
      <ul class="add">
        <li class="add_li" v-for="(item, idx) in labelList" :key="idx">
          <Input ref="labelInput" v-if="!item.edited" type="text" placeholder="标签名称" size="small" style="width:110px;margin-right:5px;" v-model="item.dlName"></Input>
          <span style="color:#fff;margin-right:18px;" v-if="item.edited">{{ item.dlName }}</span>
          <span v-if="item.edited" class="iconfont icon-bianji label_icon" style="font-size:18px;" @click="editLabel(idx)"></span>
          <Icon v-if="item._id" class="label_icon" type="ios-trash" @click="delLabel(item._id)" />
          <Icon v-if="!item.edited" class="label_icon" type="ios-cloud-upload" @click="saveLabel(item,idx)" />
        </li>
      </ul>
    </div>
    <!-- 选择标签 -->
    <div class="choose_label">
      <div class="title" style="margin-top:10px;">
        <Icon style="font-size:22px;margin-top:3px;margin-right:6px" type="ios-menu" />
        标注管理
      </div>
      <ul class="choose">
        <li class="cho_li" v-for="(item, idx) in divList" :key="idx">
          <Select :class="[item.id, 'select']" v-model="item.dlid" size="small" style="width: 150px" @on-change="selectLabel(item)" @on-open-change="openSelect(item, $event)">
            <Option v-for="(label, i) in myLabelList" :value="label._id" :key="i">{{
              label.dlName
            }}</Option>
          </Select>
          <img src="@/assets/img/delete_red.png" alt="" class="delete delete_div" @click="delDiv(item.id, 'delDiv')" />
        </li>
        <li>
          <Button type="success" size="small" @click="submit" v-if="divList.length" style="width:150px;margin-top:20px;margin-left:-30px;">提交标注结果</Button>
        </li>
      </ul>
    </div>

    <!-- 图片列表 -->
    <img-list @chooseImg="chooseImg" @back="back" :taskType="2" ref="imgList"></img-list>

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

var s1, s2, s3, s4, s5, s6

import ImgList from '@/components/ImgList.vue'
export default {
  name: "MarkImg",
  components: {
    ImgList
  },
  mounted () {
    this.dsId = this.$route.params.id
    this.getLabelList()
  },
  data () {
    return {
      imgSrc: '',
      dsId: '', // 数据集Id
      labelList: [],
      myLabelList: [],
      dlid: '',
      modal_delete: false,
      divList: [
        {
          h: 0.03202846975088968,
          id: "833434",
          dlid: "mouth",
          dlName: 'mouth',
          w: 0.13345195729537365,
          x: 0.4884341637010676,
          y: 0.4592600830367734
        }
      ],
    };
  },
  methods: {
    chooseImg (imgInfo, isChoose) {
      if(isChoose) {
        this.$Spin.show()
      }
      this.clearTime()
      this.imgSrc = imgInfo.ditFilePath

      this.ditId = imgInfo._id
      var path = '/markImg/' + this.dsId + '/' + this.ditId
      if(this.$route.path != path) {
        this.$router.push({ path })
      }
      // $('#img').remove()
      // s1 = setTimeout(() => {
      this.initPage(imgInfo)
      // }, 100);
    },
    initPage (imgInfo) {
      $('.content-box').scrollLeft(0)
      // 移除上一张图的标注
      if($('.box').length) {
        $('.box').remove()
      }
      // 解绑上一张图绑定的事件
      $('.img_box').unbind()
      $('#img').unbind()
      // 清空标注
      this.divList = []

      var _this = this;
      // var img_url = document.getElementById("img").src;
      // var img = new Image();
      // img.src = img_url;
      var ratio = imgInfo.ditWidth / imgInfo.ditHeight
      // img.onload = function () {
      //   ratio = img.width / img.height;
      // };

      s2 = setTimeout(() => {
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

        var height = img.height();
        var width = img.width();
        var iTop = img.offset().top;
        var iLeft = img.offset().left;
        var bTop = imgBox.offset().top;
        var bLeft = imgBox.offset().left;
        // console.log(iTop, iLeft)
        // console.log(ratio, width, height)

        var startX, startY, endX, endY;
        // var divList = _this.divList;

        var drawing = false;
        var dragging = false;

        var dragStartX, dragStartY, dragDiv;


        // img.css({ 'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)' })



        function handleDown (e) {
          dragging = true;
          if(e.target.className.indexOf("box") >= 0) {
            dragDiv = e.target;
          } else {
            dragDiv = e.path[1];
          }
          $(dragDiv).addClass("dragging");
          dragStartX = e.pageX;
          dragStartY = e.pageY;

          s3 = setTimeout(() => {
            $(".box").css("border", "1px dashed rgb(66, 104, 207, 0.5)");
            dragDiv.style.border = "2px solid rgb(94, 207, 66)";

            $(".cho_li .ivu-select").css("border", "none");

            // $("." + dragDiv.id).css({
            //   border: "2px solid rgb(94, 207, 66)",
            //   "border-radius": "6px",
            // });
            var index = _this.divList.findIndex(item => item.id == dragDiv.id)
            $(".cho_li .ivu-select").eq(index).css({ "border": "2px solid rgb(94, 207, 66)", "border-radius": "6px" });
          }, 50);
        }

        function handleMove (e) {
          // if(dragging && e.pageX <= width + iLeft && e.pageX >= iLeft && e.pageY <= height + iTop && e.pageY >= iTop) {
          if(dragging) {
            // 鼠标在图片范围内
            if(
              e.pageX <= width + iLeft &&
              e.pageX >= iLeft &&
              e.pageY <= height + iTop &&
              e.pageY >= iTop
            ) {
              var $dragDiv = $(dragDiv);
              var top = $dragDiv.position().top;
              var left = $dragDiv.position().left;
              var diffX = e.pageX - dragStartX;
              var diffY = e.pageY - dragStartY;

              var dWidth = $dragDiv.width() + 4;
              var dHeight = $dragDiv.height() + 4;

              var dTop = top + diffY;
              var dLeft = left + diffX;

              var iPTop = img.position().top;
              var iPLeft = img.position().left;

              dTop =
                dTop < iPTop ? iPTop : dTop > height - dHeight + iPTop ? height - dHeight + iPTop : dTop;
              dLeft =
                dLeft < iPLeft ? iPLeft : dLeft > width - dWidth + iPLeft ? width - dWidth + iPLeft : dLeft;

              dragDiv.style.top = dTop + "px";
              dragDiv.style.left = dLeft + "px";
              // dragDiv.style.left = (dLeft - $('.content-box').scrollLeft()) + "px";

              dragStartX = e.pageX;
              dragStartY = e.pageY;
            } else {
              dragDiv.removeEventListener("mouseup", null);
              dragging = false;
              $(dragDiv).removeClass("dragging");
            }
            // console.log(dragStartX, diffX, dragStartX - iLeft - diffX)
          }
        }

        function handleUp (e) {
          if(!$(dragDiv).length) return false;
          // console.log("dragdiv", dragDiv);
          dragging = false;
          // console.log(e)
          var x = $(dragDiv).position().left - img.position().left;
          var y = $(dragDiv).position().top - img.position().top;
          // console.log(x, y);
          _this.divList.forEach((item) => {
            // console.log(item.id, e.target.id)
            if(item.id == dragDiv.id) {
              item.x = x / width;
              item.y = y / height;
              item.id = (x.toString() + y.toString()).replace(/\./g, "");
            }
          });
          dragDiv.id = (x.toString() + y.toString()).replace(/\./g, "");
          $(dragDiv).removeClass("dragging");
          dragDiv = null;
        }

        s4 = setTimeout(() => {
          _this.divList = imgInfo.recLabelList.map(item => {
            return {
              x: item.rec_lt_x,
              y: item.rec_lt_y,
              w: item.rec_w,
              h: item.rec_h,
              dlid: item.dlid,
              dlName: item.dlName,
              id: item._id
            }
          })

          // 根据divList渲染div
          for(var i = 0; i < _this.divList.length; i++) {
            var item = _this.divList[i];

            var div = document.createElement("div");
            div.className = "box";
            div.style.width = item.w * width + "px";
            div.style.height = item.h * height + "px";
            div.style.top = item.y * height + img.position().top + "px";
            div.style.left = item.x * width + img.position().left + "px";
            div.id = item.id;
            div.addEventListener("mousedown", handleDown);
            div.addEventListener("mousemove", handleMove);
            div.addEventListener("mouseup", handleUp);
            $(div).html("<span>" + item.dlName + "</span>");
            img.after(div);
          }

          img.mousedown(function (e) {
            // console.log(e)
            drawing = true;
            startX = e.pageX;
            startY = e.pageY;

            var div = document.createElement("div");
            div.className = "active";
            div.style.top = startY - bTop + "px";
            div.style.left = startX - bLeft + "px";
            // div.style.left = (startX - bLeft + $('.content-box').scrollLeft()) + "px";

            // console.log($('.content-box').scrollLeft())
            // console.log(startX, iLeft)
            img.after(div);
          });
          $('.img_box').mousemove(function (e) {
            // console.log(e.pageX <= width + iLeft, e.pageX >= iLeft)
            if(drawing && e.pageX <= width + iLeft && e.pageX >= iLeft && e.pageY <= height + iTop && e.pageY >= iTop) { } else {
              $('.active').remove()
              drawing = false
            }
            if(drawing && $(".active").length) {
              $(".active").width(e.pageX - startX);
              $(".active").height(e.pageY - startY);
            }
          });
          $('.img_box').mouseup(function (e) {
            // console.log('document-mouseup')
            e.stopPropagation()
            var active = $(".active");
            if(active.length) {
              drawing = false;

              if(active.width() <= 10 && active.height() <= 10) {
                active.remove();
                return false;
              }

              var div = document.createElement("div");
              div.className = "box";
              div.style.width = active.width() + "px";
              div.style.height = active.height() + "px";
              div.style.top = active.position().top + "px";
              div.style.left = active.position().left + "px";
              div.id = (startX.toString() + startY.toString()).replace(/\./g, "");
              div.addEventListener("mousedown", handleDown);
              div.addEventListener("mousemove", handleMove);
              div.addEventListener("mouseup", handleUp);
              if(_this.divList.length) {
                $(div).html(
                  "<span>" +
                  _this.divList[_this.divList.length - 1].dlName +
                  "</span>"
                );
              }

              img.after(div);
              active.remove();

              endX = e.pageX;
              endY = e.pageY;

              _this.divList.push({
                x: (startX - iLeft) / width,
                y: (startY - iTop) / height,
                w: div.offsetWidth / width,
                h: div.offsetHeight / height,
                id: div.id,
                dlName: _this.divList.length
                  ? _this.divList[_this.divList.length - 1].dlName
                  : "",
                dlid: _this.divList.length
                  ? _this.divList[_this.divList.length - 1].dlid
                  : "",
              });
              // console.log(startX,startY,endX,endY)

              s5 = setTimeout(() => {
                $(".box").css("border", "1px dashed rgb(66, 104, 207, 0.5)");
                div.style.border = "2px solid rgb(94, 207, 66)";

                $(".cho_li .select").css("border", "none");

                $("." + div.id).css({
                  border: "2px solid rgb(94, 207, 66)",
                  "border-radius": "6px",
                });
              }, 50);
            }
            if($(dragDiv).length && e.target.className.indexOf("dragging") == -1) {
              dragDiv.removeEventListener("mouseup", null);
              dragging = false;
              $(dragDiv).removeClass("dragging");
            }
          });

          s6 = setTimeout(() => {
            this.$Spin.hide()
          }, 500);
        }, 100);
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

          // this.labelList = [...data.data]
          // this.labelList.forEach(item => {
          //   item.edited = true
          // })
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
    changeDivName (id, name) {
      // console.log(this.divList, id)
      this.divList.forEach(item => {
        if(item.dlid == id) {
          $('#' + item.id).html("<span>" + name + "</span>")
          item.dlName = name
        }
      })
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

        this.changeDivName(item._id, item.dlName)
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
          this.$Message.success('删除成功')
          this.delDiv(id, 'delLabel')
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
    // inputAddLabel (idx, e) {
    //   this.$set(this.labelList[idx], 'dlName', e);
    // },
    openSelect (item) {
      var { id } = item;
      $(".box").css("border", "1px dashed rgb(66, 104, 207, 0.5)");
      $("#" + id).css("border", "2px solid rgb(94, 207, 66)");

      $(".cho_li .select").css("border", "none");
      $("." + id).css({
        border: "2px solid rgb(94, 207, 66)",
        "border-radius": "6px",
      });
    },
    selectLabel (item) {
      var { id, dlid } = item;
      dlid = dlid ? dlid : "";
      var dlName = this.myLabelList.find(item => item._id == dlid) && this.myLabelList.find(item => item._id == dlid).dlName
      item.dlName = dlName
      $("#" + id).html("<span>" + dlName + "</span>");
    },
    delDiv (id, type) {
      console.log(id)
      console.log(this.divList)
      if(type == 'delLabel') {
        this.divList.forEach((item, idx) => {
          if(item.dlid == id) {
            this.divList.splice(idx, 1)
            $('#' + item.id).remove()
          }
        })
      } else if(type == 'delDiv') {
        this.divList = this.divList.filter((item) => item.id != id);
        $("#" + id).remove();
      }
    },
    submit () {
      var item = this.divList.find((item) => !item.dlName);
      if(item) {
        this.$Message.error("请为所有标注框选择标签");
        return false;
      }
      console.log(this.divList);
      this.$Spin.show()
      this.$post('/dsc/upImageItemRecLabels', {
        dsId: this.dsId,
        ditId: this.ditId,
        recLabelList: this.divList.map(item => {
          return {
            "rec_lt_x": item.x,
            "rec_lt_y": item.y,
            "rec_w": item.w,
            "rec_h": item.h,
            "dlid": item.dlid,
            // 'dlName': item.dlName
          }
        })
      }).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.modal_modify = false
          this.$Message.success('提交成功!');
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
      for(var i = 1; i <= 6; i++) {
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
.container {
  // width: 1200px;
  width: 100%;
  height: calc(100vh - 72px);
  margin: 0 auto;
  text-align: center;
  background: #333;
  position: relative;
  // padding-bottom: 110px;
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
    height: 78%;
    position: absolute;
    top: 42%;
    left: 50%;
    transform: translate(-50%, -50%);
    // overflow-x: auto;
    // overflow-y: hidden;
  }

  #img {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  #img:hover {
    cursor: crosshair;
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

  .choose_label,
  .add_label {
    // max-height: calc(100% - 110px);
    // overflow-y: auto;
    padding-top: 20px;
    width: 22%;
    height: 100%;
  }

  .choose_label {
    float: right;
    margin-right: 20px;
    padding-left: 20px;
  }
  .add {
    max-height: calc(100% - 228px);
    overflow-y: auto;
  }
  .choose {
    max-height: calc(100% - 175px);
    overflow-y: auto;
  }

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
    text-align: left;
    // vertical-align: middle;
  }
  .add_label {
    float: left;
    text-align: left;
    .add {
      margin: 20px 0 20px 55px;
    }
  }
}
.label_icon {
  cursor: pointer;
  color: #ccc;
  font-size: 20px;
  margin: 0 5px;
}
.add_label .title,
.choose_label .title {
  // width: 110px;
  // border-left: 3px solid #2d8cf0;
  line-height: 20px;
  margin: 20px 4px;
  color: #f0faff;
  font-size: 16px;
  text-align: left;
  // background: #f0faff;
}
</style>
