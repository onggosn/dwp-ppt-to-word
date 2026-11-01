<template>
  <RouterLink
    :to="{ name: 'om.workspace-management-rdgm' }"
    style="text-decoration: none !important"
  >
    <v-col
      class="card-rdgtk d-flex flex-column justify-space-between rounded-lg ml-4 cursor-pointer"
      style="width: 246px; height: 134px; cursor: pointer"
      :class="
        $route.name == 'om.workspace-management-rdgm'
          ? 'page-active'
          : 'page-nonActive'
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
            $route.name == 'om.workspace-management-rdgm'
              ? 'workspace-rdgtk-active'
              : 'workspace-rdgtk-inactive'
          "
          style="padding: 4px 8px; text-decoration: none"
          rounded="xl"
        >
          <template v-if="isLoading">
            <v-progress-circular
              class="ml-1"
              color="#3c8bcb"
              size="small"
              indeterminate
              style="width: 15px"
            ></v-progress-circular>
          </template>
          <template v-else>
            {{ countRDGM }}
          </template>
          Workspace
        </v-sheet>
      </v-sheet>

      <v-sheet class="bg-transparent">
        <p style="color: #3a416f; font-size: 18px; font-weight: 600">RDGM</p>
      </v-sheet>
    </v-col>
  </RouterLink>
</template>
<script setup type="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const isLoading = computed(() => store.state.workspaceStore.isLoading);
const countRDGM = computed(() => store.state.workspaceStore.countRDGM);
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
