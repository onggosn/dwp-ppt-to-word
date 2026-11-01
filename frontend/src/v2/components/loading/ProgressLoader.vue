<template>
  <div
    v-if="isVisible"
    class="loading-overlay d-flex flex-column justify-center align-center"
  >
    <!-- Main Progress Circle with Glow Effect -->
    <div class="progress-container mb-6">
      <v-progress-circular
        :model-value="progress"
        :rotate="360"
        :size="size"
        :width="strokeWidth"
        :color="color"
        :class="['progress-main', status === 'error' ? 'text-danger' : '']"
      >
        <div class="progress-content text-center">
          <div
            :class="[
              'progress-percentage',
              status === 'error' ? 'text-danger' : '',
            ]"
          >
            {{ Math.round(progress) }}%
          </div>
          <div
            :class="['progress-label', status === 'error' ? 'text-danger' : '']"
          >
            {{ status === "error" ? "FINISH" : label }}
          </div>
        </div>
      </v-progress-circular>

      <!-- Outer Ring Animation -->
      <div
        :class="[
          'progress-outer-ring',
          status === 'error' ? 'outer-danger' : '',
        ]"
        :style="{
          width: `${size + 20}px`,
          height: `${size + 20}px`,
          top: '-10px',
          left: '-10px',
        }"
      ></div>
    </div>

    <!-- Loading Message with Fade Animation -->
    <div class="loading-message-container mb-4">
      <div class="loading-dots">
        <span
          :class="[
            'loading-title',
            'mr-2',
            status === 'error' ? 'text-danger' : '',
          ]"
          >{{ message }}</span
        >
        <span :class="['dot', 'dot-1', status === 'error' ? 'text-danger' : '']"
          >●</span
        >
        <span :class="['dot', 'dot-2', status === 'error' ? 'text-danger' : '']"
          >●</span
        >
        <span :class="['dot', 'dot-3', status === 'error' ? 'text-danger' : '']"
          >●</span
        >
      </div>
    </div>

    <!-- File Info Cards -->
    <div
      v-if="showInfoCards && (formattedBytes || downloadSpeed)"
      class="info-cards"
    >
      <div v-if="formattedBytes" class="info-card">
        <div class="info-icon">📊</div>
        <div class="info-text">{{ formattedBytes }}</div>
      </div>

      <div v-if="downloadSpeed" class="info-card">
        <div class="info-icon">⚡</div>
        <div class="info-text">{{ downloadSpeed }}</div>
      </div>
    </div>

    <!-- Custom Slot for Additional Content -->
    <slot name="additional-info"></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  isVisible: boolean;
  progress: number;
  message: string;
  label?: string;
  size?: number;
  strokeWidth?: number;
  color?: string;
  showInfoCards?: boolean;
  loadedBytes?: number;
  totalBytes?: number;
  downloadStartTime?: number;
  status?: string;
}

const props = withDefaults(defineProps<Props>(), {
  label: "Loading",
  size: 120,
  strokeWidth: 8,
  color: "#065695",
  showInfoCards: true,
  loadedBytes: 0,
  totalBytes: 0,
  downloadStartTime: 0,
  status: "success",
});

// Helper function to format bytes
const formatBytes = (bytes: number, decimals = 2) => {
  if (!+bytes) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};

// Computed properties
const formattedBytes = computed(() => {
  if (props.totalBytes > 0) {
    return `${formatBytes(props.loadedBytes)} / ${formatBytes(
      props.totalBytes
    )}`;
  }
  return props.loadedBytes > 0 ? formatBytes(props.loadedBytes) : "";
});

const downloadSpeed = computed(() => {
  if (!props.downloadStartTime) return "";

  const elapsed = (Date.now() - props.downloadStartTime) / 1000;
  if (elapsed > 0 && props.loadedBytes > 0) {
    const bytesPerSecond = props.loadedBytes / elapsed;
    return `${formatBytes(bytesPerSecond)}/s`;
  }
  return "";
});
</script>

<style scoped>
/* Fresh Loading Interface Styles */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(25, 118, 210, 0.05) 0%,
    rgba(156, 39, 176, 0.05) 100%
  );
  backdrop-filter: blur(10px);
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Main Progress Container */
.progress-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-main {
  filter: drop-shadow(0 8px 32px rgba(25, 118, 210, 0.3));
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.progress-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.progress-percentage {
  font-size: 24px;
  font-weight: 700;
  color: #065695;
  line-height: 1;
}

.progress-label {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Outer Ring Animation */
.progress-outer-ring {
  position: absolute;
  border: 2px solid transparent;
  border-top: 2px solid rgba(25, 118, 210, 0.3);
  border-radius: 50%;
  animation: rotate 3s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Loading Message */
.loading-message-container {
  text-align: center;
  max-width: 500px;
}

.loading-title {
  font-size: 18px;
  font-weight: 600;
  color: #065695;
  margin: 0 0 8px 0;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animated Dots */
.loading-dots {
  display: flex;
  justify-content: center;
  gap: 4px;
  align-items: center;
}

.dot {
  font-size: 8px;
  color: #065695;
  animation: bounce 1.4s ease-in-out infinite both;
}

.dot-1 {
  animation-delay: -0.32s;
}
.dot-2 {
  animation-delay: -0.16s;
}
.dot-3 {
  animation-delay: 0s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Info Cards */
.info-cards {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.info-icon {
  font-size: 16px;
}

.info-text {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}
.text-danger {
  color: #b51532 !important;
}
.outer-danger {
  border-top: 2px solid rgba(196, 28, 62, 0.3) !important;
}
</style>
