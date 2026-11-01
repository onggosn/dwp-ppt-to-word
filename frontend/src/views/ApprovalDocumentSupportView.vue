<template>
  <v-dialog v-model="dialog" fullscreen persistent>
    <v-card>
      <div class="d-block">
        <v-row no-gutters>
          <v-col cols="1">
            <v-sheet class="pt-5 pb-5 text-end">
              <v-btn
                variant="outlined"
                size="large"
                icon="mdi-arrow-left"
                color="#045695"
                style="border: 0.5px solid #d3d3d3"
                elevation="3"
                @click="close()"
              >
              </v-btn>
            </v-sheet>
          </v-col>
          <v-col style="align-self: center">
            <v-sheet
              class="ma-2 pa-2 font-weight-bold text-18"
              style="color: #045695"
            >
              {{ documentName }}
              <free-style-shimmer
                v-if="!documentName"
                width="72vw"
                height="4vh"
                border-radius="5px"
                color="#DCDCDC"
              />
            </v-sheet>
          </v-col>
        </v-row>
      </div>
      <hr size="1" color="d3d3d3" />
      <template v-if="isLoading">
        <v-sheet class="d-flex" style="align-self: center"
          ><free-style-shimmer
            v-for="n in 3"
            :key="n"
            width="13vw"
            height="6vh"
            border-radius="5px"
            color="#DCDCDC"
            class="pa-3"
          />
        </v-sheet>
      </template>
      <template v-else>
        <button-support-approval-flow
          v-if="isShowButtonApproval"
          :document="document"
          :isNonApproval="approvalFlow?.length == 1"
          @refreshWebviewer="refreshWebviewer"
        />
      </template>

      <hr size="1" color="d3d3d3" />
      <v-row no-gutters class="bg-white">
        <v-col class="bg-white text-center">
          <free-style-shimmer
            v-if="!document"
            width="72vw"
            height="104vh"
            border-radius="5px"
            color="#DCDCDC"
            class="ml-10 mt-10"
          />

          <web-viewer-support
            :document="document"
            :key="webviewer_loader"
            @onSuccess="showButtonApproval"
            v-else
          />
        </v-col>
        <v-col
          cols="3"
          style="border-left: 1px solid #d3d3d3; max-width: 20vw"
          class="bg-white pl-4 pt-4 pr-2"
        >
          <v-sheet width="100%" class="list-detail">
            <paragraph-shimmer
              :is-loading="isLoading"
              :lines="20"
              :random-size="true"
            />
            <div class="d-block bg-white" v-if="!isLoading">
              <document-support-detail :listData="detail" />
            </div>
          </v-sheet>

          <v-sheet width="100%">
            <hr class="mt-4 mb-4" size="1" color="#d3d3d3" />
            <paragraph-shimmer
              :is-loading="isLoading"
              :lines="20"
              :random-size="true"
            />
            <div class="d-block bg-white">
              <document-support-approval-flow
                v-if="!isLoading"
                :listFlow="approvalFlow"
              />
            </div>
          </v-sheet>
        </v-col>
      </v-row>

      <progress-step
        v-if="progressStep.length"
        :listProgress="progressStep"
        @refresh="refreshWebviewer"
      />
    </v-card>
    <Toast ref="toast" />
  </v-dialog>
</template>

<script setup lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import DocumentSupportDetail from "@/components/approval/DocumentSupportDetail.vue";
import DocumentSupportApprovalFlow from "@/components/approval/DocumentSupportApprovalFlow.vue";
import WebViewerSupport from "@/components/approval/WebViewerSupport.vue";
import ButtonSupportApprovalFlow from "@/components/approval/ButtonSupportApprovalFlow.vue";
import ProgressStep from "@/components/approval/ProgressStep.vue";
import { useRouter, useRoute } from "vue-router";
import {
  getDocumentDetailSupportPreview,
  getDocumentAllDetail,
} from "@/models/document";
import Toast from "@/components/utils/ToastComponent.vue";

defineComponent({
  DocumentSupportDetail,
  DocumentSupportApprovalFlow,
  WebViewerSupport,
  ButtonSupportApprovalFlow,
  ProgressStep,
});

const router = useRouter();
const route = useRoute();
const toast = ref();

const dialog = ref(false);
// const loader = ref(0);
const loaderStep = ref(0);
const webviewer_loader = ref(0);
const isShowButtonApproval = ref(false);

const detail = ref([]);
const approvalFlow = ref([]);
const progressStep = ref([]);
const documentName = ref("");
const documentSize = ref(0);
const document = ref();
const isLoading = ref(false);

const close = () => {
  router.replace({
    name: "support",
    params: {
      workspaceId: route.params.workspaceId,
      taskId: route.params.taskId,
      pageId: route.params.pageId,
    },
  });
  dialog.value = false;
};

onMounted(() => {
  dialog.value = true;
  isLoading.value = true;
  getDocumentAllDetail(route.params.documentId).then((result) => {
    document.value = result;
    documentName.value = result.documentNameDisplay;
    documentSize.value = result.sizeDocument ?? 0;
    getDocumentDetailSupportPreview(route.params.documentId).then((result) => {
      detail.value = result.data;
      approvalFlow.value = result.trackingDocument;
      progressStep.value = result.trackingStepDocument;
      isLoading.value = false;
    });
  });
});

const refreshWebviewer = () => {
  isLoading.value = true;
  getDocumentAllDetail(route.params.documentId).then((result) => {
    document.value = result;
    documentName.value = result.documentNameDisplay;
    documentSize.value = result.sizeDocument ?? 0;
    getDocumentDetailSupportPreview(route.params.documentId).then((result) => {
      detail.value = result.data;
      approvalFlow.value = result.trackingDocument;
      progressStep.value = result.trackingStepDocument;
      loaderStep.value++;
      isLoading.value = false;
    });
  });
};

const showButtonApproval = () => {
  isShowButtonApproval.value = true;
};
</script>

<style scoped>
.list-detail {
  overflow-x: hidden !important;
  overflow-y: auto !important;
  max-height: 60vh !important;
}
.text-blue-theme {
  color: #3a416f;
}

.v-list-item__content .v-list-item-title :deep() {
  color: red;
}
</style>
