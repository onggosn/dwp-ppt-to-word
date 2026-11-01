<template>
  <div class="d-flex justify-center align-baseline ma-5" style="gap: 1rem">
    <template v-for="(item, index) in listButton" :key="index">
      <v-btn
        @click="action(item.buttonLabel, item)"
        :class="getStyles(item.buttonLabel)"
      >
        {{ item.buttonLabel }}
      </v-btn>
    </template>

    <template v-if="isApprovalInProgress">
      <p class="text-approval-in-progress">Approval In Progress...</p>
    </template>

    <template v-else-if="isUploadInProgress">
      <p class="text-approval-in-progress">Upload In Progress...</p>
    </template>

    <template v-else-if="isButtonEmpty">
      <v-btn @click="action('Download')" class="sectionBlue-button ma-2">
        Download
      </v-btn>
      <v-btn @click="action('Go to workspace')" class="sectionBlue-button ma-2">
        Go to workspace
      </v-btn>
    </template>

    <custom-loading
      v-if="isLoading"
      :title="bandwithSpend"
      :progress="downloadProgress"
      :totalProgress="sizeDocument"
      :hasProgress="hasProgress"
    />

    <custom-confirmation @deleteDoc="deleteDoc" ref="confirmDialog" />
  </div>
</template>

<script setup lang="ts">
import client from "@/library/ApiClient";
import store from "@/store/index";
import CustomLoading from "@/components/CustomLoading.vue";
import CustomConfirmation from "@/components/CustomConfirmation.vue";
import { deleteDocumentPendukung } from "@/models/document";
import { mGetApprovalButton, mApproveDocumentSupport } from "@/models/approval";
import {
  ref,
  defineComponent,
  onMounted,
  defineEmits,
  defineProps,
  getCurrentInstance,
} from "vue";
import { useRoute, useRouter } from "vue-router";

const props = defineProps({
  document: Object,
});

defineComponent({ CustomLoading, CustomConfirmation });

const route = useRoute();
const router = useRouter();
const instance = getCurrentInstance()?.root.refs;
const listButton = ref([]);
const isLoading = ref(false);
const isButtonEmpty = ref(false);
const isApprovalInProgress = ref(false);
const isUploadInProgress = ref(false);
const confirmDialog = ref();
const emits = defineEmits(["deleteDoc", "refreshWebviewer"]);
const bandwithSpend = ref("waiting for server response");
const hasProgress = ref(false);
const downloadProgress = ref(0);
const sizeDocument = ref(0);
const fileSize = ref(0);

onMounted(() => {
  fetchData();
});

const fetchData = () =>
  mGetApprovalButton(route.params.documentId).then((response) => {
    switch (response.responseCode) {
      case "011000":
        listButton.value = response.responseData;
        isButtonEmpty.value = response.responseData.length === 0;
        break;
      case "011033":
        isApprovalInProgress.value = true;
        break;
      case "011037":
        isUploadInProgress.value = true;
        break;
    }
  });

const getStyles = (label) => {
  switch (label) {
    case "Send":
      return "sectionBlue-button ma-2";
    case "Delete":
      return "sectionRed-button ma-2";
    case "Edit":
      return "sectionBlue-button ma-2";
    case "Approve":
      return "sectionBlue-button ma-2";
    case "Reject":
      return "sectionRed-button ma-2";
    default:
      return "sectionBlue-button ma-2";
  }
};

const action = (label, item) => {
  switch (label) {
    case "Send":
      return proceedFile(item, "Send");
    case "Delete":
      return remove();
    case "Edit":
      return editFile(item.linkEdit);
    case "Approve":
      return proceedFile(item, "Approve");
    case "Reject":
      return proceedFile(item, "Reject");
    case "Download":
      return downloadFile();
    default:
      return gotoWorkspace();
  }
};

const proceedFile = (item, actionName) => {
  isLoading.value = true;
  bandwithSpend.value = "Please wait..";
  mApproveDocumentSupport(item, route.params.documentId)
    .then((response) => {
      switch (response.ResponseCode) {
        case "011000": {
          showToast(actionName);
          setTimeout(() => {
            fetchData();
          }, 1000);
          break;
        }
        default: {
          showToast("Error", "error");
          break;
        }
      }
    })
    .finally(() => {
      isLoading.value = false;
      bandwithSpend.value = "waiting for server response";
    });
};

const remove = () => {
  confirmDialog.value.start(props.document.documentNameDisplay, {
    isDocumentPendukung: true,
    idDocument: route.params.documentId,
    isLinkedDocument: false,
    linkedDocumentId: "",
  });
};

const editFile = (link) => {
  window.open(link, "_blank").focus();
};

const deleteDoc = (_value) => {
  isLoading.value = true;
  deleteDocumentPendukung(_value)
    .then(() => {
      showToast("Delete");
      gotoWorkspace();
    })
    .catch(() => {
      showToast("Error", "error");
      undefined;
    })
    .finally(() => {
      this.isLoading.value = false;
    });
};

const downloadFile = () => {
  let type = getFileExtension(props.document.documentNameDisplay);
  isLoading.value = true;
  client
    .DownloadDocument({
      store: store,
      data: {
        id: route.params.documentId,
        typeDocument: type,
        traceId: "",
      },
      onDownloadProgress: (progressEvent) => {
        bandwithSpend.value =
          "Download progress: " + formatBytes(progressEvent.loaded);
        downloadProgress.value = progressEvent.loaded;
        fileSize.value = progressEvent.loaded;
      },
    })
    .then((response) => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", props.document.documentNameDisplay);
      document.body.appendChild(link);
      link.click();
    })
    .finally(() => {
      isLoading.value = false;
      bandwithSpend.value = "waiting for server response";
    });
};

const getFileExtension = (filename: string): string | null => {
  const parts = filename.split(".");
  if (parts.length > 1) {
    return parts[parts.length - 1];
  } else {
    return null;
  }
};

const formatBytes = (bytes, decimals = 2) => {
  if (!+bytes) return "0.00 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};

const gotoWorkspace = () => {
  router.replace({
    name: "support",
    params: {
      workspaceId: route.params.workspaceId,
      taskId: route.params.taskId,
      pageId: route.params.pageId,
    },
  });
};

const showToast = (message, state = "success") => {
  switch (message) {
    case "Send":
      message = "Document has been sent";
      break;
    case "Approve":
      message = "Document has been approved";
      break;
    case "Reject":
      message = "Document has been rejected";
      break;
    case "Error":
      message = "Something went wrong";
      state = "error";
      break;
    case "Delete":
      message = "Document has been deleted";
      break;
    default:
      message = "Something went wrong";
      state = "warning";
      break;
  }

  instance.toast.show({
    message: message,
    color: state,
    timeout: 3000,
    icon: "mdi-check",
  });

  if (["success"].includes(state)) {
    emits("refreshWebviewer", true);
  }
};
</script>

<style scoped>
.text-approval-in-progress {
  color: var(--place-holder, #babcca);
  text-align: center;
  font-family: Poppins;
  font-size: 15px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

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
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
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
