<template>
    <sui-container>
      <sui-container>
        <br>
            <h3 is="sui-header" floated="left">
              <sui-icon name="chart pie" />
              <sui-header-content>
                Desgloce de la Clasificación
              </sui-header-content>
            </h3>
            <sui-divider clearing />
            <sui-image style="margin-left:4%;"
              :src="img"
              size="massive"
            />
          </sui-container>
          <sui-divider clearing />

          <br>
          <sui-container>
            <br>
            <h3 is="sui-header" floated="left">
              <sui-icon name="history" size="small"/>
              <sui-header-content>
                Histórico de Datos
              </sui-header-content>
            </h3>
            <sui-divider clearing />

            <sui-table celled compact color="blue" striped textAlign="center">
             <sui-table-header>
               <sui-table-row>
                 <sui-table-header-cell>Dia</sui-table-header-cell>
                 <sui-table-header-cell>Dist Total</sui-table-header-cell>
                 <!-- <sui-table-header-cell>PSM</sui-table-header-cell> -->
                 <sui-table-header-cell>Veloc. MAX</sui-table-header-cell>
                 <sui-table-header-cell>Veloc. AVG</sui-table-header-cell>
                 <sui-table-header-cell title="Porcentaje Sobre la Media">PSM</sui-table-header-cell>
                 <sui-table-header-cell>Veloc. STD</sui-table-header-cell>
                 <sui-table-header-cell title="Porcentaje Sobre la Media">PSM</sui-table-header-cell>
                 <sui-table-header-cell positive>Prealert. B</sui-table-header-cell>
                 <sui-table-header-cell positive>Prealert. M</sui-table-header-cell>
                 <sui-table-header-cell positive>Prealert. A</sui-table-header-cell>
                 <sui-table-header-cell positive>Total/100Km</sui-table-header-cell>
                 <sui-table-header-cell title="Porcentaje Sobre la Media">PSM</sui-table-header-cell>
                 <sui-table-header-cell positive>Alertas B</sui-table-header-cell>
                 <sui-table-header-cell warning>Alertas M</sui-table-header-cell>
                 <sui-table-header-cell negative>Alertas A</sui-table-header-cell>
                 <sui-table-header-cell positive>Total/100Km.</sui-table-header-cell>
                 <sui-table-header-cell title="Porcentaje Sobre la Media">PSM</sui-table-header-cell>

               </sui-table-row>
             </sui-table-header>

           <transition-group tag="sui-table-body" name="table-row">
             <sui-table-row v-for="(entry,i) in entry_list" :key="i">
               <sui-table-cell><strong>{{entry.date | formatDate}}</strong></sui-table-cell>
               <sui-table-cell textAlign="right">{{entry.sum_distance}} Km.</sui-table-cell>
               <!-- <sui-table-cell>+30%</sui-table-cell> -->
               <sui-table-cell textAlign="right">{{entry.max_speed}}Km/h</sui-table-cell>
               <sui-table-cell textAlign="right">{{entry.mean_speed}} Km/h</sui-table-cell>
               <sui-table-cell>{{entry.speed_departure_from_weekly_mean>0?'+':''}}{{(entry.speed_departure_from_weekly_mean * 100).toFixed(0)}}%</sui-table-cell>
               <sui-table-cell textAlign="right">±{{entry.std_speed}} Km/h</sui-table-cell>
               <sui-table-cell>{{entry.std_speed_departure_from_weekly_mean>0?'+':''}}{{(entry.std_speed_departure_from_weekly_mean* 100).toFixed(0) }}%</sui-table-cell>
               <sui-table-cell :warning="entry.prealert_low_count>0">{{entry.prealert_low_count}}</sui-table-cell>
               <sui-table-cell :warning="entry.prealert_mid_count>0">{{entry.prealert_mid_count}}</sui-table-cell>
               <sui-table-cell :warning="entry.prealert_high_count>0">{{entry.prealert_high_count}}</sui-table-cell>
               <sui-table-cell>{{entry.pre_alert_count_by_100km}}</sui-table-cell>
               <sui-table-cell textAlign="left">
                 {{entry.pre_alert_count_by_100km_departure_from_weekly_mean>0?'+':''}}{{(entry.pre_alert_count_by_100km_departure_from_weekly_mean * 100.00).toFixed(0)}}%
                 <sui-icon color="orange" v-if="entry.pre_alert_count_by_100km_departure_from_weekly_mean>3" name="attention" />
               </sui-table-cell>
               <sui-table-cell :negative="entry.alert_low_count>0">{{entry.alert_low_count}}</sui-table-cell>
               <sui-table-cell :negative="entry.alert_mid_count>0">{{entry.alert_mid_count}}</sui-table-cell>
               <sui-table-cell :negative="entry.alert_high_count>0">{{entry.alert_high_count}}</sui-table-cell>
              <sui-table-cell> {{entry.alert_count_by_100km}}</sui-table-cell>
              <sui-table-cell textAlign="left">
                {{entry.alert_count_by_100km_departure_from_weekly_mean>0?'+':''}}{{(entry.alert_count_by_100km_departure_from_weekly_mean * 100.00).toFixed(0)}}%
                <sui-icon color="red" v-if="entry.alert_count_by_100km_departure_from_weekly_mean>3" name="attention" />
              </sui-table-cell>

             </sui-table-row>
           </transition-group>
          </sui-table>
          <sui-divider clearing />

          <br>
          <br>

          <h3 is="sui-header" floated="left">
            <sui-icon name="line chart" />
            <sui-header-content>
              Visualizar Componentes
            </sui-header-content>
          </h3>
          <sui-divider clearing />
          <br>

          <sui-grid :columns="3">
            <sui-grid-row>
              <sui-grid-column>
                <apexchart width="100%" type="line" :options="options[0]" :series="series[0]"></apexchart>
              </sui-grid-column>
              <sui-grid-column>
                <apexchart width="100%" type="line" :options="options[1]" :series="series[1]"></apexchart>
              </sui-grid-column>
              <sui-grid-column>
                <apexchart width="100%" type="line" :options="options[2]" :series="series[2]"></apexchart>
              </sui-grid-column>
            </sui-grid-row>
            <sui-grid-row>
              <sui-grid-column>
                <apexchart width="100%" type="line" :options="options[3]" :series="series[3]"></apexchart>
              </sui-grid-column>
              <sui-grid-column>
                <apexchart width="100%" type="line" :options="options[4]" :series="series[4]"></apexchart>
              </sui-grid-column>
              <sui-grid-column>
                <apexchart width="100%" type="line" :options="options[5]" :series="series[5]"></apexchart>
              </sui-grid-column>
            </sui-grid-row>
          </sui-grid>
          <sui-divider clearing />

          <br>
          <br>
          <br>

          <h3 is="sui-header" floated="left">
            <sui-icon name="globe americas" />
            <sui-header-content>
              Geocercas
            </sui-header-content>
          </h3>
          <sui-divider clearing />
          <div style="margin-left:20%;width:60%;height:auto !important;" v-html="geo_plot"></div>
    </sui-container>
  </sui-container>
</template>

<script>
import axios from 'axios'
import VueApexCharts from 'vue-apexcharts'

const api_url = ' http://127.0.0.1:5000'

export default{
  components:{
       apexchart: VueApexCharts
  },
  data: function(){
    return {
      geo_plot: null,
      img: 'https://flevix.com/wp-content/uploads/2019/07/Loading-Image-1-1.gif',
      entry_list: [],
      decision_plot: {image: null},
      options: [
        {
          title: {
            text: 'Indice de Riesgo',
            align: 'left'
          },
          legend:{
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -30,
            offsetX: -5
          },
          stroke: {
            width: [4, 3],
            curve: 'smooth',
            dashArray: [0, 8]
          },
          chart: {
            id: 'vuechart-example',
            toolbar: {
              show: false
            },
          },
          xaxis: {
            categories: [
              'día-9',
              'día-8',
              'día-7',
              'día-6',
              'día-5',
              'día-4',
              'día-3',
              'día-2',
              'día-1',
              'día-0'
            ]
          }
        },
        {
          title: {
            text: 'Distancia Recorrida',
            align: 'left'
          },
          legend:{
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -36,
            offsetX: -5
          },
          stroke: {
            width: [4, 3],
            curve: 'smooth',
            dashArray: [0, 8]
          },
          dataLabels: {
            enabled: true,
            enabledOnSeries: [0]
          },
          chart: {
            id: 'vuechart-example',
            toolbar: {
              show: false
            },
          },
          xaxis: {
            categories: [
              'día-9',
              'día-8',
              'día-7',
              'día-6',
              'día-5',
              'día-4',
              'día-3',
              'día-2',
              'día-1',
              'día-0'
            ]
          },
          yaxis: {
            title: {
              text: 'Distancia'
            }
          }

        },
        {
          title: {
            text: 'Velocidad Promedio',
            align: 'left'
          },
          legend:{
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -36,
            offsetX: -5
          },
          stroke: {
            width: [4, 3],
            curve: 'smooth',
            dashArray: [0, 8]
          },
          chart: {
            id: 'vuechart-example',
            toolbar: {
              show: false
            },
          },
          dataLabels: {
            enabled: true,
            enabledOnSeries: [0]
          },
          xaxis: {
            categories: [
              'día-9',
              'día-8',
              'día-7',
              'día-6',
              'día-5',
              'día-4',
              'día-3',
              'día-2',
              'día-1',
              'día-0'
            ]
          },
          yaxis: {
            title: {
              text: 'Velocidad'
            }
          }
        },
        {
          title: {
            text: 'Velocidad Maxima',
            align: 'left'
          },
          legend:{
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -36,
            offsetX: -5
          },
          dataLabels: {
            enabled: true,
            enabledOnSeries: [0]
          },
          stroke: {
            width: [4, 3],
            curve: 'smooth',
            dashArray: [0, 8]
          },
          chart: {
            id: 'vuechart-example',
            toolbar: {
              show: false
            },
          },
          xaxis: {
            categories: [
              'día-9',
              'día-8',
              'día-7',
              'día-6',
              'día-5',
              'día-4',
              'día-3',
              'día-2',
              'día-1',
              'día-0'
            ]
          },
          yaxis: {
            title: {
              text: 'Velocidad'
            }
          }
        },
        {
          title: {
            text: 'Prealertas por c/100 Km.',
            align: 'left'
          },
          legend:{
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -36,
            offsetX: -5
          },
          dataLabels: {
            enabled: true,
            enabledOnSeries: [0]
          },
          stroke: {
            width: [4, 3],
            curve: 'smooth',
            dashArray: [0, 8]
          },
          chart: {
            id: 'vuechart-example',
            toolbar: {
              show: false
            },
          },
          xaxis: {
            categories: [
              'día-9',
              'día-8',
              'día-7',
              'día-6',
              'día-5',
              'día-4',
              'día-3',
              'día-2',
              'día-1',
              'día-0'
            ]
          },
          yaxis: {
            title: {
              text: 'Cantidad'
            }
          }
        },
        {
          title: {
            text: 'Alertas por c/100 Km.',
            align: 'left'
          },
          legend:{
            position: 'top',
            horizontalAlign: 'right',
            floating: true,
            offsetY: -36,
            offsetX: -5
          },
          dataLabels: {
            enabled: true,
            enabledOnSeries: [0]
          },
          stroke: {
            width: [4, 3],
            curve: 'smooth',
            dashArray: [0, 8]
          },
          chart: {
            id: 'vuechart-example',
            toolbar: {
              show: false
            },
          },
          xaxis: {
            categories: [
              'día-9',
              'día-8',
              'día-7',
              'día-6',
              'día-5',
              'día-4',
              'día-3',
              'día-2',
              'día-1',
              'día-0'
            ]
          },
          yaxis: {
            title: {
              text: 'Cantidad'
            }
          }
        },
      ],
      series: []
    }
  },
  props:[
    'patente_id',
    'step_id_week'
  ],
  methods:{
    load_image: function() {
        this.img = 'data:image/png;base64,'+this.decision_plot.image
    }
  },
  mounted() {
    load_entries(this);
    load_series(this);
    load_decision_plot(this);
    load_geofences(this);

  }
}


const load_entries = function(self){
      self.$store.state.status="loading"
      axios({url: api_url+'/detail/'+self.patente_id, method: 'GET' })
      .then(resp => {
        let entries_response = resp.data.data
        self.entry_list = entries_response
        self.create_series()
        self.$store.state.status=resp.status

      })
      .catch(err => {
        self.$store.state.status = err.message

      })
};

const load_series = function(self){
      self.$store.state.status="loading"

      axios({url: api_url+'/detail/'+self.patente_id+'/series/', method: 'GET' })
      .then(resp => {
        let series_response = resp.data
        self.series = series_response
        self.$store.state.status=resp.status
      })
      .catch(err => {
        self.$store.state.status = err.message

      })
};

const load_decision_plot = function(self){
      self.$store.state.status="loading"
      axios({url: api_url+'/detail/'+self.patente_id+'/decision_plot/'+self.step_id_week, method: 'GET' })
      .then(resp => {
        let image_response = resp.data
        self.decision_plot = image_response
        self.load_image()
        self.$store.state.status=resp.status

      })
      .catch(err => {
        self.$store.state.status = err.message

      })
};

const load_geofences = function(self){
      self.$store.state.status="loading"
      axios({url: api_url+'/detail/'+self.patente_id+'/geofences/'+self.step_id_week, method: 'GET' })
      .then(resp => {
        let geo_response = resp.data
        self.geo_plot = geo_response
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
