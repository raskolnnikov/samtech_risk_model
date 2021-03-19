<template>
    <sui-container>
      <br>
      <h3 is="sui-header" floated="left">
        <sui-icon name="list ol" />
        <sui-header-content>
          Clasificacion Semanal
          <sui-header-subheader>Modelo de Riesgo Vers. | 1.0</sui-header-subheader>
        </sui-header-content>
      </h3>
      <sui-divider clearing />

      <sui-container>
            <sui-table compact="very" celled striped color="blue" textAlign="center">
             <sui-table-header>
               <sui-table-row>
                 <sui-table-header-cell>Posición</sui-table-header-cell>
                 <sui-table-header-cell>Cambio</sui-table-header-cell>
                 <sui-table-header-cell>Patente</sui-table-header-cell>
                 <sui-table-header-cell>Dist. Recorrida</sui-table-header-cell>
                 <sui-table-header-cell>Veloc. Promedio</sui-table-header-cell>
                 <sui-table-header-cell>No. Prealertas B.</sui-table-header-cell>
                 <sui-table-header-cell>No. Prealertas M.</sui-table-header-cell>
                 <sui-table-header-cell>No. Prealertas A.</sui-table-header-cell>
                 <sui-table-header-cell>No. Alertas B.</sui-table-header-cell>
                 <sui-table-header-cell>No. Alertas M.</sui-table-header-cell>
                 <sui-table-header-cell>No. Alertas A.</sui-table-header-cell>
                 <sui-table-header-cell>Semana</sui-table-header-cell>
                 <sui-table-header-cell>Detalles</sui-table-header-cell>
               </sui-table-row>
             </sui-table-header>

           <transition-group tag="sui-table-body" name="table-row">
             <sui-table-row v-for="entry in entry_list" :key="entry.patente">
              <sui-table-cell >
                <sui-statistic horizontal size="mini">
                  <sui-statistic-value>
                    {{entry.predicted_rank}}
                  </sui-statistic-value>
                </sui-statistic>
              </sui-table-cell >
               <sui-table-cell textAlign="left">  <sui-icon :name="entry.predicted_rank%3==0?'angle down':'angle up'" :color="entry.predicted_rank%3?'green':'red'" link size="big"/>
                 ({{entry.predicted_rank%3?'+':'-'}}{{Math.floor(Math.random() * 8)+1}})
               </sui-table-cell>

               <sui-table-cell>{{entry.patente}}</sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_sum_distance}} Km.</sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_mean_speed}} </sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_pre_alert_mid_count}} </sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_pre_alert_high_count}} </sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_pre_alert_low_count}} </sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_alert_low_count}} </sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_alert_mid_count}} </sui-table-cell>
               <sui-table-cell>  {{entry.ten_day_alert_high_count}} </sui-table-cell>
               <sui-table-cell>{{entry.starting_date}}</sui-table-cell>
               <sui-table-cell>
                   <sui-button icon="search" fluid label-position="left" content="Ver" size="tiny" color="primary" @click="$emit('selected_patent', {'patente':entry.patente, 'step_id_week':entry.step_id_week})"/>
               </sui-table-cell>
             </sui-table-row>
           </transition-group>
          </sui-table>
    </sui-container>
  </sui-container>
</template>

<script>
import axios from 'axios'

const api_url = ' http://localhost:5000'

export default{
  components:{
  },
  data: function(){
    return {
      entry_list: []
    }
  },
  methods:{
    get_color: function(rank){
        var value = (51.0 - rank) / 50
        var h = (1.0 - value) * 240
        return "hsl(" + h + ", 100%, 50%)";
    }
  },
  mounted() {
    load_entries(this)
  }
}

const load_entries = function(self){
      self.$store.state.status="loading"

      axios({url: api_url+'/ranking/', method: 'GET' })
      .then(resp => {
        let entries = resp.data.data
        self.entry_list = entries
        self.$store.state.status=resp.status

      })
      .catch(err => {
        self.$store.state.status = err.message

      })
};

</script>

<style>
.table-row-enter-active, .table-row-leave-active {
  transition: all 0.5s;
}
.table-row-enter, .table-row-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0.8;
  transform: translateY(2vh);
}
</style>
