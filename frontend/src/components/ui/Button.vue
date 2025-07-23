<template>
  <button :type="type" @click="$emit('click')">
    <slot>Buton</slot>
  </button>
</template>

<script>
export default {
  name: "UIButton",
  props: {
    type: {
      type: String,
      default: "button"
    }
  }
};
</script> 