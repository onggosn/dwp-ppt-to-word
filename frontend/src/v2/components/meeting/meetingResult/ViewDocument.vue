<template>
  <div class="position-relative">
    <!-- Progress Loader Component -->
    <ProgressLoader
      :is-visible="isLoading"
      :progress="loadingProgress"
      :message="loadingMessage"
      :loaded-bytes="loadedBytes"
      :total-bytes="totalBytes"
      :download-start-time="downloadStartTime"
      :status="status"
    />

    <!-- Document Viewer -->
    <div
      ref="viewer"
      class="h-100"
      :class="{ 'viewer-loading': isLoading }"
    ></div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import WebViewer from "@pdftron/webviewer";
import Constants from "@/library/Constants";
import { TMaterialList } from "@/v2/Type";
import { v4 as uuidv4 } from "uuid";
import clientv2 from "@v2/library/ApiClient";
import ProgressLoader from "@v2/components/loading/ProgressLoader.vue";
import { useProgressAnimation } from "@v2/composables/useProgressAnimation";
import { set } from "lodash";

const viewerParams = {
  path: "/lib",
  disabledElements: [
    "toolbarGroup-Shapes",
    "selectToolButton",
    "panToolButton",
    "toolbarGroup-Edit",
    "toolbarGroup-Insert",
    "toolbarGroup-Annotate",
    "toolsHeader",
    "toggleNotesButton",
    "thumbnailControl",
    "downloadButton",
    "outlinesPanelButton",
    "printButton",
    "documentControl",
    "freeTextToolButton",
    "freeHandToolButton",
    "highlightToolButton",
    "stickyToolButton",
    "ribbons",
    "menuButton",
    "signaturePanelButton",
    "contextMenuPopup",
  ],
  loadAsPDF: true,
  fullAPI: true,
  licenseKey: Constants.LICENSE_KEY_PDFTRON,
};

const props = defineProps<{ document: TMaterialList; size: number }>();
const viewer = ref();
// Use progress animation composable
const { loadingProgress, animateProgressTo, stopAnimation } =
  useProgressAnimation();

// Loading state variables
const isLoading = ref(false);
const loadingMessage = ref("Loading...");
const loadedBytes = ref(0);
const totalBytes = ref(0);
const downloadStartTime = ref(0);
const status = ref("success");

async function load() {
  try {
    // Start loading
    isLoading.value = true;
    loadingProgress.value = 0;
    loadingMessage.value = "Initializing viewer";
    loadedBytes.value = 0;
    totalBytes.value = 0;
    downloadStartTime.value = Date.now();

    // Initialize WebViewer
    animateProgressTo(5);
    loadingMessage.value = "Loading document viewer";
    const instance = await WebViewer(viewerParams, viewer.value);

    // Start document download
    animateProgressTo(10);
    loadingMessage.value = "Downloading document";

    setTimeout(() => {
      loadingMessage.value = "Request in progress. Please stay on this page";
    }, 10000);

    const response = await clientv2.viewDocumentResult({
      data: {
        id: props.document.id,
        traceId: uuidv4(),
      },
      onDownloadProgress: (progressEvent) => {
        loadedBytes.value = progressEvent.loaded || 0;

        // Get file size from route query parameter
        const fileSizeFromRoute = props.size ? props.size : null;

        if (progressEvent.lengthComputable && progressEvent.total > 0) {
          totalBytes.value = progressEvent.total;

          // Calculate real percentage based on actual download progress
          const realPercentage = Math.round(
            (progressEvent.loaded / progressEvent.total) * 100
          );
          animateProgressTo(Math.min(realPercentage, 100));

          if (realPercentage < 25) {
            loadingMessage.value = "Starting download";
          } else if (realPercentage < 50) {
            loadingMessage.value = "Downloading document";
          } else if (realPercentage < 75) {
            loadingMessage.value = "Processing content";
          } else if (realPercentage < 95) {
            loadingMessage.value = "Almost complete";
          } else {
            loadingMessage.value = "Finalizing";
          }
        } else if (fileSizeFromRoute && progressEvent.loaded > 0) {
          // Use file size from route if available
          totalBytes.value = fileSizeFromRoute;
          const estimatedPercentage = Math.round(
            (progressEvent.loaded / fileSizeFromRoute) * 100
          );
          animateProgressTo(Math.min(estimatedPercentage, 95));

          loadingMessage.value = "Downloading document";
        } else {
          // Fallback: estimate based on loaded bytes only
          const estimatedProgress = Math.min(
            (progressEvent.loaded / (1024 * 1024)) * 20,
            85
          );
          animateProgressTo(estimatedProgress);
          loadingMessage.value = "Downloading document";
        }
      },
    });

    // Prepare document
    animateProgressTo(98);
    loadingMessage.value = "Preparing document";

    const extension = "pdf";
    await instance.UI.loadDocument(response.data, {
      extension,
    });

    // Complete
    animateProgressTo(100);
    loadingMessage.value = "Complete!";

    // Hide loading after smooth animation completes
    setTimeout(() => {
      stopAnimation();
      isLoading.value = false;
    }, 1200);
  } catch (error: any) {
    stopAnimation();

    // Handle different error statuses
    if (error?.response?.status === 400) {
      loadingMessage.value = "Oops! Sorry, failed to load document";
      animateProgressTo(100);
      isLoading.value = true;
      status.value = "error";
    } else if (error?.response?.status === 404) {
      loadingMessage.value = "Oops! Sorry, document not found";
      animateProgressTo(100);
      isLoading.value = true;
      status.value = "error";
    } else if (error?.response?.status === 500) {
      loadingMessage.value = "Oops! Sorry, server error occurred";
      animateProgressTo(100);
      isLoading.value = true;
      status.value = "error";
    } else {
      loadingMessage.value = "Oops! Sorry, failed to load document";
      animateProgressTo(100);
      isLoading.value = true;
    }
  }
}

onMounted(() => {
  load();
});
</script>
<style scoped>
.p-0 {
  padding: 0;
  min-width: 0 !important;
  height: auto;
}

.small-icon {
  border: 1px solid;
  border-radius: 4px;
  padding: 13px;
}

/* Component Styles */
.position-relative {
  position: relative;
  height: 90vh;
}

.viewer-loading {
  opacity: 0.3;
  pointer-events: none;
  filter: blur(1px);
}
</style>
