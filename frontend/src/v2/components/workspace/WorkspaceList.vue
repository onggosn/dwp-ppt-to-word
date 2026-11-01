<template>
  <div v-if="isLoading">
    <workspace-item
      v-for="i in 5"
      :key="i"
      class="mt-3 mb-5"
      :is-loading="isLoading"
      :delay="`${(i - 1) * 0.08}s`"
    ></workspace-item>
  </div>
  <div v-else>
    <workspace-item
      v-for="(item, idx) in items"
      :key="idx"
      class="mt-3 mb-5"
      :item="item"
      :delay="`${idx * 0.08}s`"
      :type="type"
    ></workspace-item>
  </div>
</template>

<script setup lang="ts">
import type { TWorkspaceRDGL } from "@/v2/Type";
import WorkspaceItem from "./WorkspaceItem.vue";

defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  items: {
    type: Array as () => TWorkspaceRDGL[],
    default: () => [],
  },
  type: {
    type: String,
    default: "rdgb",
  },
});
</script>

<style scoped>
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
