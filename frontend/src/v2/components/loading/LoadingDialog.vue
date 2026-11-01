<template>
  <div class="text-center">
    <v-overlay :model-value="true" class="align-center justify-center">
      <v-card class="primary-gradient">
        <v-card-text>
          Please stand by
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-overlay>
  </div>
</template>
<script>
export default {
  data: () => ({}),
};
</script>
<style scoped>
.primary-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 20px;
  color: white;
}
</style>
