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
          Opening your form, please wait...
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
          Edit Answer
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

          <!-- Loading state for fetching data -->
          <div
            v-if="isLoadingData"
            class="px-6 py-6 mb-4 text-center"
            style="border: 1px solid #e0e0e0; border-radius: 8px"
          >
            <v-progress-circular
              indeterminate
              color="#065695"
              size="24"
              class="mr-3"
            ></v-progress-circular>
            <span style="color: #065695">Loading question details...</span>
          </div>

          <div
            v-else
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
                  @input="questionError = ''"
                ></v-textarea>
              </v-card>
              <div v-if="questionError" class="text-red text-caption mt-1 ml-3">
                {{ questionError }}
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
              <div v-if="answerError" class="text-red text-caption mt-1 ml-3">
                {{ answerError }}
              </div>
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
  item: {
    type: Object,
    default: () => ({ question: "", answer: "" }),
  },
});

const emit = defineEmits(["update:modelValue", "save", "refresh"]);

const store = useStore();
const dialog = ref(false);
const isLoading = ref(false);
const isConnecting = ref(false);
const isLoadingData = ref(false);
const editableItem = ref({ question: "", answer: "" });
const editorRef = ref<HTMLElement>();
const presenceListRef = ref<HTMLElement>();
const characterCount = ref(0);
const faqEditorID = ref("");
const faqQuestionId = ref<number | null>(null);
const faqAnswerId = ref<number | null>(null);
const questionError = ref("");
const answerError = ref("");
let editorInstance: any = null;

watch(
  () => props.modelValue,
  async (val) => {
    dialog.value = val;
    if (val) {
      // Fetch fresh data from API
      await fetchAnswerDetails();
      nextTick(() => {
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

// Clear answer error when user types in editor
watch(
  () => editableItem.value.answer,
  () => {
    answerError.value = "";
  }
);

async function fetchAnswerDetails() {
  if (!props.item?.questionId) return;

  isLoadingData.value = true;
  try {
    const payload = {
      questionID: props.item.questionId,
    };

    const res = await store.dispatch("adminStore/getFAQAnswer", payload);

    if (res && res.responseData) {
      editableItem.value = {
        question: res.responseData.questionDetail || props.item?.question || "",
        answer: props.item?.answer || "", // Keep existing answer from props since API doesn't return answer content
      };

      // Store IDs from API response
      faqQuestionId.value = res.responseData.questionId ?? null;
      faqAnswerId.value = res.responseData.answerId ?? null;

      // Store the answer editor ID for potential future use
      if (res.responseData.idAnswerEditor) {
        faqEditorID.value = res.responseData.idAnswerEditor;
      }
    }
  } catch (error) {
    console.error("Failed to fetch answer details:", error);
    // Use fallback data from props if API fails
    editableItem.value = {
      question: props.item?.question || "",
      answer: props.item?.answer || "",
    };
  } finally {
    isLoadingData.value = false;
  }
}

async function initEditor() {
  if (editorInstance) return;
  if (!editorRef.value) return;

  isConnecting.value = true;

  try {
    // Use the channel ID from API response if available, otherwise generate new one
    const channelId = faqEditorID.value || uuidv4();

    // Get configuration from utils
    const config = getEditorFAQConfig(store, channelId);

    // Set dynamic values
    config.initialData = editableItem.value.answer;
    config.presenceList.container = presenceListRef.value ?? null;

    editorInstance = await Editor.CustomClassicPlus.create(
      editorRef.value,
      config
    );

    // Only update faqEditorID if it wasn't set from API
    if (!faqEditorID.value) {
      faqEditorID.value = channelId;
    }

    const updateCharCount = () => {
      const data = editorInstance.getData();
      editableItem.value.answer = data;
      const plainText = data.replace(/<[^>]*>/g, "");
      characterCount.value = plainText.length;
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
  dialog.value = false;
}

async function save() {
  if (isLoading.value) return;

  // Clear previous errors
  questionError.value = "";
  answerError.value = "";

  let hasError = false;

  // Validate mandatory fields
  if (!editableItem.value.question.trim()) {
    questionError.value = "Question is required";
    hasError = true;
  }

  if (!editableItem.value.answer.trim()) {
    answerError.value = "Answer is required";
    hasError = true;
  }

  // If there are validation errors, don't proceed
  if (hasError) {
    return;
  }

  isLoading.value = true;

  try {
    const payload = {
      QuestionId: faqQuestionId.value,
      AnswerId: faqAnswerId.value,
      QuestionDetail: editableItem.value.question,
      IdAnswerEditor: faqEditorID.value,
    };

    const res: any = await store.dispatch("adminStore/editFAQAnswer", payload);

    if (res.responseCode === "011000") {
      root.refs.toast.show(LabelToast(res.responseMessage).success);
      emit("save", editableItem.value);
      emit("refresh");
      close();
    } else {
      root.refs.toast.show(LabelToast(res.responseMessage).oopss);
    }
  } catch (err: any) {
    console.error("Error updating FAQ question:", err);
    const errMessage =
      err.response?.data?.responseMessage || "Failed to update FAQ question";
    root.refs.toast.show(LabelToast(errMessage).oopss);
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
