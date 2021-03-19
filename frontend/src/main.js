import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import SuiVue from 'semantic-ui-vue'
import moment from 'moment'
import PortalVue from 'portal-vue'
import IdleVue from 'idle-vue'
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)


Vue.use(PortalVue);

const eventsHub = new Vue()

Vue.use(IdleVue, {
  eventEmitter: eventsHub,
  store,
  idleTime: 1200000, // 20 mins
  startAtIdle: false
});
Vue.use(SuiVue)
Vue.use(moment)

Vue.prototype.$http = Axios;
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

Vue.config.productionTip = false

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('YYYY-MM-DD')
  }
})



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
