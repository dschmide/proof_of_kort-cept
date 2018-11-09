// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import { sync } from 'vuex-router-sync'
import 'vuetify/dist/vuetify.min.css'
import store from '@/store/store'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.config.productionTip = false

Vue.use(Vuetify , {
  iconfont: 'mdi' // 'md' || 'mdi' || 'fa' || 'fa4'
})

//vue resource
import VueResource from 'vue-resource';
Vue.use(VueResource);


sync(store, router)

require('./assets/css/leaflet.js')
require('./assets/css/leaflet.css')
require('./assets/css/Leaflet.Editable.js')


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
