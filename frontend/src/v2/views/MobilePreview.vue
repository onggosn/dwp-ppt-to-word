<template>
  <div class="mobile-preview" ref="myEditor"></div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

const myEditor = ref();
const { ckEditorLicense } = useInitializeConfig();
class CustomDocument extends Editor.CustomDocument {}
let editorInstance: CustomDocument;

window.initEditor = (message: string) => {
  setDataEditor(message);
  //   alert(message);
};

const setDataEditor = async (data: string) => {
  if (editorInstance) {
    await editorInstance.setData(data);
  } else {
    console.error("Editor instance is not initialized.");
  }
};
const createEditor = async () => {
  const config: any = {
    initialData: "<p>This is a sample document for mobile preview.</p>",
    licenseKey: ckEditorLicense.value,
    toolbar: {
      items: ["previousPage", "nextPage", "pageNavigation"],
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
  editorInstance.isReadOnly;
  editorInstance.enableReadOnlyMode("my-feature-id");
};

onMounted(() => {
  createEditor();
});
</script>
<style scoped>
.mobile-preview .ck-content .ck-editor__editable {
  height: 100%;
  margin: 20px;
}
</style>
