<template>
  <v-sheet class="mb-5 mt-5 bg-transparent" style="text-align: -webkit-center">
    <free-style-shimmer
      v-if="isLoading"
      width="100%"
      height="10rem"
      border-radius="15px"
      class="pt-4"
    />
    <div :class="['editor-root', isLoading ? 'loading' : '']" class="parent-1">
      <div class="row row-presence d-flex justify-space-between mb-1">
        <div class="d-flex">
          <p
            class="align-self-center mr-2 text-14 font-weight-bold"
            v-if="!isNotStartEdit"
          >
            online:
          </p>
          <div ref="presenceListElement" />
        </div>
        <div class="text-end align-self-center d-flex">
          <template v-if="!getDisabledCondition">
            <v-btn
              size="small"
              variant="outlined"
              style="border-radius: 10px"
              class="mr-2 mb-2"
              color="#065695"
              prepend-icon="mdi-pencil"
              @click="startEdit(channelId)"
              :disabled="!isNotStartEdit"
            >
              Edit Section
            </v-btn>
          </template>
          <template v-if="!getDisabledCondition">
            <BtnMngMapping
              :formSource="props.eformId"
              v-if="props.detailForm.isMapping"
            />
          </template>
          <template v-if="props.detailForm.isButtonAccess">
            <template v-if="!getDisabledCondition">
              <EditAccessSection
                :sectionName="props.sectionName"
                :idDoc="props.channelId"
                :idEform="props.eformId"
                :key="store.getters['collaborationStore/getDocumentFlowCheck']"
              />
            </template>
          </template>
        </div>
      </div>
      <span
        @click="reloadCkEditor"
        ref="btnReload"
        style="color: white; font-size: 10px"
      ></span>

      <div v-if="isNotStartEdit">
        <free-style-shimmer
          v-if="isLoadingNotStarted"
          width="100%"
          height="10rem"
          border-radius="15px"
          class="pt-4"
        />

        <div ref="editors" id="readonlyeditor" />
      </div>

      <template v-if="isEditorReady">
        <div ref="editorContainer" :id="`editorContainer-${channelId}`">
          <div ref="myEditor" :name="`form-${formIndex}`"></div>
        </div>
        <p class="hidetext">{{ WordCounter }}</p>
        <p class="hidetext">{{ channelId }}</p>

        <!-- Revision History Start  -->
        <div ref="revisionContainer" class="revision-editor">
          <div class="revision-editor-container">
            <div id="revision-viewer-editor" ref="revisionEditorContainer" />
          </div>

          <div
            class="sidebar"
            id="revision-viewer-sidebar"
            ref="revisionSidebar"
          />
        </div>
        <!-- Revision History End  -->
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

      <div ref="trackChangesContainter" v-if="isTrackChangesVisible">
        <form-editor-preview
          :channelId="props.channelId"
          :eformId="props.eformId"
        />
      </div>
    </div>
  </v-sheet>
</template>
<script setup lang="ts">
/* eslint-disable */
import {
  defineComponent,
  ref,
  onMounted,
  onUnmounted,
  onBeforeMount,
  computed,
  watch,
} from "vue";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useStore } from "vuex";
import EditAccessSection from "../EditAccessSection.vue";
import BtnMngMapping from "@v2/components/collaboration/MngMappingSection.vue";
import FormEditorPreview from "@v2/components/collaboration/editor/FormEditorPreview.vue";
import { ExportSuggestion } from "@/v2/library/ApiCKEditor";
import LogDialog from "./LogDialog.vue";
import DocumentTemplateLocal from "@/v2/components/collaboration/DocumentTemplateLocal.vue";
import { consoleLog } from "@/models/log";
import { useToast } from "vue-toastification";
import { useInitializeConfig } from "@/v2/composables/useInitializeConfig";
const toast = useToast();

defineComponent([EditAccessSection, BtnMngMapping]);

const documentName = computed(
  () => store.getters["collaborationStore/getDocumentName"]
);

const eventName = computed(
  () => store.getters["collaborationStore/getEventName"]
);

const dialog = ref(false);
const editors = ref<HTMLDivElement>();
const log = ref();
const WordCounter = ref();
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
  fontFace: {
    type: String,
    default: "Frutiger 45 Light",
  },
});
const editorContainer = ref();
const isNotStartEdit = ref(true);
const trackChangesContainter = ref();
const isTrackChangesVisible = ref(false);
const getDisabledCondition = ref(false);
const isEditorReady = ref(true);
const setContainTemp = ref(null);
const counterError = ref(0);
const btnReload = ref();
const isLoading = ref(false);
const isLoadingNotStarted = ref(false);
const revisionContainer: any = ref(null);
const revisionEditorContainer: any = ref(null);
const revisionSidebar: any = ref();
const toc = ref<any>();
const isRevisionHistoryVisible = ref(false);
const originalError = console.error;
const errorCode = ref();
const errorMessage = ref();
const sidebarForRevision = ref<any>(
  document.getElementById("sidebar-forrevision")
);
const emits = defineEmits(["editorArray", "allowEditor"]);
console.error = function (...args) {
  originalError.apply(console, args);
  errorMessage.value = args[0].message;
  errorCode.value = args[0].code;
};

toc.value = document.getElementById("tableofcontent");
let observer;
const observeStyleChanges = () => {
  if (revisionContainer.value) {
    observer = new MutationObserver((mutations: any) => {
      mutations.forEach((mutation) => {
        if (mutation.attributeName === "style") {
          if (mutation.target.style.display == "block") {
            isRevisionHistoryVisible.value = true;
            toc.value.style.display = "none";

            const revSidebar = document.getElementsByClassName(
              "ck-revision-history-sidebar"
            );

            if (revSidebar.length > 0) {
              sidebarForRevision.value?.appendChild(revSidebar[0]);
              sidebarForRevision.value.style.display = "block";
              emits("allowEditor", { state: false, except: props.channelId });
            }
          }

          if (mutation.target.style.display == "none") {
            isRevisionHistoryVisible.value = false;
            toc.value.style.display = "block";
            sidebarForRevision.value.style.display = "none";
            emits("allowEditor", { state: true, except: props.channelId });
          }
        }
      });
    });
    observer.observe(revisionContainer.value, {
      attributes: true,
      attributeFilter: ["style"],
    });
  }
};

async function initEditor() {
  if (editors.value) {
    let editorInstance = await EditorOutput.CustomDocument.create(
      editors.value,
      {
        initialData: setContainTemp.value || "",
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
        placeholder: "",
        removePlugins: [
          "Pagination",
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
              classes: ["table-kop-surat", "section-header-letter"],
              styles: true,
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
      }
    );
    // editorInstance.enableReadOnlyMode("readonlyeditor");
    isLoading.value = false;
  }
}

function getContentTemp() {
  isLoading.value = true;
  store
    .dispatch("documentStore/fetchContentFromStorage", props.channelId)
    .then((data) => {
      debugger;
      setContainTemp.value = data?.responseData?.content;
      initEditor();
      getDisabledCondition.value = [29].includes(
        store.getters["collaborationStore/getDocumentStatusId"]
      )
        ? true
        : store.getters["collaborationStore/getDisableAllForm"]
        ? true
        : !props.detailForm.isEdit;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function startEdit(temp) {
  doCreate();
  if (temp) {
    isNotStartEdit.value = false;
  } else {
    isNotStartEdit.value = true;
  }
}

const getColorChip = (value) => {
  switch (value) {
    case "insertion":
      return "green";
    case "deletion":
      return "red";
    default:
      return "primary";
  }
};
const listlog = ref<any>([]);
const generateLog = async () => {
  dialog.value = true;
  log.value = await ExportSuggestion(props.channelId);
  if (log.value.data.length) {
    log.value.data.forEach((element) => {
      listlog.value.push({
        author: element.author_id,
        type: element.type,
        created_at: element.created_at,
        state: element.state,
        workspace: eventName,
        document: documentName,
        section: props.sectionName,
      });
    });
  }
};

onMounted(() => getContentTemp());
// onMounted(async () => doCreate());
onMounted(() => observeStyleChanges());
onBeforeMount(() => {
  if (observer) {
    observer.disconnect();
  }
});

const showTrackChanges = () => {
  isTrackChangesVisible.value = !isTrackChangesVisible.value;
};

const doCreate = () => {
  isEditorReady.value = true;
  isLoading.value = true;
  CustomInline.create(myEditor.value, {
    initialData: "",
    updateSourceElementOnDestroy: false,
    toolbar: {
      items: [
        "fullscreen",
        "undo",
        "redo",
        "heading",
        "|",
        "bold",
        "italic",
        "underline",
        "strikethrough",
        "formatPainter",
        "superscript",
        "subscript",
        "removeFormat",
        "|",
        "link",
        "imageInsert",
        "ckboxImageEdit",
        "ckbox",
        "insertTable",
        "insertTableLayout",
        {
          label: "Fonts",
          icon: "text",
          items: [
            "fontFamily",
            "fontSize",
            "fontColor",
            "caseChange",
            "fontBackgroundColor",
          ],
        },
        "alignment",
        "|",
        "bulletedList",
        "numberedList",
        "outdent",
        "indent",
        "|",
        "findAndReplace",
        "specialCharacters",
        "blockQuote",
        "highlight",
        "revisionHistory",
        "comment",
        "commentsArchive",
        "importWord",
        "trackChanges",
      ],
      removeItems: [
        "previousPage",
        "nextPage",
        "pageNavigation",
        "highlight",
        "horizontalLine",
        "code",
        "codeBlock",
        "htmlEmbed",
        "todoList",
        "showBlocks",
        "tableOfContents",
        "pageBreak",
        "removeFormat",
        "style",
        "insertTemplate",
      ],
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
    presenceList: {
      container: presenceListElement.value,
      collapseAt: 4,
      displayMe: true,
    },
    list: {
      properties: {
        styles: true,
        startIndex: true,
        reversed: true,
      },
    },
    style: {
      definitions: [
        {
          name: "Line Spacing 1",
          element: "p",
          classes: ["spacing-1"],
        },
        {
          name: "Line Spacing 1.5",
          element: "p",
          classes: ["spacing-1-5"],
        },
        {
          name: "Line Spacing 2",
          element: "p",
          classes: ["spacing-2"],
        },
      ],
    },
    image: {
      styles: ["alignCenter", "alignLeft", "alignRight"],
      resizeOptions: [
        {
          name: "resizeImage:original",
          label: "Original",
          value: null,
        },
        {
          name: "resizeImage:25",
          label: "25%",
          value: "25",
        },
        {
          name: "resizeImage:50",
          label: "50%",
          value: "50",
        },
        {
          name: "resizeImage:75",
          label: "75%",
          value: "75",
        },
        {
          name: "resizeImage:100",
          label: "100%",
          value: "100",
        },
      ],
      toolbar: [
        "linkImage",
        "|",
        "imageTextAlternative",
        "toggleImageCaption",
        "|",
        "imageStyle:inline",
        "imageStyle:wrapText",
        "imageStyle:breakText",
        "|",
        "resizeImage",
        "|",
        "ckboxImageEdit",
      ],
      insert: {
        integrations: ["upload", "assetManager", "url"],
      },
    },
    htmlSupport: {
      allow: [
        {
          name: "li",
          classes: ["type-heading"],
        },
        {
          name: "ol",
          classes: true,
          styles: true,
          attributes: true,
        },
        {
          name: "ul",
          classes: true,
          styles: true,
          attributes: true,
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
        },
        {
          name: "table",
          classes: [
            "table-kop-surat",
            "section-header-letter",
            "table-width-full",
          ],
        },
      ],
      disallow: [
        {
          attributes: [
            { key: /^on(.*)/i, value: true },
            {
              key: /.*/,
              value: /(\b)(on\S+)(\s*)=|javascript:|(<\s*)(\/*)script/i,
            },
            { key: /.*/, value: /data:(?!image\/(png|jpeg|gif|webp))/i },
          ],
        },
        { name: "script" },
      ],
    },
    template: {
      definitions: [
        {
          title: "Test List",
          description: "List insertion",
          data: '<ol><li>First<ol style="list-style-type:lower-roman;"><li>Second</li><li>Third<ol style="list-style-type:upper-latin;"><li>Fourth</li><li>Fifth<ol style="list-style-type:lower-latin;"><li>Sixth</li></ol></li></ol></li></ol></li></ol',
        },
      ],
    },
    removePlugins: ["HorizontalLine", "Pagination"],
    placeholder: "Type the content here!",
    revisionHistory: {
      editorContainer: editorContainer.value,
      viewerContainer: revisionContainer.value,
      viewerEditorElement: revisionEditorContainer.value,
      viewerSidebarContainer: revisionSidebar.value,
      resumeUnsavedRevision: true,
    },
    sidebar: {
      // container: revisionSidebar.value,
      preventScrollOutOfView: true,
    },
    exportPdf: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(() => {
            const token = store.getters["userStore/getTokenDocument"];
            resolve(token);
          }, 1500);
        }),
      stylesheets: [
        "/doc/fonts.css",
        "/doc/style.css",
        "/doc/ckeditor5-premium-features.css",
        "/doc/ckeditor5.css",
      ],
      converterOptions: {
        format: "A4",
        margin_top: "20mm",
        margin_bottom: "20mm",
        margin_right: "24mm",
        margin_left: "24mm",
        page_orientation: "portrait",
      },
      converterUrl: process.env.VUE_APP_EXPORT_PDF,
      // dataCallback: (editor) => {
      // },
    },
    importWord: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(() => {
            const token = store.getters["userStore/getTokenDocument"];
            resolve(token);
          }, 1500);
        }),
      converterUrl: process.env.VUE_APP_IMPORT_WORD,
      formatting: {
        resets: "none",
        defaults: "none",
        styles: "inline",
        comments: "none",
      },
    },
    exportWord: {
      fileName: "document.docx",
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(() => {
            const token = store.getters["userStore/getTokenDocument"];
            resolve(token);
          }, 1500);
        }),
      converterUrl: process.env.VUE_APP_EXPORT_WORD,
      stylesheets: [
        "/doc/fonts.css",
        "/doc/style.css",
        "/doc/ckeditor5-premium-features.css",
        "/doc/ckeditor5.css",
      ],
      converterOptions: {
        document: {
          size: "A4",
          orientation: "portrait",
          margin: {
            top: "20mm",
            bottom: "20mm",
            right: "12mm",
            left: "12mm",
          },
          language: "en", // By default it is set to editor content language.
        },
      },
      dataCallback: (editor) => editor.getData({ pagination: true }),
    },
    fontFamily: {
      supportAllValues: false,
      options: [
        "default",
        "Arial, Helvetica, sans-serif",
        "Courier New, Courier, monospace",
        "Optima",
        "Frutiger 45 Light",
        "Tahoma",
        // "Segoe UI",
        // "Segoe UI Bold",
      ],
    },
    wordCount: {
      onUpdate: (stats) => {
        WordCounter.value = `Characters: ${stats.characters}\nWords: ${stats.words}`;
        if (stats.words == 0) {
          editorInline?.execute("fontSize", { value: "11pt" });
          if (props.fontFace.split(" ").length < 2) {
            editorInline?.execute("fontFamily", { value: props.fontFace });
          } else {
            editorInline?.execute("fontFamily", {
              value: `'${props.fontFace}`,
            });
          }
        }
      },
    },
  })
    .then((editor) => {
      editorInline = editor;
      editor.editing.view.document.on("paste", (event, data) => {
        const htmlData = data.dataTransfer.getData("text/html");
        const fileUrlMatches = htmlData.match(
          /file:\/\/\/[^\s"'<>]+\.(emf|emz)/gi
        );
        if (fileUrlMatches && fileUrlMatches.length > 0) {
          const fileNames = fileUrlMatches.map((path) => {
            const parts = path.split("/");
            return parts[parts.length - 1];
          });

          fileNames.forEach((val) => {
            toast.warning(
              "Your image contain not allowed extension file : " + val,
              { timeout: 5000 }
            );
          });
        }
      });

      if (!editorInline.getData().length) {
        editorInline.execute("fontSize", { value: "11pt" });
        // check if font name is 1 suku kata
        if (props.fontFace.split(" ").length < 2) {
          editorInline.execute("fontFamily", { value: props.fontFace });
        } else {
          editorInline.execute("fontFamily", { value: `'${props.fontFace}` });
        }
      }

      isLoading.value = false;
      if (getDisabledCondition.value) {
        editor.enableReadOnlyMode("feature-id");
      }
      let inlineEditorResizeObserver;
      const rulerPlugin = editor.plugins.get("Ruler");
      const toolbarBalloonPanelContent = editor.ui.view.panel.content;
      const domRoot = editor.editing.view.getDomRoot();

      // Make sure the inline editor toolbar has the same width as the editing root for the ruler
      // to be aligned properly.
      // inlineEditorResizeObserver = new ResizeObserver(
      //   editor.editing.view.getDomRoot(),
      //   () => {
      //     editor.ui.view.panel.element.style.width =
      //       new Rect(domRoot).width + "px";
      //   }
      // );

      // Add the ruler view to the panel that hosts the inline editor toolbar.
      toolbarBalloonPanelContent.add(
        rulerPlugin.rulerView,
        toolbarBalloonPanelContent.length
      );

      emits("editorArray", props.channelId);
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
  window.CKBox = CKBox;
  getDisabledCondition.value = [29].includes(
    store.getters["collaborationStore/getDocumentStatusId"]
  )
    ? true
    : store.getters["collaborationStore/getDisableAllForm"]
    ? true
    : !props.detailForm.isEdit;
};

const reloadCkEditor = () => {
  presenceListElement.value.innerHTML = "";
  doDestroy();
  isEditorReady.value = true;
  setTimeout(() => {
    myEditor.value.innerHTML = "";
    doCreate();
  }, 2 * 1000);
};

const doDestroy = () => {
  if (editorInline) {
    editorInline.destroy();
  }
};

watch(
  () => store.state.documentStore.loadingAsync,
  (val: boolean) => {
    if (val == true) {
      if (editorInline) {
        editorInline.enableReadOnlyMode("feature-id");
      }
    }
  }
);

watch(
  () => store.state.collaborationStore.reloadTrackChanges,
  (val: number) => {
    if (val != 0) {
      if (editorInline) {
        editorInline.execute("acceptAllSuggestions");
      }
    }
  }
);

onUnmounted(() => {
  doDestroy();
});
</script>
<style>
.ck.ck-revision-history-sidebar__revision-wrapper
  .ck-revision-history-sidebar__revision:last-child {
  margin-bottom: 0;
  background: white;
  border-left: 8px solid#dfdfdf;
  margin-left: 10px;
  border-radius: 10px;
  color: black;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  width: 97%;
}
.ck.ck-revision-history-sidebar__revision-wrapper
  .ck-revision-history-sidebar__revision.ck-revision-history-sidebar__revision_selected {
  background: white;
  border-left: 8px solid#267dc2;
  margin-left: 21px;
  border-radius: 10px;
  color: black;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}
.ck.ck-revision-history-sidebar__revision.ck-revision-history-sidebar__revision_selected
  .ck-revision-history-sidebar__revision__actions
  .ck-dropdown__button {
  color: black;
}
.ck.ck-revision-history-sidebar__revision-wrapper
  .ck-revision-history-sidebar__revision.ck-revision-history-sidebar__revision_selected
  .ck-revision-history-sidebar__revision-name
  .ck-input {
  color: black;
}

.ck.ck-revision-history-sidebar__revision-wrapper
  .ck-revision-history-sidebar__revision
  .ck-revision-history-sidebar__revision__date {
  text-align: left;
  font-size: 12px;
}

.ck.ck-revision-history-sidebar__time-period {
  text-align: left;
}

.ck.ck-revision-history-sidebar__time-period
  .ck-revision-history-sidebar__time-period__label {
  background: white;
  color: black;
  font-size: 14px;
}
.ck.ck-revision-history-sidebar__revision-author .ck-icon {
  color: #02aa59;
}
.ck.ck-dialog .ck.ck-dialog__actions > * + * {
  margin-left: var(--ck-spacing-large);
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 6px;
  margin-right: 20px;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.5);
}
.ck .ck-revision-history-save-revision-form .ck-input {
  border-radius: 5px;
  padding: 10px;
  border: 1px solid white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.5);
}
.ck .ck-dialog__content {
  padding: 20px;
}

.ck.ck-form__header {
  height: 50px;
}
.ck .ck-form__header__label {
  text-align: center;
  color: #3a416f;
}
.ck-rounded-corners .ck.ck-dialog {
  border-radius: 10px;
}

.revision-editor .ck-revision-history-sidebar {
  border-radius: 3px 10px 10px 3px;
  margin-right: 5px;
  position: fixed;
  height: 89vh;
  right: 0;
  top: 0;
  margin-top: 75px;
  background: white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.5);
  transition: padding 0.3s;
}

@media (min-width: 1600px) {
  .revision-editor .ck-revision-history-sidebar {
    width: 38vw;
    height: 91vh;
  }
}

@media (min-width: 1400px) and (max-width: 1599px) {
  .revision-editor .ck-revision-history-sidebar {
    width: 33vw;
    height: 90vh;
  }
}

@media (min-width: 1300px) and (max-width: 1399px) {
  .revision-editor .ck-revision-history-sidebar {
    width: 28vw;
    height: 89vh;
  }
}

@media (min-width: 768px) and (max-width: 1299px) {
  .revision-editor .ck-revision-history-sidebar {
    width: 18vw;
    height: 87vh;
  }
}

/* For screens that are 767px or narrower */
@media (max-width: 767px) {
  .revision-editor .ck-revision-history-sidebar {
    width: 100%;
    height: 100%;
  }
}

.revision-editor .ck-rounded-corners .ck.ck-editor__main > .ck-editor__editable,
.ck.ck-editor__main > .ck-editor__editable.ck-rounded-corners {
  border-radius: 1px 1px 10px 10px;
  min-height: 200px;
  border: 1px solid grey !important;
}

.revision-editor.ck-suggestion-marker-merge {
  display: inline !important;
}

.revision-editor .ck-suggestion-marker-deletion {
  display: inline !important;
}

.revision-editor .ck-suggestion-marker-split {
  display: inline !important;
}

.revision-editor
  .ck-content
  .ck-suggestion-marker-insertion.ck-suggestion-marker--active {
  background: var(
    --ck-color-suggestion-marker-insertion-background-active
  ) !important;
  border-color: var(
    --ck-color-suggestion-marker-insertion-border-active
  ) !important;
}

.revision-editor .ck-content .ck-suggestion-marker-insertion {
  background: var(--ck-color-suggestion-marker-insertion-background) !important;
  border-bottom: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
  border-top: 3px solid var(--ck-color-suggestion-marker-insertion-border) !important;
}

.revision-editor
  .ck-content
  .ck-suggestion-marker-deletion.ck-suggestion-marker--active {
  background: var(
    --ck-color-suggestion-marker-deletion-background-active
  ) !important;
  border-color: var(
    --ck-color-suggestion-marker-deletion-border-active
  ) !important;
}

.revision-editor .ck-content .ck-suggestion-marker-deletion {
  background: var(--ck-color-suggestion-marker-deletion-background) !important;
  border-bottom: 3px solid var(--ck-color-suggestion-marker-deletion-border) !important;
  border-top: 3px solid var(--ck-color-suggestion-marker-deletion-border) !important;
  text-decoration: line-through !important;
  text-decoration-color: var(
    --ck-color-suggestion-marker-deletion-stroke
  ) !important;
  text-decoration-thickness: 3px !important;
}

.revision-editor
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

:deep(.ck.ck-presence-list) {
  flex-direction: row-reverse;
}
.ck.ck-editor__editable_inline {
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

@media (min-width: 1600px) {
  .left-side {
    width: 60vw;
  }

  .right-side {
    width: 40vw;
  }
}

@media (min-width: 1400px) and (max-width: 1599px) {
  .left-side {
    width: 65vw;
  }

  .right-side {
    width: 35vw;
  }
}

@media (min-width: 1300px) and (max-width: 1399px) {
  .left-side {
    width: 70vw;
  }

  .right-side {
    width: 30vw;
  }
}

@media (min-width: 768px) and (max-width: 1299px) {
  .left-side {
    width: 80vw;
  }
  .right-side {
    width: 20vw;
  }
}

/* For screens that are 767px or narrower */
@media (max-width: 767px) {
  .right-side {
    width: 100%;
  }
}
</style>
