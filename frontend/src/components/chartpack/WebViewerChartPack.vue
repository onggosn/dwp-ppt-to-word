<template>
  <v-row>
    <v-col cols="3" class="ml-1">
      <v-select
        v-model="selectArea"
        :loading="isLoading"
        :items="listArea"
        :disabled="isLoading"
        item-title="name"
        item-value="id"
        variant="solo"
        placeholder="Choose area"
        @update:modelValue="getPeriode"
      ></v-select>
    </v-col>
    <v-col cols="3">
      <v-select
        v-model="selectPeriode"
        :loading="isLoading"
        :items="listPeriode"
        :disabled="isLoading"
        item-title="name"
        item-value="id"
        variant="solo"
        placeholder="Choose periode"
        @update:modelValue="getChartPackSelected"
      ></v-select>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="8" class="text-title-blue">
      <free-style-shimmer
        v-if="isLoading"
        height="40px"
        width="60%"
        border-radius="8px"
        color="#DCDCDC"
        class="ml-0 mt-0"
      />
      <div v-else>
        {{
          this.resultChartPack != null ? this.resultChartPack.documentTitle : ""
        }}
      </div>
    </v-col>
    <v-col cols="4" class="text-right">
      <v-btn
        rounded="pill"
        color="primary"
        prepend-icon="mdi-eye"
        class="btn-primary"
        :disabled="btnDisabled"
        :loading="isLoading"
        @click="openMetada"
        >Metadata</v-btn
      >
      <v-btn
        rounded="pill"
        color="primary"
        prepend-icon="mdi-cloud-download"
        class="ml-2 btn-primary"
        :disabled="btnDisabled"
        :loading="isLoading"
        @click="download"
        >Download</v-btn
      >
    </v-col>
  </v-row>
  <div v-if="isLoading">
    <v-sheet
      color="#dddd"
      class="mt-5 text-center justify-center"
      :height="900"
      :max-height="900"
    >
      <div
        class="custom-loader"
        style="margin-top: 240px; display: inline-block"
      ></div>
      <p class="mt-5">Please Wait ...</p>
      <p style="font-size: 22px; font-weight: 600; color: gray">
        {{ bandwithSpend }}
      </p>
    </v-sheet>
  </div>
  <v-row>
    <v-col>
      <div ref="viewer" class="h-screen"></div>
    </v-col>
  </v-row>
  <!-- Metadata Dialog -->
  <metadata-dialog
    ref="metadataDialog"
    :item="resultChartPack"
  ></metadata-dialog>
  <loading-dialog v-if="isDownload"></loading-dialog>
</template>
<script>
import { defineComponent } from "vue";
import Client from "@/library/ApiClient";
import WebViewer from "@pdftron/webviewer";
// import { getInstance } from "@pdftron/webviewer";
import Constants from "@/library/Constants";
import MetadataDialog from "@/components/chartpack/MetadataDialog.vue";
import LoadingDialog from "@/components/LoadingDialog.vue";

// const instance = getInstance();

export default defineComponent({
  data: function () {
    return {
      isLoading: false,
      fileBlobURL: "",
      pdfTronElements: [
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
      listArea: [],
      listPeriode: [],
      selectArea: [],
      selectPeriode: [],
      resultChartPack: null,
      btnDisabled: true,
      isDownload: false,
      bandwithSpend: "Waiting for server respond",
      documentName: "",
    };
  },
  components: {
    MetadataDialog,
    LoadingDialog,
  },
  props: {
    item: Object,
    rowChartPack: Object,
    tabActive: Number,
  },
  mounted() {
    this.getMasterData();
    this.getChartPack();
  },
  methods: {
    download() {
      this.isDownload = true;
      Client.DownloadChartpack({
        store: this.$store,
        data: {
          id: this.resultChartPack.id,
        },
      })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", this.resultChartPack.documentName);
          document.body.appendChild(link);
          link.click();
        })
        .catch((error) => {
          this.$root.toast.show({
            message: "Failed download chartpack",
            color: " error",
            timeout: 5000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.isDownload = false;
        });
    },
    openMetada() {
      this.$refs.metadataDialog.start();
    },
    getPeriode() {
      let index = this.listArea.findIndex(
        (item) => item.id === this.selectArea
      );

      this.isLoading = true;
      this.selectPeriode = "";
      this.listPeriode = this.listArea[index].periodes;
      this.isLoading = false;
    },
    getMasterData() {
      this.listArea = this.item;

      if (
        this.rowChartPack != null &&
        this.tabActive == this.rowChartPack.idSektor
      ) {
        this.selectArea = this.rowChartPack.idArea;
        this.getPeriode();
        this.selectPeriode = this.rowChartPack.periode;
      } else {
        this.selectArea = this.item[0].id;
        this.getPeriode();
        this.selectPeriode = this.listPeriode[0];
      }
    },
    getChartPackSelected() {
      this.isLoading = true;
      this.btnDisabled = true;
      Client.PreviewDocumentChartPack({
        store: this.$store,
        data: {
          idSektor: this.listArea[0].idSektor,
          idArea: this.selectArea,
          periode: this.selectPeriode,
        },
        onDownloadProgress: (progressEvent) => {
          this.bandwithSpend =
            "Download Progress: " + this.formatBytes(progressEvent.loaded);
          this.fileSize = progressEvent.loaded;
        },
      })
        .then((response) => {
          let result = response.data;
          this.resultChartPack = result;

          this.fileBlobURL = this.getBlobURL(
            this.base64ToBlob(result.chartpackFile)
          );
          this.documentName = result.documentName;

          this.instance.UI.loadDocument(this.fileBlobURL, {
            extension: "pdf",
            filename: this.documentName,
          });
        })
        .catch(() => {
          this.$root.toast.show({
            message: "[400] Failed preview chartpack",
            color: " error",
            timeout: 5000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.isLoading = false;
          this.btnDisabled = false;
          this.bandwithSpend = "Waiting for server respond";
        });
    },
    getChartPack() {
      this.isLoading = true;
      this.btnDisabled = true;
      Client.PreviewDocumentChartPack({
        store: this.$store,
        data: {
          idSektor: this.listArea[0].idSektor,
          idArea: this.selectArea,
          periode: this.selectPeriode,
        },
        onDownloadProgress: (progressEvent) => {
          this.bandwithSpend =
            "Download Progress: " + this.formatBytes(progressEvent.loaded);
          this.fileSize = progressEvent.loaded;
        },
      })
        .then((response) => {
          let result = response.data;
          this.resultChartPack = result;

          this.fileBlobURL = this.getBlobURL(
            this.base64ToBlob(result.chartpackFile)
          );
          this.documentName = result.documentName;
          this.startPDFTron();
        })
        .catch(() => {
          this.$root.toast.show({
            message: "[400] Failed preview chartpack",
            color: " error",
            timeout: 5000,
            icon: "mdi-check",
          });
        })
        .finally(() => {
          this.isLoading = false;
          this.btnDisabled = false;
          this.bandwithSpend = "Waiting for server respond";
        });
    },
    startPDFTron() {
      WebViewer(
        {
          path: "/lib",
          disabledElements: this.pdfTronElements,
          loadAsPDF: true,
          fullAPI: true,
          licenseKey: Constants.LICENSE_KEY_PDFTRON,
        },
        this.$refs.viewer
      )
        .then((instance) => {
          instance.UI.loadDocument(this.fileBlobURL, {
            extension: "pdf",
            filename: this.documentName,
          });
          this.instance = instance;
        })
        .catch(() => {
          this.$root.toast.show({
            message: "Failed preview chartpack",
            color: " error",
            timeout: 5000,
            icon: "mdi-check",
          });
        });
    },
    getBlobURL(param) {
      return window.URL.createObjectURL(new Blob([param]));
    },
    base64ToBlob(base64) {
      const binaryString = window.atob(base64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; ++i) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      return new Blob([bytes], { type: "application/pdf" });
    },
    formatBytes(bytes, decimals = 2) {
      if (!+bytes) return "0.00 Bytes";
      const k = 1024;
      const dm = decimals < 0 ? 0 : decimals;
      const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    },
  },
});
</script>
<style scoped>
.btn-primary {
  background-color: rgb(38, 125, 194) !important;
}
.text-title-blue {
  font-size: 23px;
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}
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
</style>
