<template>
  <!-- Loading Dialog -->
  <v-dialog v-model="isLoading" persistent width="300">
    <v-card color="#065695" dark>
      <v-card-text class="pt-3 white--text text-center text-white">
        Sending data...
        <v-progress-linear
          indeterminate
          color="white"
          class="mb-0 mt-2"
        ></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- WebSocket Connecting Dialog -->
  <v-dialog v-model="isConnecting" persistent width="350">
    <v-card color="#065695" dark>
      <v-card-text class="pt-3 white--text text-center text-white">
        <div class="d-flex align-center justify-center mb-3">
          <v-icon class="mr-2">mdi-page-next-outline</v-icon>
          Creating your form, please wait...
        </div>
        <div class="shimmer-container">
          <div class="shimmer-line"></div>
          <div class="shimmer-line"></div>
          <div class="shimmer-line"></div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>

  <v-dialog
    v-model="dialog"
    width="850"
    persistent
    z-index="2000"
    :retain-focus="false"
    no-click-animation
  >
    <v-card class="rounded-lg pa-4">
      <v-card-title class="d-flex justify-center align-center py-4 relative">
        <h3 class="text-h6 font-weight-bold" style="color: #065695">
          Add Question
        </h3>
        <v-btn
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="close"
          style="position: absolute; right: 6px; top: -5px; color: #828282"
        />
      </v-card-title>

      <div class="mb-5 separator-gradient"></div>

      <v-card-text class="pa-0">
        <fieldset class="form-section">
          <legend>General</legend>

          <div
            class="px-6 py-6 mb-4"
            style="border: 1px solid #e0e0e0; border-radius: 8px"
          >
            <!-- Question Field -->
            <div class="mb-5">
              <p
                class="pb-2 text-left font-weight-medium"
                style="color: #065695"
              >
                Question<span class="text-red">*</span>
              </p>
              <v-card class="rounded-lg" elevation="1">
                <v-textarea
                  v-model="editableItem.question"
                  variant="solo"
                  density="default"
                  hide-details="auto"
                  placeholder="Input Question"
                  rows="1"
                  max-rows="5"
                  auto-grow
                  class="my-input"
                  @input="v$.question.$touch()"
                ></v-textarea>
              </v-card>
              <div
                v-if="v$.question.$error"
                class="text-red text-caption mt-1 ml-3"
              >
                {{ v$.question.$errors[0].$message }}
              </div>
            </div>

            <!-- Answer Field -->
            <div class="mb-4">
              <p
                class="pb-2 text-left font-weight-medium"
                style="color: #065695"
              >
                Answer<span class="text-red">*</span>
              </p>
              <v-card class="rounded-lg overflow-hidden" elevation="1">
                <div class="editor-wrapper">
                  <div
                    ref="editorRef"
                    id="faq-editor"
                    style="z-index: 1000"
                  ></div>
                  <div
                    ref="presenceListRef"
                    id="presence-list-container"
                    style="visibility: hidden; display: none"
                  ></div>
                </div>
              </v-card>
              <div
                v-if="v$.answer.$error"
                class="text-red text-caption mt-1 ml-3"
              >
                {{ v$.answer.$errors[0].$message }}
              </div>
            </div>

            <div>
              <p class="pb-2 text-left font-weight-medium text-dark">
                Lampiran
              </p>

              <div
                v-if="documentFileName"
                class="d-flex align-center justify-space-between px-3 py-2 rounded-sm mb-2"
                style="background-color: #f5f5f5; gap: 8px"
              >
                <span>
                  <v-img
                    :src="require('@/v2/assets/icon/docImage/iconPdf.svg')"
                    alt="Icon"
                    width="20"
                    height="20"
                    style="display: inline-block; vertical-align: middle"
                  ></v-img>
                  <span
                    class="font-weight-medium text-black text-body-2 ml-2"
                    style="word-break: break-all"
                  >
                    {{ documentFileName }}
                  </span>
                </span>
                <v-btn
                  size="x-small"
                  variant="text"
                  class="rounded-lg flex-shrink-0"
                  style="
                    background-color: transparent;
                    box-shadow: none;
                    width: 24px;
                    height: 24px;
                    min-width: 0;
                    border-radius: 6px;
                  "
                  :disabled="!documentFileName"
                  @click="removeDocumentFile"
                >
                  <v-icon color="black" size="16">mdi-close</v-icon>
                </v-btn>
              </div>

              <input
                ref="documentFileInput"
                type="file"
                accept="application/pdf,.pdf"
                style="display: none"
                @change="handleDocumentFileChange"
              />

              <div class="">
                <v-btn
                  variant="outlined"
                  class="text-capitalize rounded-lg"
                  style="
                    color: #065695;
                    border-color: #065695;
                    letter-spacing: 0.1px;
                  "
                  prepend-icon="mdi-paperclip"
                  :disabled="!!documentFileName"
                  @click="triggerDocumentFileInput"
                >
                  Lampirkan File
                </v-btn>
              </div>
              <span class="text-caption text-grey mt-1"
                >Please upload a .pdf file with a maximum size of 10 MB</span
              >
            </div>
          </div>
        </fieldset>
      </v-card-text>

      <v-card-actions class="justify-end px-6 pb-6 pt-0 mt-4">
        <v-btn
          class="btn-prev px-5"
          height="40"
          width="80"
          elevation="2"
          @click="close"
        >
          Cancel
        </v-btn>
        <v-btn
          class="btn-next px-5"
          height="40"
          width="80"
          variant="flat"
          elevation="2"
          @click="save"
          :loading="isLoading"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, onBeforeUnmount, nextTick, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import useVuelidate from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { getEditorFAQConfig } from "@/v2/helpers/utils";
import { v4 as uuidv4 } from "uuid";
import ToastLabel from "@/v2/label/LabelToast";

const { LabelToast } = ToastLabel;
const { root } = getCurrentInstance() as any;

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  idTopic: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue", "save", "refresh"]);

const store = useStore();
const dialog = ref(false);
const isLoading = ref(false);
const isConnecting = ref(false);
const editableItem = ref({ question: "", answer: "" });
const editorRef = ref<HTMLElement>();
const presenceListRef = ref<HTMLElement>();
const documentFileInput = ref<HTMLInputElement | null>(null);
const documentFile = ref<File | null>(null);
const documentFileName = ref<string | null>(null);
const documentFileBinary = ref<number[] | null>(null);
const characterCount = ref(0);
const faqEditorID = ref("");
const MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024;

const rules = {
  question: {
    required: helpers.withMessage("Question is required", required),
  },
  answer: {
    required: helpers.withMessage("Answer is required", (value: string) => {
      const plainText = (value || "")
        .replace(/<[^>]*>/g, "")
        .replace(/&nbsp;/g, " ")
        .trim();

      return plainText.length > 0;
    }),
  },
};

const v$ = useVuelidate(rules, editableItem);

let editorInstance: any = null;

watch(
  () => props.modelValue,
  (val) => {
    dialog.value = val;
    if (val) {
      editableItem.value = {
        question: "",
        answer: "",
      };
      resetDocumentFile();
      nextTick(() => {
        v$.value.$reset();
        initEditor();
      });
    } else {
      destroyEditor();
    }
  }
);

watch(dialog, (val) => {
  emit("update:modelValue", val);
});

async function initEditor() {
  if (editorInstance) return;
  if (!editorRef.value) return;

  isConnecting.value = true;

  try {
    const channelId = uuidv4();

    // Get configuration from utils
    const config = getEditorFAQConfig(store, channelId);

    // Set dynamic values
    config.initialData = editableItem.value.answer;
    config.presenceList.container = presenceListRef.value ?? null;

    editorInstance = await Editor.CustomClassicPlus.create(
      editorRef.value,
      config
    );

    faqEditorID.value = channelId;

    const updateCharCount = () => {
      const data = editorInstance.getData();
      editableItem.value.answer = data;
      const plainText = data.replace(/<[^>]*>/g, "");
      characterCount.value = plainText.length;

      if (v$.value.answer.$dirty) {
        v$.value.answer.$touch();
      }
    };

    editorInstance.model.document.on("change:data", updateCharCount);
    updateCharCount();

    // Hide connecting dialog when editor is ready
    isConnecting.value = false;
  } catch (error) {
    console.error("CKEditor initialization failed:", error);
    isConnecting.value = false;
    root.refs.toast.show(
      LabelToast("Failed to connect to the editor. Please try again.").oopss
    );
    close();
  }
}

function destroyEditor() {
  if (editorInstance) {
    editorInstance.destroy().then(() => {
      editorInstance = null;
    });
  }
}

onBeforeUnmount(() => {
  destroyEditor();
});

function close() {
  resetDocumentFile();
  v$.value.$reset();
  dialog.value = false;
}

function resetDocumentFile() {
  documentFile.value = null;
  documentFileName.value = null;
  documentFileBinary.value = null;
  if (documentFileInput.value) {
    documentFileInput.value.value = "";
  }
}

function triggerDocumentFileInput() {
  documentFileInput.value?.click();
}

function handleDocumentFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  if (!target.files || target.files.length === 0) return;

  const file = target.files[0];

  if (file.size > MAX_FILE_SIZE_BYTES) {
    root.refs.toast.show(
      LabelToast("File size must be less than or equal to 10 MB").oopss
    );
    resetDocumentFile();
    return;
  }

  const isPdfMime = file.type === "application/pdf";
  const isPdfExt = file.name.toLowerCase().endsWith(".pdf");

  if (!isPdfMime && !isPdfExt) {
    root.refs.toast.show(LabelToast("Only PDF files are allowed").oopss);
    if (documentFileInput.value) {
      documentFileInput.value.value = "";
    }
    return;
  }

  documentFile.value = file;
  documentFileName.value = file.name;

  const reader = new FileReader();
  reader.onload = (e) => {
    const result = e.target?.result as ArrayBuffer;
    documentFileBinary.value = Array.from(new Uint8Array(result));
  };
  reader.readAsArrayBuffer(file);
}

function removeDocumentFile() {
  resetDocumentFile();
}

function appendDocumentToFormData(formData: FormData) {
  if (!documentFileBinary.value) return;

  const binaryArray = new Uint8Array(documentFileBinary.value);
  const blob = new Blob([binaryArray], {
    type: documentFile.value?.type || "application/octet-stream",
  });

  formData.append("DocumentFile", blob, documentFile.value?.name || "file");
}

function createFAQQuestionFormData() {
  const formData = new FormData();
  formData.append("IdTopic", props.idTopic);
  formData.append("QuestionText", editableItem.value.question);
  formData.append("IdAnswerEditor", faqEditorID.value);
  appendDocumentToFormData(formData);

  return formData;
}

function handleAddQuestionResponse(res: any) {
  if (res.responseCode === "011000") {
    root.refs.toast.show(LabelToast(res.responseMessage).success);
    emit("save", editableItem.value);
    emit("refresh");
    close();
    return;
  }

  if (res.responseCode === "011064") {
    root.refs.toast.show(LabelToast("File too large").oopss);
    return;
  }

  root.refs.toast.show(LabelToast(res.responseMessage).oopss);
}

async function save() {
  if (isLoading.value) return;

  const isValid = await v$.value.$validate();
  if (!isValid) return;

  isLoading.value = true;

  try {
    const formData = createFAQQuestionFormData();

    const res: any = await store.dispatch(
      "adminStore/addFAQTopicQuestion",
      formData
    );
    handleAddQuestionResponse(res);
  } catch (error: any) {
    console.error("Error adding FAQ question:", error);
    const errorMessage =
      error.response?.data?.responseMessage || "Failed to add FAQ question";
    root.refs.toast.show(LabelToast(errorMessage).oopss);
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.form-section {
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 20px;
  color: #4b4b4b;
}

.form-section legend {
  padding: 0 10px;
  font-weight: 600;
  font-size: 14px;
}
.relative {
  position: relative;
}

.editor-wrapper :deep(.ck-editor__editable) {
  min-height: 250px;
  border: none !important;
  box-shadow: none !important;
}

.editor-wrapper :deep(.ck-toolbar) {
  border-top: none !important;
  border-left: none !important;
  border-right: none !important;
  border-bottom: 1.5px solid #e0e0e0 !important;
  background-color: #fff !important;
}

.btn-next {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px !important;
  color: white !important;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: none;
}

.btn-prev {
  background: white;
  border-radius: 10px !important;
  color: #267dc2 !important;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: none;
}

:deep(.v-field--variant-solo) {
  box-shadow: none !important;
  border-radius: 10px;
}

:deep(.v-field__input) {
  min-height: 48px;
}

:deep(.ck.ck-editor__top .ck-sticky-panel .ck-sticky-panel__content) {
  border-bottom: 1.5px solid #e0e0e0 !important;
  border: none !important;
}

:deep(.ck .ck-evaluation-badge__label) {
  display: none !important;
}

.text-red {
  color: #f44336;
}

/* Shimmer Loading Animation */
.shimmer-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px 0;
}

.shimmer-line {
  height: 8px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.5) 50%,
    rgba(255, 255, 255, 0.2) 100%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: shimmer 1.5s ease-in-out infinite;
}

.shimmer-line:nth-child(1) {
  width: 80%;
}

.shimmer-line:nth-child(2) {
  width: 60%;
  animation-delay: 0.2s;
}

.shimmer-line:nth-child(3) {
  width: 90%;
  animation-delay: 0.4s;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

:deep(.ck-content figure.table:not(.layout-table) > table > tbody > tr > td) {
  border: 1px solid hsl(0, 0%, 75%) !important;
}
</style>
