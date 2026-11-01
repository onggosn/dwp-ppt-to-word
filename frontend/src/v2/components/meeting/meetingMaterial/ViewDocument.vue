<template>
  <div class="position-relative">
    <ProgressLoader
      :is-visible="isLoading"
      :progress="loadingProgress"
      :message="loadingMessage"
      :loaded-bytes="loadedBytes"
      :total-bytes="totalBytes"
      :download-start-time="downloadStartTime"
      :status="status"
    />

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
import { TMaterialPreview } from "@/v2/Type";
import { v4 as uuidv4 } from "uuid";
import clientv2 from "@v2/library/ApiClient";
import { useRoute } from "vue-router";
import ProgressLoader from "@v2/components/loading/ProgressLoader.vue";
import { useProgressAnimation } from "@v2/composables/useProgressAnimation";
import { useRequestCancellation } from "@v2/composables/useRequestCancellation";

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

const props = defineProps<{
  document?: TMaterialPreview;
  type?: string;
  size?: string | number;
}>();
const viewer = ref();
const route = useRoute();

const { loadingProgress, animateProgressTo, stopAnimation } =
  useProgressAnimation();
const { getRequestSignal, isRequestCanceled, cleanupRequest } =
  useRequestCancellation();

const isLoading = ref(false);
const loadingMessage = ref("Loading...");
const loadedBytes = ref(0);
const totalBytes = ref(0);
const downloadStartTime = ref(0);
const status = ref("success");
type DocumentType = "material" | "result" | "finalisasi";

function getProgressMessage(percentage: number): any {
  if (percentage < 25) {
    return "Starting download";
  } else if (percentage < 50) {
    return "Downloading document";
  } else if (percentage < 75) {
    return "Processing content";
  } else if (percentage < 95) {
    return "Almost complete";
  } else {
    return "Finalizing";
  }
}

function handleDownloadProgress(progressEvent: any) {
  loadedBytes.value = progressEvent.loaded || 0;
  const maxFileSize = props.type === "material" ? route.query.size : props.size;
  const fileSizeFromRoute = maxFileSize
    ? parseInt(maxFileSize as string)
    : null;

  if (fileSizeFromRoute && progressEvent.loaded > 0) {
    totalBytes.value = fileSizeFromRoute;
    const estimatedPercentage = Math.round(
      (progressEvent.loaded / fileSizeFromRoute) * 100
    );
    animateProgressTo(Math.min(estimatedPercentage, 95));
    loadingMessage.value = getProgressMessage(estimatedPercentage);
  }
}

async function initializeViewer(): Promise<any> {
  animateProgressTo(5);
  loadingMessage.value = "Loading document viewer";
  return await WebViewer(viewerParams, viewer.value);
}

function setupLoadingState() {
  isLoading.value = true;
  loadingProgress.value = 0;
  loadingMessage.value = "Initializing viewer";
  loadedBytes.value = 0;
  totalBytes.value = 0;
  downloadStartTime.value = Date.now();
}

function completeLoading(endpoint: string) {
  setTimeout(() => {
    stopAnimation();
    isLoading.value = false;
  }, 1200);
  cleanupRequest(endpoint);
}

function handleError(error: any, endpoint: string) {
  stopAnimation();

  if (isRequestCanceled(error)) {
    isLoading.value = false;
    return;
  }

  cleanupRequest(endpoint);

  const statusCode = error?.response?.status;

  if (statusCode === 400) {
    loadingMessage.value = "Oops! Sorry, failed to load document";
    animateProgressTo(100);
    isLoading.value = true;
    status.value = "error";
  } else if (statusCode === 404) {
    loadingMessage.value = "Oops! Sorry, document not found";
    animateProgressTo(100);
    isLoading.value = true;
    status.value = "error";
  } else if (statusCode === 500) {
    loadingMessage.value = "Oops! Sorry, server error occurred";
    animateProgressTo(100);
    isLoading.value = true;
    status.value = "error";
  } else {
    loadingMessage.value = "Oops! Sorry, failed to load document";
    animateProgressTo(100);
    isLoading.value = true;
    status.value = "error";
  }
}

function getEndpoint(documentType: DocumentType): string {
  if (documentType === "finalisasi") {
    return `/BPDocument/ViewContentFinalisasi_${route.params.idDoc}`;
  }

  if (documentType === "result") {
    return `/Event/PreviewHasilPembahasan_${props.document?.id}`;
  }

  return `/Event/PreviewMaterial_${props.document?.id}`;
}

function scheduleLoadingMessageUpdates() {
  const timerIds: Array<ReturnType<typeof setTimeout>> = [];

  timerIds.push(
    setTimeout(() => {
      if (loadedBytes.value === 0) {
        loadingMessage.value = "Request in progress. Please stay on this page";
      }
    }, 10000)
  );

  timerIds.push(
    setTimeout(() => {
      if (loadedBytes.value === 0) {
        loadingMessage.value =
          "The server is currently busy. We appreciate your patience, please keep this tab open.";
      }
    }, 60000)
  );

  return () => {
    timerIds.forEach((id) => clearTimeout(id));
  };
}

async function requestDocument(
  documentType: DocumentType,
  signal: AbortSignal
): Promise<any> {
  const onDownloadProgress = (progressEvent: any) =>
    handleDownloadProgress(progressEvent);

  if (documentType === "result") {
    return await clientv2.viewDocumentResult({
      data: { id: props.document?.id, traceId: uuidv4() },
      signal,
      onDownloadProgress,
    });
  }

  if (documentType === "finalisasi") {
    return await clientv2.viewFinalisasiDocument({
      data: { idBpdoc: route.params.idDoc },
      signal,
      onDownloadProgress,
    });
  }

  return await clientv2.viewMeetingDocument({
    data: { id: route.params.idMaterial },
    signal,
    onDownloadProgress,
  });
}

function getDocumentExtension() {
  return process.env.VUE_APP_MIDDLEWARE_NEW_PATH ===
    "https://devdigiworkplacemwsos.corp.bi.go.id"
    ? props.document?.docExt.split(".")[1]
    : "pdf";
}

async function viewDocument(documentType: DocumentType) {
  const endpoint = getEndpoint(documentType);
  let clearLoadingMessageTimers: (() => void) | null = null;

  try {
    setupLoadingState();
    const instance = await initializeViewer();

    animateProgressTo(10);
    loadingMessage.value = "Preparing your view";
    clearLoadingMessageTimers = scheduleLoadingMessageUpdates();

    const signal = getRequestSignal(endpoint);

    const response = await requestDocument(documentType, signal);
    const extension = getDocumentExtension();

    await instance.UI.loadDocument(response.data, { extension });
    completeLoading(endpoint);
  } catch (error: any) {
    handleError(error, endpoint);
  } finally {
    clearLoadingMessageTimers?.();
  }
}

async function viewMaterial() {
  await viewDocument("material");
}

async function viewResult() {
  await viewDocument("result");
}

async function viewFinalisasi() {
  await viewDocument("finalisasi");
}

onMounted(() => {
  if (props.type === "material") viewMaterial();
  if (props.type === "result") viewResult();
  if (props.type === "finalisasi") viewFinalisasi();
});
</script>
<style scoped>
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
