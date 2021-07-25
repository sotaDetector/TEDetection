import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import '@/assets/css/reset.css'

import ViewUI from 'view-design';
// import 'view-design/dist/styles/iview.css'
import '@/assets/css/iview-theme.less'

// 引入iconfont
import '@/assets/font_icon/iconfont.css'

// 引入自定义主题

// md5加密
import md5 from 'js-md5'

// 引入时间插件
import moment from 'moment'
//定义时间格式全局过滤器
Vue.filter("dateFormat", function (daraStr, pattern = "YYYY-MM-DD HH:mm:ss") {
  return moment(daraStr).format(pattern)
})
// 百分比处理
Vue.filter("percent", function (number) {
  return ((number * 100).toFixed(2) + '%')
})

// 全局基本路径
import {
  baseUrl
} from './network/urlUtil'

//封装的get、postaxios，上传文件formdata格式方法
import {
  postJsonRequest,
  postRequest,
  getRequest,
  postRequest2
} from './network/http'

// import $ from 'jquery'

Vue.use(ViewUI);

// import './assets/css/reset.css'

Vue.config.productionTip = false


//定义全局变量
// Vue.prototype.$post = postRequest
Vue.prototype.$post = postJsonRequest
Vue.prototype.$post_ = postRequest2
Vue.prototype.$get = getRequest
Vue.prototype.$md5 = md5
Vue.prototype.$baseUrl = baseUrl


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')