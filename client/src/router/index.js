import Vue from 'vue'
import Router from 'vue-router'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Market from '@/components/Market'
import Stats from '@/components/Stats'
import Missions from '@/components/Missions'
import Welcome from '@/components/Welcome'


Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      name: 'root',
      component: Missions
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
      component: Missions
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
    },
    {
      path: '/missions',
      name: 'missions',
      component: Missions
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: Welcome
    }
  ]
})
