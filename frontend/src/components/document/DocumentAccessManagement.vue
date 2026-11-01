<script setup lang="ts">
import { defineProps, mergeProps, defineEmits, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import client from "@/library/ApiClient";
import store from "@/store/index";
import { v4 as uuidv4 } from "uuid";
import CustomLoading from "@/components/CustomLoading.vue";
import CustomConfirmation from "@/components/CustomConfirmation.vue";
import EditAccessDialog from "@/components/EditAccessDialog.vue";
import EditMetadataDialog from "@/components/EditMetadataDialog.vue";
import EditMetadataDocumentDialog from "@/components/EditMetadataDocumentDialog.vue";
import SendToOtherWorkspaceDialog from "@/components/task/SendToOtherWorkspaceDialog.vue";
import { insertLog } from "@/models/log";
import {
  deleteDocumentPendukung,
  deleteDocumentUtama,
} from "@/models/document";

const props = defineProps({
  document: { type: Object, required: true },
  isOwner: { type: Boolean, required: true },
});

const router = useRouter();
const route = useRoute();
const emits = defineEmits(["action"]);
const confirmDialog = ref();
const editDialog = ref();
const editMetadata = ref();
const editMetadataDocument = ref();
const sendToOther = ref();
const actionButton: any = [
  {
    position: 0,
    name: "Preview Document",
    icon: "mdi-file-document-outline",
    color: "#065695",
    show: props.document.access.isRead,
  },
  {
    position: 0,
    name: "Download",
    icon: "mdi-cloud-download",
    color: "#065695",
    show: props.document.access.isDownload,
  },
  {
    position: 0,
    name: "See Detail",
    icon: "mdi-eye",
    color: "#065695",
    show: props.document.access.isRead,
  },
  {
    position: 0,
    name: "Edit Access",
    icon: "mdi-key",
    color: "#065695",
    show: props.isOwner,
  },
  {
    position: 0,
    name: "Edit Document",
    icon: "mdi-lead-pencil",
    color: "#065695",
    show: props.document.access.isEdit,
  },
  {
    position: 0,
    name: "Edit Metadata",
    icon: "mdi-pencil-minus-outline",
    color: "#065695",
    show: props.document.access.isEditMetadata,
  },
  {
    position: 0,
    name: "Delete Document",
    icon: "mdi-delete-forever",
    color: "#065695",
    show: props.document.access.isDeleteDoc,
  },
  {
    position: 0,
    name: "Send to Other Workspace",
    icon: "mdi-send",
    color: "#065695",
    show: props.document.access.isSendLink,
  },
];
const visibleButtonCount = countVisibleButtons(actionButton);
let positionLastButtons: any = [{}];
if (visibleButtonCount >= 4) {
  positionLastButtons = actionButton.filter((button) => button.position >= 4);
}

let isLoading = ref<boolean>(false);
let titleLoading = ref<number | string>("waiting for server respond");
let downloadProgress = ref<number | string>(0);
let documentSize = ref(props.document.size);
let hasProgress = ref(props.document.size ? true : false);

let timeStart = ref(0);
let timeEnd = ref(0);
let fileSize = ref(0);
let traceId = ref("");

const action = (name) => {
  switch (name) {
    case "Preview Document": {
      switch (props.document.typeDocument) {
        case "utama":
          router.replace({
            name: "preview-document",
            params: {
              pageId: route.params.pageId,
              workspaceId: route.params.workspaceId,
              documentId: props.document.id,
              taskId: route.params.taskId,
            },
          });
          break;
        case "pendukung":
          router.replace({
            name: "preview-document-support",
            params: {
              pageId: route.params.pageId,
              workspaceId: route.params.workspaceId,
              documentId: props.document.id,
              taskId: route.params.taskId,
            },
          });
          break;
      }
      break;
    }
    case "See Detail": {
      emits("action", {
        name: "see detail",
        value: props.document.id,
      });
      break;
    }
    case "Edit Access": {
      editDialog.value.start(props.document.name, props.document.id);
      break;
    }
    case "Send to Other Workspace": {
      sendToOther.value.start(props.document);
      break;
    }
    case "Edit Document": {
      window.open(props.document.linkEdit, "_blank")?.focus();
      break;
    }
    case "Edit Metadata": {
      if (props.document.isEditDocumentPNIN) {
        editMetadata.value.start(props.document); // This form edit for PN/IN (Sprint 6)
        break;
      } else {
        editMetadataDocument.value.start(props.document); // This form edit create or upload Non PN/IN (Sprint 7)
        break;
      }
    }
    case "Delete Document": {
      titleLoading.value = "Deleting document, please wait..";
      const deleteParams =
        props.document.name.split(".")[0] +
        "_" +
        props.document.id +
        "." +
        props.document.extension;
      switch (true) {
        case props.document.typeDocument === "pendukung":
          confirmDialog.value.start(props.document.name, {
            isDocumentPendukung: true,
            idDocument: props.document.id,
            isLinkedDocument: props.document.isLinkedDocument,
            linkedDocumentId: props.document.linkedDocumentId,
          });
          break;
        default:
          confirmDialog.value.start(deleteParams);
          break;
      }

      break;
    }
    case "Download": {
      downloadDocument(props.document.extension);
      break;
    }
    case "Download as PDF": {
      downloadDocument("pdf");
      break;
    }
    case "Download as PPT": {
      downloadDocument("pptx");
      break;
    }
  }
};

const reloadPage = () => emits("action", { name: "reload page" });

const downloadDocument = (type) => {
  traceId.value = uuidv4();
  timeStart.value = performance.now();
  isLoading.value = true;

  if (props.document.typeDocument === "pendukung") {
    downloadFromSupport(type);
  } else {
    downloadFromUtama(type);
  }
};

const downloadFromUtama = (type) => {
  client
    .DownloadDocumentById({
      store: store,
      data: {
        id: props.document.id,
        typeDocument: type,
        traceId: traceId.value,
      },
      onDownloadProgress: (progressEvent) => {
        titleLoading.value =
          "Download progress: " + formatBytes(progressEvent.loaded);
        downloadProgress.value = progressEvent.loaded;
        fileSize.value = progressEvent.loaded;
      },
    })
    .then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      const documentDownloadName =
        props.document.name.split(".")[0] + "." + type;
      link.href = url;
      link.setAttribute("download", documentDownloadName);
      document.body.appendChild(link);
      link.click();

      timeEnd.value = performance.now();
      insertLog(
        traceId.value,
        props.document.id,
        documentDownloadName,
        fileSize.value,
        timeStart.value,
        timeEnd.value,
        "DOWNLOAD DOCUMENT UTAMA"
      );
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const downloadFromSupport = (type) => {
  client
    .DownloadDocument({
      store: store,
      data: {
        id: props.document.id,
        typeDocument: type,
        traceId: traceId.value,
      },
      onDownloadProgress: (progressEvent) => {
        titleLoading.value =
          "Download progress: " + formatBytes(progressEvent.loaded);
        downloadProgress.value = progressEvent.loaded;
        fileSize.value = progressEvent.loaded;
      },
    })
    .then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      const documentDownloadName =
        props.document.name.split(".")[0] + "." + type;
      link.href = url;
      link.setAttribute("download", documentDownloadName);
      document.body.appendChild(link);
      link.click();

      timeEnd.value = performance.now();
      insertLog(
        traceId.value,
        props.document.id,
        documentDownloadName,
        fileSize.value,
        timeStart.value,
        timeEnd.value,
        "DOWNLOAD DOCUMENT SUPPORT"
      );
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const deleteDoc = (_value) => {
  isLoading.value = true;
  if (route.name == "support") {
    deleteDocumentPendukung(_value)
      .then(() => emits("action", { name: "delete", value: true }))
      .catch(() => emits("action", { name: "delete", value: false }))
      .finally(() => {
        isLoading.value = false;
      });
  } else {
    deleteDocumentUtama(_value)
      .then(() => emits("action", { name: "delete", value: true }))
      .catch(() => emits("action", { name: "delete", value: false }))
      .finally(() => {
        isLoading.value = false;
      });
  }
};

function countVisibleButtons(buttons: any): number {
  let count = 0;
  for (const button of buttons) {
    if (button.show) {
      count++;
      button.position = count;
    }
  }
  return count;
}

function formatBytes(bytes, decimals = 2) {
  if (!+bytes) return "0.00 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}
</script>

<template>
  <template v-if="visibleButtonCount > 4">
    <template v-for="(item, index) in actionButton" :key="index">
      <template v-if="item.show && item.position <= 3">
        <template v-if="item.name == 'Download' && document.canDownloadPPt">
          <v-menu>
            <template v-slot:activator="{ props: menu }">
              <v-tooltip location="top">
                <template v-slot:activator="{ props: tooltip }">
                  <v-btn
                    class="rounded-lg"
                    size="x-small"
                    icon="mdi-cloud-download"
                    color="#065695"
                    variant="outlined"
                    v-bind="mergeProps(menu, tooltip)"
                  >
                  </v-btn>
                </template>
                <span>Download as PDF / PPT</span>
              </v-tooltip>
            </template>
            <v-list>
              <v-list-item>
                <v-btn
                  class="ma-0 pa-0 pl-5 pr-5"
                  elevation="0"
                  @click="action('Download as PDF')"
                >
                  <template v-slot:prepend>
                    <v-avatar>
                      <v-icon :color="item.color">mdi-file-pdf</v-icon>
                    </v-avatar>
                    <p
                      :style="{ color: '#065695' }"
                      style="letter-spacing: -0.5px"
                    >
                      Download as PDF
                    </p>
                  </template>
                </v-btn>
              </v-list-item>
              <v-list-item>
                <v-btn
                  class="ma-0 pa-0 pl-5 pr-5"
                  elevation="0"
                  @click="action('Download as PPT')"
                >
                  <template v-slot:prepend>
                    <v-avatar>
                      <v-icon :color="item.color">mdi-file-powerpoint</v-icon>
                    </v-avatar>
                    <p
                      :style="{ color: '#065695' }"
                      style="letter-spacing: -0.5px"
                    >
                      Download as PPT
                    </p>
                  </template>
                </v-btn>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
        <template v-else>
          <v-btn
            @click="action(item.name)"
            class="rounded-lg"
            size="x-small"
            :icon="item.icon"
            :color="item.color"
            variant="outlined"
          >
            <v-icon> {{ item.icon }}</v-icon>
            <v-tooltip activator="parent" location="top">
              {{ item.name }}
            </v-tooltip>
          </v-btn>
        </template>
      </template>
    </template>

    <v-menu>
      <template v-slot:activator="{ props: menu }">
        <v-tooltip location="top">
          <template v-slot:activator="{ props: tooltip }">
            <v-btn
              class="rounded-lg"
              size="x-small"
              icon="mdi-dots-horizontal"
              color="#065695"
              variant="outlined"
              v-bind="mergeProps(menu, tooltip)"
            >
            </v-btn>
          </template>
          <span>Other</span>
        </v-tooltip>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in positionLastButtons"
          :key="index"
          class="ma-0 pa-0"
        >
          <v-btn
            class="ma-0 pa-0 pl-5 pr-5"
            elevation="0"
            @click="action(item.name)"
          >
            <template v-slot:prepend>
              <v-avatar>
                <v-icon :color="item.color">{{ item.icon }}</v-icon>
              </v-avatar>
              <p :style="{ color: item.color }" style="letter-spacing: -0.5px">
                {{ item.name }}
              </p>
            </template>
          </v-btn>
        </v-list-item>
      </v-list>
    </v-menu>
  </template>
  <template v-else>
    <template v-for="(item, index) in actionButton" :key="index">
      <template v-if="item.show">
        <v-btn
          @click="action(item.name)"
          class="rounded-lg"
          size="x-small"
          :icon="item.icon"
          :color="item.color"
          variant="outlined"
        >
          <v-icon> {{ item.icon }}</v-icon>
          <v-tooltip activator="parent" location="top">
            {{ item.name }}
          </v-tooltip>
        </v-btn></template
      >
    </template>
  </template>

  <!-- START Loading Section -->
  <!-- <custom-loading v-if="isLoading" /> -->
  <custom-loading
    v-if="isLoading"
    :title="titleLoading"
    :progress="downloadProgress"
    :totalProgress="documentSize"
    :hasProgress="hasProgress"
  />
  <!-- END Loading Section -->

  <!-- START Loading Section -->
  <custom-confirmation @deleteDoc="deleteDoc" ref="confirmDialog" />
  <!-- END Loading Section -->

  <edit-access-dialog
    ref="editDialog"
    :documentType="document.typeDocument"
    @reload="reloadPage"
  />

  <edit-metadata-dialog
    ref="editMetadata"
    :documentType="'support'"
    @reload="reloadPage"
  />

  <edit-metadata-document-dialog
    ref="editMetadataDocument"
    :documentType="'support'"
    @reload="reloadPage"
  />

  <!-- START Send to Other WPC -->
  <send-to-other-workspace-dialog ref="sendToOther" />
  <!-- END Send to Other WPC -->
</template>
