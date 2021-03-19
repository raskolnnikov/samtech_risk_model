<template>
      <sui-modal size="mini" closable=closable animation="scale" v-model="open">
          <sui-modal-header>Login</sui-modal-header>
          <sui-modal-content>
            <sui-modal-description>
              <div>
                <sui-form @submit.prevent="login" :error="error">
                  <sui-form-field>
                    <label>Email</label>
                    <input required v-model="email" type="email" placeholder="Email"/>
                  </sui-form-field>
                  <sui-form-field>
                    <label>Password</label>
                    <input required v-model="password" type="password" placeholder="Password"/>
                  </sui-form-field>
                  <sui-message error>
                    <sui-message-header>Ooops</sui-message-header>
                    <p v-for="(err, index) in errors" :key="index">
                      {{err}}
                    </p>
                  </sui-message>
                </sui-form>
              </div>
            </sui-modal-description>
          </sui-modal-content>
          <sui-modal-actions>
            <sui-button-group attached="bottom">
              <sui-button positive @click="login">
                Login
              </sui-button>
              <sui-button primary @click="$router.push('register')">
                Register
              </sui-button>
            </sui-button-group>
          </sui-modal-actions>
      </sui-modal>
</template>

<script>

  export default {
    data(){
      return {
        email : "",
        password : "",
        open: false,
        closable: false,
        error: false,
        errors: []
      }
    },
    methods: {
      login: function () {
        this.errors = []
        let email = this.email
        let password = this.password
        this.$store.dispatch('login', { email, password })
       .then(() => {
          this.open = false
          var self = this
          setTimeout(function(){
              if(self.$store.state.user.admin_flag){
                self.$router.push('/dashboard/ranking')
              }
              else{
                self.$router.push('/login')
              }
          }, 500);
       })
       .catch(err => {
         this.$store.state.status = err.response.data.message
         this.error = true
         this.errors.push(err.response.data.message)
       })
     },
   },
   mounted: function() {
     var self = this;
      setTimeout(function(){
          self.open = true;
      }, 200);
   }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
