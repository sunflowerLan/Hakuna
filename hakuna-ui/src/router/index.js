import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginView from '../views/LoginView.vue'
import NavigationView from '../views/NavigationView.vue'
import ProjectList from '../components/project/ProjectList.vue'
import CaseModule from '../components/case/CaseModule.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/main',
    name: 'NavigationView',
    redirect: "/main/project",
    component: NavigationView,
    children: [
      {
        path: "project",
        component: ProjectList
      },
      {
        path: "case",
        component: CaseModule
      },
      {
        path: "task",
        // component: taskList,
      },
      {
        path: "report"
      }
    ]
  },
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

// 导航守卫，控制一些页面登录才能访问
router.beforeEach((to, from, next) => {
  if (to.path === "/login") {
    // 当路由为login时就直接下一步操作
    next()
  } else {
    // 否则就需要判断
    if (sessionStorage.token) {
      // 如果有用户名就进行下一步操作
      next()
    } else {
      next({ path: "/login" }) // 没有用户名就跳转到login页面
    }
  }
})

export default router
