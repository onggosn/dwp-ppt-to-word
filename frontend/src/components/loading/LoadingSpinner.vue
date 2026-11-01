<template>
  <v-overlay
    :model-value="overlay"
    scroll-strategy="block"
    persistent
    class="align-center justify-center"
  >
    <v-progress-circular
      color="primary"
      indeterminate
      size="40"
    ></v-progress-circular>
  </v-overlay>
</template>
<script>
export default {
  name: "loadingSpinner",
  data() {
    return {
      overlay: true,
    };
  },
};
</script>
<style scoped></style>
