// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 使用路由懒加载
const Home = () => import('../views/Home.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const PersonalCenter = () => import('../views/PersonalCenter.vue')
const DataInput = () => import('../views/DataInput.vue')
const ResultDisplay = () => import('../views/ResultDisplay.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { 
      title: '医疗数据资产价值计量器 - 首页',
      requiresGuest: true 
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { 
      title: '登录',
      requiresGuest: true 
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { 
      title: '注册',
      requiresGuest: true 
    }
  },
  {
    path: '/personal-center',
    component: PersonalCenter,
    meta: { title: '个人中心', requiresAuth: true },
    children: [
      { path: '', name: 'PersonalCenterDashboard', component: () => import('../views/PersonalCenterDashboard.vue') },
      { path: 'evaluations', name: 'PersonalCenterEvaluations', component: () => import('../views/PersonalCenterEvaluations.vue') },
      { path: 'drafts', name: 'PersonalCenterDrafts', component: () => import('../views/PersonalCenterDrafts.vue') },
      { path: 'profile', name: 'PersonalCenterProfile', component: () => import('../views/PersonalCenterProfile.vue') }
    ]
  },
  {
    path: '/data-input',
    name: 'DataInput',
    component: DataInput,
    meta: { 
      title: '数据录入',
      requiresAuth: true 
    }
  },
  {
    path: '/result/:id',
    name: 'ResultDisplay',
    component: ResultDisplay,
    meta: { 
      title: '评估结果',
      requiresAuth: true 
    },
    props: true
  },
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    redirect: '/admin/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '管理员概览', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'evaluations',
        name: 'AdminEvaluations',
        component: () => import('@/views/admin/AdminEvaluations.vue'),
        meta: { title: '评估管理', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/AdminUsers.vue'),
        meta: { title: '用户管理', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'weights',
        name: 'WeightSetting',
        component: () => import('@/views/admin/WeightSetting.vue'),
        meta: { title: '权重设置', requiresAuth: true, requiresAdmin: true }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }

  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  // 需要登录但未登录
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  // 已登录但访问登录/注册页
  if (to.meta.requiresGuest && isAuthenticated) {
    next('/personal-center')
    return
  }

  // 需要管理员权限（约定：用户名为 admin 视为管理员）
  if (to.meta.requiresAdmin && (!isAuthenticated || localStorage.getItem('isAdmin') !== 'true')) {
    next('/personal-center')
    return
  }

  next()
})

export default router