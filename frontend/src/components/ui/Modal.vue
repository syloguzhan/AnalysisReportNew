<template>
  <div v-if="visible" class="ui-modal">
    <div class="ui-modal-content">
      <slot></slot>
      <button @click="$emit('close')">Kapat</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "UIModal",
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  }
};
</script> 