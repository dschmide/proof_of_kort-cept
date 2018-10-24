import Vue from 'vue'
import Router from 'vue-router'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Waldmeistermap from '@/components/Waldmeistermap'
import Market from '@/components/Market'
import Stats from '@/components/Stats'

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      name: 'root',
      component: Waldmeistermap
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/map',
      name: 'map',
      component: Waldmeistermap
    },
    {
      path: '/market',
      name: 'market',
      component: Market
    },
    {
      path: '/stats',
      name: 'stats',
      component: Stats
    }
  ]
})
