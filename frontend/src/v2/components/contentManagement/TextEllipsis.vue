<template>
  <div class="ml-4 pb-1">
    <div
      ref="container"
      :style="{
        maxHeight: isOpen ? 'unset' : '3em',
        overflow: 'hidden',
        lineHeight: '1.5em',
      }"
    >
      <p :class="{ ellipsis: !isOpen && isOverflow }">
        <slot />
      </p>
    </div>
    <v-btn
      @click="isOpen = !isOpen"
      size="small"
      density="compact"
      variant="text"
      class="hide-ellipsis pa-0"
      min-width="0"
      v-if="isOverflow"
    >
      {{ isOpen ? "Hide" : "See All" }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const isOpen = ref(false);
const isOverflow = ref(false);
const container = ref(null);

onMounted(() => {
  const ph = container.value.querySelector("p").offsetHeight;
  const divh = container.value.clientHeight;

  if (ph > divh) {
    isOverflow.value = true;
  }
});
</script>

<style scoped lang="scss">
.ellipsis {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hide-ellipsis {
  text-decoration: underline;
  color: #065695;
  text-transform: unset;
  font-style: italic;

  p {
    margin: 0;
    padding: 0;
  }
}
</style>
