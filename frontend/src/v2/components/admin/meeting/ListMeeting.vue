<template>
  <div v-if="!searchMode" class="my-3">
    <v-tabs align-tabs="start" color="#D6212A" class="my-2">
      <v-tab
        :value="MeetingType.Meeting"
        :to="{ name: 'meeting-admin-meeting' }"
      >
        Meeting
      </v-tab>
      <v-tab
        :value="MeetingType.PresentationMaterial"
        :to="{ name: 'meeting-admin-presentation-material' }"
      >
        Presentation Material
      </v-tab>
    </v-tabs>
  </div>
  <div class="mt-5">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { watch, computed } from "vue";
import Enum from "@/v2/enum/Enum";

import { useStore } from "vuex";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);

const { MeetingType } = Enum;

watch(
  () => route.name,
  (newRouteName) => {
    if (newRouteName === "meeting-admin-meeting") {
      store.commit("adminStore/setSubTab", MeetingType.Meeting);
    } else if (newRouteName === "meeting-admin-presentation-material") {
      store.commit("adminStore/setSubTab", MeetingType.PresentationMaterial);
    }
  },
  { immediate: true }
);
</script>

<style scoped>
:deep(.v-pagination__item--is-active) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  border-radius: 10px;
}
:deep(.v-pagination .v-btn) {
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}
:deep(.v-pagination__item) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__next) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__prev) {
  color: #065695;
  border-radius: 10px;
  background: white;
}

:deep(.v-tab) {
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  padding-right: 0px;
  padding-left: 0px;
  margin-right: 15px;
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
:deep(.v-tab.v-tab--selected) {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

:deep(.v-tab.v-tab) {
  min-width: 0px;
}
</style>
