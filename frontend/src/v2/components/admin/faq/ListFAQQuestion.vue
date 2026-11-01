<template>
  <v-expansion-panels class="mt-3" @update:model-value="onToggle">
    <v-expansion-panel>
      <v-expansion-panel-title>
        <v-row align="center">
          <v-col cols="10" class="font-weight-bold ellipsis-4">
            {{ item.questionDetail }}
          </v-col>
          <v-col cols="2" class="d-flex justify-end pr-5">
            <btn-delete
              :title="'Delete Question FAQ'"
              :description="'&nbsp;'"
              :btn-title="''"
              :btn-class="'font-weight-bold mr-2 text-12'"
              :subtitle="'Are you sure delete this Question from FAQ ?'"
              :btn-color="'#D6212A'"
              :btnVariant="'outlined'"
              :positiveTextButton="'Delete'"
              :is-icon-button="true"
              @update="deleteQuestion"
            />
            <v-btn
              class="px-4"
              style="border-radius: 6px !important"
              color="#065695"
              variant="outlined"
              prepend-icon="mdi-pencil-outline"
              @click.stop="onEdit"
            >
              Edit Answer
            </v-btn>
          </v-col>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text class="text-13">
        <div v-if="loading" class="py-2">
          <div
            class="shimmer mb-2"
            style="height: 14px; width: 90%; border-radius: 4px"
          ></div>
          <div
            class="shimmer mb-2"
            style="height: 14px; width: 85%; border-radius: 4px"
          ></div>
          <div
            class="shimmer"
            style="height: 14px; width: 60%; border-radius: 4px"
          ></div>
        </div>
        <div v-else>
          <!-- WebSocket connecting indicator -->
          <div v-if="isConnecting" class="text-center py-4">
            <!-- shimmer -->
            <div
              class="shimmer mb-2"
              style="height: 14px; width: 90%; border-radius: 4px"
            ></div>
            <div
              class="shimmer mb-2"
              style="height: 14px; width: 85%; border-radius: 4px"
            ></div>
            <div
              class="shimmer"
              style="height: 14px; width: 60%; border-radius: 4px"
            ></div>
            <!-- <span style="color: #065695; font-size: 14px"
              >Connecting to editor...</span
            > -->
          </div>

          <div
            ref="previewEditorRef"
            id="faq-preview-editor"
            class="faq-preview-content"
            style="min-height: 50px; border: none"
          ></div>
          <div class="flex flex-row items-start mt-3 gap-2">
            <span class="d-block ml-3 font-weight-bold text-grey ellipsis-4"
              >Lampiran</span
            >
            <div
              v-if="answerData?.fileName"
              class="d-flex align-center justify-space-between px-3 py-4 rounded-sm my-2 ml-2 w-33"
              style="background-color: #f5f5f5; gap: 8px"
            >
              <span>
                <v-img
                  :src="require('@/v2/assets/icon/docImage/iconPdf.svg')"
                  alt="Icon"
                  width="30"
                  height="30"
                  style="display: inline-block; vertical-align: middle"
                ></v-img>
                <span
                  class="font-weight-medium text-black text-body-2 ml-1"
                  style="word-break: break-all"
                >
                  {{
                    answerData?.fileName.length > 28
                      ? `${answerData.fileName.substring(0, 28)}...`
                      : answerData.fileName
                  }}
                </span>
              </span>
              <v-btn
                size="x-small"
                variant="text"
                class="rounded-lg flex-shrink-0"
                :loading="isDownloading"
                :disabled="isDownloading"
                style="
                  background-color: transparent;
                  box-shadow: none;
                  width: 30px;
                  height: 24px;
                  min-width: 0;
                  border-radius: 6px;
                "
                @click="downloadAttachment"
              >
                <img
                  src="/images/icon/icon-download-faq.svg"
                  alt="Download attachment"
                  width="16"
                  height="16"
                />
              </v-btn>
            </div>
            <div v-else class="my-4 mx-2">
              <span class="font-weight-medium text-caption text-grey mt-1"
                >Tidak ada lampiran</span
              >
            </div>
          </div>
        </div>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { downloadFileHelper } from "@v2/helpers/DownloadFileHelper";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits<{
  (event: "edit", payload: any): void;
  (event: "refresh"): void;
}>();

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const loading = ref(false);
const isConnecting = ref(false);
const isDownloading = ref(false);
const answerData = ref<any>(null);
const answerContent = ref("");
const previewEditorRef = ref<HTMLElement>();
let previewEditor: any = null;

const { root } = getCurrentInstance() as any;

async function fetchAnswer() {
  loading.value = true;
  try {
    const payload = {
      questionID: props.item.questionId,
    };
    const res = await store.dispatch("adminStore/getFAQAnswer", payload);

    answerData.value = res.responseData || {};

    // If we have an idAnswerEditor, wait for DOM to be ready then fetch content
    if (res.responseData?.idAnswerEditor) {
      // Wait for the expansion panel to fully expand and DOM to be ready
      fetchAnswerWithCKEditor();
    }
  } catch (err) {
    console.error("Failed to fetch answers:", err);
  } finally {
    loading.value = false;
  }
}

async function fetchAnswerMetadata() {
  if (answerData.value?.answerId != null) {
    return;
  }

  try {
    const res = await store.dispatch("adminStore/getFAQAnswer", {
      questionID: props.item.questionId,
    });
    answerData.value = res.responseData || {};
  } catch (err) {
    console.error("Failed to fetch FAQ answer metadata:", err);
  }
}

async function fetchAnswerWithCKEditor() {
  try {
    isConnecting.value = true;

    // Destroy existing editor if it exists
    if (previewEditor) {
      await previewEditor.destroy();
      previewEditor = null;
    }

    // Wait for the previewEditorRef to be available with retry logic
    let retries = 0;
    const maxRetries = 10;

    while (!previewEditorRef.value && retries < maxRetries) {
      await new Promise((resolve) => setTimeout(resolve, 100));
      retries++;
    }

    if (!previewEditorRef.value) {
      console.error("Preview editor container not available after retries");
      answerContent.value = "Editor container not ready";
      isConnecting.value = false;
      return;
    }

    // Clear the editor container
    previewEditorRef.value.innerHTML = "";

    // Basic ClassicEditor configuration for preview mode
    const config = {
      toolbar: {
        items: [], // Empty toolbar for preview mode
      },
      licenseKey: ckEditorLicense.value,
      // Disable all cloud services for preview mode
      collaboration: null,
      presenceList: null,
      cloudServices: null,
      comments: null,
      trackChanges: null,
      revisionHistory: null,
      removePlugins: [
        "RealTimeCollaborativeEditing",
        "RealTimeCollaborativeComments",
        "RealTimeCollaborativeTrackChanges",
        "RealTimeCollaborativeRevisionHistory",
        "PresenceList",
        "Comments",
        "TrackChanges",
        "RevisionHistory",
        "CloudServices",
      ],
    };

    // Create basic ClassicEditor instance
    previewEditor = await Editor.CustomClassicPlus.create(
      previewEditorRef.value,
      config
    );

    // Make editor completely read-only
    if (previewEditor) {
      previewEditor.enableReadOnlyMode("preview-mode");

      // Always fetch fresh content from storage using answerIdEditor
      const answerIdEditor = answerData.value?.idAnswerEditor;
      let contentFromStorage = "No answer provided";

      if (answerIdEditor) {
        try {
          const storageRes = await store.dispatch(
            "documentStore/fetchContentFromStorage",
            answerIdEditor
          );

          contentFromStorage =
            storageRes.responseData?.content || "No content available";
        } catch (storageError) {
          console.error("Failed to fetch content from storage:", storageError);
          contentFromStorage = "Failed to load content from storage";
        }
      }

      previewEditor.setData(contentFromStorage);
      answerContent.value = contentFromStorage;
    }

    isConnecting.value = false;
  } catch (error) {
    console.error("Failed to create basic CKEditor:", error);
    answerContent.value = "Failed to load answer content";
    isConnecting.value = false;

    // Fallback to show error message in the div
    if (previewEditorRef.value) {
      previewEditorRef.value.innerHTML = "Failed to load answer content";
    }
  }
}

function onToggle(val: any) {
  if (val !== undefined && val !== null) {
    fetchAnswer();
  }
}

function onEdit() {
  emit("edit", {
    ...props.item,
    answer: answerContent.value,
  });
}

const deleteQuestion = async () => {
  if (!props.item?.questionId) return;

  await fetchAnswerMetadata();

  const payload = {
    idQuestion: props.item.questionId,
    idAnswer: answerData.value?.answerId ?? 0,
  };

  try {
    const res = await store.dispatch("adminStore/deleteFAQQuestion", payload);
    if (res?.responseCode === "011000") {
      root.refs.toast.show({
        message: res.responseMessage || "Successfully Deleted",
        color: "success",
        timeout: 3000,
      });
      emit("refresh");
    } else {
      root.refs.toast.show({
        message: res?.responseMessage || "Failed to delete",
        color: "error",
        timeout: 3000,
      });
    }
  } catch (err) {
    console.error("Failed to delete FAQ question:", err);
    root.refs.toast.show({
      message: "Failed to delete",
      color: "error",
      timeout: 3000,
    });
  }
};

async function downloadAttachment() {
  if (!answerData.value?.fileName) {
    root.refs.toast.show({
      message: "No attachment available",
      color: "error",
      timeout: 3000,
    });
    return;
  }

  const payload = {
    answerId: answerData.value?.answerId ?? 0,
    device: "web",
  };

  isDownloading.value = true;

  try {
    const res = await store.dispatch("adminStore/downloadFAQAnswer", payload);
    downloadFileHelper(res, answerData.value.fileName);
  } catch {
    root.refs.toast.show({
      message: "Failed to download attachment",
      color: "error",
      timeout: 3000,
    });
  } finally {
    isDownloading.value = false;
  }
}

onBeforeUnmount(() => {
  if (previewEditor) {
    previewEditor.destroy();
  }
});
</script>

<style scoped>
:deep(.v-expansion-panel) {
  border-radius: 16px;
}
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 2px 4px 0px #0000001f !important;
}
:deep(.v-expansion-panel-title) {
  min-height: 60px;
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.faq-preview-content :deep(.ck-editor__main) {
  border: none !important;
}

:deep(.ck-editor) {
  border: none !important;
}

:deep(.ck-content) {
  border: none !important;
}

:deep(.ck-toolbar) {
  display: none !important;
  border: none !important;
}

:deep(.ck-toolbar-container) {
  display: none !important;
  border: none !important;
}

:deep(.ck-editor__top) {
  display: none !important;
  border: none !important;
}

.faq-preview-content :deep(.ck-editor__editable) {
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  cursor: default !important;
  pointer-events: none !important;
  outline: none !important;
}

.faq-preview-content :deep(.ck-content) {
  padding: 0 !important;
  pointer-events: none !important;
  border: none !important;
  outline: none !important;
}

.faq-preview-content :deep(.ck-widget) {
  pointer-events: none !important;
  border: none !important;
}

.faq-preview-content :deep(.ck-balloon-panel) {
  display: none !important;
}

.faq-preview-content :deep(.ck-inspector-wrapper) {
  display: none !important;
}

.faq-preview-content :deep(.ck-editor__editable:focus) {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.faq-preview-content :deep(.ck-focused) {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}
</style>
