<template>
  <v-row class="ml-2">
    <v-col v-html="viewerListener"></v-col>
  </v-row>
  <template v-if="isLoading">
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
  </template>
</template>
<script lang="js">
import { defineComponent } from "vue";
import Client from "@/library/ApiClient";
import Constants from "@/library/Constants";
import WebViewer from "@pdftron/webviewer";

export default defineComponent({
  data: function () {
    return {
        isLoading : false,
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
        listArea : [],
        listPeriode : [],
        selectArea : [],
        selectPeriode : [],
        resultChartPack : null,
        btnDisabled : true,
        isDownload : false,
        bandwithSpend : "Waiting server to respond",
        viewerListener : "<div id='viewer' class='h-screen bg-red'></div>"
    };
  },
  components:{
  },
  props:{
    item : Object,
    rowChartPack : Object
  },
  methods: {
    getChartPack() {
        this.isLoading = true;
        this.btnDisabled = true;
        this.generateCanvas();
        Client.PreviewDocumentChartPack({
            store: this.$store,
            data: {
                idSektor: 1,
                idArea: 1,
                periode: "Desember 2022",
          },
          onDownloadProgress: (progressEvent) => {
            this.bandwithSpend = "Download Progress: " +
                this.formatBytes(progressEvent.loaded)
          }
        })
        .then((response) => {
            this.bandwithSpend += " Rendering...";
            let result = response.data;
            this.resultChartPack = result;
            this.fileBlobURL = this.getBlobURL(this.base64ToBlob(result.chartpackFile));
            // var stringPeriode = this.selectPeriode.replace(" ","");
            // var canvas = "viewer"+this.selectArea+stringPeriode;
            WebViewer({
                    path: "/lib",
                    disabledElements: this.pdfTronElements,
                    loadAsPDF: true,
                    fullAPI: true,
                    licenseKey: Constants.LICENSE_KEY_PDFTRON,
                },document.getElementById('viewer')
            ).then((instance) => {

                instance.UI.loadDocument(this.fileBlobURL, {
                      extension: "pdf",
                      filename: result.documentName,
                  });

                })
                .catch(() => {
                this.$root.toast.show({
                  message: "Failed preview chartpack",
                  color: " error",
                  timeout: 5000,
                  icon: "mdi-check",
                });
                });
            })
            .catch((e) => {
                this.$root.toast.show({
                  message: "Gagal preview Chartpack : " + e,
                  color: " error",
                  timeout: 5000,
                  icon: "mdi-check",
                });
            }).finally(() => {
                    this.isLoading = false;
                    this.btnDisabled = false;
                    this.bandwithSpend = "Waiting server to respond";
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
      return new Blob([bytes], { type: 'application/pdf' });
    },
    formatBytes(bytes, decimals = 2) {
          if (!+bytes) return "0.00 Bytes";

          const k = 1024;
          const dm = decimals < 0 ? 0 : decimals;
          const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

          const i = Math.floor(Math.log(bytes) / Math.log(k));
          return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }
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
