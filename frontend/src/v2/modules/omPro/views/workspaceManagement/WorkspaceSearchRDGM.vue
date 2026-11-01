<template>
  <v-menu
    transition="slide-y-transition"
    bottom
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        icon=""
        size="small"
        v-bind="props"
        class="ml-2"
        style="position: right; top: 0; margin-right: 8px"
      >
        <img
          :src="require('@/v2/assets/icon/search.png')"
          :width="21"
          :height="21"
        />
      </v-btn>
    </template>
    <v-card min-width="300" class="rounded-lg">
      <v-form ref="form" type="submit" @submit.prevent="searchEvent">
        <v-list>
          <v-list-item>
            <v-text-field
              v-model="keyword"
              hide-details="auto"
              style="border-radius: 10px"
              placeholder="Search"
              variant="outlined"
              clearable
              @click:clear="store.commit('omWorkspaceStore/setSearchRDGM', '')"
              @keyup.enter="searchEvent()"
              :autofocus="true"
            ></v-text-field>
          </v-list-item>
        </v-list>
        <v-list-item>
          <v-list-item-title class="text-right">
            <v-btn
              class="btn-primary blue-gradient text-right mb-2"
              @click="searchEvent"
              >Search</v-btn
            >
          </v-list-item-title>
        </v-list-item>
      </v-form>
    </v-card>
  </v-menu>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const router = useRouter();
const store = useStore();

const keyword = ref<string>(store.getters["omWorkspaceStore/getSearchRDGM"]);
const form = ref<any>();
async function searchEvent() {
  store.commit("omWorkspaceStore/setSearchRDGM", keyword.value);
  router.push({
    name: "om.rdgm-search-result",
  });
}
const searchRDGM = computed(
  () => store.getters["omWorkspaceStore/getSearchRDGM"]
);

watch(searchRDGM, (newVal) => {
  if (newVal === "") {
    store.commit("omWorkspaceStore/setSearchRDGM", "");
    router.push({
      name: "om.workspace-management-rdgm",
    });
  }
});
</script>

<style scoped>
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
</style>
