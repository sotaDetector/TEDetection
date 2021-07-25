<template>
  <div class="header">
    <div class="header_right">
      <div class="avatar">
        <!-- <img src="~/assets/images/default_headImage.png" alt=""> -->
        <span>{{$store.state.userName}}</span>
      </div>
      <div class="quit" @click="quit">
        <!-- <img src="~/assets/images/out.png" alt=""> -->
        <Icon type="ios-power" />
        <span>退出</span>
      </div>
      <Modal class="sys_modal" class-name="vertical_modal" v-model="quitModal" width="316">
        <div class="modal_body modal_body_delete">
          <p><img src="@/assets/img/warn_tip.png" alt="">您确定要退出系统吗?</p>
        </div>
        <div slot="footer">
          <Button type="primary" class="confirm_btn" ghost @click="ok()">确定</Button>
          <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
        </div>
      </Modal>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// 引进方法
import { quitMethod } from '@/network/login'
export default {
  name: 'Header',
  data () {
    return {
      quitModal: false
    }
  },
  methods: {
    quit () {
      // 打开模态框
      this.quitModal = true
    },
    ok () {
      //退出方法
      quitMethod(this.$store.state.userName, this.$store.state.token).then(() => {
        // 清除localStorage token值
        // localStorage.removeItem('token');// token值
        // localStorage.removeItem('menuList');// 菜单
        // localStorage.removeItem('requestPaths');// 权限
        // localStorage.removeItem('userName');// userName
        // localStorage.removeItem('headImg');// headImg

        this.$router.push('/login')
      })
    },
    cancel () {
      this.quitModal = false
    }
  }
}
</script>
<style scoped>
.header {
  width: 100%;
  height: 40px;
  position: relative;
  top: 0;
  left: 0;
  border-bottom: 1px solid #e3e3e3;
}
.header_right {
  position: absolute;
  top: 0;
  right: 15px;
  height: 40px;
  display: flex;
  /* 垂直居中，两端对齐 */
  /* align-items: center;
  justify-content: space-between; */
}
.avatar {
  margin-right: 20px;
}
.avatar,
.quit {
  display: flex;
  align-items: center;
  /* border-left: 1px solid #e3e3e3; */
  padding-left: 10px;
  cursor: pointer;
}
.avatar span,
.quit span {
  margin-left: 10px;
}
.avatar img {
  width: 30px;
  height: 30px;
  vertical-align: middle;
  align-items: center;
}
.quit img {
  width: 13px;
  height: 13px;
  vertical-align: middle;
  align-items: center;
}
</style>
