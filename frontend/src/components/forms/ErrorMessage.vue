<template>
  <div v-if="error" class="error-message">
    {{ error }}
  </div>
</template>

<script>
export default {
  name: "ErrorMessage",
  props: {
    error: String
  }
};
</script> 