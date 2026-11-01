<template>
  <div v-if="isLoading">
    <workspace-item
      v-for="i in 5"
      :key="i"
      class="mt-1"
      :is-loading="isLoading"
    ></workspace-item>
  </div>
  <div v-else>
    <workspace-item
      v-for="(item, idx) in items"
      :key="idx"
      class="mt-5"
      :item="item"
    ></workspace-item>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import type { TWorkspaceRDGL } from "@omPro/Type";
import WorkspaceItem from "@omPro/components/workspace/WorkspaceItem.vue";

defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  items: {
    type: Array as () => TWorkspaceRDGL[],
    default: () => [],
  },
});
</script>

<style scoped></style>
