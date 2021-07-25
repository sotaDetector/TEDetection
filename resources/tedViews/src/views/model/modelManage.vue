<template>
  <div class="model_manage">
    <div class="container_title">
      <!-- 面包屑 -->
      <Breadcrumb>
        <BreadcrumbItem>模型管理</BreadcrumbItem>
      </Breadcrumb>
      <!-- 操作按钮 -->
      <div class="ops_btn">
        <Button type="primary" ghost size='small' @click="addModal">新增</Button>
      </div>
    </div>
    <div class="container_info">
      <div class="container_box">
        <!-- 查询条件 -->
        <div class="query_option">
          <Input style="width: 200px;" v-model="search.dmName" placeholder="请输入模型名称"></Input>
          <Select v-model="search.cvTaskType" style="width:200px;margin-left:20px;" placeholder="请选择任务类型">
            <Option :value="item.cvTaskType" v-for="(item,idx) in cvTaskTypeList" :key="idx">{{item.cvTaskName}}</Option>
          </Select>
          <span class="query_btn">
            <Button type="primary" @click="queryPageInfo">查询</Button>
            <Button @click="clearSearch">重置</Button>
          </span>
        </div>
        <!-- 表格列表 -->
        <div class="container_table" v-for="(table,index) in pageInfo.dataList" :key="index">
          <div class="table_head">
            {{table.dmName}}
            <span style="margin-left:20px">模型ID：{{table.dmId}}</span>
            <span v-if="table.cvTaskTypeName" class="type_name">{{table.cvTaskTypeName}}</span>
            <div class="model_action">
              <span class="action" @click="trainModel(table.dmId)">
                <Icon type="ios-book-outline" /> 训练
              </span>
              <span class="action" style="margin:0 20px" @click="goHistory(table)">
                <Icon type="ios-clock-outline" /> 历史版本
              </span>
              <span class="action" style="margin-right:20px" @click="modifyModal(table.dmId)">
                <Icon type="ios-brush-outline" /> 编辑
              </span>
              <span class="action" @click="delDatas(table.dmId)">
                <Icon type="ios-trash-outline" /> 删除
              </span>
            </div>
          </div>
          <Table :columns="columns" :data="table.latestVersionItem">
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
                <span class="action" style="margin:0 6px;" @click="validateModal(table.dmName,row.dmtvid,row.dmtvName)">校验</span>
                <span class="action" style="margin-right:6px;" @click="viewStatistics(table.dmName,row.dmtvid,row.dmtvName)">训练统计</span>
                <!-- <span class="action" @click="delDatas(row.dmId)">删除</span> -->
              </div>
            </template>
          </Table>
        </div>
        <div class="pageInfo">
          <Page size="small" :total="total" :page-size='pagesize' @on-change="handleChange" show-total show-elevator></Page>
        </div>
      </div>
    </div>
    <!-- 模态框 -->
    <!-- 训练弹窗 -->
    <Modal class="sys_modal" v-model="modal_train" width="750" title="新增训练版本" :mask-closable="false">
      <div class="modal_body modal_body_train">
        <Form ref="trainInfo" label-position="left" :model="trainInfo" :label-width="110" :rules="rules">
          <FormItem label="版本名称" prop="dmtvName">
            <Input style="width: 200px;" v-model="trainInfo.dmtvName" placeholder="请输入版本名称"></Input>
          </FormItem>
          <FormItem label="模型推断平台">
            <RadioGroup v-model="trainInfo.inferencePlatform">
              <Radio :label="1">服务器</Radio>
              <Radio :label="2">移动端</Radio>
            </RadioGroup>
          </FormItem>
          <FormItem label="算法精度">
            <RadioGroup v-model="trainInfo.dmPrecision">
              <Radio :label="1">小</Radio>
              <Radio :label="2">中</Radio>
              <Radio :label="3">大</Radio>
              <Radio :label="4">特大</Radio>
            </RadioGroup>
          </FormItem>
          <FormItem label="添加训练数据">
            <Button icon="ios-add-circle-outline" type="primary" style="margin-bottom:20px" ghost size="small" @click="chooseData">请选择</Button>
            <span v-if="trainData.length" style="margin-left:20px">已选择 <span style="color: #8c0776">{{trainData.length}}</span> 个数据集，<span style="color: #8c0776">{{labelNumber}}</span> 个标签</span>
            <Table :columns="columns1" :data="trainData"></Table>
          </FormItem>
          <FormItem label="数据增强策略" prop="dataEnhanceType">
            <RadioGroup v-model="trainInfo.dataEnhanceType">
              <Radio :label="1">默认配置</Radio>
              <Radio :label="2">手动配置</Radio>
            </RadioGroup>
          </FormItem>

          <Collapse @on-change="changeAdvance">
            <Panel name="1">
              高级设置
              <div slot="content">
                <FormItem label="训练次数" :label-width="150">
                  <InputNumber :min="1" v-model="trainInfo.epochs"></InputNumber>
                </FormItem>
                <FormItem label="批大小" :label-width="150">
                  <InputNumber :min="1" v-model="trainInfo.batch_size"></InputNumber>
                </FormItem>
                <FormItem label="是否使用预训练模型" :label-width="150">
                  <RadioGroup v-model="trainInfo.isUsePreTraindModel">
                    <Radio :label="1">是</Radio>
                    <Radio :label="2">否</Radio>
                  </RadioGroup>
                </FormItem>
              </div>
            </Panel>
          </Collapse>

        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" :disabled="!trainData.length" class="confirm_btn" ghost @click="addTrainMethod('trainInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('trainInfo')">取消</Button>
      </div>
    </Modal>
    <!-- 添加训练数据 -->
    <Modal class="sys_modal" v-model="modal_trainData" width="750" title="添加训练数据" :mask-closable="false">
      <div class="modal_body">
        <Form ref="trainDataInfo" label-position="left" :model="trainDataInfo" :label-width="110">
          <FormItem label="数据集" prop="dsId">
            <Select v-model="trainDataInfo.dsId" style="width:300px;" @on-change="onSelectData">
              <Option :value="item.dsId" v-for="(item,idx) in dataList" :key="idx">{{item.dsName}}</Option>
            </Select>
          </FormItem>
          <FormItem label="可选标签">
            <Checkbox :indeterminate="indeterminate" :value="checkAll" @click.prevent.native="handleCheckAll">全选</Checkbox>
            <CheckboxGroup v-model="trainDataInfo.dlidList" @on-change="checkAllGroupChange">
              <Checkbox :label="item._id" v-for="(item,idx) in labelList" :key="idx">{{item.dlName}}</Checkbox>
            </CheckboxGroup>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="addTrainDataInfo('trainDataInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancelTrainData('trainDataInfo')">取消</Button>
      </div>
    </Modal>
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
        <p class="title" style="margin-top:10px">训练数据集</p>
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
          您确定要删除该模型吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod()">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_add" width="450" title="新增模型" :mask-closable="false">
      <div class="modal_body">
        <Form ref="addInfo" label-position="left" :model="addInfo" :rules="ruleValidate" :label-width="110">
          <FormItem label="模型名称" prop="dmName">
            <Input v-model="addInfo.dmName"></Input>
          </FormItem>
          <FormItem label="功能描述" prop="dmRemark">
            <Input v-model="addInfo.dmRemark" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
          </FormItem>
          <FormItem label="任务类型" prop="cvTaskType">
            <RadioGroup v-model="addInfo.cvTaskType">
              <Radio :label="item.cvTaskType" v-for="item in cvTaskTypeList" :key="item.cvTaskType">{{item.cvTaskName}}</Radio>
            </RadioGroup>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="addInfoMethod('addInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('addInfo')">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_modify" width="450" title="修改模型" :mask-closable="false">
      <div class="modal_body">
        <Form ref="modifyInfo" label-position="left" :model="modifyInfo" :rules="ruleValidate" :label-width="110">
          <FormItem label="模型名称" prop="dmName">
            <Input v-model="modifyInfo.dmName"></Input>
          </FormItem>
          <FormItem label="功能描述" prop="dmRemark">
            <Input v-model="modifyInfo.dmRemark" type="textarea" :autosize="{minRows: 2,maxRows: 5}"></Input>
          </FormItem>
          <FormItem label="任务类型" prop="cvTaskType">
            <span>{{modifyInfo.cvTaskType == 1 ? '图像分类' : modifyInfo.cvTaskType == 2 ? '目标检测' : '其它'}}</span>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="modifyInfoMethod('modifyInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('modifyInfo')">取消</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  mounted () {
    this.queryPageInfo()
    this.getTaskType()
  },
  data () {
    return {
      value1: '1',
      total: 0,// 初始化信息总条数
      pageNow: 1,
      pagesize: 20,// 每页显示多少条
      search: {},
      modal_delete: false,
      modal_add: false,
      modal_modify: false,
      modal_train: false, // 新增模型
      modal_trainData: false, // 新增模型数据
      modal_option: false, // 查看模型版本配置
      cvTaskTypeList: [],
      dataList: [],
      labelList: [],
      addInfo: {
        cvTaskType: 1
      },
      trainInfo: {
        inferencePlatform: 1,
        dmPrecision: 1,
        dataEnhanceType: 1,
        epochs: 3,
        batch_size: 16,
        isUsePreTraindModel: 1
      },
      indeterminate: true,
      trainDataInfo: {
        dlidList: [],
      },
      checkAll: false,
      ruleValidate: {
        dmName: [
          { required: true, message: '请输入模型名称', trigger: 'blur' },
        ],
        dmRemark: [
          { required: true, message: '请输入功能描述', trigger: 'blur' }
        ],
        cvTaskType: [
          { required: true, message: '请选择任务类型', trigger: 'blur', type: 'number' }
        ],
      },
      rules: {
        dmtvName: [
          { required: true, message: '请输入版本名称', trigger: 'blur' }
        ]
      },
      modifyInfo: {},
      optionInfo: {},
      trainData: [],
      columns: [
        {
          "title": "版本名称",
          "align": "center",
          "key": "dmtvName"
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
          "className": 'label_cell',
          "key": "datasetNames",
          'width': 190,
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
          'width': 200,
          'slot': 'action'
        }],
      columns1: [
        {
          "title": "数据集",
          "align": "center",
          "key": "dsName"
        }, {
          "title": "标签",
          "align": "center",
          "className": 'label_cell',
          "width": 210,
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
        },
        {
          "title": "操作",
          "align": "center",
          "key": "dsImageCount",
          render: (h, params) => {
            return h('span', {
              style: {
                color: '#8c0776',
                cursor: 'pointer'
              },
              on: {
                click: () => {
                  this.clearDataItem(params.index)
                }
              }
            }, '清空')
          }
        }
      ],
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
                title: params.row.dlNameList && params.row.dlNameList.join('、')
              },
            }, params.row.dlNameList && params.row.dlNameList.join('、'))
          }
        }
      ],
      columns2: [
        {
          "title": "No.",
          "align": "center",
          render: (h, params) => {
            return h('span', params.index + 1)
          }
        },
        {
          "title": "数据集名称",
          "align": "center",
          "key": "dsName"
        }, {
          "title": "训练效果",
          "align": "center",
          // "className": 'label_cell',
          "slot": 'metrics',
          'width': 210
        },
        // {
        //   "title": "操作",
        //   "align": "center",
        //   "key": "dsImageCount",
        //   render: (h, params) => {
        //     return h('span', {
        //       style: {
        //         color: '#8c0776',
        //         cursor: 'pointer'
        //       },
        //       on: {
        //         click: () => {
        //           this.clearDataItem(params.index)
        //         }
        //       }
        //     }, '清空')
        //   }
        // }
      ],
      pageInfo: {},
    }
  },
  computed: {
    labelNumber () {
      var num = 0
      this.trainData.forEach(item => {
        num += item.dlidList.length
      })
      return num
    }
  },
  methods: {
    // 获取分页信息
    queryPageInfo () {
      let params = {
        pageIndex: this.pageNow,
        pageSize: this.pagesize,
        dmName: this.search.dmName,
        cvTaskType: this.search.cvTaskType
      }
      this.$Spin.show()
      this.$post('/detectModel/getDetectModelsPages', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.pageInfo = data.pageData;
          this.total = data.pageData.totalCount;//总数
          this.chosePage = data.pageData.page;//选择页
          this.pageNow = data.pageData.page;//当前页
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
    handleChange (page) {
      this.pageNow = page;//赋值当前页
      this.queryPageInfo();
    },
    getTaskType () {
      let params = {}
      this.$Spin.show()
      this.$post('/dsc/getAllCVTaskTypes', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.cvTaskTypeList = data.taskTypeList
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    getDatas () {
      let params = {}
      this.$Spin.show()
      this.$post('/dsc/getAllDSNamesList', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.dataList = data.data
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    // 根据数据集id获取标签列表
    onSelectData (e) {
      if(!e) return false
      let params = {
        dsId: e
      }
      this.$Spin.show()
      this.$post('/dataLabel/getAllDataLabelByDsid', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.labelList = data.data
          var findItem = this.trainData.find(item => item.dsId == e)
          if(findItem) {
            this.$set(this.trainDataInfo, 'dlidList', findItem.dlidList)
          }
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    changeAdvance (e) {
      if(e.length) {
        setTimeout(() => {
          $('.modal_body_train').scrollTop($('.modal_body_train')[0].scrollHeight)
        }, 200);
      }
    },
    initTrain () {
      this.trainInfo = {
        inferencePlatform: 1,
        dmPrecision: 1,
        dataEnhanceType: 1
      }
      this.indeterminate = true
      this.trainDataInfo = {
        dlidList: []
      }
      this.checkAll = false
      this.dataList = []
    },
    trainModel (dmId) {
      this.modal_train = true
      this.dmId = dmId
      this.getDatas()
    },
    goHistory (table) {
      this.$router.push({ path: '/modelHistory/' + table.dmId, query: { dmName: table.dmName } })
    },
    chooseData () {
      this.trainDataInfo = {
        dlidList: []
      }
      this.labelList = []
      this.modal_trainData = true
    },
    handleCheckAll () {
      if(this.indeterminate) {
        this.checkAll = false;
      } else {
        this.checkAll = !this.checkAll;
      }
      this.indeterminate = false;

      if(this.checkAll) {
        this.$set(this.trainDataInfo, 'dlidList', this.labelList.map(item => { return item._id }))
      } else {
        this.trainDataInfo.dlidList = []
      }
    },
    checkAllGroupChange (data) {
      if(data.length === this.labelList.length) {
        this.indeterminate = false;
        this.checkAll = true;
      } else if(data.length > 0) {
        this.indeterminate = true;
        this.checkAll = false;
      } else {
        this.indeterminate = false;
        this.checkAll = false;
      }
    },
    addTrainDataInfo () {
      // console.log(this.trainDataInfo, this.trainData)
      if(!(this.trainDataInfo.dlidList && this.trainDataInfo.dlidList.length)) {
        this.$Message.error('请选择标签')
        return false
      }
      var index = this.trainData.findIndex(item => item.dsId == this.trainDataInfo.dsId)
      if(index >= 0) {
        this.trainData.splice(index, 1)
        this.trainData.push({
          ...this.trainDataInfo,
          isSelectAll: this.checkAll,
          dsName: this.dataList.find(item => item.dsId == this.trainDataInfo.dsId).dsName,
          dlNameList: this.trainDataInfo.dlidList.map(item => {
            return this.labelList.find(i => i._id == item).dlName
          })
        })
      } else {
        this.trainData.push({
          ...this.trainDataInfo,
          isSelectAll: this.checkAll,
          dsName: this.dataList.find(item => item.dsId == this.trainDataInfo.dsId).dsName,
          dlNameList: this.trainDataInfo.dlidList.map(item => {
            return this.labelList.find(i => i._id == item).dlName
          })
        })
      }

      // console.log(this.trainData)
      this.modal_trainData = false
    },
    clearDataItem (idx) {
      this.trainData.splice(idx, 1)
    },
    addTrainMethod (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          // console.log(this.trainInfo, this.trainData)
          let params = {
            dmid: this.dmId,
            "dmtvName": this.trainInfo.dmtvName,
            "dmPrecision": this.trainInfo.dmPrecision,
            "inferencePlatform": this.trainInfo.inferencePlatform,
            "dataEnhanceType": this.trainInfo.dataEnhanceType,
            ds_dl_list: [...this.trainData],
            advancedSet: {
              "epochs": this.trainInfo.epochs,
              "batch_size": this.trainInfo.batch_size,
              "isUsePreTraindModel": this.trainInfo.isUsePreTraindModel == 1 ? 'true' : 'false'
            }
          }
          this.$Spin.show()
          this.$post('/detectModelTrain/DMVersionTrain', params).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.$Message.success('新增成功！')
              this.modal_train = false
              this.queryPageInfo()
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
            dmType: 1,
            cvTaskType: this.addInfo.cvTaskType
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
    // 编辑弹框
    modifyModal (dmId) {
      this.dmId = dmId
      this.modal_modify = true
      this.$post('/detectModel/getDetectModelDetail', {
        dmId: dmId
      }).then(data => {
        if(data.rs === 1) {
          this.modifyInfo = data.data
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    // 确认编辑
    modifyInfoMethod (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          this.$Spin.show()
          var params = {
            dmId: this.dmId,
            updateClolumn: {
              dmName: this.modifyInfo.dmName,
              dmType: 1,
              dmRemark: this.modifyInfo.dmRemark
            }
          }
          this.$post('/detectModel/updateDetectModel', params).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.modal_modify = false
              this.$Message.success('修改成功!');
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
          this.$Message.error('修改失败!');
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
      this.dmId = id
      this.modal_delete = true
    },
    deleteMethod () {
      this.$Spin.show()
      this.$post('/detectModel/delDetectModel', { dmId: this.dmId }).then(data => {
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
    // 重置
    clearSearch () {
      this.search = {
        dmName: ''
      }
    }
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
    .type_name {
      padding: 4px 8px;
      border-radius: 11px;
      text-align: center;
      margin-left: 25px;
      border: 1px solid #8c0776;
      font-size: 12px;
      color: #8c0776;
    }
    .model_action {
      float: right;
      text-align: right;
    }
  }
}

.modal_body_option .title:before {
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