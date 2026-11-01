<template>
  <div>
    <div class="line" />

    <div class="info my-4">
      <div class="item-label">Workspace type</div>
      <div class="item-information mt-2">RDG Bulanan</div>

      <div class="item-label mt-2">Description</div>
      <div class="item-information mt-2">Lorem Ipsum</div>

      <div class="item-label mt-2">Due Date</div>
      <div class="item-information mt-2">Mon 01/10/2024 - Tue 31/10/2024</div>

      <!-- <div class="dashed-line my-6" />

      <v-tabs v-model="tab" align-tabs="left" color="#D6212A" class="my-2 mx-0">
        <v-tab :value="1">Acivity & Task</v-tab>
        <v-tab :value="2">Document</v-tab>
        <v-tab :value="3">Meeting</v-tab>
        <v-tab :value="4">Assignment</v-tab>
      </v-tabs>

      <div>
        <v-window v-model="tab" class="my-5">
          <v-window-item :value="1"> <activity-task /> </v-window-item>
          <v-window-item :value="2"> Document Content </v-window-item>
          <v-window-item :value="3"> Meeting Content </v-window-item>
          <v-window-item :value="4"> Assignment Content </v-window-item>
        </v-window>
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
// import { ref } from "vue";
// import ActivityTask from "@/v2/components/history/HistoryActivityAndTask.vue";

// const tab = ref("one");
</script>

<style scoped>
.line {
  width: 100%;
  height: 1px;
  background-color: #eeeeee;
}

.item-information {
  color: #4b4b4b;
  font-size: 13px;
  line-height: 19.5px;
}

.item-label {
  color: #a6abc7;
  font-size: 13px;
  line-height: 19.5px;
}

.dashed-line {
  width: 100%;
  height: 1px;
  background-image: repeating-linear-gradient(
    to right,
    #065695,
    #267dc2 10px,
    transparent 10px,
    transparent 20px
  );
}
</style>
