<template>
  <div v-if="isLoading">
    <rdgm-item
      v-for="i in 10"
      :key="i"
      class="mt-3 mb-5"
      :is-loading="isLoading"
      :delay="`${(i - 1) * 0.08}s`"
    ></rdgm-item>
  </div>
  <div v-else>
    <rdgm-item
      v-for="(item, idx) in items"
      :key="idx"
      class="mt-3 mb-5"
      :item="item"
      :delay="`${idx * 0.08}s`"
    ></rdgm-item>
  </div>
</template>

<script setup lang="ts">
import type { TWorkspaceRDGL } from "@/v2/Type";
import RdgmItem from "./RDGMItem.vue";

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

<style scoped>
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 18px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
