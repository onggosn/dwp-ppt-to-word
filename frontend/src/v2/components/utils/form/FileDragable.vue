<template>
  <input
    type="file"
    ref="file"
    class="d-none"
    :accept="prop.formatFile.join(', ')"
    @change="onChange"
  />
  <div
    @dragover="dragover"
    @dragleave="dragleave"
    @drop="dropApproval"
    class="mt-2 d-flex justify-center"
    :style="dragableStyle"
  >
    <div v-if="isLoading" class="text-center py-12">
      <v-progress-linear
        :rotate="360"
        :size="100"
        :width="15"
        :model-value="progressLoading"
        :value="progressLoading"
        style="width: 20vw"
        class="mb-0 mt-2 mb-4"
        color="#045695"
      />
      <p class="mt-2 text-13" v-html="progressMessage"></p>
      <p class="text-14 font-weight-bold">progress: {{ progressLoading }}%</p>
    </div>
    <div class="text-center" v-else-if="!modelValue.name">
      <img
        :src="require('@v2/assets/icon/doc_upload.svg')"
        alt=""
        height="100"
      />
      <div class="text-12 fw-500">
        Drag and Drop Here or
        <span style="color: #065391; cursor: pointer" @click="file.click()">
          Browse Here
        </span>
      </div>
      <div class="text-10 fw-400 mt-1">
        Please upload a {{ prop.formatFile.join(", ") }} file with a maximum
        size of {{ prop.maxSizeLabel }}
      </div>
    </div>
    <div v-else>
      <slot name="clear-icon" :clearForm="clearForm">
        <img
          :src="require('@v2/assets/icon/close_red_block.svg')"
          alt=""
          height="20"
          style="position: absolute; right: 35px; cursor: pointer"
          @click="clearForm"
        />
      </slot>
      <div class="text-center">
        <img :src="docIcon" alt="" height="100" />
        <div class="pt-1 text-14 fs-500" v-html="modelValue.name"></div>
        <div class="text-12 fs-400" v-html="modelValue.sizeString"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";
import { ref } from "vue";
import { formatBytes } from "@v2/helpers/utils";
import { TFileDragable } from "@v2/Type.d";
import { computed } from "vue";

const emit = defineEmits(["update:modelValue"]);
const prop = defineProps({
  modelValue: {
    type: Object as PropType<TFileDragable>,
    default: function () {
      return {};
    },
  },
  formatFile: {
    type: Array as PropType<string[]>,
    default: () => ["*/*"],
  },
  loadingPercent: {
    type: Number,
    default: 0,
  },
  isDashedBorder: {
    type: Boolean,
    default: true,
  },
  backgroundColor: {
    type: String,
    default: "#e9f5ff",
  },
  borderColor: {
    type: String,
    default: "#797979",
  },
  maxSizeLabel: {
    type: String,
    default: "150MB",
  },
});

const file = ref();
const isDragging = ref(false);

const progressLoading = computed((): number => {
  if (prop.loadingPercent <= 100) return prop.loadingPercent;
  return 100;
});

const dragableStyle = computed(() => {
  const borderStyle = prop.isDashedBorder ? "dashed" : "solid";
  return {
    border: `2.3px ${borderStyle} ${prop.borderColor}`,
    borderStyle,
    borderRadius: "10px",
    padding: "10px",
    background: prop.backgroundColor,
    position: "relative",
  };
});

const progressMessage = computed((): string => {
  if (progressLoading.value == 100) {
    return "just a bit longer, we're almost there!";
  }
  return "Creating your document, please wait..";
});

const isLoading = computed((): boolean => {
  return prop.loadingPercent > 0;
});

const docIcon = computed((): string => {
  const ext = prop.modelValue?.name.split(".").at(-1);
  if (ext === "pdf") return require("@/v2/assets/icon/docImage/iconPdf.svg");
  else if (ext === "doc" || ext === "docx")
    return require("@/v2/assets/icon/docImage/iconWord.svg");
  else if (ext === "xls" || ext === "xlsx")
    return require("@/v2/assets/icon/docImage/iconExcel.png");
  else if (ext === "ppt" || ext === "pptx")
    return require("@/v2/assets/icon/docImage/iconPpt.svg");
  return require("@/v2/assets/icon/docImage/iconOther.png");
});

function dragover(e: any) {
  e.preventDefault();
  e.stopPropagation();
  isDragging.value = true;
}

function dragleave(e: any) {
  e.preventDefault();
  e.stopPropagation();
  isDragging.value = false;
}

function dropApproval(e: any) {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  const fileType = file.name.split(".");
  const allowedFormats = prop.formatFile;
  if (!allowedFormats.includes(`.${fileType.at(-1)}`)) {
    alert("format file not support");
  }
  emit("update:modelValue", {
    name: file.name,
    sizeString: formatBytes(file.size),
    sizeNumber: file.size,
    file: file,
  });
}

function onChange(e: any) {
  const file = e.target.files[0];
  e.target.value = null;

  emit("update:modelValue", {
    name: file.name,
    sizeString: formatBytes(file.size),
    sizeNumber: file.size,
    file: file,
  });
}

function clearForm() {
  emit("update:modelValue", {
    name: "",
    sizeString: "",
    sizeNumber: 0,
    file: null,
  });
}
</script>
