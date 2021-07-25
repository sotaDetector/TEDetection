<template>
  <div class="data_manage">
    <div class="container_title">
      <!-- 面包屑 -->
      <Breadcrumb>
        <BreadcrumbItem>检测服务</BreadcrumbItem>
      </Breadcrumb>
      <!-- 操作按钮 -->
      <div class="ops_btn">
        <Button type="primary" ghost size='small' @click="addModal">新增</Button>
      </div>
    </div>
    <div class="container_info">
      <div class="container_box">
        <!-- 查询条件 -->
        <!-- <div class="query_option">
          <Input style="width: 200px;" v-model="search.dtsName" placeholder="请输入服务名称"></Input>
          <span class="query_btn">
            <Button type="primary" @click="queryPageInfo">查询</Button>
            <Button @click="clearSearch">重置</Button>
          </span>
        </div> -->
        <!-- 表格列表 -->
        <div class="container_table">
          <Table :columns="columns" :data="pageInfo.dataList">
            <template slot-scope="{row, index}" slot="switch">
              <i-switch size="large" :value="row.dtsSwitch==1?true:false" @on-change="changeState(row._id, row.dtsSwitch)">
                <span slot="open">开启</span>
                <span slot="close">关闭</span>
              </i-switch>
            </template>
            <template slot-scope="{row, index}" slot="action">
              <div>
                <span class="action" style="margin-right:5px" @click="modifyModal(row._id)">编辑</span>
                <span class="action" @click="deleteModal(row._id)">删除</span>
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
    <Modal class="sys_modal" v-model="modal_view" class-name="vertical_modal" width="350">
      <div class="modal_body modal_body_view">
        {{secret}}
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="cancel()">确定</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_delete" class-name="vertical_modal" width="316">
      <div class="modal_body modal_body_delete">
        <p>
          <img src="@/assets/img/warn_tip.png" alt="">
          您确定要删除该服务吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod()">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_add" width="450" title="新增服务">
      <div class="modal_body">
        <Form ref="addInfo" label-position="left" :model="addInfo" :rules="ruleValidate" :label-width="120">
          <FormItem label="服务名称" prop="dtsName">
            <Input v-model="addInfo.dtsName"></Input>
          </FormItem>
          <FormItem label="模型" prop="dmId">
            <Select v-model="addInfo.dmId" @on-change="changeModel">
              <Option v-for="item in modelList" :key="item.dmId" :value="item.dmId">{{item.dmName}}</Option>
            </Select>
          </FormItem>
          <FormItem label="模型版本" prop="dmtvId">
            <Select v-model="addInfo.dmtvId">
              <Option v-for="item in versionList" :key="item.dmtvid" :value="item.dmtvid">{{item.dmtvName}}</Option>
            </Select>
          </FormItem>
          <FormItem label="是否开启服务" prop="dmtvId">
            <i-switch size="large" v-model="addInfo.switch">
              <span slot="open">开启</span>
              <span slot="close">关闭</span>
            </i-switch>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="addInfoMethod('addInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('addInfo')">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_modify" width="450" title="修改服务">
      <div class="modal_body">
        <Form ref="modifyInfo" label-position="left" :model="modifyInfo" :rules="ruleValidate" :label-width="120">
          <FormItem label="服务名称" prop="dtsName">
            <Input v-model="modifyInfo.dtsName"></Input>
          </FormItem>
          <FormItem label="模型" prop="dmId">
            <Select v-model="modifyInfo.dmId" @on-change="changeModel">
              <Option v-for="item in modelList" :key="item.dmId" :value="item.dmId">{{item.dmName}}</Option>
            </Select>
          </FormItem>
          <FormItem label="模型版本" prop="dmtvId">
            <Select v-model="modifyInfo.dmtvId">
              <Option v-for="item in versionList" :key="item.dmtvid" :value="item.dmtvid">{{item.dmtvName}}</Option>
            </Select>
          </FormItem>
          <FormItem label="是否开启服务" prop="dmtvId">
            <i-switch size="large" v-model="modifyInfo.switch">
              <span slot="open">开启</span>
              <span slot="close">关闭</span>
            </i-switch>
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
    this.getAllDetectModels()
  },
  data () {
    return {
      total: 0,// 初始化信息总条数
      pageNow: 1,
      pagesize: 20,// 每页显示多少条
      // search: {},
      secret: '',
      modal_delete: false,
      modal_view: false,
      modal_add: false,
      modal_modify: false,
      modelList: [],
      versionList: [],
      addInfo: {
        switch: true, // 服务默认开启
      },
      modifyInfo: {},
      ruleValidate: {
        dtsName: [
          { required: true, message: '请输入服务名称', trigger: 'blur' },
        ],
        dmId: [
          { required: true, message: '请选择模型', trigger: 'blur', type: 'number' }
        ],
        dmtvId: [
          { required: true, message: '请选择模型版本', trigger: 'blur', type: 'number' }
        ]
      },
      columns: [
        {
          "title": "服务名称",
          "align": "center",
          "key": "dtsName"
        }, {
          "title": "服务id",
          "align": "center",
          "key": "dtsServiceKey",
          "width": 280
        }, {
          "title": "模型",
          "align": "center",
          "key": "model",
          render: (h, params) => {
            return h('span', params.row.model[0] && params.row.model[0].dmName)
          }
        }, {
          "title": "模型版本",
          "align": "center",
          "key": "modelVersion",
          render: (h, params) => {
            return h('span', params.row.modelVersion[0] && params.row.modelVersion[0].dmtvName)
          }
        }, {
          "title": "服务状态",
          "align": "center",
          "key": "dsImgTagSP",
          "slot": 'switch'
        }, {
          "title": "秘钥",
          "align": "center",
          render: (h, params) => {
            return h('div', {
              style: {
                color: '#8c0776',
                cursor: 'pointer'
              },
              on: {
                click: () => {
                  this.viewSecret(params.row.dtsSecret)
                }
              }
            }, '查看')
          }
        }, {
          "title": "创建时间",
          "align": "center",
          "key": "create_date",
          "width": 160
        }, {
          'title': '操作',
          'align': 'center',
          'key': 'action',
          'slot': 'action'
        }],
      pageInfo: {},
    }
  },
  methods: {
    getAllDetectModels () {
      this.$Spin.show()
      this.$post('/detectModel/getAllDetectModels', {}).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.modelList = data.data
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    changeModel (e) {
      if(!e) return false
      this.$Spin.show()
      this.$post('/detectModelTrain/getDMVersionNameList', { dmid: e }).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.versionList = data.data
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    // 获取分页信息
    queryPageInfo () {
      let params = {
        pageIndex: this.pageNow,
        pageSize: this.pagesize,
      }
      this.$Spin.show()
      this.$post('/dts/getDetectServicePageList', params).then(data => {
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
    // 新增弹框
    addModal () {
      this.modal_add = true
    },
    // 确认新增
    addInfoMethod (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          this.$Spin.show()
          this.$post('/dts/addDetectService', {
            dtsName: this.addInfo.dtsName,
            dmId: this.addInfo.dmId,
            dmtvId: this.addInfo.dmtvId,
            dtsSwitch: this.addInfo.switch ? 1 : 2
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
    modifyModal (dtsid) {
      this.dtsid = dtsid
      this.modal_modify = true
      this.$post('/dts/getDetectServiceDetail', {
        dtsid: dtsid
      }).then(data => {
        if(data.rs === 1) {
          this.modifyInfo = data.data
          this.modifyInfo.switch = data.data.dtsSwitch == 1 ? true : false
          this.changeModel(data.data.dmId)
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
            "dtsid": this.dtsid,
            "updateClolumn": {
              dtsName: this.modifyInfo.dtsName,
              dmId: this.modifyInfo.dmId,
              dmtvId: this.modifyInfo.dmtvId,
              dtsSwitch: this.modifyInfo.switch ? 1 : 2
            }
          }
          this.$post('/dts/updateDetectService', params).then(data => {
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
    viewSecret (secret) {
      this.secret = secret
      this.modal_view = true
    },
    deleteModal (id) {
      this.dtsid = id
      this.modal_delete = true
    },
    deleteMethod () {
      this.$Spin.show()
      this.$post('/dts/delDetectService', { dtsid: this.dtsid }).then(data => {
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
    changeState (id, dtsSwitch) {
      var params = {
        dtsid: id,
        dtsSwitch: dtsSwitch == 1 ? 2 : 1
      }
      this.$Spin.show()
      this.$post('/dts/changeDtsSwitch', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
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
    cancel (name) {
      this.modal_add = false
      this.modal_modify = false
      this.modal_delete = false
      this.modal_view = false
      if(name) {
        this.$refs[name].resetFields();
      }
    },

    // 重置
    // clearSearch () {
    //   this.search = {
    //     dtsName: ''
    //   }
    // }
  }
}
</script>


<style lang="scss">
.data_manage {
  .action {
    color: #8c0776;
    cursor: pointer;
  }
  .container_info .ivu-table-overflowX {
    overflow: initial;
  }
}
.modal_body.modal_body_view {
  max-height: 362px;
  overflow-y: auto;
}
</style>