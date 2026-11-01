<template>
  <div v-if="!searchMode" class="my-3">
    <v-tabs align-tabs="start" color="#D6212A" class="my-2">
      <v-tab
        :value="ContentType.PredefineContent"
        :to="{ name: 'content-admin-predefine' }"
      >
        Pre-Define Content
      </v-tab>
      <v-tab
        v-if="isOnGoingAccess"
        :value="ContentType.OngoingContent"
        :to="{ name: 'content-admin-ongoing' }"
      >
        On-Going Content
      </v-tab>
    </v-tabs>
  </div>
  <div class="mt-5">
    <router-view />
  </div>
</template>
<script setup lang="ts">
import { watch, computed, onMounted } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import Enum from "@/v2/enum/Enum";

// Make Enum available in template
const { ContentType } = Enum;

const store = useStore();
const route = useRoute();

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);

const isOnGoingAccess = computed(
  () => store.getters["adminStore/getTypeOngoing"]
);

watch(
  () => route.name,
  (newRouteName) => {
    if (newRouteName === "content-admin-predefine") {
      store.commit("adminStore/setSubTab", ContentType.PredefineContent);
    } else if (newRouteName === "content-admin-ongoing") {
      store.commit("adminStore/setSubTab", ContentType.OngoingContent);
    }
  },
  { immediate: true }
);
</script>
<style scoped>
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
</style>
