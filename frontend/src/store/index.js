import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const api_url = ' http://127.0.0.1:5000'

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user : JSON.parse(localStorage.getItem('user')) || {},
    open_analysis: JSON.parse(localStorage.getItem('open_analysis')) || {},
    admin_flag: JSON.parse(localStorage.getItem('admin_flag')) || false,
  },
  mutations: {
    auth_request(state){
      state.status = 'loading'
    },
    auth_success(state, payload){
      state.status = 'success'
      state.token = payload.token
      state.user = payload.user
      state.admin_flag = payload.user.admin_flag
    },
    auth_error(state){
      state.status = 'error'
    },
    logout(state){
      state.status = ''
      state.token = ''
      state.open_analysis = {}
    },
    save_request(state){
      state.status = 'loading'
    },
    save_success(state){
      state.status = 'success'
    }
  },
  actions: {
    login({commit}, user){
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({url: api_url+'/auth/login', data: user, method: 'POST' })
        .then(resp => {
          const token = resp.data.Authorization
          const user = resp.data.user
          const payload = {
            "token": token,
            "user": user
          }
          localStorage.setItem('token', token)
          localStorage.setItem('admin_flag', user.admin_flag)
          localStorage.setItem('user', JSON.stringify(user))
          axios.defaults.headers.common['Authorization'] = token
          commit('auth_success', payload)
          resolve(resp)
        })
        .catch(err => {
          commit('auth_error')
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },
    register({commit}, user){
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({url: api_url+'/user/', data: user, method: 'POST' })
        .then(resp => {
          const token = resp.data.Authorization
          const user = resp.data.user
          const payload = {
            "token": token,
            "user": user
          }
          localStorage.setItem('token', token)
          localStorage.setItem('admin_flag', user.admin_flag)
          localStorage.setItem('user', JSON.stringify(user))
          axios.defaults.headers.common['Authorization'] = token
          commit('auth_success', payload)
          resolve(resp)
        })
        .catch(err => {
          commit('auth_error', err)
          localStorage.removeItem('token')
          localStorage.removeItem('admin_flag')
          localStorage.removeItem('user')
          reject(err)
        })
      })
    },
    logout({commit}){
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('admin_flag')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    }
  },
  modules: {
  },
  getters : {
    isLoggedIn: state => !!state.token,
    isAdmin: state => !!state.admin_flag,
    authStatus: state => state.status
  }
})
