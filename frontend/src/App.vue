<template>
  <sui-segment :loading="loading_flag" id="app" class="content-box ui raised segment">
    <portal-target name="semantic-ui-vue"/>
    <sui-grid >
      <sui-grid-row class="nav-bar">
        <sui-grid-column :width="16">
          <MenuBar></MenuBar>
        </sui-grid-column>
      </sui-grid-row>
      <sui-grid-row>
        <sui-grid-column :width="16">
          <router-view/>
        </sui-grid-column>
      </sui-grid-row>
    </sui-grid>
    <InactivityModal
      :open="timeOut"
    />

  </sui-segment>
</template>

<script>
  import MenuBar from './components/MenuBar.vue'
  import InactivityModal from './components/widgets/InactivityModal.vue'

  export default {
      computed: {
        loading_flag: function(){
          return this.$store.state.status === "loading"
        },
        timeOut() {
          return this.isAppIdle && this.$store.getters.isLoggedIn
        }
      },
      components:{
        MenuBar,
        InactivityModal
      },
      created: function () {
        this.$http.interceptors.response.use(undefined, function (err) {
          return new Promise(function () {
            if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
              this.$store.dispatch('logout')
            }
            throw err;
          });
        });
      }
  }
</script>


<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.content-box {
  min-height: 90vh;
}

.nested-content{
  min-height: 60vh;
}


html {
  margin-left: 110px;
  margin-right: 110px;
}

body{
  background: #edebe9 linear-gradient(to top, #dbd7d1, #edebe9 116px) no-repeat !important;
}

h2.ui.header > .icon {
  background: #2185d0;
  color: white;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

div.ui.container {
  margin-left: 20px;
  width:100%;
}
</style>
