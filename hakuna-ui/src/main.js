import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

Vue.config.productionTip = false
Vue.use(ElementUI)


// import moment from 'moment'
// Vue.filter('moment', function(value, formatString){
//   formatString = formatString || 'YYYY-MM-DD HH:mm:ss';
//   return moment(value).format("YYYY-MM-DD");
// })
Vue.prototype.$axios = axios
// 请求超时时间
axios.defaults.timeout = 8000;
// 请求的地址
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1'
// 请求携带cookie
axios.defaults.withCredentials = true
// 异步请求 不阻塞 headers请求头
axios.defaults.headers.post['X-Requested-With'] = 'XMLHttprequest'
// 内容类型
axios.defaults.headers.post['Content-Type'] = 'application/json'
// 获取本地token 没有则为空字符串
axios.defaults.headers['token'] = localStorage.getItem("token") || ""

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
