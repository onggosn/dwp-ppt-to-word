<template>
  <v-expansion-panels
    class="ma-3 mb-5 elevation-0"
    @update:model-value="onToggle"
  >
    <v-expansion-panel :value="item.idQuestion">
      <v-expansion-panel-title>
        <template v-slot:actions="{ expanded }">
          <v-icon
            color="#1387df"
            icon="mdi-minus"
            class="pa-5"
            style="background: #c3d8e8; border-radius: 50%"
            v-if="expanded"
          ></v-icon>
          <v-icon
            icon="mdi-plus"
            class="pa-5"
            style="background: #f7f6f4; border-radius: 50%"
            v-else
          ></v-icon>
        </template>
        <p class="text-blueTheme font-weight-bold">
          {{ item.question || "-" }}
        </p>
      </v-expansion-panel-title>

      <v-expansion-panel-text
        class="ml-5 pa-3 text-blueTheme font-weight-medium"
      >
        <div v-if="loading && !isFetched" class="py-2">
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

        <div v-show="!loading || isFetched">
          <div
            ref="previewEditorRef"
            class="faq-preview-content"
            style="min-height: 50px; border: none"
          ></div>
        </div>
        <div class="flex flex-row items-start mt-3 gap-2">
          <span class="d-block ml-3 font-weight-bold text-darkBlue ellipsis-4"
            >Lampiran</span
          >
          <div
            v-if="filename"
            class="d-flex align-center justify-space-between px-3 py-2 rounded-sm my-2 ml-2 w-33"
            style="background-color: #f5f5f5; gap: 8px"
          >
            <span>
              <v-img
                :src="require('@/v2/assets/icon/docImage/iconPdf.svg')"
                alt="Icon"
                width="40"
                height="40"
                style="display: inline-block; vertical-align: middle"
              ></v-img>
              <span
                class="font-weight-medium text-black text-body-2 ml-2"
                style="word-break: break-all"
              >
                {{
                  filename.length > 25
                    ? `${filename.substring(0, 25)}...`
                    : filename
                }}
              </span>
            </span>
            <v-btn
              size="x-small"
              variant="text"
              class="rounded-lg flex-shrink-0"
              style="
                background-color: transparent;
                box-shadow: none;
                width: 30px;
                height: 24px;
                min-width: 0;
                border-radius: 6px;
              "
              :loading="isDownloading"
              :disabled="isDownloading"
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
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, nextTick, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { downloadFileHelper } from "@v2/helpers/DownloadFileHelper";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const loading = ref(false);
const previewEditorRef = ref<HTMLElement>();
let previewEditor: any = null;
const isFetched = ref(false);
const { root } = getCurrentInstance() as any;
//download attachment
const filename = ref<string>("");
const isDownloading = ref<boolean>(false);
const answerData = ref<any>(null);

async function destroyEditor() {
  if (previewEditor) {
    try {
      await previewEditor.destroy();
    } catch (e) {
      console.warn("Editor destroy error:", e);
    }
    previewEditor = null;
  }
  if (previewEditorRef.value) {
    previewEditorRef.value.innerHTML = "";
  }
}

async function fetchAnswerWithCKEditor() {
  // Always start fresh: destroy any existing editor first
  await destroyEditor();

  isFetched.value = false;
  loading.value = true;

  try {
    // Wait for the previewEditorRef to be available with retry logic
    let retries = 0;
    const maxRetries = 10;

    while (!previewEditorRef.value && retries < maxRetries) {
      await new Promise((resolve) => setTimeout(resolve, 100));
      retries++;
    }

    if (!previewEditorRef.value) {
      loading.value = false;
      return;
    }

    // Always create a brand-new editor instance on each expand
    const config = {
      toolbar: {
        items: [], // Empty toolbar for preview mode
      },
      licenseKey: ckEditorLicense.value,
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

    previewEditor = await Editor.CustomClassicPlus.create(
      previewEditorRef.value,
      config
    );

    if (previewEditor) {
      previewEditor.enableReadOnlyMode("preview-mode");
    }

    // Fetch fresh content from storage
    const idAnswerEditor = props.item?.idAnswerEditor;
    let contentFromStorage = "No answer provided";

    if (idAnswerEditor) {
      try {
        const storageRes = await store.dispatch(
          "documentStore/fetchContentFromStorage",
          idAnswerEditor
        );
        contentFromStorage =
          storageRes.responseData?.content || "No content available";
      } catch (storageError) {
        console.error("Failed to fetch content from storage:", storageError);
        contentFromStorage = "Failed to load content from storage";
      }
    }

    if (previewEditor) {
      previewEditor.setData(contentFromStorage);
      isFetched.value = true;
    }
  } catch (error) {
    console.error("Failed to create CKEditor preview:", error);
    if (previewEditorRef.value) {
      previewEditorRef.value.innerHTML = "Failed to load answer content";
    }
  } finally {
    loading.value = false;
  }
}

async function fetchAnswer() {
  try {
    const res = await store.dispatch("userStore/getAnswer", {
      IdQuestion: props.item.idQuestion,
    });
    answerData.value = res.responseData || null;
    filename.value = res.responseData?.fileName || "";
  } catch (err) {
    console.error("Failed to fetch FAQ answer metadata:", err);
  }
}

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
    answerId: answerData.value?.idAnswer ?? 0,
    device: "web",
  };

  isDownloading.value = true;

  try {
    const res = await store.dispatch("adminStore/downloadFAQAnswer", payload);
    downloadFileHelper(res, answerData.value.fileName);
  } catch (error) {
    root.refs.toast.show({
      message: "Failed to download attachment",
      color: "error",
      timeout: 3000,
    });
  } finally {
    isDownloading.value = false;
  }
}

function onToggle(val: any) {
  if (val !== undefined && val !== null) {
    // Panel expanded — recreate editor
    nextTick(() => {
      fetchAnswerWithCKEditor();
      fetchAnswer();
    });
  } else {
    // Panel collapsed — destroy editor to free memory
    destroyEditor();
    isFetched.value = false;
  }
}

onBeforeUnmount(() => {
  destroyEditor();
});
</script>

<style scoped>
:deep(.v-expansion-panel) {
  background-color: #fff;
  border-radius: 25px !important;
  padding: 15px;
  margin-bottom: 10px;
}

:deep(.v-expansion-panels) {
  border-radius: 15px;
  background: transparent !important;
}

:deep(.v-expansion-panel:not(:first-child)::after) {
  border-top-style: none;
}

:deep(.v-expansion-panel-title__overlay) {
  background-color: #fff;
}

:deep(.v-expansion-panel__shadow) {
  box-shadow: none;
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
  background: transparent !important;
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
</style>
