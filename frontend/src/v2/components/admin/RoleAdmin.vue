<template>
  <div v-if="!searchMode" class="my-3">
    <v-tabs align-tabs="start" color="#D6212A">
      <!-- <v-tab :value="RoleType.Role" :to="{ name: 'role-admin-role' }">
        Role
      </v-tab> -->
      <v-tab :value="RoleType.User" :to="{ name: 'role-admin-user' }">
        User
      </v-tab>
      <v-tab
        v-if="isAdgAccess"
        :value="RoleType.Adg"
        :to="{ name: 'role-admin-adg' }"
      >
        ADG
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

const isAdgAccess = computed(() => store.getters["adminStore/getAdgAccess"]);

const { RoleType } = Enum;

watch(
  () => route.name,
  (newRouteName) => {
    if (newRouteName === "role-admin-role") {
      store.commit("adminStore/setSubTab", RoleType.Role);
    } else if (newRouteName === "role-admin-user") {
      store.commit("adminStore/setSubTab", RoleType.User);
    } else if (newRouteName === "role-admin-adg") {
      store.commit("adminStore/setSubTab", RoleType.Adg);
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
