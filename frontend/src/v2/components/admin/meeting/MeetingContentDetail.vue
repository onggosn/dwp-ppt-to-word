<template>
  <div class="my-2">
    <!-- <v-tabs
      v-model="tab"
      align-tabs="left"
      color="#D6212A"
      style="color: #065695"
    >
      <v-tab :value="1">GENERAL</v-tab>
      <v-tab :value="2">DESCRIPTION</v-tab>
      <v-tab :value="3">MEMBER</v-tab>
      <v-tab :value="4">AGENDA</v-tab>
    </v-tabs> -->
  </div>
  <!-- <div class="mt-5">
    <v-window v-model="tab">
      <v-window-item :value="1"> GENERAL </v-window-item>
      <v-window-item :value="2"> DESCRIPTION </v-window-item>
      <v-window-item :value="3"> MEMBER </v-window-item>
      <v-window-item :value="4"> AGENDA </v-window-item>
    </v-window>
  </div> -->
</template>
<script setup lang="ts">
import { ref } from "vue";

const tab = ref<number | string>(1);
</script>
<style scoped></style>
