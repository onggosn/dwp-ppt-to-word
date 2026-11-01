<template>
  <v-row>
    <v-col col="7">
      <div>
        <div class="mt-3 mb-5">
          <span class="info-title mb-3">Title</span>
          <p class="text-newBlack">
            {{ item?.title }}
          </p>
        </div>
        <div>
          <span class="info-title my-3">Method</span>
          <p class="text-newBlack">{{ item?.method }}</p>
        </div>
      </div>
    </v-col>
    <v-col col="5">
      <div class="my-3">
        <span class="info-title mb-3">Media</span>
        <p class="text-newBlack">{{ item?.media }}</p>
      </div>
      <div class="my-3">
        <span class="info-title mb-3">Time</span>
        <p class="text-newBlack">
          {{ item?.time }}
        </p>
      </div>
    </v-col>
    <v-col col="2" class="d-flex justify-end">
      <v-btn variant="outlined" color="#065695" class="rounded-lg">
        <img :src="require('@/v2/assets/icon/edit.svg')" />
        Edit Meeting
      </v-btn>
    </v-col>
  </v-row>
</template>
<script setup lang="ts">
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});
</script>
<style scoped>
.info-title {
  color: #a6abc7;
  font-weight: 500;
  line-height: 100%;
  font-size: 13px;
}
.text-newBlack {
  font-weight: 400;
  font-size: 13px;
}
</style>
