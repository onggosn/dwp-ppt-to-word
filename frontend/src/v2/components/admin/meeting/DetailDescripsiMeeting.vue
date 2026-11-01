<template>
  <div class="my-2">
    <!-- {{ props.item }} -->
    <v-card class="mt-5 ml-n3 mb-10 description-detail">
      <v-sheet
        class="mt-10 ml-10 mb-10 pa-2 ma-2 text-left font-weight-bold text-newBlack"
      >
        <div class="editor-desc__container">
          <div ref="editors" id="readonlyeditor" />
        </div>
      </v-sheet>
    </v-card>
  </div>
</template>
<script setup lang="ts">
/* eslint-disable */
import { ref, watch, onMounted } from "vue";
import { useStore } from "vuex";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();
const props = defineProps({
  item: {
    type: String,
    default: "",
  },
});

const editors = ref<HTMLDivElement>();

async function initEditor() {
  if (editors.value) {
    let editorInstance = await EditorOutput.CustomClassic.create(
      editors.value,
      {
        initialData: props.item,
        updateSourceElementOnDestroy: false,
        toolbar: {
          items: [],
        },
        licenseKey: ckEditorLicense.value,
      }
    );
    editorInstance.enableReadOnlyMode("readonlyeditor");
  }
}

onMounted(() => {
  initEditor();
});
</script>

<style>
.editor-desc__container > .ck .ck-sticky-panel__content {
  display: none;
}
</style>
<style scoped>
.description-detail {
  /* border-radius: 12px; */
  background: var(--White-Colot, #fff);
  /* box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25); */
  flex-shrink: 0;
}

:deep(.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused)) {
  border: 0;
}

.link-media {
  text-decoration: none;
}
</style>
