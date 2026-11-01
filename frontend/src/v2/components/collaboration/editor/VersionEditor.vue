<template>
  <div class="row" style="overflow-y: auto">
    <div v-if="loading">
      <div class="d-flex justify-center">
        <free-style-shimmer
          width="30rem"
          height="30px"
          border-radius="10px"
          class="py-8"
        />
      </div>
      <div class="mb-8 text-left">
        <paragraph-shimmer :lines="16" :random-size="true" />
      </div>
    </div>
    <template v-if="dontHaveDocument">
      <div class="d-flex justify-center">
        <img
          :src="require('@/v2/assets/empty/empty_box.svg')"
          class="img-no-available"
          width="400"
          style="margin-bottom: -50px"
        />
      </div>
      <p class="text-grey text-center mt-2 text-13">
        Oh no, we couldn't load your document. <br />Please come back later.
      </p>
    </template>
    <div class="parent-preview">
      <div
        class="main-container"
        :class="[loading && dontHaveDocument == false ? 'loading' : '']"
      >
        <div
          class="editor-container editor-container_document-editor"
          ref="editorContainer"
        >
          <div class="editor-container__toolbar" ref="toolbarElement"></div>
          <div class="editor-container__editor-wrapper" style="">
            <div class="editor-container__editor">
              <div ref="myEditor" id="readonlyeditor" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { getCurrentInstance } from "vue";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const route = useRoute();
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const loading = ref<boolean>(false);
const result = ref();
const titleEvent = ref();
const myEditor = ref<any>(null);
const dontHaveDocument = ref(false);
// const documentID = ref();
const toolbarElement = ref();
const instance: any = getCurrentInstance()?.root.refs;
const props = defineProps({
  idBPDocumentVersion: {
    type: String,
    required: true,
  },
});

let editorInstance: any;

const createEditor = async () => {
  try {
    loading.value = true;
    // result.value = await GetDocumentContentFromStorage(id); //hit this through BE endpoint

    if (myEditor.value) {
      editorInstance = await EditorOutput.CustomDocument.create(
        myEditor.value,
        {
          initialData: result.value || "",
          updateSourceElementOnDestroy: false,
          toolbar: {
            items: ["previousPage", "nextPage", "pageNavigation"],
          },
          licenseKey: ckEditorLicense.value,
          ckbox: {
            tokenUrl: () =>
              new Promise((resolve) => {
                setTimeout(async () => {
                  const token = await store.dispatch(
                    "userStore/getDecryptedCKBoxToken"
                  );
                  resolve(token);
                }, 1500);
              }),
            serviceOrigin: process.env.VUE_APP_CKBOX,
          },
          list: {
            properties: {
              styles: true,
              startIndex: true,
              reversed: true,
            },
          },
          placeholder: "this document is empty..",
          htmlSupport: {
            allow: [
              {
                name: "li",
                classes: ["type-heading"],
              },
              {
                name: "div",
                classes: [
                  "title-level-1",
                  "title-level-2",
                  "title-level-3",
                  "title-level-4",
                  "title-level-5",
                  "content-level-1",
                  "content-level-2",
                  "content-level-3",
                  "content-level-4",
                  "content-level-5",
                  "title-document",
                  "text-version-1",
                  "chip-version",
                  "justify-right",
                ],
              },
              {
                name: "tr",
                classes: ["blank-space"],
              },
              {
                name: "p",
                classes: ["spacing-1", "spacing-1-5", "spacing-2"],
                styles: true,
              },
              {
                name: /^h[1-6]$/,
                styles: true,
              },
              {
                name: "table",
                classes: ["table-kop-surat"],
              },
              {
                name: "ol",
                attributes: {
                  start: true,
                },
              },
              {
                name: "span",
                styles: true,
              },
            ],
            disallow: [],
          },
          removePlugins: [
            "Comments",
            "PresenceList",
            "RealTimeCollaborativeComments",
            "RealTimeCollaborativeEditing",
            "RealTimeCollaborativeTrackChanges",
            "TrackChanges",
            // "Pagination",
          ],
        }
      ).then((editor) => {
        editor.isReadOnly;
        editor.enableReadOnlyMode("my-feature-id");
        const toolbarContainer = toolbarElement.value as unknown as HTMLElement;
        toolbarContainer.appendChild(
          editor.ui.view.toolbar.element as HTMLElement
        );
        const editorContainer = myEditor.value as unknown as HTMLElement;
        const vSheetElement = document.createElement("div");
        vSheetElement.innerHTML =
          `
          <div class="text-version-1 justify-right">
            <div class="ml-10">
              <div class="chip-version">
                <span class="text-newBlack">` +
          titleEvent.value +
          `</span>
              </div>
            </div>
         </div>
        `;
        const tempElement = document.createElement("div");
        tempElement.innerHTML = result.value;
        tempElement.insertAdjacentHTML("afterbegin", vSheetElement.innerHTML);
        editorContainer.appendChild(tempElement);
        editorInstance = editor;
        editor.data.set(tempElement.innerHTML, {
          suppressErrorInCollaboration: true,
        });
        loading.value = false;
      });
    }
  } finally {
    loading.value = false;
  }
};

const doDestroy = () => {
  if (editorInstance) {
    editorInstance.destroy();
  }
};

onMounted(() => {
  loading.value = true;
  const reqData = {
    idBPDocument: route.params.idDoc as string,
    idBPDocumentVersion: props.idBPDocumentVersion as string,
  };
  store
    .dispatch("eFormStore/getVersionPreviewByBPDocVerAndUsername", reqData)
    .then(({ responseData }) => {
      if (responseData === null) {
        loading.value = false;
        dontHaveDocument.value = true;
      } else {
        result.value = responseData.data?.content;
        titleEvent.value = responseData.data?.version;
        createEditor();
      }
    })
    .catch((error) => {
      if (error.response.status === 400)
        if (error.response.data.responseCode === "011013") {
          loading.value = false;
          dontHaveDocument.value = true;
        } else if (error.response.data.responseCode === "011049") {
          loading.value = false;
          instance.toast.show({
            message: error.response.data.responseMessage,
            color: "warning",
            timeout: 3000,
          });
          dontHaveDocument.value = true;
        }
    });
});

onUnmounted(() => {
  doDestroy();
});

watch(result, (newVal) => {
  if (editorInstance && newVal) {
    editorInstance.setData(newVal);
  }
});
</script>

<style>
.loading {
  transform: scale(0);
}
:deep(.ck.ck-pagination-view-line) {
  z-index: 10001 !important;
}
</style>

<style scoped>
.parent-preview .ck.ck-presence-list {
  display: none;
}
.parent-preview .main-container {
  margin-left: auto;
  margin-right: auto;
  height: 85vh;
  width: 100%;
}

.parent-preview .ck-content {
  line-height: 1.6;
  word-break: break-word;
}

.parent-preview .editor-container__editor-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.parent-preview .editor-container_document-editor .editor-container__toolbar {
  display: flex;
  position: sticky;
  top: -1px;
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
  z-index: 10001;
}

.parent-preview
  .editor-container_document-editor
  .editor-container__toolbar
  > .ck.ck-toolbar {
  flex-grow: 1;
  width: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  border-top: 0;
  border-left: 0;
  border-right: 0;
}

.parent-preview
  .editor-container_document-editor
  .editor-container__editor-wrapper {
  max-height: var(--ckeditor5-preview-height);
  min-height: var(--ckeditor5-preview-height);
  background: var(--ck-color-base-foreground);
}

.parent-preview .editor-container_document-editor .editor-container__editor {
  margin-top: 28px;
  margin-bottom: 28px;
  height: 100%;
}

.parent-preview
  .editor-container_document-editor
  .editor-container__editor
  .ck.ck-editor__editable {
  box-sizing: border-box;
  min-width: calc(210mm + 2px);
  max-width: calc(210mm + 2px);
  min-height: 297mm;
  height: fit-content;
  padding: 20mm 12mm;
  border: 1px hsl(0, 0%, 82.7%) solid;
  background: hsl(0, 0%, 100%);
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
  flex: 1 1 auto;
  margin-left: 72px;
  margin-right: 72px;
}

.parent-preview .editor-container__sidebar {
  min-width: var(--ckeditor5-preview-sidebar-width);
  max-width: var(--ckeditor5-preview-sidebar-width);
  margin-top: 28px;
  margin-left: 10px;
  margin-right: 10px;
}

.parent-preview .editor-container__minimap-wrapper {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.parent-preview .editor-container__sidebar_minimap {
  margin: 0;
  flex: 0 0 auto;
  border-left: 1px solid var(--ck-color-toolbar-border);
  position: relative;
  overflow: hidden;
  max-height: 100%;
}

.parent-preview .editor-container_include-minimap.ck-minimap__iframe-content {
  background: hsl(0, 0%, 100%);
}

.parent-preview
  .editor-container_include-minimap.ck-minimap__iframe-content
  .ck.ck-editor__editable {
  line-height: 1.6;
  flex: 1 1 auto;
  word-break: break-word;
  box-sizing: border-box;
  min-width: calc(210mm + 2px);
  max-width: calc(210mm + 2px);
  min-height: 297mm;
  height: fit-content;
  padding: 20mm 12mm;
}

.parent-preview
  .editor-container_include-minimap
  .editor-container__editor-wrapper {
  height: 100%;
}

.parent-preview
  .editor-container_include-minimap
  .editor-container__sidebar_minimap {
  max-width: calc(var(--ckeditor5-preview-sidebar-width) / 2);
  min-width: calc(var(--ckeditor5-preview-sidebar-width) / 2);
}

.parent-preview .ck-content .table thead {
  display: table-row-group;
}

.parent-preview .ck-content .table tr {
  break-inside: avoid;
  break-after: auto;
}

.parent-preview .ck-content .table thead {
  display: table-row-group;
}

.parent-preview .ck-content .table tr {
  break-inside: avoid;
  break-after: auto;
}
:deep(.ck-content .page-break) {
  opacity: 0;
}

:deep(.justify-right) {
  justify-content: right !important;
}
</style>
