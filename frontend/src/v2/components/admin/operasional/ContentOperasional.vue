<template>
  <div v-if="!searchMode" class="my-3">
    <v-tabs align-tabs="start" color="#D6212A" class="my-2">
      <v-tab
        :value="OperasionalType.User"
        :to="{ name: 'operasional-admin-user' }"
      >
        User
      </v-tab>
    </v-tabs>
  </div>
  <div class="mt-5">
    <router-view />
  </div>
</template>
<script setup lang="ts">
import { watch, computed } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import Enum from "@/v2/enum/Enum";

// Make Enum available in template
const { OperasionalType } = Enum;

const store = useStore();
const route = useRoute();
const router = useRouter();

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);

// Auto-redirect to user tab if no specific route is matched
watch(
  () => route.name,
  (newRouteName) => {
    if (newRouteName === "operasional-admin-user") {
      store.commit("adminStore/setSubTab", OperasionalType.User);
    } else if (
      newRouteName &&
      String(newRouteName).includes("operasional-admin") &&
      newRouteName !== "operasional-admin-user"
    ) {
      // If user is on the main operasional page without a specific tab, redirect to user tab
      router.push({ name: "operasional-admin-user" });
    }
  },
  { immediate: true }
);
</script>
<style scoped>
:deep(.v-tab) {
  min-width: 0px !important;
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
