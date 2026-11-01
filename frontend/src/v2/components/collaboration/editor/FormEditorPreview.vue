<template>
  <v-sheet class="mb-5 mt-5 bg-transparent" style="text-align: -webkit-center">
    <free-style-shimmer
      v-if="isLoading"
      width="100%"
      height="10rem"
      border-radius="15px"
      class="pt-4"
    />
    <div class="text-left mb-1 font-weight-bold text-14">Track Changes</div>
    <div
      :class="['editor-root', isLoading ? 'loading' : '']"
      class="editor-preview"
    >
      <div class="row row-presence justify-space-between mb-1 d-none">
        <div class="d-none">
          <p class="align-self-center mr-2 text-14 font-weight-bold">online:</p>
          <div ref="presenceListElement" />
        </div>
      </div>
      <span
        @click="reloadCkEditor"
        ref="btnReload"
        style="color: white; font-size: 10px"
      ></span>
      <template v-if="isEditorReady">
        <div class="d-flex">
          <div
            ref="myEditor"
            :name="`form-${formIndex}`"
            style="width: 100%"
          ></div>
          <div
            ref="sidebar"
            class="sidebar narrow"
            id="sidebar"
            style="min-width: 65px"
          ></div>
        </div>
      </template>
      <template v-else>
        <v-card class="rounded-lg" min-height="200">
          <v-card-text class="mt-5 text-center">
            <v-icon size="50" color="red">mdi-file-alert-outline</v-icon>
            <p class="mt-4 text-grey">
              Oops Sorry, the editor went wrong.
              <span style="cursor: pointer; color: red" @click="reloadCkEditor">
                reload
              </span>
            </p>
            <p style="font-size: 11px">
              {{ errorCode != undefined ? "(" + errorCode + ") " : "" }}
              {{ errorMessage }}
            </p>
          </v-card-text>
        </v-card>
      </template>
    </div>
  </v-sheet>
</template>
<script setup lang="ts">
/* eslint-disable */
import { defineComponent, ref, onMounted, onUnmounted } from "vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useStore } from "vuex";
import EditAccessSection from "../EditAccessSection.vue";
import BtnMngMapping from "@v2/components/collaboration/MngMappingSection.vue";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

defineComponent([EditAccessSection, BtnMngMapping]);

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();

const presenceListElement = ref();
const myEditor = ref<any>(null);
class CustomInline extends EditorOutput.CustomInline {}
let editorInline: CustomInline;

const props = defineProps({
  channelId: {
    type: String,
    default: "",
  },
  eformId: {
    type: String,
    default: "",
  },
  sectionName: {
    type: String,
    default: "",
  },
  detailForm: {
    type: Object,
    default: null,
  },
  formIndex: {
    type: Number,
    default: 0,
  },
});

const isEditorReady = ref(true);
const counterError = ref(0);
const btnReload = ref();
const sidebar = ref();
const isLoading = ref(false);
onMounted(async () => {
  doCreate();
});

const originalError = console.error;
const errorCode = ref();
const errorMessage = ref();
console.error = function (...args) {
  originalError.apply(console, args);
  errorMessage.value = args[0].message;
  errorCode.value = args[0].code;
};

function doCreate() {
  isEditorReady.value = true;
  isLoading.value = true;
  CustomInline.create(myEditor.value, {
    initialData: "",
    updateSourceElementOnDestroy: false,
    toolbar: {
      items: [],
    },
    licenseKey: ckEditorLicense.value,
    cloudServices: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const response = await store.dispatch(
              "userStore/getDecryptedCKEditorToken"
            );
            const token = response?.ResponseData?.value;
            resolve(token);
          }, 1500);
        }),
      webSocketUrl: process.env.VUE_APP_WEBSOCKET,
      bundleVersion: process.env.VUE_APP_CKEDITOR_BUNDLE_VERSION,
    },
    collaboration: {
      channelId: `${props.channelId.toLowerCase()}`,
    },
    presenceList: {
      container: presenceListElement.value,
      collapseAt: 4,
      displayMe: true,
    },
    removePlugins: ["HorizontalLine", "Pagination"],
    sidebar: {
      container: sidebar.value,
    },
  })
    .then((editor) => {
      editorInline = editor;
      editor.enableReadOnlyMode("feature-id");
      editor.execute("trackChanges");
      editor.commands.get("trackChanges")?.forceDisabled("suggestionMode");
      editor.commands.get("acceptSuggestion")?.forceDisabled("suggestionMode");
      editor.commands
        .get("acceptAllSuggestion")
        ?.forceDisabled("suggestionMode");
      editor.commands
        .get("discardAllSuggestion")
        ?.forceDisabled("suggestionMode");
      editor.commands.get("discardSuggestion")?.forceDisabled("suggestionMode");
      editor.plugins.get("AnnotationsUIs").switchTo("narrowSidebar");

      isLoading.value = false;
    })
    .catch((err) => {
      counterError.value++;
      isEditorReady.value = false;
      if (!errorMessage.value) {
        errorMessage.value = err;
      }
      if (["409"].includes(errorCode.value)) {
        store.dispatch("eFormStore/restoreCollabSession", {
          id: props.channelId,
        });
      } else if (
        errorMessage.value.toString().includes("token-not-in-jwt-format")
      ) {
        store.dispatch("userStore/fetchCKEditorToken");
      }
      if (counterError.value <= 3) {
        setTimeout(() => {
          if (btnReload.value) btnReload.value.click();
        }, 3000);
      } else {
        isLoading.value = false;
      }
    });
}

function reloadCkEditor() {
  presenceListElement.value.innerHTML = "";
  doDestroy();
  isEditorReady.value = true;
  setTimeout(() => {
    myEditor.value.innerHTML = "";
    doCreate();
  }, 2 * 1000);
}

const doDestroy = () => {
  if (editorInline) {
    editorInline.destroy();
  }
};

onUnmounted(() => {
  doDestroy();
});
</script>
<style>
/*.editor-preview .ck-content ol .ck-suggestion-marker-formatBlock,
.editor-preview .ck-content ul .ck-suggestion-marker-formatBlock {
  box-shadow: -2px 0 0 0 var(--ck-color-base-background),
    -5px 0 0 0 rgba(0, 0, 0, 0);
}
.editor-preview .ck-content .ck-suggestion-marker-formatBlock {
  background: none;
  border: 0;
  box-shadow: -7px 0 0 0 var(--ck-color-base-background), -10px 0 0 0 white;
}

.editor-preview
  .ck-content
  .ck-suggestion-marker-insertion.table
  > table
  > tbody
  > tr
  > td {
  background: var(--ck-color-suggestion-marker-insertion-background) !important;
  border-color: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
}

.editor-preview .ck-content .ck-suggestion-marker-insertion.ck-widget {
  border: white;
}

.editor-preview .ck-content .ck-suggestion-marker-insertion {
  background: var(--ck-color-suggestion-marker-insertion-background) !important;
  border-bottom: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
  border-top: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
}

.editor-preview
  .ck-content
  .ck-suggestion-marker-insertion.ck-suggestion-marker--active {
  background: var(
    --ck-color-suggestion-marker-insertion-background-active
  ) !important;
  border-color: var(
    --ck-color-suggestion-marker-insertion-border-active
  ) !important;
}

.editor-preview .ck-content .ck-suggestion-marker-formatInline {
  border-bottom: 0px solid var(--ck-color-suggestion-marker-format-border);
  border-top: 0px solid var(--ck-color-suggestion-marker-format-border);
}

.editor-preview .ck-suggestion-marker-deletion {
  display: none;
}

.editor-preview .ck-suggestion-marker-split {
  display: none;
}

*/

.editor-preview .ck-suggestion-marker-merge {
  display: inline !important;
}

.editor-preview .ck-suggestion-marker-deletion {
  display: inline !important;
}

.editor-preview .ck-suggestion-marker-split {
  display: inline !important;
}

.editor-preview
  .ck-content
  .ck-suggestion-marker-insertion.ck-suggestion-marker--active {
  background: var(
    --ck-color-suggestion-marker-insertion-background-active
  ) !important;
  border-color: var(
    --ck-color-suggestion-marker-insertion-border-active
  ) !important;
}

.editor-preview .ck-content .ck-suggestion-marker-insertion {
  background: var(--ck-color-suggestion-marker-insertion-background) !important;
  border-bottom: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
  border-top: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
}

.editor-preview
  .ck-content
  .ck-suggestion-marker-deletion.ck-suggestion-marker--active {
  background: var(
    --ck-color-suggestion-marker-deletion-background-active
  ) !important;
  border-color: var(
    --ck-color-suggestion-marker-deletion-border-active
  ) !important;
}

.editor-preview .ck-content .ck-suggestion-marker-deletion {
  background: var(--ck-color-suggestion-marker-deletion-background) !important;
  border-bottom: 3px solid var(--ck-color-suggestion-marker-deletion-border) !important;
  border-top: 3px solid var(--ck-color-suggestion-marker-deletion-border) !important;
  text-decoration: line-through !important;
  text-decoration-color: var(
    --ck-color-suggestion-marker-deletion-stroke
  ) !important;
  text-decoration-thickness: 3px !important;
}

.editor-preview
  .ck-content
  .ck-suggestion-marker-insertion.table
  > table
  > tbody
  > tr
  > td {
  background-color: var(
    --ck-color-suggestion-widget-insertion-background
  ) !important;
  border-color: var(--ck-color-suggestion-marker-insertion-border) !important;
}

.editor-container__sidebar {
  min-width: 65px;
}

.editor-preview
  .ck
  .ck-balloon-panel
  .ck-balloon-panel_toolbar_west
  .ck-balloon-panel_visible
  .ck-toolbar-container {
  display: none;
}
.ck.ck-editor__top.ck-reset_all {
  display: block;
}

.ck-balloon-panel_toolbar_west {
  width: 717px !important;
}

@media (min-width: 1600px) {
  .ck-balloon-panel_toolbar_west {
    width: 50.5vw !important;
  }
}

@media (min-width: 1400px) and (max-width: 1599px) {
  .ck-balloon-panel_toolbar_west {
    width: 54vw !important;
  }
}

@media (min-width: 1300px) and (max-width: 1399px) {
  .ck-balloon-panel_toolbar_west {
    width: 57.5vw !important;
  }
}

@media (min-width: 768px) and (max-width: 1299px) {
  .ck-balloon-panel_toolbar_west {
    width: 717px !important;
  }
}

/* For screens that are 767px or narrower */
@media (max-width: 767px) {
  .ck-balloon-panel_toolbar_west {
    width: 717px !important;
  }
}
</style>
<style scoped>
.loading {
  transform: scale(0);
}
:deep(.ck.ck-presence-list__counter) {
  margin-left: 10px;
}
/* :deep(.ck.ck-presence-list__marker) {
  height: 5px !important;
  border-radius: 10px;
} */

/* :deep(.ck.ck-user.ck-user_me) {
  background-color: var(--ck-user-colors--1) !important;
  border: 1px solid #fff !important;
  outline: 2px solid var(--ck-user-colors--1) !important;
}

:deep(.ck.ck-user) {
  background-color: darkgray;
  height: 30px !important;
  width: 30px !important;
  min-height: 30px !important;
  min-width: 30px !important;
} */

:deep(.ck.ck-presence-list) {
  flex-direction: row-reverse;
}
.ck.ck-editor__editable_inline {
  /* background-color: #fff !important; */
  border-radius: 13px 13px 13px 13px !important;
  min-height: 200px;
  padding-left: 30px !important;
  padding-right: 30px !important;
  padding-top: 5px !important;
  padding-bottom: 5px !important;
}
.ck.ck-editor__editable_inline.ck-focused {
  border: 1px solid #89cff0 !important;
  box-shadow: 0 0 0 1.5px #7393b3 !important;
}

.ck.ck-editor__editable_inline.ck-blurred {
  border: 1.5px solid grey !important;
}

.disabled-editing-mode {
  background: red !important;
}
:deep(.ck-read-only) {
  background: #c3c3c3 !important;
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

.hidetext {
  color: black;
  font-size: 10px;
  opacity: 0;
}
</style>
