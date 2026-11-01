<template>
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
  <div class="approved-editor">
    <div ref="myEditor" id="readonlyeditor" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
// import { GetDocumentContentFromStorage } from "@/v2/library/ApiCKEditor";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const result = ref<string | null>(null);
const loading = ref<boolean>(false);
const myEditor = ref<HTMLElement | null>(null);
const route = useRoute();
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();

let editorInstance: any;

onMounted(async () => {
  try {
    loading.value = true;
    // result.value = await GetDocumentContentFromStorage(
    //   route.params.idDoc as string
    // ); //hit this through BE endpoint

    store
      .dispatch("documentStore/fetchContentFromStorage", route.params.idDoc)
      .then((data) => {
        if (data.responseCode === "011000") {
          result.value = data.responseData.content;
        } else {
          result.value = "";
        }
      })
      .catch(() => {
        result.value = "";
      });

    if (myEditor.value) {
      editorInstance = await EditorOutput.CustomDocument.create(
        myEditor.value,
        {
          initialData: result.value || "",
          updateSourceElementOnDestroy: false,
          toolbar: {
            items: [],
          },
          licenseKey: ckEditorLicense.value,
          list: {
            properties: {
              styles: true,
              startIndex: true,
              reversed: true,
            },
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
                ],
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
                styles: true,
                attributes: {
                  start: true,
                },
              },
            ],
            disallow: [],
          },
          removePlugins: [
            "Pagination",
            "Comments",
            "PresenceList",
            "RealTimeCollaborativeComments",
            "RealTimeCollaborativeEditing",
            "RealTimeCollaborativeTrackChanges",
            "TrackChanges",
          ],
        }
      );
      editorInstance.enableReadOnlyMode("readonlyeditor");
    }
  } catch (error) {
    undefined;
  }
});

watch(result, (newVal) => {
  if (editorInstance && newVal) {
    editorInstance.setData(newVal);
    loading.value = false;
  }
});
</script>
<style scoped>
:deep(.ck-content .page-break) {
  opacity: 0;
}
</style>
<style>
.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused) {
  border-color: white !important;
  cursor: none;
  pointer-events: none;
  margin-top: 0px !important;
}

.ck.ck-editor__top.ck-reset_all {
  display: none;
}
.ck .ck-widget__selection-handle {
  display: none;
}
.ck-widget.ck-widget_selected {
  outline-color: white !important;
}
.approved-editor
  > .ck
  > .ck-editor__main
  > .ck-editor__editable
  > .ck-widget.ck-widget_with-selection-handle:first-child {
  margin-top: -20px !important;
}
</style>
