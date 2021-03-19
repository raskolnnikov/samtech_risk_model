<template>
  <sui-container>
      <sui-form v-on:change="saved=false;">
        <div is="sui-divider" horizontal>
          <h3 is="sui-header">
            <i class="user icon"></i>
            Informaci&oacute;n Personal
          </h3>
        </div>
        <sui-form-field>
          <label>Nombre</label>
          <sui-form-fields fields="four">
            <sui-form-field>
              <input
                type="text"
                v-model="user.name"
                placeholder="Primer Nombre"
              />
            </sui-form-field>
            <sui-form-field>
              <input
                type="text"
                v-model="user.last_name_1"
                placeholder="Primer Apellido"
              />
            </sui-form-field>
            <sui-form-field>
              <input
                type="text"
                v-model="user.last_name_2"
                placeholder="Segundo Apellido"
              />
            </sui-form-field>
          </sui-form-fields>
        </sui-form-field>
          <div is="sui-divider" horizontal style="margin-top:40px;">
            <h3 is="sui-header">
              <i class="phone icon"></i>
              Informaci&oacute;n De Contacto
            </h3>
          </div>
          <sui-form-fields fields="four">
            <sui-form-field>
              <label>Correo Electr&oacute;nico</label>

              <input
                type="email"
                v-model="user.email"
                placeholder="name@host.com"
              />
            </sui-form-field>
          </sui-form-fields>
          <sui-form-fields fields="four">
            <sui-form-field>
              <label>Tel&eacute;fono</label>

              <input
                type="text"
                v-model="user.phone"
                placeholder="Primer Apellido"
              />
            </sui-form-field>
          </sui-form-fields>
      </sui-form>
    <!-- <sui-button class="bottomButton" icon="left chevron" floated="left" label-position="left" content="Regresar" size="large" @click="$router.back()"/> -->
    <sui-button class="bottomButton" floated="right" size="large" :icon="saved?'check':'save'" label-position="left" :color="!saved?'blue':'green'" @click="save_user" :content="!saved?'Guardar':'Guardado'"></sui-button>

  </sui-container>
</template>

<script>
  import axios from 'axios'

  const api_url = ' http://63.250.41.246:5000'

  export default{
    name: 'userView',
    components: {
    },
    data: function(){
      return {
        user: {
            "name": "",
            "last_name_1": "",
            "last_name_2": "",
            "email": "",
            "phone": "",
        },
        saved: false
      }

    },
    props:[
      'user_public_id'
    ],
    methods:{
      save_user: function(){
        let payload = {
          'name': this.user.name,
          'last_name_1': this.user.last_name_1,
          'last_name_2': this.user.last_name_2,
          'email': this.user.email,
          'phone': this.user.phone
        }
        if(!this.user_public_id){
          payload.public_id = this.user.public_id
        }
        update_user_data(this, payload)
        this.saved = true
      }
    },
    created() {
        if(!this.user_public_id){
          this.user_public_id = this.$store.state.user.id
        }
        load_user_data(this)
    }

  }

const load_user_data = function(self){
  self.$store.state.status = "loading"
      axios({url: api_url+'/user/'+self.user_public_id, method: 'GET' })
      .then(resp => {
        let users_response = resp.data.data
        self.user = users_response
        self.$store.state.status = 'success'
      })
      .catch(err => {
        self.$store.state.status = err
      })
};

const update_user_data = function(self, payload){
  self.$store.state.status = "loading"
      axios({url: api_url+'/user/', data: payload, method: 'PUT' })
      .then(() => {
        self.$store.state.status = 'success'
      })
      .catch(err => {
        self.$store.state.status = err
      })
};

</script>

<style>
.ui.form .field > label {
  text-align: left;
}

.bottomButton {
  margin-top: 30px !important;
}

.bottomButton{
  margin-top: 30px !important;
}

</style>
