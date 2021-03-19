<template>
  <sui-segment>
  <h2 is="sui-header" text-align="left">
    <sui-icon :name="icon" circular color="#fff"/>
    <sui-header-content text-align="center">
      {{l1}} {{l2?'|':''}} {{l2}}
    </sui-header-content>
  </h2>
  </sui-segment>
</template>

<script>
export default{
  name: "SectionHeader",
  props: [
    "l1",
    "l2",
    "icon"
  ]
}
</script>
