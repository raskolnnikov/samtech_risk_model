<template>
  <p>
    {{label}}
    <span @dblclick="editing=true" v-show="!editing">
      {{value}}
    </span>
    <span v-show="editing" >
      <sui-dropdown
          :value="input"
          @input="$emit('input', $event); editing=false"
          fluid
          :options="options_freq"
          :placeholder="value"
          selection
      />
    </span>
  </p>
</template>

<script>
  export default{
    name: "ClickToEdit",
    data(){
      return {
        editing: false,
        options_freq: [
          {
            text: 'Antes del Desayuno',
            value: 'Antes del Desayuno',
          },
          {
            text: 'Desayuno',
            value: 'Desayuno',
          },
          {
            text: 'Merienda Mañana',
            value: 'Merienda Mañana',
          },
          {
            text: 'Almuerzo',
            value: 'Almuerzo',
          },
          {
            text: 'Merienda Tarde',
            value: 'Merienda Tarde',
          },
          {
            text: 'Cena',
            value: 'Cena',
          },
          {
            text: 'Merienda Noche',
            value: 'Merienda Noche',
          },
          {
            text: 'Otro',
            value: 'Otro',
          },
        ],
      }
    },
    props: [
      "label",
      "value"
    ]
  }
</script>

<style>

</style>
