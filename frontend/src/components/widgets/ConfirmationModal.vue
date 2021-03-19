<template>
  <sui-modal v-model="open" size="tiny" dimmer="inverted">
    <sui-modal-content>
      <sui-modal-description>
        <sui-header>{{header}}</sui-header>
        <p>{{text}}</p>
      </sui-modal-description>
    </sui-modal-content>
    <sui-modal-actions>
      <sui-button positive @click.native="selection(true)">
        {{yes_text}}
      </sui-button>
      <sui-button negative @click.native="selection(false)">
        {{no_text}}
      </sui-button>
    </sui-modal-actions>
  </sui-modal>
</template>

<script>
  export default{
    name: 'ConfirmationModal',
    methods:{
      selection(confirm){
        this.$emit('clicked', confirm)
        this.open = false
      },

    },
    props: {
      open:{
        type: Boolean
      },
      header: {
        type: String
      },
      text: {
        type: String
      },
      yes_text: {
        type: String
      },
      no_text: {
        type: String
      }
    }
  }
</script>

<style>

</style>
