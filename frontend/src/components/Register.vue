<template>
  <sui-modal size="mini" closable=closable animation="scale" v-model="open">
      <sui-modal-header>SNPS Sentence-Level Model Showcase</sui-modal-header>
      <sui-modal-content>
        <sui-modal-description>
          <div>
            <sui-form @submit.prevent="login" :error="error">
              <sui-form-field>
                <label>Email</label>
                <input required v-model="email" type="email" placeholder="john@hp.com"/>
              </sui-form-field>
              <sui-form-field>
                <label>Org</label>
                <input required v-model="org" type="text" placeholder="Reporting Americas"/>
              </sui-form-field>
              <sui-form-field>
                <label>Password</label>
                <input required v-model="password" type="password" placeholder="Password"/>
              </sui-form-field>
              <sui-form-field>
                <label>Repeat password</label>
                <input required v-model="password_confirmation" type="password"/>
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
        <sui-button primary @click="register">
          Register
        </sui-button>
      </sui-modal-actions>
  </sui-modal>
</template>

<script>
  export default {
    data(){
      return {
        email : "",
        org: "",
        password : "",
        password_confirmation : "",
        open: false,
        closable: false,
        error: false,
        errors: []
      }
    },
    methods: {
      validate: function(data){
        let errors = []
        if (!data.email){
          errors.push("Email field is required.")
        }
        if (data.password != data.password_confirmation){
          errors.push("The provided passwords don't match.")
        }
        return errors
      },
      register: function () {
        this.error = false
        this.errors = []

        var data = {
          email: this.email,
          org: this.org,
          password: this.password,
          password_confirmation: this.password_confirmation,
        }
        let errors = this.validate(data)
        if(!errors.length){
          this.$store.dispatch('register', data)
         .then(() => {
             this.open = false
             var self = this
             setTimeout(function(){
                 self.$router.push('/dashboard')
             }, 500);
         })
         .catch(err => {
           this.$store.state.status = err.message
           this.error = true
           this.errors.push(err.response.data.message)
         })
        }
        else{
          this.error = true
          errors.forEach((item) => {
            this.errors .push("- "+item)
          });

        }
     }
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
