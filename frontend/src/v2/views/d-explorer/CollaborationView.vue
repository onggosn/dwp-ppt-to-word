<template>
  <v-sheet
    class="pl-10 pt-3 pb-3 d-flex justify-space-between align-center"
    style="background: #e0efff"
  >
    <div class="d-flex align-center">
      <v-btn
        density="default"
        icon="mdi-arrow-left"
        style="color: #267dc2"
        :to="{
          name: 'v2.workspace-rdg-detail',
          params: { typeRDG: 'rdgb', idEvent: idEvent },
        }"
      ></v-btn>
      <p class="ml-3 font-weight-bold text-18" style="color: #267dc2">
        {{ eventName }}
      </p>
    </div>
    <div>
      <ApprovalSection
        v-if="hasForms"
        :key="documentFlowCheck"
        :isDocSec="isDocument2d"
      />
    </div>
  </v-sheet>
  <div class="container">
    <div class="left-side text-end">
      <alert-manage-workplace :data="detailData" v-if="canSeeAlert" />
      <chip-status-form :key="loaderChip" />
      <import-ppt-button
        v-if="canImportPPT"
        :idBPDocument="idDoc"
        :is-disable="isDisableImportPPT"
      ></import-ppt-button>
      <v-btn
        size="small"
        variant="outlined"
        style="border-radius: 10px"
        color="#065695"
        @click="download('docx')"
        :loading="downloadLoading"
        class="mr-2"
        v-if="canExportWord"
      >
        Export
        <v-tooltip activator="parent" location="top">Export Word</v-tooltip>
        <template v-slot:prepend>
          <img
            :src="require('@/v2/assets/icon/icon-export.svg')"
            class="mb-1"
          />
        </template>
      </v-btn>
      <select-status-version v-if="canSeeVersion" />
      <update-aiu-otomatis v-if="isCanUpdateAiu" @refresh="reloadDocument" />
      <edit-access-form
        v-if="accessStatus || accessStatusFinal"
        :isFinal="accessStatusFinal"
        :isRisalahDoc="isRisalahDoc"
      />

      <v-btn
        size="small"
        variant="outlined"
        style="border-radius: 10px"
        color="#065695"
        @click="editForm"
        :loading="isLoading"
        v-if="canEdit"
      >
        Edit E-Form
        <template v-slot:prepend>
          <img :src="require('@/v2/assets/icon/edit.svg')" />
        </template>
      </v-btn>

      <v-btn
        size="small"
        variant="outlined"
        style="border-radius: 10px"
        color="#065695"
        @click="download('pdf')"
        :loading="downloadLoading"
        prepend-icon="mdi-download"
        class="mr-2"
        v-if="canDownload"
      >
        Download
      </v-btn>

      <preview-button v-if="canPreview" />
      <preview-PDF-button v-if="canPreviewPDF" />
      <work-sheet :key="idDoc" />
    </div>
    <div class="right-side">
      <div id="sidebar-forrevision" class="sidebar-revision"></div>
      <!-- style="min-height: calc(100vh - 2rem)" -->
      <v-card
        class="mx-auto overflow-auto toc mt-4"
        height="calc(100vh - 2rem)"
        id="tableofcontent"
      >
        <div
          class="d-flex justify-space-between mb-6 align-center mx-4 mt-3 align-start"
        >
          <p class="font-weight-bold">Content</p>
          <div class="d-flex" style="gap: 8px">
            <div v-if="isDocument2d || listTabMetadata.length">
              <ButtonMetadataSectoral :key="idDoc" />
            </div>
            <div v-else>
              <ButtonMetadata :key="idDoc" />
            </div>
            <BtnCreate @refreshToc="refreshDataToc" />
          </div>
        </div>
        <v-divider />
        <TableOfContent
          :onRegisterRefresh="setRefreshFunction"
          @refreshToc="refreshDataToc"
          :key="reloadToc"
        />
      </v-card>
    </div>
  </div>
  <LoadingDownload
    v-if="downloadLoading"
    :title="bandwidthSpend"
  ></LoadingDownload>
</template>

<script lang="ts" setup>
/* eslint-disable */
import { ref, computed, onMounted, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import EditAccessForm from "@v2/components/collaboration/EditAccessForm.vue";
import UpdateAiuOtomatis from "@v2/components/collaboration/UpdateAiuOtomatis.vue";
import TableOfContent from "@v2/components/contentManagement/TableOfContent.vue";
import BtnCreate from "@v2/components/contentManagement/BtnCreate.vue";
import ButtonMetadata from "@v2/components/contentManagement/ButtonMetadata.vue";
import ButtonMetadataSectoral from "@v2/components/contentManagement/ButtonMetadataSectoral.vue";
import ApprovalSection from "@v2/components/collaboration/approval/ApprovalSection.vue";
import ChipStatusForm from "@v2/components/collaboration/ChipStatusForm.vue";
import PreviewButton from "@v2/components/collaboration/PreviewButton.vue";
import PreviewPDFButton from "@v2/components/collaboration/PreviewPDFButton.vue";
import WorkSheet from "@v2/components/collaboration/WorkSheet.vue";
import SelectStatusVersion from "@v2/components/collaboration/SelectStatusVersion.vue";
import AlertManageWorkplace from "@v2/components/collaboration/AlertManageWorkplace.vue";
import LoadingDownload from "@/v2/components/utils/dialog/LoadingDownload.vue";
import ImportPptButton from "@/v2/components/collaboration/ImportPptButton.vue";
import { secureRandomFloat } from "@/v2/helpers/utils";
import PreviewWordButton from "@/v2/components/collaboration/PreviewWordButton.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();
const { root } = getCurrentInstance() as any;
const isLoading = ref(false);
const idEvent = computed(() => route.params.idEvent as string);
const idDoc = computed(() => route.params.idDoc as string);
const typeRDG = computed(() => route.params.typeRDG as string);

const bandwidthSpend = computed(
  () => store.getters["documentStore/getLabelProgress"]
);
const downloadProgress = computed(
  () => store.getters["documentStore/getLoadingProgress"]
);
const eventName = computed(
  () => store.getters["collaborationStore/getEventName"]
);
const documentFlowCheck = computed(
  () => store.getters["collaborationStore/getDocumentFlowCheck"]
);
const loaderChip = computed(
  () => store.getters["collaborationStore/getLoaderChip"]
);
const accessStatus = computed(
  () => store.getters["collaborationStore/getAccessStatus"]
);
const accessStatusFinal = computed(
  () => store.getters["collaborationStore/getaccessStatusFinal"]
);
const reloadToc = computed(() => store.getters["contentStore/getReloadToc"]);
const documentStatusId = computed(
  () => store.getters["collaborationStore/getDocumentStatusId"]
);
const canDownload = computed(
  () =>
    ![29].includes(documentStatusId.value) &&
    store.getters["collaborationStore/getDownloadCondition"]
);
const isCanUpdateAiu = computed(
  () => store.getters["collaborationStore/getUpdateAiu"]
);
const isDocument2d = computed(
  () => store.getters["collaborationStore/getDocumentSectoral"]
);
const documentType = computed(
  () => store.getters["collaborationStore/getDocumentTypeId"]
);
const isRisalahDoc = computed(() => documentType.value === 9);
const hasForms = computed(
  () =>
    store.getters["collaborationStore/getListForm"]?.length > 0 ||
    store.getters["collaborationStore/getListForm"]?.length != ""
);
const canEdit = computed(() => store.getters["collaborationStore/getStartDoc"]);
const canPreview = computed(
  () => store.getters["collaborationStore/getPreviewDoc"]
);

const canPreviewPDF = computed(
  () => store.getters["collaborationStore/getPreviewPDF"]
);

const canExportWord = computed(
  () => store.getters["collaborationStore/getExportWord"]
);

const canImportPPT = computed(
  () => store.getters["collaborationStore/getImportPPT"]
);

const isDisableImportPPT = computed(
  () => store.getters["collaborationStore/getDisableImportPPT"]
);

const canSeeVersion = computed(
  () =>
    ![29].includes(documentStatusId.value) &&
    store.getters["collaborationStore/getButtonVersion"]
);

const canSeeReasonReject = computed(() => {
  return store.getters["collaborationStore/getReasonReject"];
});

const listTabMetadata = computed(
  () => store.getters["collaborationStore/getListTabMetadata"]
);

const canSeeAlert = computed(
  () =>
    (store.getters["collaborationStore/getReasonCancel"] != null &&
      (store.getters["collaborationStore/getFlagAlertCancel"] ||
        store.getters["collaborationStore/getFlagAlertAiu"])) ||
    (["AIU", "Policy Note", "Issue Note"].includes(
      detailData.value.isTypeDoc
    ) &&
      detailData.value.isReason) ||
    canSeeReasonReject.value
);

const detailData = computed(() => ({
  isCancel: store.getters["collaborationStore/getFlagAlertCancel"],
  isReason:
    store.getters["collaborationStore/getReasonCancel"] ||
    canSeeReasonReject.value,
  isTypeDoc: store.getters["collaborationStore/getAlartLabelCancel"],
  isDelete: store.getters["collaborationStore/getFlagAlertAiu"],
}));

const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);

const downloadLoading = ref(false);

const download = (param) => {
  downloadLoading.value = true;
  const payload = {
    id: idDoc.value,
    exportType: param,
  };
  store
    .dispatch("documentStore/downloadDocument", payload)
    .then((res) => {
      if (Object.keys(res).length === 0) {
        root.refs.toast.show({
          message:
            "Document is in the process of uploading:There was an error in the system, please contact the admin",
          color: "oopss",
          timeout: 5000,
        });
      } else {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(new Blob([res.data]));
        link.setAttribute("download", `${documentName.value}.${param}`);
        document.body.appendChild(link);
        link.click();
      }
    })
    .catch(() => {
      root.refs.toast.show({
        message: "Download file expired",
        color: "oopss",
        timeout: 5000,
      });
    })
    .finally(() => (downloadLoading.value = false));
};

const getContentPlaceholder = async (type) => {
  downloadLoading.value = true;

  const payload = {
    DocumentId: idDoc.value,
    DocumentType: type,
  };

  store
    .dispatch("documentStore/getContentPlaceholder", payload)
    .then((res) => {
      if (Object.keys(res).length === 0) {
        root.refs.toast.show({
          message:
            "Document is in the process of uploading:There was an error in the system, please contact the admin",
          color: "oopss",
          timeout: 5000,
        });
      } else {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(
          new Blob([res.data], { type: res.headers["content-type"] })
        );
        link.setAttribute("download", `${documentName.value}.${type}`);
        document.body.appendChild(link);
        link.click();
      }
    })
    .catch((e) => {
      root.refs.toast.show({
        message: "Download file expired",
        color: "oopss",
        timeout: 5000,
      });
    })
    .finally(() => (downloadLoading.value = false));
};

function editForm() {
  isLoading.value = true;
  const reqData = { idBpDoc: idDoc.value };
  store
    .dispatch("eFormStore/updateBPDocStatusById", reqData)
    .then(() => {
      store.commit("collaborationStore/setStartEditEForm", false);
      store.commit(
        "collaborationStore/setDocumentFlowCheck",
        secureRandomFloat()
      );
      store.commit("collaborationStore/setLoaderChip", secureRandomFloat());
      reloadDocument();
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function reloadDocument() {
  store.dispatch("documentStore/fetchFormDocument", idDoc.value);
}

onMounted(() => {
  if (!["rdgb", "rdgtk"].includes(typeRDG.value.toLowerCase())) {
    router.push({ name: "v2.rdgb" });
  }
});

const refreshDataToc = ref<((...args: any[]) => any) | undefined>(undefined);
const setRefreshFunction = (refreshFunction) => {
  refreshDataToc.value = refreshFunction;
};
</script>

<style scoped>
.sidebar-revision {
  background: white;
  border-radius: 5px 15px 15px 5px;
  position: sticky;
  top: 1rem;
  z-index: 0;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.5);
  height: calc(100vh - 2rem);
  display: none;
}

.toc {
  border-radius: 5px 15px 15px 5px;
  position: sticky;
  top: 1rem;
  z-index: 0;
}
.container {
  padding-left: 20px;
  display: flex;
  width: 100%;
}

.left-side {
  background-color: transparent;
  padding: 20px;
  font-size: 1rem;
  z-index: 10;
  height: 100vh;
  overflow-y: auto;
  padding-right: 5px;
}

/* .left-side:hover {
  overflow-y: auto;
  padding-right: 5px;
} */

.right-side {
  background-color: transparent;
  padding: 3px;
  margin-bottom: 18px;
  font-size: 1rem;
}

@media (min-width: 1600px) {
  .left-side {
    width: 60vw;
  }

  .right-side {
    width: 40vw;
  }
}

@media (min-width: 1400px) and (max-width: 1599px) {
  .left-side {
    width: 65vw;
  }

  .right-side {
    width: 35vw;
  }
}

@media (min-width: 1300px) and (max-width: 1399px) {
  .left-side {
    width: 70vw;
  }

  .right-side {
    width: 30vw;
  }
}

@media (min-width: 768px) and (max-width: 1299px) {
  .left-side {
    width: 80vw;
  }
  .right-side {
    width: 20vw;
  }
}

/* For screens that are 767px or narrower */
@media (max-width: 767px) {
  .right-side {
    width: 100%;
  }
}

::-webkit-scrollbar {
  width: 5px !important;
}
</style>
<style>
.ck-content p:not(li p) {
  margin-top: var(--ck-spacing-large);
  margin-bottom: var(--ck-spacing-large);
}
</style>
