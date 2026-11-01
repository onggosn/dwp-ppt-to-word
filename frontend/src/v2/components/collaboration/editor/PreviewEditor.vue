<template>
  <v-sheet class="bg-transparent document-style" style="pointer-events: none">
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
    <div ref="myEditor" />
  </v-sheet>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const route = useRoute();
const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const loading = ref<boolean>(false);
const result = ref();
const myEditor = ref<any>(null);
const dontHaveDocument = ref(false);
const documentID = ref();

let editorInstance: any;

const createEditor = async () => {
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
        }
      );
      editorInstance.enableReadOnlyMode("readonlyeditor");
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
  };
  store
    .dispatch("eFormStore/getPreviewbeforeSendByBPDocAndUsername", reqData)
    .then(({ responseData }) => {
      if (responseData === null) {
        loading.value = false;
        dontHaveDocument.value = true;
      } else {
        result.value = responseData?.content;
        createEditor();
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
.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused) {
  border-color: white !important;
  cursor: none;
  pointer-events: none;
  margin-top: 0px;
}

.ck.ck-editor__top.ck-reset_all {
  display: none;
}
</style>

<style scoped>
:deep(.ck .ck-widget__selection-handle) {
  display: none;
}
:deep(.ck-widget.ck-widget_selected) {
  outline-color: white !important;
}

:deep(.table .ck-widget .ck-widget_with-selection-handle .ck-widget_selected) {
  margin-top: 0px;
}
</style>
