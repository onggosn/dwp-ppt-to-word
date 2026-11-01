<template>
  <v-sheet class="bg-transparent ml-5 px-7 mb-10">
    <v-row no-gutters align="center" class="my-10">
      <v-col>
        <div class="d-flex flex-row align-center">
          <img
            :src="require('@/v2/assets/workspace/profile.svg')"
            width="84"
            height="84"
          />
          <p
            class="ml-7 font-weight-bold"
            style="font-size: 24px !important; color: #4b4b4b !important"
          >
            {{ fullname }}'s Workspace
          </p>
        </div>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-sheet
        class="align-self-center bg-transparent"
        style="margin-left: 14px"
      >
        <v-row class="mb-11">
          <RouterLink
            :to="{ name: 'v2.rdgb' }"
            style="text-decoration: none !important"
          >
            <v-col
              class="card-rdgb d-flex flex-column justify-space-between rounded-lg"
              style="width: 246px; height: 134px; cursor: pointer"
              :class="
                $route.name == 'v2.rdgb' ? 'page-active' : 'page-nonActive'
              "
            >
              <v-sheet
                class="bg-transparent d-flex flex-row align-center justify-space-between"
              >
                <v-sheet class="bg-transparent">
                  <img
                    :src="require('@/v2/assets/workspace/folder.svg')"
                    width="32"
                    height="32"
                    class="bg-transparent"
                  />
                </v-sheet>
                <v-sheet
                  class="font-weight-medium text-10"
                  :class="
                    $route.name == 'v2.rdgb'
                      ? 'workspace-rdgb-active'
                      : 'workspace-rdgb-inactive'
                  "
                  style="padding: 4px 8px"
                  rounded="xl"
                >
                  <template v-if="$store.state.workspaceStore.isLoading">
                    <v-progress-circular
                      class="ml-1"
                      color="#3c8bcb"
                      size="small"
                      indeterminate
                      style="width: 15px"
                    ></v-progress-circular>
                  </template>
                  <template v-else>
                    {{ $store.state.workspaceStore.countRDGB }}</template
                  >
                  Workspace
                </v-sheet>
              </v-sheet>

              <v-sheet class="bg-transparent">
                <p style="color: #3a416f; font-size: 18px; font-weight: 600">
                  RDGB
                </p>
              </v-sheet>
            </v-col>
          </RouterLink>
          <CardRDGM />
          <RouterLink
            :to="{ name: 'v2.rdgtk' }"
            style="text-decoration: none !important"
          >
            <v-col
              class="card-rdgtk d-flex flex-column justify-space-between rounded-lg ml-4 cursor-pointer"
              style="width: 246px; height: 134px; cursor: pointer"
              :class="
                $route.name == 'v2.rdgtk' ? 'page-active' : 'page-nonActive'
              "
            >
              <v-sheet
                class="bg-transparent d-flex flex-row align-center justify-space-between"
              >
                <v-sheet class="bg-transparent">
                  <img
                    :src="require('@/v2/assets/workspace/folder.svg')"
                    width="32"
                    height="32"
                    class="bg-transparent"
                  />
                </v-sheet>
                <v-sheet
                  class="font-weight-medium text-10"
                  :class="
                    $route.name == 'v2.rdgtk'
                      ? 'workspace-rdgtk-active'
                      : 'workspace-rdgtk-inactive'
                  "
                  style="padding: 4px 8px; text-decoration: none"
                  rounded="xl"
                >
                  <template v-if="$store.state.workspaceStore.isLoading">
                    <v-progress-circular
                      class="ml-1"
                      color="#3c8bcb"
                      size="small"
                      indeterminate
                      style="width: 15px"
                    ></v-progress-circular>
                  </template>
                  <template v-else>
                    {{ $store.state.workspaceStore.countRDGTK }}</template
                  >
                  Workspace
                </v-sheet>
              </v-sheet>

              <v-sheet class="bg-transparent">
                <p style="color: #3a416f; font-size: 18px; font-weight: 600">
                  RDGTK
                </p>
              </v-sheet>
            </v-col>
          </RouterLink>
        </v-row>
      </v-sheet>
    </v-row>
    <RouterView></RouterView>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { useStore } from "vuex";
import CardRDGM from "@omPro/components/workspace/CardRDGM.vue";

const store = useStore();
const fullname = ref<string>(store.state.fullname);

onBeforeMount(() => {
  store.dispatch("workspaceStore/fetchCounterByRDGType");
});
</script>

<style scoped>
.workspace-rdgb-active,
.workspace-rdgtk-active {
  background-color: #6eb3ea;
  color: white;
}
.workspace-rdgb-inactive,
.workspace-rdgtk-inactive {
  background-color: #e9f5ff;
  color: #2279bd;
}

.page-active {
  border-radius: 12px;
  border: 3px solid var(--Gradient-Blue, #065695);
  background: #e9f5ff;

  /* Drop Shadow White Element */
  box-shadow: 0px 3px 7px 0px rgba(133, 133, 133, 0.25);
}
.page-nonActive {
  border-radius: 12px;
  background: #fff;

  /* Drop Shadow White Element */
  box-shadow: 0px 3px 7px 0px rgba(133, 133, 133, 0.25);
}
</style>
