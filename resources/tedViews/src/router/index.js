import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login.vue')
  }, {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/register.vue')
  }, {
    path: '/main',
    name: 'Main',
    component: () => import('@/components/common/Main.vue'),
    children: [{
        path: '/dataManage',
        name: 'DataManage',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import( /* webpackChunkName: "about" */ '../views/data/dataManage.vue')
      },
      // {
      //   path: '/markData',
      //   name: 'MarkData',
      //   component: () => import('@/views/data/markData.vue')
      // },
      {
        path: '/markImg/:id/',
        name: 'MarkImg',
        component: () => import('@/views/data/markImg.vue')
      },
      {
        path: '/markImg/:id/:ditId', // 数据集id，数据集图片id
        name: 'MarkImgDetail',
        component: () => import('@/views/data/markImg.vue')
      },
      {
        path: '/classifyImg/:id/', // 数据集id
        name: 'ClassifyImg',
        component: () => import('@/views/data/classifyImg.vue')
      },
      {
        path: '/classifyImg/:id/:ditId', // 数据集id，数据集图片id
        name: 'ClassifyImgDetail',
        component: () => import('@/views/data/classifyImg.vue')
      },
      {
        path: '/modelManage',
        name: 'ModelManage',
        component: () => import('@/views/model/modelManage.vue')
      },
      {
        path: '/modelHistory/:id',
        name: 'ModelHistory',
        component: () => import('@/views/model/modelHistory.vue')
      },
      {
        path: '/trainStatistics/:id',
        name: 'TrainStatistics',
        component: () => import('@/views/model/trainStatistics.vue')
      },
      {
        path: '/modelValidate/:id',
        name: 'ModelValidate',
        component: () => import('@/views/model/modelValidate.vue')
      },
      {
        path: '/detectService/',
        name: 'DetectService',
        component: () => import('@/views/application/detectService.vue')
      },
      {
        path: '/detectTask/',
        name: 'DetectTask',
        component: () => import('@/views/application/detectTask.vue')
      },
    ]
  },
]

const router = new VueRouter({
  routes
})

export default router