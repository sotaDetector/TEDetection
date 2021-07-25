<template>
  <div class="model_manage">
    <div class="container_title">
      <!-- 面包屑 -->
      <Breadcrumb>
        <BreadcrumbItem>历史版本</BreadcrumbItem>
      </Breadcrumb>
      <!-- 操作按钮 -->
      <div class="ops_btn">
        <Button type="primary" icon="ios-arrow-back" size="small" @click="back">返 回</Button>
      </div>
    </div>
    <div class="container_info">
      <p class="title">{{dmName}}全部版本</p>
      <div class="container_box">
        <!-- 查询条件 -->
        <!-- <div class="query_option">
          <Input style="width: 200px;" v-model="search.dmName" placeholder="请输入模型名称"></Input>
          <span class="query_btn">
            <Button type="primary" @click="queryPageInfo">查询</Button>
            <Button @click="clearSearch">重置</Button>
          </span>
        </div> -->
        <!-- 表格列表 -->
        <div class="container_table">
          <!-- <div class="table_head">
            {{table.dmName}}
            <div class="model_action">
              <span class="action" @click="trainModel(table.dmId)">
                <Icon type="ios-book-outline" /> 训练
              </span>
              <span class="action" style="margin:0 20px" @click="goHistory(table.dmId)">
                <Icon type="ios-clock-outline" /> 历史版本
              </span>
              <span class="action" style="margin-right:20px" @click="modifyModal(table.dmId)">
                <Icon type="ios-brush-outline" /> 编辑
              </span>
              <span class="action" @click="delDatas(table.dmId)">
                <Icon type="ios-trash-outline" /> 删除
              </span>
            </div>
          </div> -->
          <Table :columns="columns" :data="versionList">
            <template slot-scope="{row, index}" slot="metrics">
              <div>mAp： {{row.metrics_mAP | percent}}
                <Tooltip placement="right-start" max-width="250" :transfer="true" theme="light">
                  <Icon type="ios-help-circle-outline" color="#8c0776" style="cursor:pointer" />
                  <div slot="content">
                    mAP(mean average precision)是物体检测(Object Detection)算法中衡量算法效果的指标。对于物体检测任务，每一类object都可以计算出其精确率(Precision)和召回率(Recall)，在不同阈值下多次计算/试验，每个类都可以得到一条P-R曲线，曲线下的面积就是average precision(AP)的值。“mean”的意思是对每个类的AP再求平均，得到的就是mAP的值。mAP在[0,1]区间，越接近1模型效果越好。
                  </div>
                </Tooltip>
              </div>
              <div>精确率： {{row.metrics_precision | percent}}
                <Tooltip placement="right-start" max-width="250" :transfer="true" theme="light">
                  <Icon type="ios-help-circle-outline" color="#8c0776" style="cursor:pointer" />
                  <div slot="content">「某类样本正确预测为该类的样本数」占「预测为该类的总样本数」的比率，此处为各类别精确率的平均数。</div>
                </Tooltip>
              </div>
              <div>召回率： {{row.metrics_recall | percent}}
                <Tooltip placement="right-start" max-width="250" :transfer="true" theme="light">
                  <Icon type="ios-help-circle-outline" color="#8c0776" style="cursor:pointer" />
                  <div slot="content">「某类样本正确预测为该类的样本数」占「标注为该类的总样本数」的比率，此处为各类别召回率的平均数。</div>
                </Tooltip>
              </div>
            </template>
            <template slot-scope="{row, index}" slot="action">
              <div>
                <span class="action" @click="viewOptions(row.dmtvid)">查看版本配置</span>
                <span class="action" style="margin:0 4px;" @click="validateModal(dmName,row.dmtvid,row.dmtvName)">校验</span>
                <span class="action" style="margin-right:4px;" @click="viewStatistics(dmName,row.dmtvid,row.dmtvName)">训练统计</span>
                <span class="action" @click="delDatas(row.dmtvid)">删除</span>
              </div>
            </template>
          </Table>
        </div>
        <!-- <div class="pageInfo">
          <Page size="small" :total="total" :page-size='pagesize' @on-change="handleChange" show-total show-elevator></Page>
        </div> -->
      </div>
    </div>
    <!-- 模态框 -->
    <!-- 查看训练模型版本配置 -->
    <Modal class="sys_modal" v-model="modal_option" class-name="vertical_modal" title="版本配置" width="600" :mask-closable="false">
      <div class="modal_body modal_body_option">
        <div class="basic clear-fix">
          <p class="title">基础信息</p>
          <div class="left">
            <div>版本名称：{{optionInfo.dmtvName}}</div>
            <div>模型推断平台：{{optionInfo.inferencePlatform == 1 ? '服务器' : '移动端'}}</div>
            <div>算法精度：{{optionInfo.dmPrecision == 1 ? '小' : optionInfo.dmPrecision == 2 ? '中' : optionInfo.dmPrecision == 3 ? '大' : '特大'}}</div>
            <div>数据增强策略：{{optionInfo.dataEnhanceType == 1 ? '默认配置' : '手动配置'}}</div>
          </div>
          <div class="right">
            <div>训练次数：{{optionInfo.epochs}}</div>
            <div>批大小：{{optionInfo.batch_size}}</div>
            <div>是否使用预训练模型：{{optionInfo.isUsePreTraindModel == 'true' ? '是' : '否'}}</div>
            <div>训练完成时间：{{optionInfo.trainEndDateTime && optionInfo.trainEndDateTime.$date | dateFormat}}</div>
          </div>
        </div>
        <p class="title" style="margin-top:10px;">训练数据集</p>
        <div class="modal_body modal_body_train">
          <Table :columns="columns3" :data="optionInfo.ds_dl_list"></Table>
        </div>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="cancel()">确定</Button>
        <!-- <Button type="default" class="clear_btn" @click="cancel()">取消</Button> -->
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_delete" class-name="vertical_modal" width="316">
      <div class="modal_body modal_body_delete">
        <p>
          <img src="@/assets/img/warn_tip.png" alt="">
          您确定要删除该版本吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod()">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  mounted () {
    this.dmid = parseInt(this.$route.params.id)
    this.dmName = this.$route.query.dmName
    this.queryPageInfo()
  },
  data () {
    return {
      // total: 0,// 初始化信息总条数
      // pageNow: 1,
      // pagesize: 20,// 每页显示多少条
      dmName: '',
      search: {},
      modal_delete: false,
      modal_option: false, // 查看模型版本配置
      versionList: [],
      // dataList: [],
      // labelList: [],
      optionInfo: {},
      columns: [
        {
          "title": "版本名称",
          "align": "center",
          "key": "dmtvName",
          'width': 140,
        }, {
          "title": "训练状态",
          "align": "center",
          "key": "trainState",
        },
        {
          "title": "算法精度",
          "align": "center",
          "key": "dmPrecisionValue",
        }, {
          "title": "平台",
          "align": "center",
          "key": "inferencePlatformValue"
        }, {
          "title": "数据集",
          "align": "center",
          "key": "datasetNames",
          "className": 'label_cell',
          'width': 170,
          render: (h, params) => {
            var datasetNames = params.row.datasetNames && params.row.datasetNames.map((item, idx) => {
              return idx == 0 ? item : '、' + item
            })
            return h('div', datasetNames)
          }
        }, {
          "title": "模型效果",
          "align": "center",
          "slot": 'metrics',
          'width': 190
        }, {
          'title': '操作',
          'align': 'center',
          'key': 'action',
          'width': 220,
          'slot': 'action'
        }],
      columns3: [
        {
          "title": "数据集",
          "align": "center",
          "key": "dsName"
        }, {
          "title": "标签",
          "align": "center",
          "className": 'label_cell',
          "width": 220,
          "key": "dlNameList",
          render: (h, params) => {
            var title = ''
            // var dlNameList = params.row.dlNameList && params.row.dlNameList.map((item, idx) => {
            //   return idx == 0 ? item : '、' + item
            // })
            return h('div', {
              attrs: {
                title: params.row.dlNameList.join('、')
              },
            }, params.row.dlNameList.join('、'))
          }
        }
      ],
      pageInfo: {},
    }
  },
  methods: {
    // 获取版本信息
    queryPageInfo () {
      let params = {
        // pageIndex: this.pageNow,
        // pageSize: this.pagesize,
        // dmName: this.search.dmName
        dmid: this.dmid
      }
      this.$Spin.show()
      this.$post('/detectModelTrain/getDMVersionList', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.versionList = data.data;
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
    //分页
    // handleChange (page) {
    //   this.pageNow = page;//赋值当前页
    //   this.queryPageInfo();
    // },
    // 新增弹框
    addModal () {
      this.modal_add = true
    },
    // 确认新增
    addInfoMethod (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          this.$Spin.show()
          this.$post('/detectModel/addDetectModel', {
            dmName: this.addInfo.dmName,
            dmRemark: this.addInfo.dmRemark,
            dmType: 1
          }).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.modal_add = false
              this.$Message.success('新增成功!');
              this.$refs[name].resetFields();// 清空
              this.queryPageInfo();
            } else {
              if(data.data && data.data.errorMsg) {
                this.$Message.error(data.data.errorMsg);
              } else {
                this.$Message.error(data.errorMsg);
              }
            }
          })
        } else {
          this.$Message.error('新增失败!');
        }
      })
    },
    viewOptions (dmtvid, idx) {
      this.dmtvid = dmtvid
      this.$Spin.show()
      this.$post('/detectModelTrain/getDMVersionDetail', {
        dmtvid: dmtvid
      }).then(data => {
        if(data.rs === 1) {
          this.$Spin.hide()
          this.optionInfo = data.data
          this.modal_option = true
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    validateModal (dmName, dmtvid, dmtvName) {
      this.$router.push({ path: '/modelValidate/' + dmtvid, query: { dmName, dmtvName } })
    },
    viewStatistics (dmName, dmtvid, dmtvName) {
      this.$router.push({ path: '/trainStatistics/' + dmtvid, query: { dmName, dmtvName } })
    },
    delDatas (id) {
      this.dmtvid = id
      this.modal_delete = true
    },
    deleteMethod () {
      this.$Spin.show()
      this.$post('/detectModelTrain/delDMVersion', { dmtvid: this.dmtvid }).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.modal_delete = false
          this.$Message.success('删除成功!');
          this.queryPageInfo();
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    cancelTrainData (name) {
      this.modal_trainData = false
      if(name) {
        this.$refs[name].resetFields();
      }
    },
    cancel (name) {
      this.modal_add = false
      this.modal_modify = false
      this.modal_delete = false
      this.modal_train = false
      this.modal_option = false
      if(name) {
        this.$refs[name].resetFields();
      }
    },
    back () {
      this.$router.go(-1)
    }
    // 重置
    // clearSearch () {
    //   this.search = {
    //     dmName: ''
    //   }
    // }
  }
}
</script>

<style lang="scss">
.model_manage {
  .action {
    color: #8c0776;
    cursor: pointer;
    i {
      font-size: 16px;
    }
  }
  .table_head {
    border-bottom: 1px solid #eee;
    padding: 0 20px 0 14px;
    line-height: 64px;
    background-color: #eee;
    .model_action {
      float: right;
      text-align: right;
    }
  }
}

.modal_body_option .title:before,
.container_info p.title:before {
  content: "";
  display: inline-block;
  vertical-align: middle;
  width: 4px;
  height: 15px;
  background: #8c0776;
  margin: 10px 20px 10px 0;
}
.basic div {
  margin: 10px;
}
.modal_body.modal_body_option {
  max-height: 378px;
  overflow-y: auto;
}
.label_cell .ivu-table-cell div {
  // width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.modal_body_train {
  max-height: 450px;
  overflow-y: auto;
}
.basic .left {
  float: left;
  margin: 0;
}
.basic .right {
  float: right;
  margin: 0;
}
</style>