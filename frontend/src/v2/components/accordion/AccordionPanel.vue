<template>
  <v-expansion-panels v-model="panel" class="mb-5">
    <v-expansion-panel :value="items?.idFormasi">
      <v-expansion-panel-title>
        <slot name="title"></slot>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <slot name="body"></slot>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";

const panel = ref<string>();

const props = defineProps<{
  items: {
    idFormasi?: string;
  };
}>();

const emit = defineEmits<{
  (e: "onDroped", value?: string): void;
}>();

watch(panel, (newValue) => {
  if (newValue) {
    emit("onDroped", newValue);
  }
});
</script>
