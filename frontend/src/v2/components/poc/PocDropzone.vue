<template>
  <!-- POC: drag and drop / browse for one file (.pptx or .pdf) -->
  <input
    ref="input"
    type="file"
    class="d-none"
    :accept="accept"
    @change="onPick"
  />
  <div
    class="dropzone d-flex flex-column align-center justify-center"
    :class="{ dragging }"
    @dragover.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="onDrop"
  >
    <template v-if="!modelValue">
      <v-icon size="56" color="#267dc2">mdi-file-upload-outline</v-icon>
      <p class="text-13 fw-500 mt-2 mb-0" style="color: #4b4b4b">
        Drag and Drop or
        <span class="browse" @click="input?.click()">Browse Files</span>
      </p>
      <p class="text-12 mt-1 mb-0" style="color: #9e9e9e">{{ hint }}</p>
    </template>
    <template v-else>
      <v-btn
        v-if="clearable"
        icon="mdi-close"
        size="x-small"
        variant="text"
        class="clear"
        @click="emit('update:modelValue', null)"
      />
      <FileBadge :ext="ext" size="large" />
      <p
        class="text-13 fw-500 mt-3 mb-0 text-center px-4"
        style="color: #4b4b4b"
      >
        {{ modelValue.name }}
      </p>
      <p class="text-12 mt-1 mb-0" style="color: #9e9e9e">
        {{ formatSize(modelValue.size) }}
      </p>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import FileBadge from "./FileBadge.vue";
import { formatSize } from "@/v2/poc/format";

const props = withDefaults(
  defineProps<{
    modelValue: File | null;
    accept?: string;
    hint?: string;
    clearable?: boolean;
  }>(),
  {
    accept: ".pptx",
    hint: "Please upload a .pptx only, max 150MB",
    clearable: true,
  }
);
const emit = defineEmits<{
  (e: "update:modelValue", file: File | null): void;
}>();

const input = ref<HTMLInputElement>();
const dragging = ref(false);
const ext = computed(
  () => props.modelValue?.name.split(".").pop()?.toLowerCase() || ""
);

function onPick(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0];
  if (f) emit("update:modelValue", f);
  (e.target as HTMLInputElement).value = "";
}

function onDrop(e: DragEvent) {
  dragging.value = false;
  const f = e.dataTransfer?.files?.[0];
  if (f) emit("update:modelValue", f);
}
</script>

<style scoped>
.dropzone {
  position: relative;
  border: 1.5px dashed #267dc2;
  border-radius: 10px;
  min-height: 190px;
  padding: 24px 12px;
  background: #fff;
  transition: background 0.15s;
}
.dropzone.dragging {
  background: #eef6fd;
}
.browse {
  color: #065695;
  font-weight: 600;
  cursor: pointer;
}
.clear {
  position: absolute;
  top: 8px;
  right: 8px;
}
</style>
