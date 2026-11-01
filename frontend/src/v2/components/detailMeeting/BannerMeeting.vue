<template>
  <div
    v-if="property.itemBanner.eventTemplateType === 'RDG'"
    :class="['meeting-banner']"
    :style="{
      backgroundImage: `url('${property.itemBanner.bannerEvent}')`,
    }"
  >
    <h1 class="text-banner">
      {{ property.itemBanner.title }}
    </h1>
    <v-card class="mx-auto meeting-card" outlined> </v-card>
  </div>
  <div v-else :class="['meeting-banner', 'non-rdg-banner']">
    <h1 class="text-banner">
      {{ property.itemBanner.title }}
    </h1>
    <v-card class="mx-auto meeting-card" outlined> </v-card>
  </div>
</template>

<script setup lang="ts">
const property: any = defineProps({
  itemBanner: Object,
});
</script>

<style scoped>
/* .meeting-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 102%;
  background-size: 100% 100%;
  margin-left: calc(31px + 21px);
  margin-top: 10px;
  border-radius: 12px;
  background-image: url(itemBanner == 'RDG' ? ""@/v2/assets/meeting/meeting_banner.png" : ""@/v2/assets/meeting/meeting_banner2.png");
  background-position: center;
  background-repeat: no-repeat;
  max-width: 100%;
} */

.meeting-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-size: 100% 100%;
  border-radius: 12px;
  background-position: center;
  height: 100%;
  padding: 20px;
  margin-left: 50px;
  width: 435px;
}

.text-banner {
  position: relative;
  top: -20%;
  font-size: 2vw;
  color: var(--Flowkit-White, #fff);
  text-align: center;
  font-family: Poppins;
  font-size: 25px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  padding: 5px;
}

.rdg-banner {
  background-image: url("~@/v2/assets/meeting/meeting_banner_2026_1.png");
}

.non-rdg-banner {
  background-image: url("~@/v2/assets/meeting/meeting_banner2.png");
}
</style>
