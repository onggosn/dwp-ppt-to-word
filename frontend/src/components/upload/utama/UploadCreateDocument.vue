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
          color="red"
          icon="mdi-alert-octagon-outline"
          size="112"
        ></v-icon>

        <h2 class="text-h5 mb-6">{{ message }}</h2>

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
      timeStart = performance.now();

      const penyusunParams: Array<object> = [];

      props.approver._penyusun.filter((element) => {
        penyusunParams.push({
          username: element.username,
          groupName: element.groupName,
        });
      });

      let jenisApproval = [];

      client
        .GetMdocumentApprovalByIdMdocumentType({
          store: store,
          data: {
            id: props.metadata._typeDocument,
          },
        })
        .then((response) => {
          let temp = [];
          let i = 0;
          for (i in response.data) {
            if (response.data[i].needApproval == true) {
              temp.push(response.data[i]);
            }
          }
          jenisApproval = temp;

          let approveDoc = [
            {
              idTaskDocument: route.params.taskId,
              idMDocumentApproval: jenisApproval[0].id,
              username: store.state.username,
              needApproval: true,
              status: 0,
            },
            {
              idTaskDocument: route.params.taskId,
              idMDocumentApproval: jenisApproval[1].id,
              username: props.approver._pengaju,
              needApproval: false,
              status: 0,
            },
            {
              idTaskDocument: route.params.taskId,
              idMDocumentApproval: jenisApproval[2].id,
              username: props.approver._penyetuju,
              needApproval: false,
              status: 0,
            },
          ];

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
                .insertTaskDocumentByUpload({
                  store: store,
                  data: {
                    idTask: route.params.taskId,
                    idDocumentType: props.metadata._typeDocument,
                    nomor: "string",
                    topicName: props.metadata._namaDokumen,
                    presenter: props.metadata._presenter,
                    editor: "",
                    keyword: props.metadata._keyword,
                    idProgramStrategis: props.metadata._programStrategis,
                    idMEvent: props.metadata._eventName,
                    idMSatkerPembuat: props.metadata._listSatker,
                    approvalDocument: approveDoc,
                    username: store.state.username,
                    userId: 0,
                    listPenyusun: penyusunParams,
                    traceId: traceId,
                  },
                  additional: {
                    tokenCookie: store.state.tokenCookie,
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
                    fileSize = progressEvent.loaded;
                  },
                })
                .then((response) => {
                  switch (response.plainData.responseCode) {
                    case "011000":
                      message.value = "Successfully Created Document!";
                      isSuccess.value = true;
                      break;
                    case "011001":
                      message.value = response.plainData.responseMessage;
                      isFail.value = true;
                      break;
                    default:
                      message.value = "Unkown Error Encounter";
                      isFail.value = true;
                      break;
                  }

                  timeEnd = performance.now();
                  insertLog(
                    traceId,
                    "",
                    props.metadata._namaDokumen,
                    fileSize,
                    timeStart,
                    timeEnd,
                    "UPLOAD DOCUMENT UTAMA APPROVAL"
                  );
                })
                .catch(() => {
                  message.value = "Fail Create Document";
                  isFail.value = true;

                  timeEnd = performance.now();
                  insertLog(
                    traceId,
                    "-",
                    props.metadata._namaDokumen,
                    fileSize,
                    timeStart,
                    timeEnd,
                    "FAIL UPLOAD DOCUMENT UTAMA APPROVAL"
                  );
                })
                .finally(() => {
                  isLoading.value = false;
                });
            });
        });
      break;
    }
    case "Upload Non Approval Document": {
      message.value = "Uploading your document, please wait..";

      traceId = uuidv4();
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
            .uploadFinalTaskDocument({
              store: store,
              data: {
                idTask: route.params.taskId,
                idDocumentType: props.metadata._documentType,
                nomor: "string",
                topicName: props.metadata._documentName,
                presenter: props.metadata._presenterName,
                editor: "noName",
                keyword: props.metadata._keyword,
                idProgramStrategis: props.metadata._programStrategis,
                idMEvent: props.metadata._eventName,
                idMSatkerPembuat: props.metadata._satkerName,
                documentFile: props.file.file,
                approvalDocument: "[]",
                username: store.state.username,
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
                fileSize = progressEvent.loaded;
              },
            })
            .then(() => {
              message.value = "Upload Success";
              isSuccess.value = true;

              timeEnd = performance.now();

              insertLog(
                traceId,
                "",
                props.metadata._namaDokumen,
                fileSize,
                timeStart,
                timeEnd,
                "UPLOAD DOCUMENT NON APPROVAL"
              );
            })
            .catch(() => {
              message.value = "Fail Upload Document";
              isFail.value = true;

              timeEnd = performance.now();

              insertLog(
                traceId,
                "",
                props.metadata._namaDokumen,
                fileSize,
                timeStart,
                timeEnd,
                "FAIL UPLOAD DOCUMENT NON APPROVAL"
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
        });
      break;
    }
  }
});
</script>
