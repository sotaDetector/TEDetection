<template>
  <div class="data_manage">
    <div class="container_title">
      <!-- 面包屑 -->
      <Breadcrumb>
        <BreadcrumbItem>数据集管理</BreadcrumbItem>
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
          <Input style="width: 200px;" v-model="search.dsName" placeholder="请输入数据集名称"></Input>
          <Select v-model="search.cvTaskType" style="width:200px;margin-left:20px;" placeholder="请选择任务类型">
            <Option :value="item.cvTaskType" v-for="(item,idx) in cvTaskTypeList" :key="idx">{{item.cvTaskName}}</Option>
          </Select>
          <span class="query_btn">
            <Button type="primary" @click="queryPageInfo">查询</Button>
            <Button @click="clearSearch">重置</Button>
          </span>
        </div>
        <!-- 表格列表 -->
        <div class="container_table">
          <Table :columns="columns" :data="pageInfo.dataList">
            <template slot-scope="{row}" slot="action">
              <div>
                <span v-if="row.dsImageCount" class="action" @click="markDatas(row)">标注</span>
                <span class="action" style="margin:0 4px;" @click="clickImport(row.dsId)">导入</span>
                <span class="action" style="margin-right:4px;" @click="modifyModal(row.dsId)">编辑</span>
                <span class="action" @click="deleteModal(row.dsId)">删除</span>
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
    <Modal class="sys_modal" v-model="modal_list" class-name="vertical_modal" width="400" :mask-closable="false">
      <div class="modal_body modal_body_delete">
        <Upload style="display:inline-block;margin:0 4px;" multiple ref="upload" :before-upload="handleBeforeUpload" :action="$baseUrl + '/dsc/upImageData'">
          <Button type="primary" ghost>选择文件</Button>
        </Upload>
        <ul>
          <li v-for="(item,idx) in files" :key="idx">
            <span>{{item.name}}</span>
            <Icon type="md-remove-circle" @click="delFile(idx)" style="margin-left:10px;" />
          </li>
        </ul>
      </div>
      <div slot="footer">
        <Button type="success" @click="importDatas" icon="ios-cloud-upload-outline" style="width:115px;">点击上传</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_view" class-name="vertical_modal" width="316">
      <div class="modal_body modal_body_view">
        <ul>
          <li v-for="(item,idx) in labelList" :key="idx">
            {{item}}
          </li>
        </ul>
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
          您确定要删除该数据集吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod()">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_add" width="450" title="新增数据集">
      <div class="modal_body">
        <Form ref="addInfo" label-position="left" :model="addInfo" :rules="ruleValidate" :label-width="110">
          <FormItem label="数据集名称" prop="dsName">
            <Input v-model="addInfo.dsName"></Input>
          </FormItem>
          <FormItem label="数据类型" prop="dsType">
            <Select v-model="addInfo.dsType">
              <Option :value=1>图片</Option>
              <!-- <Option :value=1>开启</Option> -->
            </Select>
          </FormItem>
          <FormItem label="任务类型" prop="cvTaskType">
            <RadioGroup v-model="addInfo.cvTaskType">
              <Radio :label="item.cvTaskType" v-for="item in cvTaskTypeList" :key="item.cvTaskType">{{item.cvTaskName}}</Radio>
              <!-- <Radio :label="2">物体检测</Radio> -->
            </RadioGroup>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="addInfoMethod('addInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('addInfo')">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_modify" width="450" title="修改数据集">
      <div class="modal_body">
        <Form ref="modifyInfo" label-position="left" :model="modifyInfo" :rules="ruleValidate" :label-width="110">
          <FormItem label="数据集名称" prop="dsName">
            <Input v-model="modifyInfo.dsName"></Input>
          </FormItem>
          <FormItem label="数据类型" prop="dsType">
            <span v-if="modifyInfo.dsType == 1">图片</span>
            <span v-else>其它</span>
            <!-- <Select v-model="modifyInfo.dsType">
              <Option :value=1>图片</Option>
            </Select> -->
          </FormItem>
          <FormItem label="任务类型" prop="cvTaskType">
            <span>{{modifyInfo.cvTaskType == 1 ? '图像分类' : modifyInfo.cvTaskType == 2 ? '目标检测' : '其它'}}</span>
            <!-- <RadioGroup v-model="modifyInfo.cvTaskType">
              <Radio :label="item.cvTaskType" v-for="item in cvTaskTypeList" :key="item.cvTaskType">{{item.cvTaskName}}</Radio>
            </RadioGroup> -->
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
    if(!this.cvTaskTypeList.length) {
      this.getTaskType()
    }
  },
  data () {
    return {
      total: 0,// 初始化信息总条数
      pageNow: 1,
      pagesize: 20,// 每页显示多少条
      search: {},
      modal_list: false,
      modal_delete: false,
      modal_view: false,
      modal_add: false,
      modal_modify: false,
      cvTaskTypeList: [],
      labelList: [],
      addInfo: {
        dsName: '',
        dsType: 1,
        cvTaskType: 1
      },
      ruleValidate: {
        dsName: [
          { required: true, message: '请输入数据集名称', trigger: 'blur' },
        ],
        dsType: [
          { required: true, message: '请选择数据类型', trigger: 'blur', type: 'number' }
        ],
        cvTaskType: [
          { required: true, message: '请选择任务类型', trigger: 'blur', type: 'number' }
        ],
      },
      modifyInfo: {
        dsName: '',
        dsType: ''
      },
      columns: [
        {
          "title": "数据集名称",
          "align": "center",
          "key": "dsName"
        }, {
          "title": "数据类型",
          "align": "center",
          "key": "dsType",
          render: (h, params) => {
            return h('span', params.row.dsType == 1 ? '图片' : '其它')
          }
        }, {
          "title": "任务类型",
          "align": "center",
          "key": "cvTaskName",
        }, {
          "title": "数据数量",
          "align": "center",
          "key": "dsImageCount",
        }, {
          "title": "标注进度",
          "align": "center",
          "key": "dsImgTagSP"
        }, {
          "title": "标签数量",
          "align": "center",
          "key": "labelCount",
        }, {
          "title": "标签",
          "align": "center",
          "key": "labelList",
          render: (h, params) => {
            return h('div', {
              style: {
                color: '#8c0776',
                cursor: 'pointer',
                display: params.row.labelList.length ? 'block' : 'none'
              },
              on: {
                click: () => {
                  this.viewLabel(params.row.labelList)
                }
              }
            }, '查看')
          }
        }, {
          'title': '操作',
          'align': 'center',
          'key': 'action',
          'slot': 'action'
        }],
      pageInfo: {},
      files: []
    }
  },
  methods: {
    // 获取分页信息
    queryPageInfo () {
      let params = {
        pageIndex: this.pageNow,
        pageSize: this.pagesize,
        dsName: this.search.dsName,
        cvTaskType: this.search.cvTaskType
      }
      this.$Spin.show()
      this.$post('/dsc/getDataSetPages', params).then(data => {
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
    handleBeforeUpload (e) {
      if(e.type == 'application/x-zip-compressed') {
        this.fileType = 1
        this.files.push(e)
      } else if(e.type.indexOf('image/') >= 0) {
        this.fileType = 2
        this.files.push(e)
      } else {
        this.$Message.error('请上传图片或zip压缩包！')
      }
      // this.importDatas()
      return false
    },
    delFile (idx) {
      this.files.splice(idx, 1)
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
          this.$post('/dsc/addDataSet', this.addInfo).then(data => {
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
    modifyModal (dsId) {
      this.dsId = dsId
      this.modal_modify = true
      this.$post('/dsc/getDataSetDetail', {
        dsId: dsId
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
            dsId: this.dsId,
            updateClolumn: {
              dsName: this.modifyInfo.dsName
            }
          }
          this.$post('/dsc/updateDataSet', params).then(data => {
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
    viewLabel (list) {
      this.labelList = list
      this.modal_view = true
    },
    markDatas (row, idx) {
      if(row.cvTaskType == 1) {
        this.$router.push({ path: '/classifyImg/' + row.dsId })
      } else {
        this.$router.push({ path: '/markImg/' + row.dsId })
      }
    },
    clickImport (id) {
      this.dsId = id
      this.files = []
      this.modal_list = true
    },
    importDatas () {
      if(!this.files.length) {
        this.$Message.error('请选择文件')
        return false
      }

      var fd = new FormData()
      if(this.fileType == 1) { // 压缩包
        if(this.files.length > 1) {
          this.$Message.error('请上传图片或zip压缩包！')
          return false
        }
        fd.append('compreImgPack', this.files[0])
      } else {
        this.files.forEach(item => {
          if(item.type.indexOf('image') < 0) {
            this.$Message.error('请上传图片或zip压缩包！')
            return false
          }
          fd.append('imageslist', item)
        })
      }
      fd.append('dsId', this.dsId)
      fd.append('fileType', this.fileType)

      this.$Spin.show()
      this.$post_('/dsc/upImageData', fd).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.$Message.success('导入成功');
          this.files = []
          this.fileType = ''
          this.modal_list = false
          this.queryPageInfo()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    deleteModal (id) {
      this.dsId = id
      this.modal_delete = true
    },
    deleteMethod () {
      this.$Spin.show()
      this.$post('/dsc/delDataSet', { dsId: this.dsId }).then(data => {
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
    cancel (name) {
      this.modal_add = false
      this.modal_modify = false
      this.modal_delete = false
      this.modal_view = false
      this.modal_list = false
      if(name) {
        this.$refs[name].resetFields();
      }
    },
    // 重置
    clearSearch () {
      this.search = {
        dsName: ''
      }
    }
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