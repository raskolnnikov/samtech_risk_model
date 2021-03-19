<template>
    <sui-container>
      <sui-container>
            <sui-table compact celled stackable color="orange">
             <sui-table-header>
               <sui-table-row>
                 <sui-table-header-cell>Nombre</sui-table-header-cell>
                 <sui-table-header-cell>Apellidos</sui-table-header-cell>
                 <sui-table-header-cell>Ingreso</sui-table-header-cell>
                 <sui-table-header-cell>Activo</sui-table-header-cell>
                 <sui-table-header-cell>Admin</sui-table-header-cell>
                 <sui-table-header-cell>Contacto</sui-table-header-cell>
                 <sui-table-header-cell>Acciones</sui-table-header-cell>
               </sui-table-row>
             </sui-table-header>

           <transition-group tag="sui-table-body" name="table-row">
             <sui-table-row v-for="user in user_list" :key="user.public_id">
               <sui-table-cell>{{user.name}}</sui-table-cell>
               <sui-table-cell>{{user.last_name_1+" "+user.last_name_2}}</sui-table-cell>
               <sui-table-cell>{{user.registered_on | formatDate}}</sui-table-cell>
               <sui-table-cell>
                 <sui-form-field>
                    <sui-checkbox toggle :disabled="user.public_id === $store.state.user.id" v-model="user.active" @click.prevent="toggle_active(user.public_id)"/>
                 </sui-form-field>
               </sui-table-cell>
               <sui-table-cell>
                 <sui-form-field>
                    <sui-checkbox toggle :disabled="user.public_id === $store.state.user.id" v-model="user.admin"  @click.prevent="toggle_admin(user.public_id)"/>
                 </sui-form-field>
               </sui-table-cell>
               <sui-table-cell>
                 <sui-icon name="mail" color="grey" circular />{{user.email}} <br>
                 <sui-icon name="phone" color="grey" circular />{{user.phone}}</sui-table-cell>
               <sui-table-cell>
                  <sui-button-group>
                    <sui-button icon="edit" label-position="left" content="Editar" size="standard" @click="$router.push('user/'+user.public_id)"/>
                 </sui-button-group></sui-table-cell>
             </sui-table-row>
           </transition-group>
          </sui-table>
        <ConfirmationModal
          :open="show_modal"
          header="Confirmar Accion"
          text="Desea eliminar el paciente seleccionado?"
          yes_text="Si"
          no_text="No"
          @clicked="remove"
        />
    </sui-container>
  </sui-container>
</template>

<script>
import ConfirmationModal from './widgets/ConfirmationModal.vue'
import axios from 'axios'

const api_url = ' http://63.250.41.246:5000'

export default{
  components:{
    ConfirmationModal,
  },
  data: function(){
    return {
      show_modal: false,
      user_list: []
    }
  },
  props:[
    'id'
  ],
  methods:{
    remove: function(confirm){
      if(confirm){
        this.user_list.pop()
      }
      this.show_modal = false
    },
    show_confirmation_modal: function(){
      this.show_modal = true
      this.$forceUpdate()
    },
    toggle_admin: function(user_public_id){
      if(!(user_public_id === this.$store.state.user.id)){
        toggle_admin_request(this, user_public_id)
      }
    },
    toggle_active: function(user_public_id){
      if(!(user_public_id === this.$store.state.user.id)){
        toggle_active_request(this, user_public_id)
      }
    }
  },
  mounted() {
    load_users(this)
  }
}

const load_users = function(self){
      self.$store.state.status="loading"

      axios({url: api_url+'/user/', method: 'GET' })
      .then(resp => {
        let users_response = resp.data.data
        self.user_list = users_response
        self.$store.state.status=resp.status

      })
      .catch(err => {
        self.$store.state.status = err.message

      })
};

const toggle_admin_request = function(self, user_public_id){
      self.$store.state.status="loading"
      axios({url: api_url+'/user/'+user_public_id+'/toggle_admin', method: 'PUT' })
      .then(resp => {
        self.$store.state.status=resp.status
      })
      .catch(err => {
        self.$store.state.status = err.message
      })
};

const toggle_active_request = function(self, user_public_id){
      self.$store.state.status="loading"
      axios({url: api_url+'/user/'+user_public_id+'/toggle_active', method: 'PUT' })
      .then(resp => {
        self.$store.state.status=resp.status

      })
      .catch(err => {
        self.$store.state.status = err.message
      })
};
</script>

<style>
.table-row-enter-active, .table-row-leave-active {
  transition: all 0.4s;
}
.table-row-enter, .table-row-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0.4;
  transform: translateY(60vh);
}
</style>
