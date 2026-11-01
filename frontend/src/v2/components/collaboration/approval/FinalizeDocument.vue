<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" max-width="750" persistent>
      <v-card class="border-radius-dwp h-100">
        <v-card-title class="d-flex mt-3 justify-center align-center">
          <div class="pb-1 text-left text-darkBlue font-weight-bold">
            Finalized Document
          </div>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onclose"
          />
        </v-card-title>
        <hr class="line my-3 d-block pb-1" />
        <v-card-text>
          <Steppy v-model:step="step" :tabs="tabs">
            <template #1>
              <v-row>
                <v-col :cols="12">
                  <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                    Pengaju<span class="text-danger">*</span>
                  </p>
                  <SearchBar
                    v-model="state.pengaju"
                    :items="props.searchItem"
                    :showSearchIcon="false"
                    :isRequired="true"
                    :error-messages="v$.pengaju.$errors.map((e) => e.$message)"
                  />
                </v-col>
                <v-col :cols="12">
                  <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                    Penyetuju<span class="text-danger">*</span>
                  </p>
                  <SearchBar
                    v-model="state.penyetuju"
                    :items="props.searchItem"
                    :showSearchIcon="false"
                    :isRequired="true"
                    :error-messages="
                      v$.penyetuju.$errors.map((e) => e.$message)
                    "
                  />
                </v-col>
              </v-row>
            </template>
            <template #2>
              <v-row>
                <v-col :cols="12">
                  <div class="warning-banner">
                    <v-icon
                      icon="mdi-alert"
                      color="#957100"
                      class="warning-icon my-auto"
                    />
                    <div
                      class="warning-text text-12 text-left my-auto py-1 ml-n1"
                    >
                      Once you upload this document, it will become the final
                      version and can no longer be edited
                    </div>
                  </div>
                </v-col>
                <v-col :cols="12">
                  <FileDragable
                    v-model="file"
                    :formatFile="['.pdf']"
                    maxSizeLabel="10 MB"
                    :loadingPercent="loadingPercent"
                    :isDashedBorder="false"
                    :backgroundColor="bgColor"
                    borderColor="#065695"
                  >
                    <template #clear-icon="{ clearForm }">
                      <v-icon
                        icon="mdi-close"
                        color="#065391"
                        style="
                          position: absolute;
                          top: 10px;
                          right: 12px;
                          cursor: pointer;
                          z-index: 2;
                        "
                        @click="clearForm"
                      />
                    </template>
                  </FileDragable>
                  <p
                    v-if="showFileError && (!file || !file.file)"
                    class="text-12 text-danger text-left pl-0"
                  >
                    File harus di-upload
                  </p>
                  <p
                    v-else-if="showFileError && !isPdfFile"
                    class="text-12 text-danger text-left pl-0"
                  >
                    File harus berformat PDF
                  </p>
                  <p
                    v-else-if="showFileError && !isFileSizeValid"
                    class="text-12 text-danger text-left pl-0"
                  >
                    Ukuran file tidak boleh lebih dari 10 MB
                  </p>
                </v-col>
              </v-row>
            </template>
          </Steppy>
        </v-card-text>
        <v-card-actions class="mt-n4 justify-end mb-3">
          <v-btn
            v-if="step === 1"
            elevation="3"
            class="btn-cancel"
            @click="onclose"
            :loading="onLoading"
          >
            Cancel
          </v-btn>
          <v-btn
            v-else
            elevation="3"
            class="btn-cancel"
            @click="backStep"
            :loading="onLoading"
          >
            Back
          </v-btn>
          <v-btn
            v-if="step !== tabs.length"
            @click="nextStep"
            elevation="3"
            type="submit"
            class="ml-2 rounded-lg font-weight-bold primary-gradient py-2 mr-2 px-5"
            :loading="onLoading"
          >
            Next
          </v-btn>
          <v-btn
            v-else
            @click="submitDocument"
            type="submit"
            class="ml-2 rounded-lg font-weight-bold primary-gradient mr-2 py-2 px-5"
            :loading="onLoading"
          >
            Finalized
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import SearchBar from "@v2/components/utils/dialog/SearchBar.vue";
import { Steppy } from "vue3-steppy";
import { TFileDragable } from "@v2/Type.d";
import useVuelidate from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import FileDragable from "@v2/components/utils/form/FileDragable.vue";

type SearchItem = {
  value: string;
  id: string;
  type: string;
  department: string;
};

const props = defineProps<{
  searchItem: SearchItem[] | undefined;
  idBpdoc: string | string[];
}>();

const store = useStore();
const instance = ref<any>(getCurrentInstance()?.root.refs);

const dialog = ref<boolean>(false);
const step = ref<number>(1);
const isLoading = ref<boolean>(false);
const file = ref<TFileDragable | undefined>(undefined);
const loadingPercent = ref<number>(0);
const showFileError = ref<boolean>(false);
const maxFileSize = 10 * 1024 * 1024;

const bgColor = computed(() => {
  return file.value?.file ? "#e9f5ff" : "#f5f5f5";
});

const isFileSizeValid = computed(() => {
  return (file.value?.file?.size ?? 0) <= maxFileSize;
});

const isPdfFile = computed(() => {
  if (!file.value?.file) return true;
  const fileName = file.value.file.name.toLowerCase();
  return fileName.endsWith(".pdf");
});

const state = ref({
  pengaju: null as string | number | null,
  penyetuju: null as any,
});

const rules = {
  pengaju: {
    required: helpers.withMessage("Pengaju harus dipilih", required),
  },
  penyetuju: {
    required: helpers.withMessage("Penyetuju harus dipilih", required),
  },
};

const v$ = useVuelidate(rules, state);

const disableAllApprovalButton = computed(() => {
  return store.getters["collaborationStore/getDisableAllApprovalButton"];
});

const onLoading = computed(() => {
  return isLoading.value || disableAllApprovalButton.value;
});
const tabs = computed(() => {
  return [
    {
      title: "Assign",
      iconSuccess: null,
      isValid: true,
    },
    {
      title: "Upload",
      iconSuccess: null,
      isValid: true,
    },
  ];
});

async function nextStep() {
  const isValid = await v$.value.$validate();
  if (!isValid) return;
  if (step.value === tabs.value.length) return;
  step.value++;
}

const backStep = () => {
  if (step.value === 1) return;

  step.value--;
};

function showDialog() {
  loadingPercent.value = 0;
  step.value = 1;
  dialog.value = true;
}

function onclose() {
  dialog.value = false;
  v$.value.$reset();
  showFileError.value = false;
  state.value = {
    pengaju: null,
    penyetuju: null,
  };
  file.value = undefined;
}

async function submitDocument() {
  const isValid = await v$.value.$validate();
  if (!isValid) return;

  showFileError.value = true;
  if (!file.value || !file.value.file) return;
  if (!isPdfFile.value) return;
  if (!isFileSizeValid.value) return;

  isLoading.value = true;

  const selectedFile = file.value.file;
  const extension = selectedFile.name.split(".").pop() ?? "";
  const name = selectedFile.name.split(".")[0] ?? "";

  const formData = new FormData();
  formData.append(
    "idBpdoc",
    Array.isArray(props.idBpdoc)
      ? String(props.idBpdoc[0] ?? "")
      : String(props.idBpdoc)
  );
  formData.append("IdMUserPengaju", String(state.value.pengaju ?? ""));
  formData.append("IdMUserPenyetuju", String(state.value.penyetuju ?? ""));
  formData.append("file", selectedFile);
  formData.append("size", String(selectedFile.size));
  formData.append("extension", extension);
  formData.append("title", name);

  store
    .dispatch("eFormStore/uploadFinalizedDoc", {
      request: formData,
      onUploadProgress: (progressEvent: any) => {
        var percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        loadingPercent.value = percent;
      },
    })
    .then((res) => {
      store.dispatch("documentStore/checkStatusAsyncDocument", {
        id: Array.isArray(props.idBpdoc)
          ? String(props.idBpdoc[0] ?? "")
          : String(props.idBpdoc),
        type: "approval",
      });
      onclose();

      nextTick(() => {
        //harcode dulu, nunggu identifier yang fix dari BE
        store.commit("collaborationStore/setDocumentVersion", "Version 2");
      });
    })
    .catch((error) => {
      loadingPercent.value = 0;
      instance.value.toast.show({
        message:
          error.response?.data?.responseMessage ??
          "Failed to upload finalized document",
        timeout: 1000,
        color: "error",
      });
    })
    .finally(() => {
      isLoading.value = false;
    });
}

defineExpose({ showDialog, onclose });
</script>

<style lang="scss" scoped>
:deep(.steppy) {
  margin-left: 35%;
  margin-right: 35%;
}

:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding: 25px 10px 0px 10px !important;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  margin: 30px 0 0 0 !important;
  padding: 25px 0 !important;
}
:deep(.steppy-item.success .steppy-item-counter) {
  border: 8px solid #267dc2 !important;
}

:deep(.steppy-item-counter) {
  height: 20px !important;
  width: 20px !important;
  border: 5px solid grey !important;
  background-color: white !important;
}

:deep(.current .steppy-item-counter) {
  border: 5px solid #065695 !important;
}

:deep(.steppy-item.success .steppy-item-counter .icon-success) {
  width: 15px !important;
  height: 15px !important;
  fill: white !important;
  background-color: #267dc2 !important;
  border-radius: 50% !important;
}

:deep(.steppy-item-title) {
  font-size: 14px !important;
  font-weight: 900 !important;
  color: #3a416f !important;
  white-space: nowrap !important;
}

:deep(.steppy-progress) {
  background: #d9d9d9 !important;
  height: 3px !important;
}

:deep(.steppy-progress-bar) {
  background: #267dc2 !important;
  height: 3px !important;
}

:deep(.wrapper-steppy > .controls) {
  display: none;
}

.btn-cancel {
  background: linear-gradient(#fff -46.47%, #fff 157.9%);
  border-radius: 10px;
  font-weight: 800;
  color: #065695 !important;
}

.line {
  border: none;
  height: 3px;
  margin: 16px 0;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.warning-banner {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background-color: #fef3c7;
  border-radius: 6px;
  padding: 12px 16px;
  margin-bottom: 16px;
}

.warning-icon {
  font-size: 20px;
  flex-shrink: 0;
  color: #d97706;
}

.warning-text {
  font-size: 14px;
  color: #957100;
  line-height: 1.5;
  margin: 0;
}
</style>
