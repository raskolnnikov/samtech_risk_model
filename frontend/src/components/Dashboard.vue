<template>
  <div>
    <SectionHeader l1="Samtech" l2="Modelo de Predicción de Riesgo" icon="braille"/>
    <sui-menu attached="top" tabular>
      <a
        v-if="!$store.state.admin_flag"
        is="sui-menu-item"
        :active="isActive('my_data')"
        @click="select('my_data'); $router.push('/dashboard/user/'+$store.state.user.id)"
      >
        Mis Datos
      </a>
      <a
        is="sui-menu-item"
        :active="isActive('ranking')"
        @click="select('ranking'); $router.push('/dashboard/ranking')"
      >
        <sui-icon v-if="active=='ranking'" name="bars" link /> Ranking
      </a>
      <a v-if="active=='details'"
        is="sui-menu-item"
        :active="isActive('details')"
        @click="select('details'); $router.push('/dashboard/patente/0')"
      >
        <sui-icon name="truck" link /> Detalles ({{patente}})
      </a>
      <a
        v-if="$store.state.admin_flag"
        is="sui-menu-item"
        :active="isActive('statistics')"
        @click="select('statistics'); $router.push('/dashboard/statistics')"
      >
        <sui-icon v-if="active=='statistics'" name="chart pie" link /> Estadísticas
      </a>
    </sui-menu>
    <sui-segment attached="bottom">
      <router-view @selected_patent="go_to_patent"></router-view>
    </sui-segment>
  </div>

</template>

<script>
import SectionHeader from './widgets/SectionHeader.vue'

  export default{
    components: {
      SectionHeader
    },
    data: function(){
      return {
        tabs: {},
        patente: null,
        active: 'ranking',
      }
    },
    mounted(){
      this.patente = null;
    },
    methods: {
      isActive(name) {
        return this.active === name;
      },
      select(name) {
        this.active = name;
      },
      go_to_patent(event){
        console.log(event)
        this.patente = event.patente
        this.active = 'details';
        this.$router.push('/dashboard/patente/'+event.patente+'/'+event.step_id_week);
      }
    },
  }
</script>

<style>

</style>
