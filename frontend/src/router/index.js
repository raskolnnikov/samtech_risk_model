import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import UserView from '../components/UserView.vue'
import AdminUsersList from '../components/AdminUsersList.vue'
import RankingList from '../components/RankingList.vue'
import Statistics from '../components/Statistics.vue'
import PatenteDetails from '../components/PatenteDetails.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import store from '../store'
import 'semantic-ui-css/semantic.min.css';

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'user/:user_public_id',
        name: 'UserView',
        component: UserView,
        meta: {
          requiresAuth: true
        },
        props: true,
      },
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'list',
        name: 'AdminUsersList',
        component: AdminUsersList,
        meta: {
          requiresAuth: true,
          requiresAdmin: true

        },
        props: true,
      },
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'ranking',
        name: 'RankingList',
        component: RankingList,
        meta: {
          requiresAuth: true,
          requiresAdmin: false

        },
        props: true,
      },
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'statistics',
        name: 'Statistics',
        component: Statistics,
        meta: {
          requiresAuth: true,
          requiresAdmin: false
        },
        props: true,
      },
      {
        // UserProfile will be rendered inside User's <router-view>
        // when /user/:id/profile is matched
        path: 'patente/:patente_id/:step_id_week',
        name: 'PatenteDetails',
        component: PatenteDetails,
        meta: {
          requiresAuth: true,
          requiresAdmin: false

        },
        props: true,
      },
    ],
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    router.push('/login').catch(()=>{})
  } else {
    next()
  }
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAdmin)) {
    if (store.getters.isAdmin) {
      next()
      return
    }
    router.push('/patients').catch(()=>{})
  } else {
    next()
  }
})

export default router
