<template>
  <div class="d-flex justify-center align-baseline ma-5" style="gap: 1rem">
    <template v-if="resItem.responseCode == '011000'">
      <template v-if="resItem.responseData.length > 0">
        <template
          v-if="resItem.responseData[0].username != $store.state.username"
        >
          <v-btn class="sectionBlue-button ma-2" @click="downloadFile()">
            Download
          </v-btn>
          <v-btn class="sectionBlue-button ml-5 ma-2" @click="gotoWorkspace()">
            Go to Workspace
          </v-btn>
        </template>
        <template v-else>
          <template v-for="(item, index) in resItem.responseData" :key="index">
            <template
              v-if="
                (item.IdDocumentApprovalCurrent == 1 ||
                  item.IdDocumentApprovalCurrent == 6 ||
                  item.IdDocumentApprovalCurrent == 11 ||
                  item.IdDocumentApprovalCurrent == 24) &&
                item.username == $store.state.username
              "
            >
              <v-btn class="sectionRed-button ma-2" @click="load(1)">
                Delete
              </v-btn>
              <v-btn
                class="sectionBlue-button ma-2"
                @click="editFile(item.linkEdit)"
              >
                Edit
              </v-btn>
              <v-btn class="sectionBlue-button ma-2" @click="proceedFile(item)">
                Send
              </v-btn>
            </template>

            <template
              v-if="
                (item.IdDocumentApprovalCurrent == 2 ||
                  item.IdDocumentApprovalCurrent == 7 ||
                  item.IdDocumentApprovalCurrent == 12 ||
                  item.IdDocumentApprovalCurrent == 25) &&
                item.username == $store.state.username
              "
            >
              <v-btn
                class="sectionBlue-button ma-2"
                @click="editFile(item.linkEdit)"
              >
                Edit
              </v-btn>
              <v-btn class="sectionBlue-button ma-2" @click="proceedFile(item)">
                Send
              </v-btn>
            </template>

            <template
              v-if="
                (item.IdDocumentApprovalCurrent == 3 ||
                  item.IdDocumentApprovalCurrent == 8 ||
                  item.IdDocumentApprovalCurrent == 13 ||
                  item.IdDocumentApprovalCurrent == 26) &&
                item.username == $store.state.username
              "
            >
              <v-btn
                v-if="item.description == 'Reject'"
                class="sectionRed-button ma-2"
                @click="proceedFile(item)"
              >
                Reject
              </v-btn>
              <v-btn
                v-if="item.description == 'Approve'"
                class="sectionBlue-button ma-2"
                @click="proceedFile(item)"
              >
                Approve
              </v-btn>
            </template>
          </template>
        </template>
      </template>
      <template v-else>
        <v-btn class="sectionBlue-button ma-2" @click="downloadFile()">
          Download
        </v-btn>

        <v-btn class="sectionBlue-button ma-2" @click="gotoWorkspace()">
          Go to Workspace
        </v-btn>
      </template>
    </template>
    <template v-else-if="resItem.responseCode == '011033'">
      <div style="color: rgba(186, 188, 202, 1)">
        {{ resItem.responseMessage }}
      </div>
    </template>

    <!-- START Loading Section -->
    <custom-loading
      v-if="isLoading"
      :title="bandwithSpend"
      :progress="downloadProgress"
      :totalProgress="sizeDocument"
      :hasProgress="hasProgress"
    />
    <!-- END Loading Section -->
  </div>
</template>

<script>
import client from "@/library/ApiClient";
import CustomLoading from "@/components/CustomLoading.vue";
import { v4 as uuidv4 } from "uuid";

export default {
  components: { CustomLoading },
  props: {
    documentName: String,
    documentId: String,
    document: Object,
  },
  data() {
    return {
      isLoading: false,
      bandwithSpend: "waiting for server response",
      downloadProgress: 0,
      sizeDocument: 0,
      hasProgress: false,
      resItem: {},

      //===== log attr =====
      timeStart: 0,
      timeEnd: 0,
      timeStartRender: 0,
      timeEndRender: 0,
      fileSize: 0,
      traceId: "",
      //===== log attr =====
    };
  },
  methods: {
    getFlow() {
      client
        .GetListFlowDetailbyTaskDocumentId({
          store: this.$store,
          data: {
            id: this.$route.params.documentId,
          },
        })
        .then((res) => {
          this.resItem = res.plainData;
        });
    },
    gotoWorkspace() {
      this.$router.replace({
        name: "main",
        params: {
          workspaceId: this.$route.params.workspaceId,
          taskId: this.$route.params.taskId,
          pageId: this.$route.params.pageId,
        },
      });
    },
    downloadFile() {
      this.traceId = uuidv4();
      this.timeStart = performance.now();
      this.isLoading = true;

      this.sizeDocument = this.document.sizeDocument;
      this.hasProgress = this.document.sizeDocument ? true : false;
      client
        .DownloadDocumentById({
          store: this.$store,
          data: {
            id: this.$route.params.documentId,
            traceId: this.traceId,
          },
          onDownloadProgress: (progressEvent) => {
            this.bandwithSpend =
              "Download progress: " + this.formatBytes(progressEvent.loaded);
            this.downloadProgress = progressEvent.loaded;
            this.fileSize = progressEvent.loaded;
          },
        })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", this.documentName);
          document.body.appendChild(link);
          link.click();

          this.timeEnd = performance.now();
          this.writeLog({
            traceId: this.traceId ?? "",
            documentId: this.documentId ?? "",
            documentName: this.documentName ?? "",
            fileSize: this.fileSize ?? 0,
            timeExecution: this.timeEnd - this.timeStart,
            description: "DOWNLOAD DOCUMENT UTAMA",
          });
        })
        .finally(() => {
          this.isLoading = false;
          this.bandwithSpend = "waiting for server response";
        });
    },
    proceedFile(item) {
      this.resItem = {};
      this.traceId = uuidv4();
      this.timeStart = performance.now();
      this.isLoading = true;
      client
        .ApproveDocument({
          store: this.$store,
          data: {
            idDocumentType: item.idDocumentType,
            username: this.$store.state.username,
            idDocumentApprovalCurrent: item.IdDocumentApprovalCurrent,
            idDocumentApprovalNext: item.IdDocumentApprovalNext,
            approvalDocumentId: item.approvalDocumentId,
            description: item.description,
            taskDocumentId: this.$route.params.documentId,
            comment: "",
            traceId: this.traceId,
          },
        })
        .then((response) => {
          this.timeEnd = performance.now();
          if (response.plainData.ResponseCode == "011000") {
            if (item.description == "Reject") {
              this.showToast("Successfully Reject", "success");
            } else if (item.description == "Approve") {
              this.writeLog({
                traceId: this.traceId ?? "",
                documentId: this.documentId ?? "",
                documentName: this.documentName ?? "",
                fileSize: this.fileSize ?? 0,
                timeExecution: this.timeEnd - this.timeStart,
                description: "APPROVE DOCUMENT UTAMA",
              });
            } else {
              this.showToast("Successfully Sent", "success");
            }
          }
          this.$emit("trigger", 0);
          setTimeout(() => {
            this.getFlow();
          }, 500);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    editFile(link) {
      window.open(link, "_blank").focus();
    },
    writeLog(params) {
      client.writeLog({
        store: this.$store,
        data: {
          traceId: params.traceId,
          documentId: params.documentId,
          documentName: params.documentName,
          fileSize: params.fileSize,
          timeExecution: params.timeExecution,
          description: params.description,
        },
      });
    },
    showToast(message, state) {
      this.$root.toast.show({
        message: message,
        color: state,
        timeout: 3000,
        // icon: "mdi-check",
      });
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
  created() {
    this.getFlow();
  },
};
</script>

<style scoped>
.sectionBlue-button {
  width: 13vw;
  color: #fff;
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}

.sectionRed-button {
  width: 13vw;
  color: #fff;
  /* Gradient Red */

  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  /* drop shadow button open file */

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}
.sectionGrey-button {
  width: 13vw;
  color: #fff !important;

  background: linear-gradient(180deg, #dfdfdf 0%, #e4e2e2 100%);

  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}

.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}

@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }

  to {
    transform: rotate(360deg);
  }
}

@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }

  to {
    transform: rotate(360deg);
  }
}

@-o-keyframes loader {
  from {
    transform: rotate(0);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes loader {
  from {
    transform: rotate(0);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>
