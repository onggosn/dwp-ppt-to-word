<template>
  <div class="d-block">
    <v-row align-content="center" justify="center">
      <div class="py-5 ps-5 my-3">
        <v-btn
          variant="outlined"
          size="large"
          icon="mdi-arrow-left"
          color="#045695"
          style="border: 0.5px solid #d3d3d3"
          elevation="3"
          @click="$router.go(-1)"
        />
      </div>
      <v-col style="align-self: center">
        <v-sheet
          class="ma-2 py-2 pe-2 font-weight-bold text-18"
          style="color: #045695"
        >
          <free-style-shimmer
            v-if="isLoading[0]"
            width="100%"
            height="5vh"
            border-radius="5px"
            color="#DCDCDC"
          />
          <template v-else>{{ responseData?.assignmentName }}</template>
        </v-sheet>
      </v-col>
    </v-row>
  </div>

  <hr size="1" color="d3d3d3" />
  <v-row no-gutters>
    <v-col cols="9">
      <div class="d-flex justify-center text-center" style="height: 80px">
        <BtnFlowApproveAssignmentVue
          :id="idAssignment"
          :isDisabled="!isHasDiscussion"
          @doneProcess="getDetailAssignment()"
        />
      </div>
    </v-col>
    <v-col cols="3"></v-col>
  </v-row>

  <hr size="1" color="d3d3d3" />

  <v-row no-gutters class="bg-white">
    <v-col cols="9" class="bg-white text-center px-4">
      <v-row>
        <v-col cols="12">
          <div class="view-chat" id="view_chat">
            <template v-if="isLoading[1]">
              <free-style-shimmer
                v-for="idx in 4"
                :key="idx"
                :is-loading="true"
                width="100%"
                height="4.3rem"
                border-radius="10px"
                class="my-2"
              />
            </template>
            <template v-else>
              <template v-for="(item, idx) in discussionItems" :key="idx">
                <RowDiscutionComponent :item="item" />
              </template>
            </template>
          </div>
        </v-col>
        <v-col cols="12" style="bottom: 0px">
          <hr size="1" color="d3d3d3" />
          <div class="d-flex justify-space-between align-center">
            <v-textarea
              rows="2"
              max-rows="3"
              placeholder="Type Message"
              variant="plain"
              style="border-radius: 20px; background: white"
              class="mx-1"
              v-model="chatMsg"
              @keydown.enter.exact.prevent="sendDiscution()"
              :hide-details="true"
              :disabled="!isCanSendDisccussion"
            ></v-textarea>
            <v-btn
              class="mr-3"
              icon="mdi-paperclip"
              @click="sendFile()"
              :disabled="!isCanSendDisccussion"
              :style="[
                isCanSendDisccussion
                  ? { color: '#267dc2', 'background-color': 'white' }
                  : { color: '#grey', 'background-color': 'white' },
              ]"
            ></v-btn>
            <v-btn
              icon="mdi-send"
              @click="sendDiscution()"
              :disabled="!isCanSendDisccussion"
              :style="[
                isCanSendDisccussion
                  ? { color: '#267dc2', 'background-color': 'white' }
                  : { color: '#grey', 'background-color': 'white' },
              ]"
            ></v-btn>
          </div>
          <input
            type="file"
            name="file"
            class="hidden-input d-none"
            @change="onChangeFileInput"
            ref="fileInput"
            accept=".pptx, .ppt, .doc, .docx, .pdf"
          />
        </v-col>
      </v-row>
    </v-col>
    <v-col
      cols="3"
      style="border-left: 1px solid #d3d3d3"
      class="bg-white pl-4 pt-4 pr-2"
    >
      <div class="d-block bg-white">
        <p class="text-body" style="font-size: 20px">Detail Penugasan</p>
        <p class="text-title">Deskripsi Penugasan</p>
        <p class="text-body" v-text="responseData?.description"></p>
        <p class="text-title">Status</p>
        <v-chip
          :style="matchChipStyle(responseData?.statusName ?? '') as StyleValue"
        >
          {{ responseData?.statusName }}
        </v-chip>
        <p class="text-title">Satker Koordinator</p>
        <p class="text-body" v-text="responseData?.satkerKoordinatorList"></p>
        <p class="text-title">Ditugaskan Kepada</p>
        <p class="text-body" v-text="responseData?.listDitugaskanKepada"></p>
        <p class="text-title">Pembuat Penugasan</p>
        <p class="text-body" v-text="responseData?.name"></p>
      </div>
    </v-col>
  </v-row>

  <custom-loading
    v-if="isLoading[2]"
    :title="fileLoading.bandwithTxt"
    :progress="fileLoading.downloadProgress"
    :totalProgress="fileLoading.sizeDocument"
    :hasProgress="fileLoading.hasProgress"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, StyleValue, getCurrentInstance } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { v4 as uuidv4 } from "uuid";

import client from "@/library/ApiClient";

import { formatBytes } from "../../helpers/utils";
import { TDetailAssignment, TFileLoading } from "@v2/Type";

import BtnFlowApproveAssignmentVue from "@v2/components/assignment/BtnFlowApproveAssignment.vue";
import RowDiscutionComponent from "@v2/components/discussion/RowDiscussionComponent.vue";
import CustomLoading from "@v2/components/loading/CustomLoading.vue";
import { matchChipStyle } from "@/v2/helpers/color";

const route = useRoute();
const router = useRouter();
const { root } = getCurrentInstance() as any;
const store = useStore();
const fileInput = ref(null);
const idAssignment = ref<string>(route.params.id as string);
const isLoading = ref<boolean[]>([false, false, false]);
const chatMsg = ref<string | null>("");
const discussionItems = ref([]);
const responseData = ref<TDetailAssignment>();
const fileLoading = ref<TFileLoading>({
  hasProgress: false,
  sizeDocument: 0,
  downloadProgress: 0,
  bandwithTxt: "waiting for server response",
});

const isHasDiscussion = computed(() => {
  return discussionItems.value.length > 0;
});

const isCanSendDisccussion = computed(() => {
  if (responseData.value) return responseData.value.isAvailable;

  return false;
});

function scroolDown() {
  let el = document.getElementById("view_chat");
  if (el) {
    el.scrollTop = el.scrollHeight;
  }
}

function getColor() {
  let colorStatus = {
    19: "text-warning",
    20: "text-warning",
    21: "text-success",
  };
  if (responseData.value) return colorStatus[responseData.value.idStatus];

  return "text-warning";
}

function getDetailAssignment() {
  client
    .getAssignmentDetailNew({
      store: store,
      data: {
        id: idAssignment.value,
      },
    })
    .then((res) => {
      responseData.value = res.plainData.responseData;
    });
}

function sendDiscution() {
  if (chatMsg.value) {
    const payload = {
      idAssignment: idAssignment.value,
      comment: chatMsg.value,
    };

    client
      .insertDiscussionAssignmentNew({
        store: store,
        data: payload,
      })
      .finally(() => {
        chatMsg.value = null;
        getDiscussion();
      });
  }
}

function sendFile() {
  fileInput.value.value = null;
  fileLoading.value = {
    hasProgress: false,
    sizeDocument: 0,
    downloadProgress: 0,
    bandwithTxt: "waiting for server response",
  };
  fileInput?.value.click();
}

function getDiscussion() {
  client
    .getListDiscussionAssignmentNew({
      store: store,
      data: {
        IdAssignment: idAssignment.value,
      },
    })
    .then((res) => {
      discussionItems.value = res.plainData.responseData.map((e) => {
        let document = e.dataDocument;
        if (document) document.tag = "assignment";
        return {
          message: e.comment,
          datetime: e.createdDate,
          sender: e.name,
          username: e.username,
          document: document,
        };
      });
    })
    .catch((err) => {
      if (err.response) {
        if (err.response.status == 403) {
          root.refs.toast.show({
            message: "tidak memiliki akses ke halaman ini",
            color: "warning",
            timeout: 3000,
          });
          router.push({ name: "home" });
        }
      }
    })
    .finally(() => {
      scroolDown();
    });
}

function onChangeFileInput(e) {
  const maxSize = 150 * 1024 * 1024;
  let file = e.target.files[0];

  if (file.name.length > 60) {
    root.refs.toast.show({
      message: "File name cannot be more than 60 characters",
      color: "error",
      timeout: 3000,
    });

    return;
  }

  if (file.size > maxSize) {
    root.refs.toast.show({
      message: "File size is more than 150MB",
      color: "error",
      timeout: 3000,
    });
  } else {
    isLoading.value[2] = true;
    fileLoading.value.sizeDocument = file.size;
    fileLoading.value.hasProgress = true;

    let reqData = {
      idAssignment: idAssignment.value,
      documentName: file.name,
      fileToUploadSize: file.size,
      documentFile: file,
      traceId: uuidv4(),
    };
    client
      .getRefreshToken({
        store: store,
        data: {
          username: store.state.username,
        },
      })
      .then((response) => {
        let refToken = response.plainData.responseData;
        client
          .uploadFileAssignmentNew({
            store: store,
            data: reqData,
            additional: {
              tokenCookie: refToken,
            },
            onUploadProgress: (progressEvent) => {
              if (progressEvent.loaded >= reqData.fileToUploadSize) {
                fileLoading.value.bandwithTxt =
                  formatBytes(progressEvent.loaded) +
                  " / " +
                  formatBytes(reqData.fileToUploadSize) +
                  " (please wait, almost there..)";
              } else {
                fileLoading.value.bandwithTxt =
                  formatBytes(progressEvent.loaded) +
                  " / " +
                  formatBytes(reqData.fileToUploadSize);
              }

              fileLoading.value.downloadProgress = progressEvent.loaded;
            },
          })
          .then((res) => {
            if (res.plainData.responseCode == "011000") {
              root.refs.toast.show({
                message: "success upload file",
                color: "success",
                timeout: 3000,
              });
            }
            // error be
            else if (res.plainData.responseCode == "011001") {
              root.refs.toast.show({
                message: res.plainData.responseMessage,
                color: "error",
                timeout: 3000,
              });
            }
            getDiscussion();
          })
          .finally(() => {
            isLoading.value[2] = false;
            fileLoading.value.bandwithTxt = "waiting for server response";
          });
      });
  }
}

onMounted(() => {
  getDetailAssignment();
  getDiscussion();
});
</script>

<style scope>
.text-body {
  color: var(--base-color-blue, #3a416f);
  font-family: Poppins;
  font-style: normal;
  font-weight: 500;
  font-size: 15px;
  line-height: normal;
}

.text-title {
  margin-top: 7px;
  color: #a6abc7 !important;
  font-family: Poppins;
  font-style: normal;
  font-weight: 500;
  font-size: 15px;
  line-height: normal;
}

.text-status {
  font-family: Poppins;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.text-warning {
  color: #fe7411;
}
.text-success {
  color: #02aa59;
}
.view-chat {
  height: 65vh;
  overflow: hidden auto;
  margin-top: 0px;
  margin-bottom: 20px;
}
</style>
