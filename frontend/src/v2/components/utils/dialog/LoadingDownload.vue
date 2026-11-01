<template>
  <v-dialog v-model="dialog" :scrim="true" persistent width="auto">
    <v-card color="rgb(10, 91, 154)" class="rounded-lg">
      <v-card-text class="text-white pt-2 pb-0 pl-5 pr-5">
        <p class="font-weight-medium text-15" style="letter-spacing: -0.2px">
          {{ title }}
        </p>
        <v-progress-linear
          v-if="hasProgress"
          :model-value="(progress / totalProgress) * 100"
          :indeterminate="progress == 0"
          style="width: 20vw"
          color="white"
          class="mb-0 mt-2 mb-4"
        ></v-progress-linear>
        <v-progress-linear
          v-else
          indeterminate
          style="width: 20vw"
          color="white"
          class="mb-0 mt-2 mb-4"
        ></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
// eslint-disable-next-line
const props = defineProps({
  title: {
    type: String,
    default: "Please stand by",
  },
  progress: {
    type: Number,
    default: 0,
  },
  totalProgress: {
    type: Number,
    default: 0,
  },
  hasProgress: {
    type: Boolean,
    default: false,
  },
  isShowProgress: {
    type: Boolean,
    default: false,
  },
});
const dialog = ref(true);
</script>
