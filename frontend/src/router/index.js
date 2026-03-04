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
    name: 'PersonalCenter',
    component: PersonalCenter,
    meta: { 
      title: '个人中心',
      requiresAuth: true 
    }
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

  next()
})

export default router