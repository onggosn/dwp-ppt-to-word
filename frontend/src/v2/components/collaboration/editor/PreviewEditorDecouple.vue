<template>
  <div class="row" style="overflow-y: auto">
    <div v-if="isLoading">
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
    <div class="landscape-preview" v-if="documentType === 5">
      <div
        class="main-container"
        :class="[isLoading && dontHaveDocument == false ? 'loading' : '']"
      >
        <div
          class="editor-container editor-container_document-editor"
          ref="editorContainer"
        >
          <div class="editor-container__toolbar" ref="toolbarElement"></div>
          <div class="editor-container__editor-wrapper">
            <div class="editor-container__editor">
              <div ref="myEditor"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="potrait-preview" v-else>
      <div
        class="main-container"
        :class="[isLoading && dontHaveDocument == false ? 'loading' : '']"
      >
        <div
          class="editor-container editor-container_document-editor"
          ref="editorContainer"
        >
          <div class="editor-container__toolbar" ref="toolbarElement"></div>
          <div class="editor-container__editor-wrapper">
            <div class="editor-container__editor">
              <div ref="myEditor"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
/* eslint-disable */
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const myEditor = ref();
const toolbarElement = ref();
const editorContainer = ref();
const editorRef = ref<HTMLDivElement | null>(null);

const route = useRoute();
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const result = ref();
const isLoading = ref(false);
const dontHaveDocument = ref(false);
const documentType = computed(
  () => store.getters["collaborationStore/getDocumentTypeId"]
);

class CustomDocument extends Editor.CustomDocument {}
let editorInstance: CustomDocument;

const createEditor = async () => {
  isLoading.value = true;

  const config: any = {
    initialData: result.value,
    licenseKey: ckEditorLicense.value,
    toolbar: {
      items: ["previousPage", "nextPage", "pageNavigation"],
    },
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
    pagination: {
      // A4
      pageWidth: "210mm",
      pageHeight: "297mm",
      pageMargins: {
        top: "20mm",
        bottom: "20mm",
        right: "12mm",
        left: "12mm",
      },
    },
    removePlugins: [
      "SourceEditing",
      "Comments",
      "PresenceList",
      "RealTimeCollaborativeComments",
      "RealTimeCollaborativeEditing",
      "RealTimeCollaborativeTrackChanges",
      "TrackChanges",
    ],
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
          classes: [
            "table-kop-surat",
            "section-header-letter",
            "table-width-full",
            "layout-table",
          ],
        },
        {
          name: "ol",
          styles: true,
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
  };

  editorInstance = await Editor.CustomDocument.create(myEditor.value, config);

  if (documentType.value === 5) {
    config.pagination = {
      pageWidth: "297mm",
      pageHeight: "210mm",
      pageMargins: {
        top: "20mm",
        bottom: "20mm",
        right: "12mm",
        left: "12mm",
      },
    };
  }

  editorInstance.isReadOnly;
  editorInstance.enableReadOnlyMode("my-feature-id");
  const toolbarContainer = toolbarElement.value as unknown as HTMLElement;
  toolbarContainer.appendChild(
    editorInstance.ui.view.toolbar.element as HTMLElement
  );
  isLoading.value = false;
};

onMounted(async () => {
  isLoading.value = true;
  const reqData = {
    idBPDocument: route.params.idDoc as string,
    isRevision: store.state.documentStore.validasiRevision.isRevision,
  };
  store
    .dispatch("eFormStore/getPreviewbeforeSendByBPDocAndUsername", reqData)
    .then(({ responseData }) => {
      if (responseData === null) {
        dontHaveDocument.value = true;
      } else {
        result.value = responseData?.content;
        createEditor();
      }
    });
});
</script>
<style scoped>
:deep(
    .ck-editor__editable
      .table.layout-table
      > table
      > tbody
      > tr
      > td:not(
        [style*="border:"],
        [style*="border-top"],
        [style*="border-bottom"],
        [style*="border-left"],
        [style*="border-right"],
        [style*="border-width"],
        [style*="border-style"],
        [style*="border-color"]
      )
  ) {
  outline: white 1px none;
}

.loading {
  transform: scale(0);
}
:deep(.ck.ck-editor__editable_inline > *:first-child) {
  margin-top: 0px;
}

:deep(.ck.ck-editor__editable_inline) {
  border: none;
}

:deep(.ck.ck-editor__editable.ck-focused:not(.ck-editor__nested-editable)) {
  border: none !important;
}
:deep(.ck-content .page-break) {
  opacity: 0;
}
</style>
<style>
.ck.ck-pagination-view-line {
  z-index: 10001 !important;
}
.parent-preview .ck.ck-presence-list {
  display: none;
}

.landscape-preview .main-container,
.potrait-preview .main-container {
  margin-left: auto;
  margin-right: auto;
  height: 85vh;
  width: 100%;
}

.parent-preview .ck-content {
  line-height: 1.6;
  word-break: break-word;
}

.landscape-preview .ck-content,
.potrait-preview .ck-content {
  line-height: 1.6;
  word-break: break-word;
}

.parent-preview .editor-container__editor-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.landscape-preview .editor-container__editor-wrapper,
.potrait-preview .editor-container__editor-wrapper {
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

.landscape-preview .editor-container_document-editor .editor-container__toolbar,
.potrait-preview .editor-container_document-editor .editor-container__toolbar {
  display: flex;
  position: sticky;
  top: -1px;
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
  z-index: 10001;
}

.landscape-preview
  .editor-container_document-editor
  .editor-container__toolbar
  > .ck.ck-toolbar,
.potrait-preview
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

.landscape-preview
  .editor-container_document-editor
  .editor-container__editor-wrapper,
.potrait-preview
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

.landscape-preview .editor-container_document-editor .editor-container__editor,
.potrait-preview .editor-container_document-editor .editor-container__editor {
  margin-top: 28px;
  margin-bottom: 28px;
  height: 100%;
}

.potrait-preview
  .editor-container_document-editor
  .editor-container__editor
  .ck.ck-editor__editable {
  min-width: 210mm;
  max-width: 210mm;
  min-height: 297mm;
  height: fit-content;
  padding: 20mm 12mm;
  background: hsl(0, 0%, 100%);
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
}

.landscape-preview
  .editor-container_document-editor
  .editor-container__editor
  .ck.ck-editor__editable {
  min-width: 297mm;
  max-width: 297mm;
  min-height: 210mm;
  height: fit-content;
  padding: 20mm 12mm;
  background: hsl(0, 0%, 100%);
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
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
</style>
