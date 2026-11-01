<template>
  <v-dialog v-model="dialog" width="400" persistent>
    <v-card class="rounded-xl pa-0 overflow-hidden" elevation="24">
      <!-- Header with Gradient -->
      <div
        class="header-gradient pa-6 d-flex flex-column align-center text-white relative"
      >
        <v-btn
          icon="mdi-close"
          variant="text"
          density="comfortable"
          class="btn-close"
          @click="close"
        />
        <div class="icon-container mb-4">
          <div class="icon-glow"></div>
          <img
            v-if="iconName && !imageError"
            :src="iconSrc"
            class="preview-icon-img"
            @error="handleImageError"
          />
          <v-icon v-else size="64" color="white">mdi-file-image</v-icon>
        </div>
        <h3 class="text-h6 font-weight-bold mb-1">Icon Preview</h3>
        <p class="text-caption opacity-80">
          {{ iconName || "No icon selected" }}
        </p>
      </div>

      <v-card-text class="pa-6 bg-preview">
        <p class="text-subtitle-2 font-weight-bold mb-4 text-grey-darken-2">
          How it looks on topic list:
        </p>

        <!-- Mockup of a list item -->
        <div class="mockup-item pa-4 d-flex align-center">
          <div class="mockup-icon-wrapper mr-4">
            <img
              v-if="iconName && !imageError"
              :src="getIconUrl(iconName)"
              style="width: 28px; height: 28px; object-fit: contain"
            />
            <v-icon v-else color="#065695" size="28">mdi-file-image</v-icon>
          </div>
          <div class="flex-grow-1">
            <div class="mockup-text-bold">{{ topicName || "Topic Name" }}</div>
            <!-- <div class="mockup-text-small">Description about this topic...</div> -->
          </div>
          <!-- <v-icon color="#BDBDBD">mdi-chevron-right</v-icon> -->
        </div>

        <div class="mt-8 d-flex justify-center">
          <v-btn
            class="btn-done px-10"
            height="44"
            variant="flat"
            @click="close"
          >
            Close Preview
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  iconName: {
    type: String,
    default: "",
  },
  iconSrc: {
    type: String,
    default: "",
  },
  topicName: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue"]);

const dialog = ref(false);
const imageError = ref(false);

watch(
  () => props.modelValue,
  (val) => {
    dialog.value = val;
    if (val) imageError.value = false;
  }
);

watch(dialog, (val) => {
  emit("update:modelValue", val);
});

function close() {
  dialog.value = false;
}

function getIconUrl(name: string) {
  if (props.iconSrc) return props.iconSrc;
  if (!name) return "";
  // If it's already a full URL
  if (name.startsWith("http")) return name;
  // Try to load from assets if it's a known icon name or just return it as a path
  // Since we don't know the exact base path for backend icons, we use the environment variable
  const base = process.env.VUE_APP_ENDPOINT_OSS || "";
  return `${base}/faq/${name}`;
}

function handleImageError() {
  imageError.value = true;
}
</script>

<style scoped>
.header-gradient {
  background: linear-gradient(135deg, #065695 0%, #267dc2 100%);
  position: relative;
}

.btn-close {
  position: absolute;
  right: 12px;
  top: 12px;
  color: rgba(255, 255, 255, 0.7);
}

.icon-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
}

.icon-glow {
  position: absolute;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  filter: blur(20px);
  border-radius: 50%;
}

.preview-icon-img {
  width: 64px;
  height: 64px;
  object-fit: contain;
  z-index: 1;
}

.bg-preview {
  background-color: #f8fafc;
}

.mockup-item {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #eef2f6;
}

.mockup-icon-wrapper {
  width: 48px;
  height: 48px;
  background-color: #f0f7ff;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mockup-text-bold {
  font-weight: 700;
  font-size: 15px;
  color: #1a202c;
  line-height: 1.2;
}

.mockup-text-small {
  font-size: 12px;
  color: #718096;
  margin-top: 2px;
}

.btn-done {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 12px !important;
  color: white !important;
  font-weight: 700;
  text-transform: none;
  letter-spacing: 0.5px;
}

.opacity-80 {
  opacity: 0.8;
}
</style>
