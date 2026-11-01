<template>
  <v-card
    v-if="!rail"
    class="rounded-lg mx-4 mb-4"
    @click="handleReturnToBISuperApps"
  >
    <v-card-text>
      <v-icon icon="mdi-arrow-left" color="#065695" class="mb-4"></v-icon>
      <div class="d-flex align-center">
        <img :src="require(`@/v2/assets/icon/icon-bisa.png`)" height="30" />
        <p class="font-weight-bold text-16 ml-2 py-4">
          Return to BI Super Apps
        </p>
      </div>
      <div>
        <span class="text-12 font-weight-400 text-#616161">
          You will leave this page and be redirected to BI Super Apps
        </span>
      </div>
    </v-card-text>
  </v-card>

  <div v-else class="d-flex justify-center mb-4">
    <v-btn icon rounded="lg" @click="handleReturnToBISuperApps">
      <img :src="require(`@/v2/assets/icon/icon-bisa.png`)" height="30" />
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { redirectToBisa } from "@/v2/helpers/utils";

interface Props {
  rail: boolean;
}

defineProps<Props>();

const handleReturnToBISuperApps = () => {
  redirectToBisa();
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>
