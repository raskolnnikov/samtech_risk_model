<template>
  <sui-modal v-model="open" size="tiny" dimmer="inverted">
    <sui-modal-content>
      <sui-modal-description>
        <sui-header>Alerta de Inactividad</sui-header>
        <p>{{time / 1000}} segundos restantes</p>
      </sui-modal-description>
    </sui-modal-content>
  </sui-modal>
</template>

<script>
  export default{
    name: 'InactivityModal',
    data(){
      return {
        time: 10000
      }
    },
    props: ['open'],
    created: function(){
      let self = this
      setInterval(function(){
        self.time -= 1000;
        if (!self.$store.state.idleVue.isIdle) self.time = 10000;
        if (self.time < 1) {
          self.time = 0;
          // Your logout function should be over here
          self.$store.dispatch('logout').then(()=> {
            self.$router.push('/login').catch(()=>{})
          })
        }
      }, 1000);
    }
  }
</script>

<style>

</style>
