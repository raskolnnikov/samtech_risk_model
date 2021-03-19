<template>
  <sui-menu pointing secondary>
    <a
      v-if="isLoggedIn"
      is="sui-menu-item"
      content="Inicio"
      :active="isActive('dashboard')"
      @click="select('dashboard')"
    />
    <!-- <a
      v-if="isLoggedIn"
      is="sui-menu-item"
      content="About"
      :active="isActive('about')"
      @click="select('about'); $router.push('/about')"
    /> -->

    <sui-menu-menu position="right">
      <router-link
        v-if="!isLoggedIn"
        to="/register"
        content="Signup"
        is="sui-menu-item"
      >
      </router-link>
      <a
        v-if="isLoggedIn"
        is="sui-menu-item"
        :content="'Logged as: '+$store.state.user.email"
        @click="select('dashboard'); $router.push('/dashboard').catch(() => {})"
      />
      <a
        v-if="isLoggedIn"
        is="sui-menu-item"
        content="Logout"
        @click="logout"
      />
      <a
        v-if="!isLoggedIn"
        is="sui-menu-item"
        content="Login"
        @click="$router.push('login').catch(() => {})"
      />
    </sui-menu-menu>
  </sui-menu>
</template>

<script>
  export default{
      data() {
        return {
          active: 'ranking'
        }
      },
    created(){
      this.active = this.$route.path.split('/')[0]
    },
    computed : {
      isLoggedIn : function(){ return this.$store.getters.isLoggedIn},
      isAdmin : function(){ return this.$store.getters.isAdmin}
    },
    methods: {
      logout: function () {
        this.$store.dispatch('logout').catch(() => {})
        .then(() => {
          this.$router.push('/login').catch(() => {})
        })
      },
      isActive(name) {
        return this.active === name;
      },
      select(name) {
        this.active = name;
        if(this.$store.state.admin_flag){
          if(this.$route.path != '/dashboard/ranking'){
            this.$router.push('/dashboard/ranking').catch(() => {})
          }
        }
        else {
          if(this.$route.path != '/dashboard'){
            this.$router.push('/dashboard').catch(() => {})
          }
        }
      },
    },
  }
</script>
