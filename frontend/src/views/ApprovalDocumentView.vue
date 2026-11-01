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
              {{ title }}
              <free-style-shimmer
                v-if="!title"
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

      <template v-if="!title">
        <v-sheet class="d-flex" style="align-self: center">
          <free-style-shimmer
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
        <button-approval-flow
          v-if="isShowButtonApproval"
          :documentName="title"
          :documentId="documentId"
          :document="documentBundle"
          @trigger="doTrigger"
        />
      </template>

      <hr size="1" color="d3d3d3" />
      <v-row no-gutters class="bg-white">
        <v-col class="bg-white text-center">
          <free-style-shimmer
            v-if="!title"
            width="72vw"
            height="104vh"
            border-radius="5px"
            color="#DCDCDC"
            class="ml-10 mt-10"
          />
          <web-viewer
            :documentId="documentId"
            :documentName="title"
            :document="documentBundle"
            :key="loader"
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
              <document-detail :documentDetail="documentDetail" :key="loader" />
            </div>
          </v-sheet>
          <!-- <div class="d-block bg-white">
            <document-detail :documentDetail="documentDetail" :key="loader" />
          </div> -->
          <!-- <hr class="mt-4 mb-4" size="1" color="#d3d3d3" /> -->
          <!-- <div class="d-block bg-white">
            <document-approval-flow :listFlow="approvalFlow" :key="loader" />
          </div> -->
          <v-sheet width="100%">
            <hr class="mt-4 mb-4" size="1" color="#d3d3d3" />
            <paragraph-shimmer
              :is-loading="isLoading"
              :lines="20"
              :random-size="true"
            />
            <div class="d-block bg-white">
              <document-approval-flow
                v-if="!isLoading"
                :listFlow="approvalFlow"
                :key="loader"
              />
            </div>
          </v-sheet>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import DocumentDetail from "@/components/approval/DocumentDetail.vue";
import DocumentApprovalFlow from "@/components/approval/DocumentApprovalFlow.vue";
import ButtonApprovalFlow from "@/components/approval/ButtonApprovalFlow.vue";
import WebViewer from "@/components/approval/WebViewer.vue";
import { ref, onMounted, defineComponent } from "vue";
import {
  getDocumentDetailMainPreview,
  getMainDocumentAllDetail,
} from "@/models/document";
import { useRouter, useRoute } from "vue-router";

defineComponent({
  DocumentDetail,
  DocumentApprovalFlow,
  ButtonApprovalFlow,
  WebViewer,
});

const dialog = ref(false);
const router = useRouter();
const route = useRoute();
const title = ref("");
const documentId = ref("");
const documentBundle = ref({});
const documentDetail = ref({});
const loader = ref(0);
const isShowButtonApproval = ref(false);
const isLoading = ref(false);
const approvalFlow = ref({});

const fetchData = () => {
  isLoading.value = true;
  getMainDocumentAllDetail(route.params.documentId).then((res) => {
    documentBundle.value = res;
    title.value = documentBundle.value.documentNameDisplay;
    documentId.value = route.params.documentId;
    getDocumentDetailMainPreview(route.params.documentId)
      .then((res) => {
        documentDetail.value = res.data;
        approvalFlow.value = res.trackingDocument;
      })
      .finally(() => {
        isLoading.value = false;
      });
  });
};

const doTrigger = () => {
  loader.value++;
  fetchData();
};

const showButtonApproval = () => {
  isShowButtonApproval.value = true;
};

const close = () => {
  router.replace({
    name: "main",
    params: {
      workspaceId: route.params.workspaceId,
      taskId: route.params.taskId,
      pageId: route.params.pageId,
    },
  });
  dialog.value = false;
};

onMounted(() => {
  fetchData();
  dialog.value = true;
});
</script>
<!-- <script>
import { defineComponent } from "vue";
import DocumentDetail from "@/components/approval/DocumentDetail.vue";
import DocumentApprovalFlow from "@/components/approval/DocumentApprovalFlow.vue";
import ButtonApprovalFlow from "@/components/approval/ButtonApprovalFlow.vue";
import WebViewer from "@/components/approval/WebViewer.vue";

export default defineComponent({
  components: {
    DocumentDetail,
    DocumentApprovalFlow,
    ButtonApprovalFlow,
    WebViewer,
  },
  data: function () {
    return {
      dialog: false,
      title: "",
      documentId: "",
      loader: 0,
      isShowButtonApproval: false,
      document: {},
    };
  },
  methods: {
    close() {
      this.$router.replace({
        name: "main",
        params: {
          workspaceId: this.$route.params.workspaceId,
          taskId: this.$route.params.taskId,
          pageId: this.$route.params.pageId,
        },
      });
      this.dialog = false;
    },
    getName(value) {
      this.title = value;
    },
    getId(value) {
      this.documentId = value;
    },
    getDocumentBundle(value) {
      this.document = value;
    },
    doTrigger() {
      this.loader++;
    },
    showButtonApproval() {
      this.isShowButtonApproval = true;
    },
  },
  mounted() {
    this.dialog = true;
  },
});
</script> -->

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
