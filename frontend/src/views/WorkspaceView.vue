<script setup lang="ts">
import { defineComponent, ref } from "vue";
import WorkspaceCard from "@/components/workspace/WorkspaceCard.vue";

defineComponent({ WorkspaceCard });
const workspaceLevel = ref<number>(1);
const inProgress = 1;
const notStarted = 2;
const past = 3;
const changeLevel = (level) => (workspaceLevel.value = level);
</script>

<template>
  <div class="ml-10 mt-10" v-if="$route.name == 'workspace-management'">
    <v-sheet class="d-flex bg-transparent">
      <v-sheet class="me-auto bg-transparent">
        <v-list-item>
          <p
            class="text-h6 font-weight-medium text-blue-theme ml-0 d-none d-md-flex"
            style="font-size: 16px; color: #4b4b4b"
          >
            {{ $store.state.fullname }}'s Workspace
          </p>
          <template v-slot:prepend>
            <img
              class="ml-n5"
              src="/images/account_icon.svg"
              style="width: 10vw; height: 10vh"
            />
          </template>
        </v-list-item>
      </v-sheet>
      <v-sheet class="align-self-center bg-transparent"
        ><v-btn
          rounded="lg"
          elevation="3"
          min-width="140"
          class="text-13"
          :class="workspaceLevel == 1 ? 'btn-active' : 'btn-nonActive'"
          @click="changeLevel(1)"
        >
          LEVEL BI WIDE
        </v-btn></v-sheet
      >
      <v-sheet class="align-self-center mr-10"
        ><v-btn
          class="ml-4 mr-4 text-13"
          rounded="lg"
          elevation="3"
          variant="flat"
          min-width="140"
          :class="workspaceLevel == 2 ? 'btn-active' : 'btn-nonActive'"
          @click="changeLevel(2)"
        >
          LEVEL SATKER
        </v-btn></v-sheet
      >
    </v-sheet>

    <div class="d-block pa-2 mt-0 mb-0"></div>
    <workspace-card
      :workspaceLevel="workspaceLevel"
      :type="inProgress"
      :key="workspaceLevel"
    >
      <template #title>
        <p class="font-weight-bold ml-md-7 mb-2 mt-2">Workspace In Progress</p>
      </template>
    </workspace-card>
    <workspace-card
      :workspaceLevel="workspaceLevel"
      :type="notStarted"
      :key="workspaceLevel"
    >
      <template #title>
        <p class="font-weight-bold ml-md-7 mb-4 mt-4">Not Started Workspace</p>
      </template>
    </workspace-card>
    <workspace-card
      :workspaceLevel="workspaceLevel"
      :type="past"
      :key="workspaceLevel"
    >
      <template #title>
        <p class="font-weight-bold ml-md-7 mb-4 mt-4">Past Workspace</p>
      </template>
    </workspace-card>
  </div>
  <router-view v-else />
</template>

<style scoped>
.btn-active {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: #fff !important;
  font-weight: 700;
}

.btn-nonActive {
  background: white;
  color: red !important;
  font-weight: 700;
}
</style>
