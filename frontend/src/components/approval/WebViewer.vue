<template>
  <div>
    <!-- {{ document }} -->
    <div ref="viewer" class="pa-5"></div>
    <div v-if="isLoading">
      <template v-if="document.sizeDocument">
        <v-progress-circular
          style="margin-top: 240px"
          :rotate="360"
          :size="70"
          :width="8"
          :indeterminate="bandwithSpend == 0"
          :model-value="bandwithSpend"
          color="#065695"
        >
          <p class="font-weight-bold">{{ bandwithSpend }}%</p>
        </v-progress-circular>
        <p class="mt-5">Please Wait ...</p>
        <p
          style="font-size: 22px; font-weight: 600; color: gray"
          v-if="bandwithSpend == 0"
        >
          Waiting for server respond
        </p>
      </template>
      <template v-else>
        <div
          class="custom-loader"
          style="margin-top: 240px; display: inline-block"
        ></div>
        <p class="mt-5">Please Wait ...</p>
        <p
          style="font-size: 22px; font-weight: 600; color: gray"
          v-if="bandwithSpend == 0"
        >
          Waiting for server respond
        </p>
        <p style="font-size: 22px; font-weight: 600; color: gray" v-else>
          {{ bandwithSpend }}
        </p>
      </template>
    </div>
    <div v-if="isFailed" id="pdf-error" style="margin: auto; width: 50%">
      <img
        src="/images/no_document_preview.png"
        style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
      />
      <div style="display: block; margin: 0 auto">
        <h4
          style="
            text-align: center;
            font-style: italic;
            font-weight: 800;
            color: #797979;
          "
        >
          Whoops!
        </h4>
        <h5
          style="
            text-align: center;
            font-style: italic;
            font-size: 15px;
            color: #797979 !important;
          "
        >
          There was a problem previewing this document...
        </h5>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, defineProps, ref, defineEmits } from "vue";
import client from "@/library/ApiClient";
import WebViewer from "@pdftron/webviewer";
import Constants from "@/library/Constants";
import { v4 as uuidv4 } from "uuid";
import store from "@/store/index";
import { useRoute } from "vue-router";
import { consoleTable, consoleLog, insertLog } from "@/models/log";

const props = defineProps({ document: Object });
const route = useRoute();
const bandwithSpend = ref(0);
const isLoading = ref(false);
const isFailed = ref(false);
const viewer = ref();
// const fileSize = ref(0);
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

const emits = defineEmits(["onSuccess"]);

let traceId = "";
let timeStart = 0;
let timeEnd = 0;
let timeStartRender = 0;
let timeEndRender = 0;
let fileSize = 0;

onMounted(() => fetchData());

const fetchData = () => {
  isLoading.value = true;
  viewer.value.style.display = "none";
  timeStart = performance.now();
  traceId = uuidv4();

  client
    .previewDocumentUtama({
      store: store,
      data: {
        id: route.params.documentId,
        formatBase64: true,
        traceId: "",
      },
      onDownloadProgress: (progressEvent) => {
        if (props.document?.sizeDocument) {
          if (bandwithSpend.value < 100) {
            bandwithSpend.value = parseInt(
              (progressEvent.loaded / parseInt(props.document.sizeDocument)) *
                100
            );
          }
        } else {
          bandwithSpend.value =
            "Download Progress: " + formatBytes(progressEvent.loaded);
        }

        if (bandwithSpend.value > 100) {
          bandwithSpend.value = 100;
        }

        fileSize = progressEvent.loaded;
      },
    })
    .then((response) => {
      WebViewer(viewerParams, viewer.value).then((instance) => {
        const { Core } = instance;
        const { documentViewer } = Core;

        let url = base64ToBlobURL(response?.data.data);
        let ext = getFileExtension(response?.data.filename);
        let name = props.document?.documentNameDisplay;

        timeStartRender = performance.now();

        consoleTable({
          filename: response?.data.filename,
          load_filename: name,
          extension: ext,
        });

        instance.UI.loadDocument(url, {
          extension: ext,
          filename: name,
        });

        instance.UI.addEventListener("loaderror", () => {
          viewer.value.style.display = "none";
          isFailed.value = true;
          isLoading.value = false;

          timeEnd = performance.now();
          insertLog(
            traceId,
            route.params.documentId,
            name,
            fileSize,
            timeStart,
            timeEnd,
            "DOCUMENT UTAMA PREVIEW FAILED"
          );
        });

        documentViewer.addEventListener("documentLoaded", () => {
          consoleLog("berhasil load");
          emits("onSuccess");
          viewer.value.style.display = "block";
          isLoading.value = false;

          timeEnd = performance.now();
          timeEndRender = performance.now();

          insertLog(
            traceId,
            route.params.documentId,
            name,
            fileSize,
            timeStart,
            timeEnd,
            "DOCUMENT UTAMA PREVIEW"
          );

          insertLog(
            traceId,
            route.params.documentId,
            name,
            fileSize,
            timeStartRender,
            timeEndRender,
            "DOCUMENT UTAMA PREVIEW - RENDER"
          );
        });
      });
    })
    .catch((error) => {
      viewer.value.style.display = "none";
      isFailed.value = true;
    })
    .finally(() => {
      undefined;
      undefined;
    });
};

function getFileExtension(filename: string): string | null {
  const parts = filename?.split(".") ?? ["noname", "pdf"];
  if (parts.length > 1) {
    return parts[parts.length - 1];
  } else {
    return "pdf"; // No file extension found
  }
}

const getBlobURL = (param) => {
  return window.URL.createObjectURL(new Blob([param]));
};

const base64ToBlobURL = (base64) => {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; ++i) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  return getBlobURL(new Blob([bytes], { type: "application/pdf" }));
};

const formatBytes = (bytes, decimals = 2) => {
  if (!+bytes) return "0.00 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};
</script>

<style scoped>
.custom-loader {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: radial-gradient(farthest-side, #065695 94%, #0000) top/8px 8px
      no-repeat,
    conic-gradient(#0000 30%, #065695);
  -webkit-mask: radial-gradient(farthest-side, #0000 calc(100% - 8px), #000 0);
  animation: s3 1s infinite linear;
}

@keyframes s3 {
  100% {
    transform: rotate(1turn);
  }
}
div {
  width: 100%;
  height: 100vh;
}
</style>
