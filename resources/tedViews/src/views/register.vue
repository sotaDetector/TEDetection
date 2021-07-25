<template>
  <div class="login">
    <div class="inner">
      <!-- <img src="../assets/images/avatar.jpg" alt="" class="avatar"> -->
      <div class="logo_box">
        <img class="logo" src="@/assets/img/logo1.png" alt="">
      </div>
      <div class="title"><Icon size="26" type="ios-planet" /><span class="en"> TED</span> 千眼通用目标检测平台</div>
      <Form class="formItem ivu-form-label-left" ref="userInfo" :model="userInfo" :rules="rules" style="width:90%;margin:0 auto">
        <FormItem prop="nick">
          <Input type="text" v-model="userInfo.nick" placeholder="昵称">
          </Input>
        </FormItem>
        <FormItem prop="user">
          <Input type="text" v-model="userInfo.user" placeholder="用户名">
          </Input>
        </FormItem>
        <FormItem prop="password" style="margin-bottom:10px;">
          <Input type="password" v-model="userInfo.password" placeholder="密码">
          </Input>
        </FormItem>
        <div class="ivu-form-item">
          <div class="go_login" @click="goLogin">
            已有账号，直接登录
          </div>
        </div>
        <FormItem>
          <Button style="height:40px;width:80%;margin:0 auto;display:block;" long type="primary" @click="handleSubmit('userInfo')">注 册</Button>
        </FormItem>
      </Form>
    </div>
  </div>
</template>

<script>
import { registerMethod } from '@/network/login'
let Base64 = require('js-base64').Base64
export default {
  name: 'Register',
  data () {
    return {
      userInfo: {
        nick: '',
        user: '',
        password: ''
      },
      rules: {
        nick: [{ required: true, message: '请输入昵称' }],
        user: [{ required: true, message: '请输入用户名' }],
        password: [
          { required: true, message: '请输入密码' },
          { min: 6, message: '最少 6 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    goLogin () {
      this.$router.push('/login')
    },
    //登录方法
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          // 引用login.js中的方法，.then回调
          this.$Spin.show()
          registerMethod(this.userInfo.nick, this.userInfo.user, this.$md5(this.userInfo.password)).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.$Message.success('注册成功!');
              this.$router.push('/login')
            } else {
              if(data.data && data.data.errorMsg) {
                this.$Message.error(data.data.errorMsg);
              } else {
                this.$Message.error(data.errorMsg);
              }
            }
          })
        } else {
          this.$Message.error('登录失败!');
        }
      })
    },
  }
}
</script>

<style lang="scss" scoped>
.login {
  width: 100%;
  height: 100vh;
  background: url("../assets/img/login.jpg") no-repeat center;
  background-size: 100% 100%;
  overflow: hidden;
}
.inner {
  width: 390px;
  height: 380px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -195px;
  margin-top: -250px;
  padding: 0 20px 20px;
}
.inner .title {
  text-align: center;
  line-height: 125px;
  height: 110px;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 2px;
  background-image: linear-gradient(135deg, red, blue);
  -webkit-background-clip: text;
  color: transparent;
  .en {
    font:italic 1em Georgia, serif;
  }
}
@keyframes logo {
  from {
  }
  to {
    transform: rotate(360deg);
    width: 60px;
    height: 60px;
  }
}
.logo_box {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  position: absolute;
  top: -30px;
  left: 50%;
  margin-left: -30px;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: logo 8s linear infinite;
  .logo {
    width: 75%;
    height: 75%;
    display: inline-block;
  }
}
.go_login {
  float: right;
  width: auto;
  margin-top: 10px;
  font-size: 12px;
  text-decoration: underline;
  cursor: pointer;
}
</style>
