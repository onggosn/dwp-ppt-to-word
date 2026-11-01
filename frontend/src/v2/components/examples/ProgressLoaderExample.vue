<!-- Example of how to use the ProgressLoader component in other components -->
<template>
  <div class="example-container">
    <button @click="startDownload" :disabled="isDownloading">
      {{ isDownloading ? "Downloading..." : "Start Download" }}
    </button>

    <!-- Using the ProgressLoader component -->
    <ProgressLoader
      :is-visible="isDownloading"
      :progress="progress"
      :message="message"
      :loaded-bytes="loadedBytes"
      :total-bytes="totalBytes"
      :download-start-time="downloadStartTime"
      :size="100"
      :stroke-width="6"
      color="#4CAF50"
      :show-info-cards="true"
    >
      <!-- Custom content slot -->
      <template #additional-info>
        <div class="custom-info">Custom information can go here</div>
      </template>
    </ProgressLoader>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ProgressLoader from "@v2/components/loading/ProgressLoader.vue";
import { useProgressAnimation } from "@v2/composables/useProgressAnimation";

// Use the composable
const {
  loadingProgress: progress,
  animateProgressTo,
  resetProgress,
} = useProgressAnimation();

// Component state
const isDownloading = ref(false);
const message = ref("Ready to start");
const loadedBytes = ref(0);
const totalBytes = ref(0);
const downloadStartTime = ref(0);

// Example function that simulates a download
const startDownload = () => {
  isDownloading.value = true;
  downloadStartTime.value = Date.now();
  totalBytes.value = 5 * 1024 * 1024; // 5MB example
  loadedBytes.value = 0;

  // Simulate download progress
  const interval = setInterval(() => {
    loadedBytes.value += Math.random() * 100000; // Random progress
    const progressPercentage = (loadedBytes.value / totalBytes.value) * 100;

    animateProgressTo(Math.min(progressPercentage, 100));

    if (progressPercentage < 25) {
      message.value = "Starting download...";
    } else if (progressPercentage < 50) {
      message.value = "Downloading files...";
    } else if (progressPercentage < 75) {
      message.value = "Processing content...";
    } else if (progressPercentage < 95) {
      message.value = "Almost complete...";
    } else {
      message.value = "Finishing up...";
    }

    if (loadedBytes.value >= totalBytes.value) {
      clearInterval(interval);
      animateProgressTo(100);
      message.value = "Complete!";

      // Hide progress after 2 seconds
      setTimeout(() => {
        isDownloading.value = false;
        resetProgress();
        message.value = "Ready to start";
        loadedBytes.value = 0;
        totalBytes.value = 0;
      }, 2000);
    }
  }, 100);
};
</script>

<style scoped>
.example-container {
  position: relative;
  height: 300px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  border-radius: 8px;
}

button {
  padding: 12px 24px;
  background: #2196f3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background 0.3s;
}

button:hover:not(:disabled) {
  background: #1976d2;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.custom-info {
  background: rgba(76, 175, 80, 0.1);
  padding: 8px 16px;
  border-radius: 16px;
  font-size: 14px;
  color: #4caf50;
  font-weight: 500;
}
</style>
