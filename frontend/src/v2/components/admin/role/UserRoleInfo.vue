<template>
  <div v-if="isLoading">
    <v-col v-for="i in 2" :key="i" cols="12">
      <free-style-shimmer
        width="100%"
        height="40px"
        border-radius="10px"
        color="#d3d3d3"
      />
    </v-col>
  </div>

  <v-row v-else>
    <v-col col="7">
      <div>
        <div class="mt-3 mb-5">
          <span class="info-title mb-3">Pangkat</span>
          <p class="text-newBlack">
            {{ item.pangkatName }}
          </p>
        </div>
        <div>
          <span class="info-title my-3">Jabatan</span>
          <p class="text-newBlack">{{ item.jabatanName }}</p>
        </div>
      </div>
    </v-col>
    <v-col col="5">
      <div class="my-3">
        <span class="info-title mb-3">Email</span>
        <p class="text-newBlack">{{ item.email }}</p>
      </div>
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
  isLoading: {
    type: Boolean,
    default: false,
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
  line-height: 100%;
}
</style>
