<template>
  <Teleport to="body">
    <v-dialog v-model="isShow" persistent class="dialog-visible" fullscreen>
      <v-card class="content-dialog pb-2">
        <v-toolbar
          class="pa-4 bg-white"
          style="border-bottom: solid 2px #e4e4e4"
        >
          <div class="d-block">
            <v-btn
              variant="outlined"
              size="large"
              icon="mdi-arrow-left"
              class="ml-5 ml-md-0"
              color="#045695"
              style="border: 0.01px solid #d3d3d3; color: white !important"
              elevation="2"
              @click="close"
              ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon>
            </v-btn>
            <span class="view-title ml-3">{{ documentName }} </span>
          </div>
        </v-toolbar>

        <div class="center-div" v-if="loading">
          <v-sheet>
            {{ store.getters["documentStore/getLoadingProgress"] }}
            <br />
            converting your document...

            <v-progress-linear
              class="mt-3"
              color="#045695"
              indeterminate
            ></v-progress-linear>
          </v-sheet>
        </div>

        <div ref="viewer" class="viewer" style="height: 100vh"></div>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import WebViewer from "@pdftron/webviewer";
import Constants from "@/library/Constants";
import { useRoute } from "vue-router";

const route = useRoute();
const isShow = ref(false);
const store = useStore();
const viewer = ref(null);
const loading = ref(false);
const file = ref();
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
const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);

function show() {
  isShow.value = true;

  loading.value = true;
  store
    .dispatch("documentStore/getPDFPreview", route.params.idDoc)
    .then((res) => {
      file.value = getBlobURL(res.data);
    })
    .finally(() => {
      loading.value = false;

      setTimeout(() => {
        WebViewer(viewerParams, viewer.value).then((instance) => {
          const { Core } = instance;
          const { documentViewer } = Core;
          const rotation = instance.Core.PageRotation;
          instance.UI.loadDocument(file.value, {
            extension: "pdf",
            filename: name,
          });

          instance.UI.addEventListener("loaderror", () => {
            undefined;
          });

          documentViewer.addEventListener("documentLoaded", async () => {
            loading.value = false;

            const pageCount = documentViewer.getPageCount();
            const doc = documentViewer.getDocument();
            // for (let i = 1; i <= pageCount; i++) {
            //   await doc.rotatePages([i], rotation.E_90);
            // }
          });
        });
      }, 1000);
    });
}

const getBlobURL = (param) => {
  return window.URL.createObjectURL(new Blob([param]));
};

function close() {
  isShow.value = false;
  const element = document.querySelector(".viewer");
  if (element) {
    element.remove();
  }
}

defineExpose({
  show,
  close,
});
</script>

<style scoped>
.view-title {
  font-family: Poppins;
  font-size: 20px;
  font-weight: 700;
  line-height: 30px;
  color: #3a416f;
  margin-left: 17px;
}
.content-dialog {
  overflow-y: hidden !important;
}
.modal-container {
  margin: auto;
  background: #fff;
  border-radius: 10px;
  position: relative;
  padding-top: 1cm;
  padding-left: 1cm;
  padding-right: 1cm;
  padding-bottom: 1cm;
  width: 21.01cm;
  display: flex;
  flex-direction: column;
  overflow-y: scroll;
  width: 21.01cm;
}
.modal-warning-btn-close {
  position: absolute;
  top: 15px;
  right: 15px;
}

.preview-container {
  overflow-x: scroll;
}

.custom-loader {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 8px solid #0000;
  border-right-color: #766df497;
  position: relative;
  animation: s4 1s infinite linear;
}
.custom-loader:before,
.custom-loader:after {
  content: "";
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: inherit;
  animation: inherit;
  animation-duration: 2s;
}
.custom-loader:after {
  animation-duration: 4s;
}

@keyframes s4 {
  100% {
    transform: rotate(1turn);
  }
}

.center-div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Takes up the full viewport height */
  text-align: center; /* Centers the text inside the div */
}
</style>
