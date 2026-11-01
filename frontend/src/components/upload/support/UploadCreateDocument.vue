<template>
  <v-container style="min-height: 25vh">
    <v-row
      class="fill-height mt-5"
      align-content="center"
      justify="center"
      v-if="isLoading"
    >
      <v-col cols="8">
        <v-progress-linear
          color="#045695"
          rounded
          :indeterminate="action == 'Create Document'"
          height="6"
          :model-value="progress"
          :value="progress"
        ></v-progress-linear>
      </v-col>
      <v-col class="text-12 text-center" cols="12">
        {{ message }}
      </v-col>
      <v-col
        class="text-14 font-weight-bold text-center mt-n5"
        cols="12"
        v-if="progress != 100 && action != 'Create Document'"
      >
        progress: {{ progress }}%
      </v-col>
      <v-col
        class="text-14 font-weight-bold text-center mt-n5"
        cols="12"
        v-if="progress == 100"
      >
        "just a bit longer, we're almost there!"
      </v-col>
      <v-col
        class="text-14 font-weight-bold text-center mt-n5"
        cols="12"
        v-if="progress == 100"
      >
        <v-progress-circular
          :width="3"
          color="#045695"
          indeterminate
        ></v-progress-circular>
      </v-col>
    </v-row>
    <v-row
      class="fill-height mt-5"
      align-content="center"
      justify="center"
      v-if="isSuccess"
    >
      <v-sheet
        elevation="0"
        max-width="600"
        rounded="lg"
        width="100%"
        class="pa-4 text-center mx-auto"
      >
        <v-icon
          class="mb-5"
          color="success"
          icon="mdi-check-circle"
          size="112"
        ></v-icon>

        <h2 class="text-h5 mb-6">{{ message }}</h2>

        <p class="mb-4 text-medium-emphasis text-body-2">
          To see document list close this dialog
          <br />
          You're done!
          <br />
        </p>

        <v-divider class="mb-4"></v-divider>

        <div class="text-end">
          <v-btn
            class="text-none font-weight-bold text-green"
            color="white"
            rounded
            elevation="2"
            variant="flat"
            width="90"
            @click="close()"
          >
            Close
          </v-btn>
        </div>
      </v-sheet>
    </v-row>
    <v-row
      class="fill-height mt-5"
      align-content="center"
      justify="center"
      v-if="isFail"
    >
      <v-sheet
        elevation="0"
        max-width="600"
        rounded="lg"
        width="100%"
        class="pa-4 text-center mx-auto"
      >
        <v-icon
          class="mb-5"
          color="#c51c24"
          icon="mdi-alert-circle-outline"
          size="112"
        ></v-icon>

        <h2 class="text-h5 mb-6">{{ message }}</h2>
        <p class="text-12 mb-5">
          We couldn't upload/download your document. Please double-check your
          internet connection and try again. If the problem persists, please
          contact support for assistance.
        </p>

        <v-divider class="mb-4"></v-divider>

        <div class="text-end">
          <v-btn
            class="text-none font-weight-bold pl-3 pr-3 text-red"
            color="white"
            rounded
            elevation="2"
            variant="flat"
            width="90"
            @click="close()"
          >
            Close
          </v-btn>
        </div>
      </v-sheet>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps, defineEmits } from "vue";
import client from "@/library/ApiClient";
import { useRoute } from "vue-router";
import store from "@/store/index";
import { v4 as uuidv4 } from "uuid";
import { insertLog } from "@/models/log";

const props = defineProps({
  metadata: { type: Object, default: null },
  approver: { type: Object, default: null },
  file: { type: Object, default: null },
  action: { type: String, required: true, default: "" },
});

const emits = defineEmits(["updateStep"]);
const route = useRoute();
const progress = ref<number>(0);
const isLoading = ref<boolean>(true);
const isSuccess = ref(false);
const isFail = ref(false);
const message = ref("Creating your document, please wait..");
const close = () => emits("updateStep", "Close");

let traceId = "";
let timeStart = 0;
let timeEnd = 0;
let fileSize = 0;

onMounted(() => {
  switch (props.action) {
    case "Create Document": {
      traceId = uuidv4();
      const penyusunParams: Array<object> = [];

      props.approver._penyusun.filter((element) => {
        penyusunParams.push({
          username: element.username,
          groupName: element.groupName,
        });
      });

      const paramDataPNIN = {
        idTask: route.params.taskId,
        idDocumentSupportType: props.metadata._typeDocument,
        topicName: props.metadata._namaDokumen,
        codeDocument: props.metadata._kodePNIN,
        codeIku: props.metadata._kodeIKUICK,
        idMBusinessProcess: props.metadata._prosesBisnis,
        idMClassification: props.metadata._sifatDokumen,
        keyword: props.metadata._keyword,
        descriptions: props.metadata._keterangan,
        idMEvent: props.metadata._eventName,
        dueDate: props.metadata._batasWaktu,
        listSatkerPembuat: Object.values(props.metadata._listSatker),
        listPS: Object.values(props.metadata._programStrategis),
        traceId: traceId,
        listPenyusun: penyusunParams,
        approvalDocumentSupport: [
          {
            username: props.approver._reviewer,
            description: "reviewer",
          },
          {
            username: props.approver._pengaju,
            description: "pengaju",
          },
          {
            username: props.approver._penyetuju,
            description: "penyetuju",
          },
        ],
      };

      timeStart = performance.now();
      client
        .CreateDocumentSupport({
          store: store,
          data: paramDataPNIN,
          onUploadProgress: (progressEvent) => {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / props.file.filesize
            );

            if (percentCompleted < 100) {
              progress.value = percentCompleted;
            } else {
              progress.value = 100;
            }
            fileSize = progressEvent.loaded;
          },
        })
        .then((response) => {
          message.value = response.plainData.responseData.description;
          switch (response.plainData.responseCode) {
            case "011000": {
              isSuccess.value = true;
              break;
            }
            default: {
              message.value = "Fail Create Document";
              isFail.value = true;
              break;
            }
          }

          timeEnd = performance.now();
          insertLog(
            traceId,
            "",
            props.metadata._namaDokumen,
            fileSize,
            timeStart,
            timeEnd,
            "CREATE DOCUMENT SUPPORT"
          );
        })
        .catch(() => {
          message.value = "Fail Create Document";
          isFail.value = true;

          timeEnd = performance.now();
          insertLog(
            traceId,
            "",
            props.metadata._namaDokumen,
            fileSize,
            timeStart,
            timeEnd,
            "FAIL CREATE DOCUMENT SUPPORT"
          );
        })
        .finally(() => {
          isLoading.value = false;
        });
      break;
    }
    case "Create Document Standarisasi": {
      traceId = uuidv4();
      const penyusunParams: Array<object> = [];

      props.approver._penyusun.filter((element) => {
        penyusunParams.push({
          username: element.username,
          groupName: element.groupName,
        });
      });

      const paramDataStandarisasi = {
        idTask: route.params.taskId,
        idDocumentSupportType: props.metadata._typeDocument,
        topicName: props.metadata._namaDokumen,
        presenter: props.metadata._presenter,
        keyword: props.metadata._keyword,
        idMEvent: props.metadata._eventName,
        listSatkerPembuat: Object.values(props.metadata._listSatker),
        listPS: [],
        traceId: traceId,
        listPenyusun: penyusunParams,
        approvalDocumentSupport: [
          {
            username: props.approver._pengaju,
            description: "pengaju",
          },
          {
            username: props.approver._penyetuju,
            description: "penyetuju",
          },
        ],
      };
      timeStart = performance.now();
      client
        .CreateDocumentSupport({
          store: store,
          data: paramDataStandarisasi,
          onUploadProgress: (progressEvent) => {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / props.file.filesize
            );

            if (percentCompleted < 100) {
              progress.value = percentCompleted;
            } else {
              progress.value = 100;
            }
            fileSize = progressEvent.loaded;
          },
        })
        .then((response) => {
          message.value = response.plainData.responseData.description;
          switch (response.plainData.responseCode) {
            case "011000": {
              isSuccess.value = true;
              break;
            }
            default: {
              message.value = "Fail Create Document";
              isFail.value = true;
              break;
            }
          }

          timeEnd = performance.now();
          insertLog(
            traceId,
            "",
            props.metadata._namaDokumen,
            fileSize,
            timeStart,
            timeEnd,
            "CREATE DOCUMENT SUPPORT"
          );
        })
        .catch(() => {
          message.value = "Fail Create Document";
          isFail.value = true;

          timeEnd = performance.now();
          insertLog(
            traceId,
            "",
            props.metadata._namaDokumen,
            fileSize,
            timeStart,
            timeEnd,
            "FAIL CREATE DOCUMENT SUPPORT"
          );
        })
        .finally(() => {
          isLoading.value = false;
        });
      break;
    }
    case "Upload Approval Document": {
      traceId = uuidv4();
      message.value = "Uploading your document, please wait..";

      const penyusunParams: Array<object> = [];

      props.approver._penyusun.filter((element) => {
        penyusunParams.push({
          username: element.username,
          groupName: element.groupName,
        });
      });

      timeStart = performance.now();

      client
        .getRefreshToken({
          store: store,
          data: {
            username: store.state.username,
          },
        })
        .then((response) => {
          store.state.tokenCookie = response.plainData.responseData;

          let approveDoc = "";

          approveDoc = JSON.stringify([
            {
              username: props.approver._pengaju,
              description: "pengaju",
            },
            {
              username: props.approver._penyetuju,
              description: "penyetuju",
            },
          ]);

          // const paramUpload = {
          //   taskId: route.params.taskId,
          //   documentTypeId: props.metadata._documentType,
          //   documentName: props.file.filename.split(".")[0],
          //   documentTopic: props.metadata._documentName,
          //   presenter: props.metadata._presenterName,
          //   editor: "NoOne",
          //   keyword: props.metadata._keyword,
          //   programStrategisId: props.metadata._programStrategis,
          //   eventId: props.metadata._eventName,
          //   listSatkerPembuat: props.metadata._satkerName,
          //   documentFile: props.file.file,
          //   createdBy: store.state.username,
          //   versi: null,
          //   ApprovalDocumentSupport: approveDoc.toString(),
          //   listPenyusun: JSON.stringify(penyusunParams),
          //   traceId: traceId,
          // };

          client
            .insertTaskDocumentSupportByUpload({
              store: store,
              data: {
                taskId: route.params.taskId,
                documentTypeId: props.metadata._documentType,
                documentName: props.file.filename.split(".")[0],
                documentTopic: props.metadata._documentName,
                presenter: props.metadata._presenterName,
                editor: "NoOne",
                keyword: props.metadata._keyword,
                programStrategisId: props.metadata._programStrategis,
                eventId: props.metadata._eventName,
                listSatkerPembuat: props.metadata._satkerName,
                documentFile: props.file.file,
                createdBy: store.state.username,
                versi: null,
                ApprovalDocumentSupport: approveDoc.toString(),
                listPenyusun: JSON.stringify(penyusunParams),
                traceId: traceId,
              },
              additional: {
                tokenCookie: store.state.tokenCookie,
              },
              onUploadProgress: (progressEvent) => {
                var percentCompleted = Math.round(
                  (progressEvent.loaded * 100) / props.file.filesize
                );

                if (percentCompleted < 100) {
                  progress.value = percentCompleted;
                } else {
                  progress.value = 100;
                }

                fileSize = props.file.filesize;
              },
            })
            .then(() => {
              message.value = "Upload Success";
              isSuccess.value = true;

              timeEnd = performance.now();
              insertLog(
                traceId,
                "",
                props.metadata._documentName,
                fileSize,
                timeStart,
                timeEnd,
                "UPLOAD DOCUMENT SUPPORT APPROVAL"
              );
            })
            .catch(() => {
              isFail.value = true;
              message.value = "Oops! Something Went Wrong";

              timeEnd = performance.now();
              insertLog(
                traceId,
                "-",
                props.metadata._documentName,
                fileSize,
                timeStart,
                timeEnd,
                "FAIL UPLOAD DOCUMENT SUPPORT APPROVAL"
              );
            })
            .finally(() => {
              isLoading.value = false;
            });
        })
        .catch(() => {
          isFail.value = true;
          message.value = "Fail Upload Document";
        })
        .finally(() => {
          undefined;
        });
      break;
    }
    case "Upload Non Approval Document": {
      traceId = uuidv4();
      message.value = "Uploading your document, please wait..";

      timeStart = performance.now();

      client
        .getRefreshToken({
          store: store,
          data: {
            username: store.state.username,
          },
        })
        .then((response) => {
          store.state.tokenCookie = response.plainData.responseData;
          client
            .insertTaskDocumentSupport({
              store: store,
              data: {
                taskId: route.params.taskId,
                documentTypeId: 1,
                documentName: props.file.filename.split(".")[0],
                documentTopic: props.file.filename.split(".")[0],
                presenter: props.metadata._presenterName,
                editor: "NoOne",
                keyword: props.metadata._keyword,
                programStrategisId: props.metadata._programStrategis,
                eventId: props.metadata._eventName,
                MSatkerPembuatId: props.metadata._satkerName,
                documentFile: props.file.file,
                createdBy: store.state.username,
                listPenyusun: "none",
                traceId: traceId,
              },
              additional: {
                tokenCookie: store.state.tokenCookie,
              },
              onUploadProgress: (progressEvent) => {
                var percentCompleted = Math.round(
                  (progressEvent.loaded * 100) / props.file.filesize
                );

                if (percentCompleted < 100) {
                  progress.value = percentCompleted;
                } else {
                  progress.value = 100;
                }
                fileSize = props.file.filesize;
              },
            })
            .then(() => {
              message.value = "Upload Success";
              isSuccess.value = true;

              timeEnd = performance.now();
              insertLog(
                traceId,
                "",
                props.metadata._documentName,
                fileSize,
                timeStart,
                timeEnd,
                "UPLOAD DOCUMENT SUPPORT NON APPROVAL"
              );
            })
            .catch(() => {
              message.value = "Fail Upload Document";
              isFail.value = true;

              timeEnd = performance.now();
              insertLog(
                traceId,
                "",
                props.metadata._documentName,
                fileSize,
                timeStart,
                timeEnd,
                "FAIL UPLOAD DOCUMENT SUPPORT NON APPROVAL"
              );
            })
            .finally(() => {
              isLoading.value = false;
            });
        })
        .catch(() => {
          message.value = "Fail Upload Document";
          isFail.value = true;
        })
        .finally(() => {
          undefined;
          // isLoading.value = false;
        });
      break;
    }
    case "Edit Document": {
      const penyusunParams: Array<object> = [];
      props.approver.value._penyusun.filter((element) => {
        penyusunParams.push({
          username: element.username,
          groupName: element.groupName,
        });
      });

      client
        .updateMetadataDokumen({
          store: store,
          data: {
            id: props.approver.documentId,
            idTask: route.params.taskId,
            idDocumentSupportType: props.metadata._typeDocument,
            topicName: props.metadata._namaDokumen,
            codeDocument: props.metadata._kodePNIN,
            codeIku: props.metadata._kodeIKUICK,
            idMBusinessProcess: props.metadata._prosesBisnis,
            idMClassification: props.metadata._sifatDokumen,
            keyword: props.metadata._keyword,
            descriptions: props.metadata._keterangan,
            idMEvent: props.metadata._eventName,
            dueDate: props.metadata._batasWaktu,
            listSatkerPembuat: props.metadata._listSatker,
            listPS: props.metadata._programStrategis,
            username: store.state.username,
            deviceType: "web",
            traceId: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            listPenyusun: penyusunParams,
            approvalDocumentSupport: props.approver.param,
          },
          onUploadProgress: (progressEvent) => {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );

            if (percentCompleted < 100) {
              progress.value = percentCompleted;
            } else {
              progress.value = 100;
            }
          },
        })
        .then((response) => {
          switch (response.plainData.responseCode) {
            case "011000": {
              message.value = "Successfully Edited";
              isSuccess.value = true;
              break;
            }
          }
        })
        .finally(() => {
          isLoading.value = false;
        });

      break;
    }
    case "Download Document Template": {
      message.value = "Downloading your document, please wait..";
      client
        .downloadTemplate({
          store: store,
          data: {
            idDocumentSupportType: props.metadata.id,
          },
          onDownloadProgress: (progressEvent) => {
            var percentCompleted = Math.round(
              (progressEvent.loaded * 100) / props.metadata.fileSize
            );
            progress.value = percentCompleted;
          },
        })
        .then((response) => {
          const url = window.URL.createObjectURL(response.data);
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", props.metadata.value + ".pptx");
          document.body.appendChild(link);
          link.click();
          message.value = "Download Success";
          isSuccess.value = true;
        })
        .catch(() => {
          isFail.value = true;
          message.value = "Oops! Something Went Wrong";
        })
        .finally(() => {
          isLoading.value = false;
        });
      break;
    }
  }
});
</script>
