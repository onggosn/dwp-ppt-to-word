<template>
  <div class="d-inline">
    <v-btn
      size="small"
      variant="outlined"
      style="border-radius: 10px"
      color="#065695"
      class="mr-2"
      type="file"
      :disabled="isDisable || !buttonState"
      @click="handleUpload"
    >
      Import
      <template v-slot:prepend>
        <img :src="require('@/v2/assets/icon/icon-import.svg')" class="mb-1" />
      </template>
      <input
        ref="uploadFileInput"
        type="file"
        class="d-none upload-center"
        accept=".pptx,application/vnd.openxmlformats-officedocument.presentationml.presentation"
        @change="onSelectFile"
      />
    </v-btn>

    <v-tooltip v-if="!isDisable" activator="parent" location="top"
      >Import</v-tooltip
    >

    <v-tooltip v-if="isDisable" activator="parent" location="bottom"
      >Destination Mapping is not available.<br />
      Configure it in the Admin Management menu before importing
      documents</v-tooltip
    >
  </div>
  <template v-if="progress > 0">
    <LoadingProgressBar ref="modal">
      <template v-slot:footer-loading v-if="progress >= 100"
        >Just a bit longer, we're almost there!. The PPT is currently being
        extracted...
        <v-progress-circular
          class="ml-1"
          color="#3c8bcb"
          size="small"
          indeterminate
          style="width: 15px"
        ></v-progress-circular
      ></template>
    </LoadingProgressBar>
  </template>
  <ModalConfirm
    ref="modalConfirm"
    :form-config="dialogConfig"
    :is-warning="true"
    @action-confirm="actionConfirm"
  >
    <template v-slot:icon-img>
      <v-avatar
        style="margin-top: -50px; filter: drop-shadow(#9b9b9b 1px 1px 1.5px)"
        size="90"
        :image="require('@v2/assets/icon/icon-yellow-warning.svg')"
      ></v-avatar>
    </template>
  </ModalConfirm>
  <ModalConfirm
    ref="modalConfirmSelect"
    @action-confirm="actionConfirm"
    @action-cancel="handleCancel"
    :form-config="dialogSelectConfig"
  >
    <template v-slot:icon-img>
      <v-avatar
        color="white"
        size="80"
        style="margin-top: -60px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img src="/images/checkNotif2.png" style="width: 75px" />
      </v-avatar>
    </template>
    <template v-slot:btn-action>
      <div>
        <v-btn
          class="ml-2 rounded-lg btn mr-2 btn-replaced"
          :loading="isLoading"
          @click="onUploadFile('Replaced')"
        >
          Replaced
        </v-btn>
        <v-btn
          class="primary-gradient rounded-lg"
          :loading="isLoading"
          @click="onUploadFile('Append')"
        >
          Append
        </v-btn>
      </div>
    </template>
  </ModalConfirm>
  <ModalConfirm ref="modalErrorImport" :form-config="dialogConfigErrorImport">
    <template v-slot:icon-img>
      <v-row class="mt-2 text-left">
        <v-col cols="1" class="mt-1">
          <img src="/images/icon/iconWarningCircle.svg" style="width: 50px" />
        </v-col>
        <v-col class="ml-6">
          <span class="text-24 font-weight-500">Oops</span><br />
          <span class="text-14"
            >Data yang anda gunakan tidak valid atau belum lengkap.<br />Silahkan
            lengkapi terlebih dahulu, berikut detailnya.</span
          >
        </v-col>
      </v-row>
    </template>
    <template v-slot:desc>
      <div class="text-left ml-2">
        <div v-for="(error, index) in errorDetails" :key="index" class="mb-4">
          <div class="text-14 font-weight-bold ml-1 d-flex align-center">
            <v-icon color="error" size="small" class="mr-2"
              >mdi-alert-circle</v-icon
            >
            Slide {{ error.slideNumber }}
            <v-chip
              v-if="error.sectionName"
              size="small"
              color="#227cc4"
              variant="outlined"
              class="ml-2"
            >
              {{ error.sectionName }}
            </v-chip>
          </div>
          <div
            class="text-14 font-weight-500 pa-3 mt-2"
            style="border-radius: 12px; background-color: #ffebee"
          >
            {{ error.message }}
          </div>
        </div>

        <div class="mt-4 pa-3 rounded-lg" style="background-color: #f5f5f5">
          <v-icon color="warning" class="mr-2">mdi-information</v-icon>
          <span class="text-14 font-weight-medium">
            Total {{ errorDetails.length }} error(s) found in PowerPoint import
          </span>
        </div>
      </div>
    </template>
    <template v-slot:btn-action>
      <v-btn
        class="primary-gradient rounded-lg"
        :loading="isLoading"
        @click="handleClose()"
      >
        Close
      </v-btn>
    </template>
  </ModalConfirm>
</template>
<script lang="ts" setup>
import { ref, computed, defineProps, getCurrentInstance, nextTick } from "vue";
import LoadingProgressBar from "@/v2/components/loading/LoadingProgressBar.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { useStore } from "vuex";
import type { TModalConfirm, TDialogError } from "@v2/Type.d";

const uploadFileInput = ref<HTMLInputElement | null>(null);
const isLoading = ref<boolean>(false);
const { root } = getCurrentInstance() as any;
const props = defineProps({
  idBPDocument: {
    type: String,
    default: "",
  },
  isDisable: {
    type: Boolean,
    default: false,
  },
});

const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);

const dialogConfig = ref<TModalConfirm>({
  title: "Oops",
  message:
    "Unsupported file format. Please upload a<br> PowerPoint file with a .pptx extension",
  btnSubmitLabel: "Close",
  usingTimeOut: true,
  btnSubmitColor: "primary-gradient",
  icon: {
    typeImage: "@v2/assets/icon/icon-yellow-warning.svg",
  },
});
const dialogSelectConfig = ref<TModalConfirm>({
  title: "Import",
  message: "Should the submit data be appended or replaced?",
  usingTimeOut: false,
});

const modalConfirmSelect = ref();
const fileUpload = ref<File | null>(null);
const store = useStore();
const progress = computed(() => {
  return store.getters["loadingStore/getProgress"];
});

const handleUpload = () => {
  uploadFileInput.value?.click();
};

const onSelectFile = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files && target.files[0];
  if (file) {
    const isPptx = file.name.toLowerCase().endsWith(".pptx");
    const maxSize = 150 * 1024 * 1024; // 150MB
    if (!isPptx) {
      modalConfirmSelect.value.hide();
      modalConfirm.value.show({}, 0);
      target.value = "";
      return;
    } else if (file.size > maxSize) {
      modalConfirmSelect.value.hide();
      dialogConfig.value.message =
        "Sorry, your file is too large. Maximum upload size <br>is 150 MB.";
      modalConfirm.value.show({}, 0);
      target.value = "";
      return;
    } else {
      fileUpload.value = file;
      modalConfirmSelect.value.show({}, 0);
    }
  }
};

function onUploadFile(type: string) {
  isLoading.value = true;
  nextTick(() => {
    modalConfirmSelect.value.hide();
  });
  store
    .dispatch("documentStore/importPpt", {
      request: {
        idBPDocument: props.idBPDocument,
        typeAction: type,
        documentFile: fileUpload.value,
      },
      onUploadProgress: (progressEvent: any) => {
        var percent = Math.round(
          (progressEvent.loaded * 100) / (fileUpload.value?.size || 1)
        );
        store.dispatch("loadingStore/updateProgress", percent);
      },
    })
    .then((res) => {
      if (res.responseCode === "011054") {
        //error slide
        if (Array.isArray(res.responseData)) {
          errorDetails.value = res.responseData.map((error: any) => ({
            slideNumber: error.slideNumber,
            message: error.message,
            sectionName: error.sectionName || "",
          }));
        } else {
          errorDetails.value = [
            {
              slideNumber: res.responseData?.slideNumber || 0,
              message: res.responseData?.message || "Unknown error",
              sectionName: res.responseData?.sectionName || "",
            },
          ];
        }

        dialogConfigErrorImport.value.slideNumber =
          errorDetails.value.length > 1
            ? `Multiple Slides (${errorDetails.value.length} errors)`
            : `Slide ${errorDetails.value[0]?.slideNumber || "Unknown"}`;

        dialogConfigErrorImport.value.message =
          errorDetails.value.length > 1
            ? `${errorDetails.value.length} errors found in PowerPoint import`
            : errorDetails.value[0]?.message || "Unknown error";

        modalErrorImport.value.show({});
      } else if (res.responseCode === "011000") {
        //success import
        store.dispatch("documentStore/fetchDocumentStatus", props.idBPDocument);
        root.refs.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 5000,
        });

        errorDetails.value = [];
      } else if (res.responseCode === "011055") {
        //error max upload file
        dialogConfig.value.title = "Oops";
        dialogConfig.value.message =
          "Sorry, your file is too large. Maximum upload size <br>is 150 MB.";
        modalConfirm.value.show({}, 0);
      } else if (res.responseCode === "011056") {
        //error salah template
        dialogConfig.value.title = "Oops";
        dialogConfig.value.message = "PPT file must follow the template";
        modalConfirm.value.show({}, 0);
      } else {
        root.refs.toast.show({
          message: res.responseMessage,
          color: "error",
          timeout: 5000,
        });
      }
    })
    .catch(() => {
      dialogConfig.value.title = "Import Failed";
      dialogConfig.value.message =
        "The file could not be imported due to a system issue.<br>Please try again later.";
      modalConfirm.value.show({}, 0);

      errorDetails.value = [];
    })
    .finally(() => {
      modalConfirmSelect.value.hide();
      if (uploadFileInput.value) {
        uploadFileInput.value.value = "";
      }
      isLoading.value = false;
      store.dispatch("loadingStore/updateProgress", 0);
    });
}

const modalConfirm = ref();
const actionConfirm = () => {
  modalConfirm.value.hide();
};
const handleCancel = () => {
  if (uploadFileInput.value) {
    uploadFileInput.value.value = "";
  }
  fileUpload.value = null;
};

const modalErrorImport = ref();
const dialogConfigErrorImport = ref<TDialogError>({
  width: 700,
  slideNumber: "",
  message: "",
  sectionName: "",
});
const handleClose = () => {
  modalErrorImport.value.hide();
  errorDetails.value = [];
};

const errorDetails = ref<
  Array<{
    slideNumber: number;
    message: string;
    sectionName: string;
  }>
>([]);
</script>

<style>
.btn-replaced {
  color: #065695;
}

.error-item {
  border-left: 4px solid #ff5722;
  transition: background-color 0.2s ease;
}

.error-item:hover {
  background-color: #ffebee !important;
}

.error-container {
  max-height: 400px;
  overflow-y: auto;
}

.error-container::-webkit-scrollbar {
  width: 6px;
}

.error-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.error-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.error-container::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}
</style>
