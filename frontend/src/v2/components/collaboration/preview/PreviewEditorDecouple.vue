<template>
  <div class="row">
    <v-toolbar class="pa-4 bg-white" style="border-bottom: solid 2px #e4e4e4">
      <div class="d-block">
        <v-btn
          variant="outlined"
          size="large"
          icon="mdi-arrow-left"
          class="ml-5 ml-md-0"
          color="#045695"
          style="border: 0.01px solid #d3d3d3; color: white !important"
          elevation="2"
          @click="router.back()"
          ><v-icon icon="mdi-arrow-left" color="#045695"> </v-icon>
        </v-btn>
        <span class="view-title ml-3">{{ documentName }}</span>
      </div>
    </v-toolbar>
  </div>
  <div class="row">
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
    <div
      :class="{
        'landscape-preview': isLandscape,
        'potrait-preview': !isLandscape,
      }"
    >
      <div
        :class="[
          'document-container',
          { loading: isLoading && !dontHaveDocument },
        ]"
      >
        <div id="toolbar-container" ref="toolbarElement"></div>
        <div class="editor-container">
          <div id="editor" ref="editorRef">
            <p>This is the initial editor content.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { getEditorDocumentConfig } from "@/v2/helpers/utils";
import Editor from "@v2/components/side-project/ckeditor/build/ckeditor";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { DocumentType } from "@/v2/enum/Enum";

const router = useRouter();
const store = useStore();

const isLoading = ref<boolean>(false);
const dontHaveDocument = ref<boolean>(false);
const editorRef = ref<HTMLElement | null>(null);
const isInitializing = ref<boolean>(false);
const toolbarElement = ref<HTMLElement | null>(null);
const result = ref<string | null>(null);
const documentName = ref<string | null>(null);
const documentType = ref<number | null>(null);
const paddingTop = ref<string>("20mm");
const paddingBottom = ref<string>("20mm");
const paddingLeft = ref<string>("12mm");
const paddingRight = ref<string>("12mm");

class CustomDocument extends Editor.CustomDocument {}
let editorInstance: CustomDocument;

const isLandscape = computed(() => {
  return documentType.value === DocumentType.ringsek;
});

const createEditor = async () => {
  if (!editorRef.value) return;
  isInitializing.value = true;

  try {
    const config = await getEditorDocumentConfig(store);
    if (documentType.value === DocumentType.ringsek) {
      config.pagination = {
        pageWidth: "297mm",
        pageHeight: "210mm",
        pageMargins: {
          top: paddingTop.value,
          bottom: paddingBottom.value,
          right: paddingRight.value,
          left: paddingLeft.value,
        },
      };
    }
    config.initialData = result.value;
    config.toolbar = {
      items: ["previousPage", "nextPage", "pageNavigation"],
    };

    editorInstance = await Editor.CustomDocument.create(
      editorRef.value,
      config
    );
    editorInstance.isReadOnly;
    editorInstance.enableReadOnlyMode("my-feature-id");
    const toolbarContainer = toolbarElement.value as unknown as HTMLElement;
    toolbarContainer.appendChild(
      editorInstance.ui.view.toolbar.element as HTMLElement
    );
  } catch {
    void 0;
  } finally {
    isInitializing.value = false;
  }
};

const mergeContent = () => {
  isLoading.value = true;
  const reqData = {
    idBPDocument: router.currentRoute.value.params.idDoc as string,
    isRevision: store.state.documentStore.validasiRevision.isRevision,
  };

  store
    .dispatch("eFormStore/getPreviewbeforeSendByBPDocAndUsername", reqData)
    .then(({ responseData }) => {
      if (responseData === null) {
        dontHaveDocument.value = true;
      } else {
        documentName.value = responseData?.bpDocumentName ?? null;
        documentType.value = responseData?.idDocumentType ?? null;
        result.value = responseData?.content;
        paddingTop.value = responseData?.marginTop ?? "20mm";
        paddingBottom.value = responseData?.marginBottom ?? "20mm";
        paddingLeft.value = responseData?.marginLeft ?? "12mm";
        paddingRight.value = responseData?.marginRight ?? "12mm";
        createEditor();
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
};

onMounted(() => {
  mergeContent();
});

onBeforeUnmount(() => {
  editorInstance?.destroy();
});
</script>
<style scoped>
:deep(.blank-space) {
  height: 80px !important;
}
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

:deep(
    .ck.ck-editor__editable.ck-blurred .ck-widget.ck-widget_selected,
    .ck.ck-editor__editable.ck-blurred .ck-widget.ck-widget_selected:hover
  ) {
  outline-color: white !important;
}

:deep(
    .ck.ck-editor__editable.ck-read-only
      .ck-widget.ck-widget_with-selection-handle
      .ck-widget__selection-handle,
    .ck.ck-editor__editable.ck-read-only
      .ck-widget.ck-widget_with-selection-handle
      .ck-widget__selection-handle:hover
  ) {
  display: none;
}

.loading {
  transform: scale(0);
}
.view-title {
  font-family: Poppins;
  font-size: 20px;
  font-weight: 700;
  line-height: 30px;
  color: #3a416f;
  margin-left: 17px;
}
/* Editor styles */
.document-container {
  margin: auto;
  background-color: rgb(238, 238, 238);
}
.editor-container {
  border: 1px solid hsl(0, 0%, 80%);
  max-height: calc(100vh - 100px);
  overflow: auto;
  height: 80vh;
}
.potrait-preview .ck.ck-editor__editable_inline {
  /*
        A4 size.
        Expand the width by 2px because of the border and "box-sizing: border-box".
    */
  width: calc(210mm + 2px);
  min-height: 1123px;
  height: auto;
  padding: v-bind(
    "`${paddingTop} ${paddingRight} ${paddingBottom} ${paddingLeft}`"
  );
  box-sizing: border-box;
  border: 1px solid hsl(0, 0%, 88%);
  background: hsl(0, 0%, 100%);
  box-shadow: 0 2px 8px hsla(0, 0%, 0%, 0.08);
  margin: 40px auto;
}

.landscape-preview .ck.ck-editor__editable_inline {
  /*
        A4 size.
        Expand the width by 2px because of the border and "box-sizing: border-box".
    */
  width: calc(297mm + 2px);
  height: auto;
  padding: v-bind(
    "`${paddingTop} ${paddingRight} ${paddingBottom} ${paddingLeft}`"
  );
  box-sizing: border-box;
  border: 1px solid hsl(0, 0%, 88%);
  background: hsl(0, 0%, 100%);
  box-shadow: 0 2px 8px hsla(0, 0%, 0%, 0.08);
  margin: 40px auto;
}

/* Content styles */
@media print {
  body {
    margin: 0 !important;
  }
}
.ck-content .table thead {
  display: table-row-group;
}
.ck-content .table tr {
  break-inside: avoid;
  break-after: auto;
}
</style>
