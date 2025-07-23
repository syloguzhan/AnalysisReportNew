<template>
  <div class="custom-input">
    <label :for="id">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :placeholder="placeholder"
      :value="value"
      @input="$emit('input', $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  name: "CustomInput",
  props: {
    label: String,
    id: String,
    value: String,
    type: {
      type: String,
      default: "text",
    },
    placeholder: String,
  },
};
</script>
