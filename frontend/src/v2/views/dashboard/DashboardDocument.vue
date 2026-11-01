<template>
  <div v-if="!searchMode" class="my-3">
    <v-tabs align-tabs="left" color="#D6212A" class="my-2 mx-2">
      <v-tab
        :value="DocumentDashboardType.Materi"
        :to="{ name: 'dashboard.document.v2.materi' }"
      >
        Materi Pembahasan
      </v-tab>
      <v-tab
        :value="DocumentDashboardType.Hasil"
        :to="{ name: 'dashboard.document.v2.hasil' }"
      >
        Hasil Pembahasan
      </v-tab>
    </v-tabs>
  </div>
  <div class="mt-5">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { DocumentDashboardType } from "@/v2/enum/Search";
import { useStore } from "vuex";

const store = useStore();

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
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
  line-height: 24px;
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
