<template>
  <v-card
    elevation="0"
    style="
      border-radius: 10px;
      padding: 30px 0;
      border: 2px dashed #065695;
      text-align: -webkit-center;
    "
    @drop="drop"
  >
    <v-sheet align="center" justify="center" v-if="!selectedFile">
      <img src="/images/icon/paper-upload.svg" style="width: 85px" />
      <p
        style="word-spacing: 0.15rem; margin-bottom: 5px !important"
        class="font-weight-bold"
      >
        <span style="color: #3a416f"> Drag and Drop a image or </span>
        <span style="color: #065391; cursor: pointer" @click="handleFileImport">
          Browse Files
        </span>
      </p>
      <span
        style="
          font-weight: 400;
          font-size: 14px;
          line-height: 21px;
          color: #a6abc7;
        "
        >Please upload a PNG file with a 2:1 aspect ratio and a maximum file
        size of 5 MB</span
      >
      <template>
        <input
          type="file"
          accept="image/png"
          class="d-none"
          id="uploaderButton"
          ref="fileInput"
          @change="onFileChanged"
        />
      </template>
    </v-sheet>
    <v-sheet v-else>
      <v-btn
        class="text-red remove-btn"
        icon="mdi-delete"
        density="comfortable"
        rounded="lg"
        @click="removeImage"
      ></v-btn>
      <img
        class="image-highlight"
        :src="selectedFile"
        style="border-radius: 5px"
      />
    </v-sheet>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from "vue";

const fileInput = ref<HTMLInputElement | null>(null);

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps<{
  modelValue?: string | null;
  fileName?: string | null;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", v: string | null): void;
  (e: "update:fileName", v: string | null): void;
}>();

const isDragging = ref<boolean>(false);

const selectedFile = ref<string | null>(null);
const file = ref<File | null>(null);
const base64 = ref<string | null>(null);
const filename = ref<string | null>(null);

const fileToBase64 = (file: File): Promise<string> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });

async function setFile(f: File) {
  if (f.type !== "image/png") {
    alert("PNG File Only!");
    return;
  }

  file.value = f;
  filename.value = f.name;
  selectedFile.value = URL.createObjectURL(f);
  base64.value = (await fileToBase64(f)).split(",")[1] ?? null;

  emit("update:modelValue", base64.value);
  emit("update:fileName", filename.value);
}

function drop(e: DragEvent) {
  e.preventDefault();
  const f = e.dataTransfer?.files?.[0];
  if (!f) return;

  setFile(f);
  isDragging.value = false;
}

function handleFileImport() {
  fileInput.value?.click();
}

function onFileChanged(e: Event) {
  const input = e.target as HTMLInputElement;
  const f = input.files?.[0];
  if (!f) return;
  setFile(f);
  input.value = "";
}

function removeImage() {
  if (selectedFile.value) URL.revokeObjectURL(selectedFile.value);
  selectedFile.value = null;
  file.value = null;
  base64.value = null;

  emit("update:modelValue", null);
  emit("update:fileName", null);
}
</script>

<style scoped>
.remove-btn {
  position: absolute;
  top: 12px;
  right: 3px;
}

.image-highlight {
  max-width: 200px;
}
</style>
