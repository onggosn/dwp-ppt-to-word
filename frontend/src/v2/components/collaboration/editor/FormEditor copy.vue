<template>
  <v-sheet class="mb-5 mt-5 bg-transparent">
    <div class="editor-root">
      <div class="row row-presence d-flex justify-space-between mb-1">
        <div class="d-flex">
          <p class="align-self-center mr-2 text-14 font-weight-bold">online:</p>
          <div ref="presenceListElement" class="presence" />
        </div>

        <div class="text-end align-self-center">
          <!-- <v-btn
            v-if="!isLoading"
            variant="outlined"
            rounded
            color="#065695"
            class="mr-2"
            :disabled="true"
            size="small"
            >Mapping
            <template #prepend>
              <img :src="require('@/v2/assets/icon/mapping.svg')" />
            </template>
          </v-btn> -->
          <!-- {{ getDisabledCondition }} -->
          <template v-if="!isLoading && !getDisabledCondition">
            <EditAccessSection
              :sectionName="props.sectionName"
              :idDoc="props.channelId"
              :idEform="props.eformId"
            />
          </template>
          <template v-if="!isLoading && !getDisabledCondition">
            <SaveEachContent :idFormEditor="props.channelId" />
          </template>
        </div>
      </div>

      <free-style-shimmer
        v-if="isLoading"
        width="100%"
        height="10rem"
        border-radius="15px"
        class="pt-4"
      />

      <!-- {{ channelId }} -->
      <ckeditor
        v-model="initialData"
        v-if="isLayoutReady"
        :config="editorConfig"
        :editor="editor"
        ref="editorElement"
        :disabled="getDisabledCondition"
        @ready="onEditorReady"
      />
    </div>
  </v-sheet>
</template>
<script setup lang="ts">
import { defineComponent, ref, onMounted } from "vue";
// import CustomInlineEditor from "@/v2/components/editorBuild/custom-inline/build/ckeditor";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useStore } from "vuex";
import EditAccessSection from "../EditAccessSection.vue";
import SaveEachContent from "../SaveEachContent.vue";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";

defineComponent([EditAccessSection]);

const store = useStore();
const { ckEditorLicense } = useInitializeConfig();

const isLayoutReady = ref(false);
const presenceListElement = ref();
const editorElement = ref();
const initialData = ref("");
const isLoading = ref<boolean>(true);

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
});
const getDisabledCondition = ref(false);
const editor = EditorOutput.CustomInline;
const editorConfig = ref({
  initialData: "",
  toolbar: {
    removeItems: [
      "previousPage",
      "nextPage",
      "pageNavigation",
      "highlight",
      "horizontalLine",
      "blockQuote",
      "code",
      "codeBlock",
      "htmlEmbed",
      "todoList",
      "showBlocks",
      "tableOfContents",
      "pageBreak",
      "removeFormat",
      "exportPdf",
      "exportWord",
      "importWord",
    ],
  },
  licenseKey: ckEditorLicense.value,
  cloudServices: {
    tokenUrl: !process.env.VUE_APP_CKEDITOR_TOKEN
      ? () =>
          new Promise((resolve, reject) => {
            store
              .dispatch("userStore/fetchCKEditorToken")
              .then((data) => resolve(data.ResponseData.value))
              .catch((error) => reject(error));
          })
      : "https://107440.cke-cs.com/token/dev/vweAiWiSPIvvaQFyKOLay34eFiHV2njU0Gze?limit=10",
    webSocketUrl: process.env.VUE_APP_WEBSOCKET,
    bundleVersion: process.env.VUE_APP_CKEDITOR_BUNDLE_VERSION,
  },
  collaboration: {
    channelId: `${props.channelId}`,
  },
  ckbox: {
    tokenUrl: !process.env.VUE_APP_CKEDITOR_TOKEN
      ? () =>
          new Promise((resolve, reject) => {
            store
              .dispatch("userStore/fetchCKBoxToken")
              .then((data) => resolve(data.ResponseData.value))
              .catch((error) => reject(error));
          })
      : "https://107440.cke-cs.com/token/dev/vweAiWiSPIvvaQFyKOLay34eFiHV2njU0Gze?limit=10",
    serviceOrigin:
      "https://ckbox-ckeditor-ckeditor.apps.development.corp.bi.go.id",
  },
  sidebar: {
    container: null,
  },
  presenceList: {
    container: null,
    collapseAt: 3,
  },
  documentOutline: {
    container: null,
  },
  removePlugins: [
    "CodeBlock",
    "Code",
    "RemoveFormat",
    "BlockQuote",
    "PageBreak",
    "TableOfContents",
    "TodoList",
    "HorizontalLine",
    "HtmlEmbed",
    "Highlight",
    "ShowBlocks",
    "ExportPdf",
    "ExportWord",
    "ImportWord",
    "Pagination",
  ],
});

onMounted(async () => {
  window.CKBox = CKBox;
  editorConfig.value.presenceList.container = presenceListElement.value;
  isLayoutReady.value = true;
  getDisabledCondition.value = [29].includes(
    store.getters["collaborationStore/getDocumentStatusId"]
  )
    ? true
    : store.getters["collaborationStore/getDisableAllForm"]
    ? true
    : !props.detailForm.isEdit;

  store.commit(
    "collaborationStore/setStartEditEForm",
    getDisabledCondition.value
  );
});

// const getDisabledCondition = () => {
//   if ([29].includes(store.getters["collaborationStore/getDocumentStatusId"])) {
//     return true;
//   } else {
//     return false;
//   }
// };

function onEditorReady() {
  isLoading.value = false;
}
</script>

<style scoped>
:deep(.ck.ck-presence-list__counter) {
  display: none;
}

:deep(.ck.ck-presence-list__marker) {
  height: 5px !important;
  border-radius: 10px;
}

:deep(.ck.ck-user.ck-user_me) {
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
</style>
