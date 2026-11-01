<template>
  <div ref="target" :id="id">
    <p class="font-weight-bold text-darkBlue text-left">Title</p>
    <v-chip style="height: 56px; border-radius: 10px; width: 100%">
      {{ documentName }}
    </v-chip>
  </div>

  <v-card
    class="my-5 pb-10"
    style="
      border-radius: 8px;
      padding-left: 1cm;
      padding-right: 1cm;
      padding-top: 1cm;
    "
    min-height="29.7cm"
  >
    <paragraph-shimmer :lines="16" :random-size="true" v-if="loading" />
    <v-sheet class="mb-5 mt-5 bg-transparent" style="pointer-events: none">
      <div class="editor-root ml-5 mr-5">
        <div v-if="!allowed" class="text-grey mt-10 text-center">
          <v-icon size="x-large">mdi-shield-key-outline</v-icon>
          <p class="mt-4">Don't Have Any Document</p>
        </div>
        <template v-else>
          <div
            v-if="loading === false && result == null"
            class="text-grey mt-10 text-center"
          >
            <v-icon size="x-large">mdi-file-alert-outline</v-icon>
            <p class="mt-4">Document in Progress</p>
          </div>
          <div class="approved-editor">
            <div ref="myEditor" id="readonlyeditor" />
          </div>
        </template>
      </div>
    </v-sheet>
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { useStore } from "vuex";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

let editorInstance: any;
const props = defineProps<{ id: string; observer: any; isLoaded: boolean }>();
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const target = ref<Element>();
const documentName = ref("");
const allowed = ref(true);
const myEditor = ref();
const result = ref();
const loading = ref(false);

console.time("LoadTime");
watch(
  () => props.isLoaded,
  () => {
    if (props.isLoaded) {
      loading.value = true;
      store
        .dispatch("documentStore/fetchFormDocument", props.id)
        .then((data) => {
          documentName.value = data.responseData.documentName;
          allowed.value = data.responseData.children.length > 0;
          if (allowed.value === false) loading.value = false;
        });

      store
        .dispatch("documentStore/fetchContentFromStorage", props.id)
        .then((data) => {
          if (data.responseCode === "011000") {
            result.value = data.responseData.content;
          } else {
            result.value = "";
          }
        })
        .catch(() => {
          result.value = "";
        })
        .finally(() => {
          loading.value = false;
        });
    }
  }
);

watch(result, (newVal) => {
  if (editorInstance && newVal) {
    editorInstance.setData(newVal);
  }
});

onMounted(async () => {
  props.observer.observe(target.value);
  try {
    loading.value = true;
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
          placeholder: "this document is empty..",
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
  } finally {
    loading.value = false;
  }

  console.timeEnd("LoadTime");
});
</script>

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

<style scoped>
.documentStyle {
  border-radius: 8px;
  margin-top: 20px;
  width: 21.01cm;
  padding-top: 1cm;
  padding-left: 1cm;
  padding-right: 1cm;
  padding-bottom: 1cm;
}
</style>
