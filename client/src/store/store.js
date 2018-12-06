import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  strict: true,
  state: {
    token: null,
    user: null,
    isUserLoggedIn: false,
    toggleVegetation: true,
    toggleUserAreas: true,
    mapPos: null,
    mapZoom: null,
  },

  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem("jwt", token)
      if (token) {
        state.isUserLoggedIn = true
      } else {
        state.isUserLoggedIn = false
      }
    },

    setUser(state, user) {
      state.user = user
    },
    
    saveMapPos(state, MapCenter) {
      state.mapPos = MapCenter
    },

    saveMapZoom(state, MapZoom) {
      state.mapZoom = MapZoom
    },

  },
  actions: {
    setToken({ commit }, token) {
      commit('setToken', token)
    },
    setUser({ commit }, user) {
      commit('setUser', user)
    },
    saveMapPos({ commit }, MapCenter) {
      commit('saveMapPos', MapCenter)
    },
    saveMapZoom({ commit }, MapZoom) {
      commit('saveMapZoom', MapZoom)
    },
  }
})
