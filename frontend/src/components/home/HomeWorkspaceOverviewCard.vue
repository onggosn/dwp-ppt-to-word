<template>
  <v-card
    elevation="2"
    class="background-overview-style pa-6 rounded-lg shadow-10"
    :style="`background-image: url('${imageUrl}')`"
  >
    <api-loader :apiMethod="apiMethod" :hasOverlay="false">
      <template v-slot:default="props">
        <h2 class="text-redTheme-gradien mb-0 text-40 fw-600">
          {{ props.response.plainData }}
        </h2>
        <h6 class="text-blackTheme text-13 fw-600">{{ label }}</h6>
      </template>
      <template v-slot:loading>
        <free-style-shimmer
          height="40px"
          width="40px"
          border-radius="100px"
          color="#DCDCDC"
          class="mt-2 mb-4"
        />
        <free-style-shimmer
          height="20px"
          width="100px"
          border-radius="20px"
          color="#DCDCDC"
          class="mt-2 mb-2"
        />
      </template>
    </api-loader>
  </v-card>
</template>

<script>
import ApiLoader from "@/components/ApiLoader.vue";

export default {
  components: { ApiLoader },
  props: ["apiMethod", "imageUrl", "label"],
  data() {
    return {};
  },
};
</script>

<style scoped>
.background-overview-style {
  background-repeat: no-repeat;
  background-size: 50%;
  background-position: 125px 29px;
  border-radius: 20px !important;
}
.shadow-10 {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1) !important;
}
</style>
