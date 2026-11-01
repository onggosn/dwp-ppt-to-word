<template>
  <v-sheet elevation="0" class="mt-2">
    <v-tabs color="primary" v-model="tab">
      <v-tab value="1">Activity & Task</v-tab>
      <v-tab value="2">Document</v-tab>
      <v-tab value="3">Meeting</v-tab>
      <v-tab value="4">Assignment</v-tab>
    </v-tabs>

    <!-- <v-sheet elevation="3" class="pa-5 rounded-lg mt-3"> -->
    <v-window v-model="tab">
      <v-window-item value="1">
        <ActivityTask :id="id" />
      </v-window-item>
      <v-window-item value="2">
        <HistoryDocument :id="id" />
      </v-window-item>
      <v-window-item value="3">
        <Meeting :id="id" />
      </v-window-item>
      <v-window-item value="4">
        <HistoryAssignment :id="id" />
      </v-window-item>
    </v-window>
    <!-- </v-sheet> -->
  </v-sheet>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import ActivityTask from "@/v2/components/history/HistoryActivityAndTask.vue";
import Meeting from "@/v2/components/history/HistoryMeeting.vue";
import HistoryDocument from "@/v2/components/history/HistoryDocument.vue";
import HistoryAssignment from "@v2/components/history/HistoryAssignment.vue";

defineProps<{ id: string }>();

// Reactive data
const tab = ref("1");
</script>

<style scoped>
/* Add any specific styles for this component here */
</style>
