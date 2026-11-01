<template>
  <v-sheet>
    <!-- Error State -->
    <template v-if="errorState && !isInitializing">
      <div
        class="rounded-lg ma-2 elevation-0 text-center"
        style="min-height: 200px; border: 1px solid grey; background: #dfdfdf"
      >
        <p class="text-center ma-8 text-red text-14">
          {{ errorInfo || "Something went wrong while loading the editor." }}
        </p>
        <v-btn
          class="mx-auto mb-3 outlined rounded-lg"
          variant="outlined"
          color="red"
          @click="reloadEditor()"
        >
          Reload
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </div>
    </template>
    <!-- Editor Toolbar & Button -->
    <div v-if="!errorState" class="d-flex justify-space-between align-center">
      <div class="d-flex">
        <p
          v-if="collabMode"
          class="align-self-center mr-2 text-14 font-weight-bold"
        >
          online:
        </p>
        <div :class="`presenceListRef-${item.idFormEditor}`" />
        <v-chip
          v-if="hasTrackChanges"
          size="small"
          class="ml-2 track-changes-badge"
        >
          Active Track Changes
        </v-chip>
      </div>

      <EditorActionButton
        v-if="!isInitializing"
        @startCollaboration="startCollaboration"
        :collabMode="collabMode"
        :isInitializing="isInitializing"
        :item="item"
      />
    </div>

    <!-- Editor Container -->
    <div
      v-if="!errorState"
      class="mb-5"
      :class="[
        'editorContainer-' + item.idFormEditor,
        isInitializing ? 'loading' : '',
      ]"
      :id="`editorContainer-${item.idFormEditor}`"
    >
      <div
        :key="editorKey"
        ref="editorRef"
        :id="`editor-${item.idEForm}`"
        class="mb-5"
      />
    </div>

    <!-- Revision History -->
    <div
      ref="revisionContainer"
      class="revision-editor mb-5"
      :class="`revisionContainer-${item.idFormEditor}`"
    >
      <div class="revision-editor-container">
        <div
          ref="revisionEditorContainer"
          :class="`revisionEditorContainer-${item.idFormEditor}`"
        />
      </div>
      <div
        class="sidebar"
        ref="revisionSidebar"
        :class="`revisionSidebar-${item.idFormEditor}`"
      />
    </div>

    <!-- Loading Shimmer -->
    <free-style-shimmer
      v-if="isInitializing"
      width="100%"
      height="13rem"
      border-radius="15px"
      class="mb-5 mt-n4"
    />
  </v-sheet>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  onBeforeUnmount,
  onBeforeMount,
  nextTick,
  watch,
  computed,
} from "vue";
import Editor from "@/v2/components/side-project/ckeditor/build/ckeditor";
import * as CKBox from "ckbox";
import "ckbox/dist/styles/ckbox.css";
import { useStore } from "vuex";
import {
  getEditorInlineConfig,
  getFontFace,
  paperSize,
} from "@/v2/helpers/utils";
import EditorActionButton from "./EditorActionButton.vue";
import { DocConfig, TFormEditor } from "@v2/Type.d";
import { useToast } from "vue-toastification";
import { getNumberFromString } from "@/helpers/utils";

const toast = useToast();
const props = defineProps<{ item: TFormEditor; allFormIds: string[] }>();
const store = useStore();

const editorRef = ref<HTMLElement>();
const isInitializing = ref(false);
const editorKey = ref(0);
const collabMode = ref(false);
const errorState = ref(false);
const errorInfo = ref<string | null>(null);
const retryCount = ref(0);
const MAX_RETRY = 3;
const isUserLimitError = ref(false);
const isConnectionError = ref(false);
const hasTrackChanges = ref(false);
const docConfig = computed<DocConfig>(
  () => store.getters["collaborationStore/getDocConfig"]
);

let editorInstance: any;

// Function to detect user limit errors
const isUserLimitExceeded = (error: unknown): boolean => {
  const errorMsg = getErrorMessage(error).toLowerCase();
  const userLimitPatterns = ["users limit exceeded", "user limit exceeded"];

  const hasUserLimitInMessage = userLimitPatterns.some((pattern) =>
    errorMsg.includes(pattern)
  );

  let hasUserLimitInProperties = false;
  if (typeof error === "object" && error !== null) {
    const errorObj = error as any;
    const propsToCheck = ["code", "type", "name", "message", "description"];

    hasUserLimitInProperties = propsToCheck.some((prop) => {
      const propValue = errorObj[prop];
      if (typeof propValue === "string") {
        return userLimitPatterns.some((pattern) =>
          propValue.toLowerCase().includes(pattern)
        );
      }
      return false;
    });
  }

  return hasUserLimitInMessage || hasUserLimitInProperties;
};

// Function to detect connection errors
const isConnectionFailed = (error: unknown): boolean => {
  const errorMsg = getErrorMessage(error).toLowerCase();
  const connectionPatterns = [
    "connection attempts failed",
    "connection failed",
    "connection attempts exceeded",
    "network error",
    "connection timeout",
    "websocket connection failed",
    "collaboration server unreachable",
    "unable to connect to server",
    "connection refused",
    "server unavailable",
  ];

  const hasConnectionErrorInMessage = connectionPatterns.some((pattern) =>
    errorMsg.includes(pattern)
  );

  let hasConnectionErrorInProperties = false;
  if (typeof error === "object" && error !== null) {
    const errorObj = error as any;
    const propsToCheck = ["code", "type", "name", "message", "description"];

    hasConnectionErrorInProperties = propsToCheck.some((prop) => {
      const propValue = errorObj[prop];
      if (typeof propValue === "string") {
        return connectionPatterns.some((pattern) =>
          propValue.toLowerCase().includes(pattern)
        );
      }
      return false;
    });
  }

  return hasConnectionErrorInMessage || hasConnectionErrorInProperties;
};

const handleEditorError = async (error: unknown) => {
  errorState.value = true;
  errorInfo.value = getErrorMessage(error);

  // Check for user limit errors first
  if (isUserLimitExceeded(error)) {
    isUserLimitError.value = true;
    isConnectionError.value = false;

    // Set user limit error in store for global tracking
    await store.dispatch("documentStore/checkUserLimit", true);
    toast.error("CKEditor user limit exceeded. Check console for details.");

    return;
  }

  // Check for connection errors
  if (isConnectionFailed(error)) {
    isConnectionError.value = true;
    isUserLimitError.value = false;

    // Set connection error in store for global tracking
    await store.dispatch("documentStore/checkConnectionFailed", true);
    return;
  }

  // Regular error logging
  console.error("[CKEDITOR Error]", error);

  if (errorInfo.value?.toString().includes("token-not-in-jwt-format")) {
    console.error("Token not in JWT format, fetching CKEditor token.");
    store.dispatch("userStore/fetchCKEditorToken").then(() => {
      retryCount.value = 0;
      reloadEditor();
    });
  }

  //Restore document 409
  const errorMsg = getErrorMessage(error);
  if (
    (typeof error === "object" &&
      error !== null &&
      (error as any).code === 409) ||
    errorMsg.includes("409")
  ) {
    // Jalankan restoreCollabSession jika terjadi 409
    await store.dispatch("eFormStore/restoreCollabSession", {
      id: props.item.idFormEditor,
    });
    toast.warning(
      "Collaboration session conflict detected. Restoring session..."
    );
    return;
  }
};

const getErrorMessage = (error: unknown): string => {
  if (typeof error === "string") return error;
  if (error instanceof Error) return error.message;
  try {
    return JSON.stringify(error);
  } catch {
    return "Unknown error occurred";
  }
};

const setupUserLimitMonitoring = () => {
  const originalConsoleError = console.error;

  console.error = (...args) => {
    const errorString = args.join(" ").toLowerCase();

    // Check for user limit errors
    if (
      errorString.includes("users limit exceeded") ||
      errorString.includes("user limit exceeded")
    ) {
      // Set user limit error in store
      store.dispatch("documentStore/checkUserLimit", true);
      isUserLimitError.value = true;
      isConnectionError.value = false;
    }

    // Check for connection errors in console
    if (
      errorString.includes("connection attempts failed") ||
      errorString.includes("connection attempts exceeded") ||
      errorString.includes("failed to connect") ||
      errorString.includes("network error") ||
      errorString.includes("websocket connection failed")
    ) {
      isConnectionError.value = true;
      isUserLimitError.value = false;

      // Set connection error in store for global tracking
      store.dispatch("documentStore/checkConnectionFailed", true);
    }

    // Call original console.error
    originalConsoleError.apply(console, args);
  };
};

const createEditor = async (withCollab = false) => {
  setupUserLimitMonitoring();
  if (!editorRef.value) return;
  isInitializing.value = true;
  try {
    const config = await getEditorInlineConfig({
      store,
      channelId: props.item.idFormEditor,
      withCollab,
    });

    editorInstance = await Editor.CustomInline.create(editorRef.value, config);

    if (!withCollab) {
      editorInstance.enableReadOnlyMode("readOnlyMode");
      await fetchInitialContent();
    }

    onEditorCreated(editorInstance);

    // Reset error states on success
    errorState.value = false;
    errorInfo.value = null;
    isUserLimitError.value = false;
    isConnectionError.value = false;

    // Reset user limit flag in store on successful editor creation
    await store.dispatch("documentStore/checkUserLimit", false);
    await store.dispatch("documentStore/checkConnectionFailed", false);
  } catch (error) {
    await handleEditorError(error);
  } finally {
    collabMode.value = withCollab;
    isInitializing.value = false;
  }
};

const startCollaboration = async () => {
  setupUserLimitMonitoring();
  if (retryCount.value >= MAX_RETRY) {
    toast.error("Maximum retry attempts reached.");
    return;
  }

  // Check for user limit errors
  if (isUserLimitError.value) {
    toast.warning("Cannot start collaboration - user limit reached.");
    return;
  }

  // Check for connection errors
  if (isConnectionError.value && retryCount.value >= MAX_RETRY) {
    toast.error(
      "Cannot start collaboration - connection failed. Please check your network."
    );
    return;
  }

  // Reset error flags in store before starting collaboration
  await store.dispatch("documentStore/checkUserLimit", false);
  await store.dispatch("documentStore/checkConnectionFailed", false);

  isConnectionError.value = false;

  errorState.value = false;
  await editorInstance?.destroy();
  editorKey.value++;
  await nextTick();
  retryCount.value++;
  await createEditor(true);
};

const reloadEditor = async () => {
  if (retryCount.value >= MAX_RETRY) {
    // Different handling based on error type
    if (isConnectionError.value) {
      toast.error(
        "Connection attempts failed. Please check your network and reload the page manually."
      );
    } else if (isUserLimitError.value) {
      toast.error(
        "User limit reached. Please try again later or reload the page."
      );
    } else {
      toast.error("Maximum retry attempts reached, reloading the page.");
    }

    setTimeout(() => {
      window.location.reload();
    }, 2000);
    return;
  }

  // Block reload for user limit errors
  if (isUserLimitError.value) {
    toast.warning("Cannot reload editor - user limit reached.");
    return;
  }

  // Show retry message for connection errors
  if (isConnectionError.value) {
    toast.info(`Retrying connection... (${retryCount.value + 1}/${MAX_RETRY})`);
  }

  // Reset error flags in store before retry
  await store.dispatch("documentStore/checkUserLimit", false);
  await store.dispatch("documentStore/checkConnectionFailed", false);

  isConnectionError.value = false;

  errorState.value = false;
  await editorInstance?.destroy();
  editorKey.value++;
  await nextTick();
  retryCount.value++;
  await createEditor(false);
};

// Watch for store user limit changes
const userLimitErrorFromStore = computed(
  () => store.getters["documentStore/getUserLimitError"]
);

// Watch for store connection error changes
const connectionErrorFromStore = computed(
  () => store.getters["documentStore/getConnectionFailed"]
);

watch(userLimitErrorFromStore, (newValue) => {
  if (newValue) {
    isUserLimitError.value = true;
    isConnectionError.value = false;
    errorState.value = true;
    errorInfo.value = "User limit exceeded";
  }
});

// Watch for store connection error changes
watch(connectionErrorFromStore, (newValue) => {
  if (newValue) {
    isConnectionError.value = true;
    isUserLimitError.value = false;
    errorState.value = true;
    errorInfo.value = "Connection failed";
  }
});

onMounted(() => {
  // Check initial store states
  if (userLimitErrorFromStore.value) {
    isUserLimitError.value = true;
    errorState.value = true;
    errorInfo.value = "User limit exceeded";
  }

  if (connectionErrorFromStore.value) {
    isConnectionError.value = true;
    errorState.value = true;
    errorInfo.value = "Connection failed";
  }

  createEditor();
});

onBeforeUnmount(() => {
  editorInstance?.destroy();
  store.dispatch("documentStore/checkUserLimit", false);
  store.dispatch("documentStore/checkConnectionFailed", false);
});

const onEditorCreated = (editor: any) => {
  editor.editing.view.document.on("paste", (event, data) => {
    const htmlData = data.dataTransfer.getData("text/html");
    const fileUrlMatches = htmlData.match(/file:\/\/\/[^\s"'<>]+\.(emf|emz)/gi);
    if (fileUrlMatches?.length) {
      const fileNames = fileUrlMatches.map(
        (path) => path.split("/").pop() || ""
      );
      fileNames.forEach((val) => {
        toast.warning(
          "Your image contains a forbidden file extension: " + val,
          { timeout: 5000 }
        );
      });
    }
    setTimeout(() => {
      validateContent(editor);
    }, 1000);
  });

  const tableWidthCommand = editor.commands.get("tableWidth");
  tableWidthCommand.on("execute", () => validateContent(editor));
  const resizeColumnWidthsCommand = editor.commands.get("resizeColumnWidths");
  resizeColumnWidthsCommand.on("execute", () => validateContent(editor));

  const acceptSuggestionCommand = editor.commands.get("acceptSuggestion");
  if (acceptSuggestionCommand) {
    acceptSuggestionCommand.on("execute", () => {
      setTimeout(() => {
        const currentData = editor.getData();
        hasTrackChanges.value = /<suggestion-start[^>]*>/i.test(currentData);
      }, 300);
    });
  }

  if (!editor.getData().length) {
    editor.execute("fontSize", { value: "11pt" });
    const fontName = getFontFace(documentType.value);
    editor.execute("fontFamily", {
      value: fontName.includes(" ") ? `'${fontName}` : fontName,
    });
  }

  // const rulerPlugin = editor.plugins.get("Ruler");
  // const toolbarBalloonPanelContent = editor.ui.view.panel.content;
  // toolbarBalloonPanelContent.add(
  //   rulerPlugin.rulerView,
  //   toolbarBalloonPanelContent.length
  // );

  window.CKBox = CKBox;
};

const validateContent = (editor: any) => {
  for (const node of (editor as any).model.document.getRoot().getChildren()) {
    validateNodeWidth(editor, node);
  }
};

const validateNodeWidth = (editor: any, node: any) => {
  if (node.name === "table" && node.getAttribute("tableWidth")) {
    const tablePropertiesUI = editor.plugins.get("TablePropertiesUI");
    const tablePropertiesView = tablePropertiesUI.view;
    const tableWidth = node.getAttribute("tableWidth");
    const paperConfig: { width: number; height: number } =
      paperSize[docConfig.value.size ?? "A4"];
    const widthType: string = tableWidth.includes("%") ? "%" : "px";
    const widthValue: number = parseFloat(getNumberFromString(tableWidth));
    const paperWidthInPx =
      docConfig.value.orientation == "landscape"
        ? paperConfig.height
        : paperConfig.width;
    let maxWidth = widthType === "%" ? 100 : paperWidthInPx;

    if (tableWidth) {
      /**
        Adjust maxWidth based on document margins if they are defined and the width type is in pixels
      */
      if (
        (docConfig.value.margins.left || docConfig.value.margins.right) &&
        widthType === "px"
      ) {
        // docConfig margins ex. 20mm
        const margins = {
          left: parseFloat(getNumberFromString(docConfig.value.margins.left)),
          right: parseFloat(getNumberFromString(docConfig.value.margins.right)),
        };
        maxWidth -= margins.left * 3.7795 + margins.right * 3.7795;
      }

      /** Set maximal table width */
      if (widthValue > maxWidth) {
        editor.model.change((writer: any) => {
          writer.setAttribute("tableWidth", "100%", node);
        });
        if (tablePropertiesView) {
          tablePropertiesView.width = "100%";
        }
      }

      /** validate column widths */
      const minColWidth = 40; // Minimal width for columns in pixels
      const tableWidthInPx =
        widthType === "%" ? (paperWidthInPx * widthValue) / 100 : widthValue; // Convert percentage to pixels if needed
      node._children._nodes.map((item) => {
        if (item.name === "tableColumnGroup") {
          item._children._nodes.map((col) => {
            let colWidth = col.getAttribute("columnWidth"); // always in percentage
            const colWidthInPx =
              (tableWidthInPx * parseFloat(getNumberFromString(colWidth))) /
              100;

            if (colWidthInPx < minColWidth) {
              colWidth = `${(minColWidth / tableWidthInPx) * 100}%`; // convert back to percentage
            }

            if (col.name === "tableColumn") {
              editor.model.change((writer: any) => {
                writer.setAttribute("columnWidth", colWidth, col);
              });
            }
          });
        }
      });
    }
  } else {
    if (node._children) {
      for (const nd of node._children._nodes) {
        validateNodeWidth(editor, nd);
      }
    }
  }
};

const fetchInitialContent = async () => {
  isInitializing.value = true;
  const data = await store.dispatch(
    "documentStore/fetchContentFromStorage",
    props.item.idFormEditor
  );

  const initData = data.responseData?.content || "";
  hasTrackChanges.value = /<suggestion-start[^>]*>/i.test(initData);
  const sanitizedData = sanitizeSuggestions(initData);

  if (editorInstance) {
    editorInstance.setData(sanitizedData);
  } else {
    await createEditor();
    if (editorInstance) {
      editorInstance.setData(sanitizedData);
    }
  }
};

const sanitizeSuggestions = (htmlString) => {
  if (!htmlString) {
    return "";
  }
  // Remove suggestion tags: <suggestion-start>, </suggestion-start>, <suggestion-end>, </suggestion-end>
  const suggestionTagRegex = /<\/?suggestion-(start|end)[^>]*>/gi;

  // Remove data-suggestion attributes from elements
  const suggestionDataRegex =
    /\s*data-suggestion-(start-before|end-after)="[^"]*"/gi;

  return htmlString
    .replace(suggestionTagRegex, "")
    .replace(suggestionDataRegex, "");
};

const documentType = computed(
  () => store.getters["collaborationStore/getDocumentTypeId"]
);

watch(
  () => store.state.documentStore.loadingAsync,
  (val: boolean) => {
    if (val && editorInstance) {
      editorInstance.enableReadOnlyMode("readOnlyMode");
    }
  }
);

watch(
  () => store.state.collaborationStore.reloadTrackChanges,
  async (val: number) => {
    if (val && editorInstance) {
      try {
        await nextTick();
        let trackChangesActive = false;
        try {
          const trackChangesPlugin = editorInstance.plugins.get("TrackChanges");
          if (trackChangesPlugin) {
            const suggestions = trackChangesPlugin.getSuggestions();
            if (suggestions && suggestions.length > 0) {
              editorInstance.execute("acceptAllSuggestions");
              trackChangesActive = true;
              await nextTick();
              await new Promise((resolve) => setTimeout(resolve, 500));
            }
          }
        } catch (e) {
          console.error("TrackChanges plugin not available");
        }
        if (!trackChangesActive) {
          const currentData = editorInstance.getData();
          const cleanedData = sanitizeSuggestions(currentData);
          if (cleanedData !== currentData) {
            editorInstance.setData(cleanedData);
            await nextTick();
          }
        }
        const finalData = editorInstance.getData();
        hasTrackChanges.value = /<suggestion-start[^>]*>/i.test(finalData);
      } catch (error) {
        console.error("Error accepting suggestions:", error);
      }
    }
  }
);

// Revision History Handling
const editorContainer = ref(null);
const revisionContainer = ref(
  document.querySelector(`.revisionContainer-${props.item.idFormEditor}`)
);
const revisionEditorContainer = ref(
  document.querySelector(`.revisionEditorContainer-${props.item.idFormEditor}`)
);
const revisionSidebar = ref(
  document.querySelector(`.revisionSidebar-${props.item.idFormEditor}`)
);
const sidebarForRevision = ref(document.getElementById("sidebar-forrevision"));
const toc = ref(document.getElementById("tableofcontent"));
const isRevisionHistoryVisible = ref(false);
let observer: MutationObserver | undefined;

const observeStyleChanges = () => {
  if (!revisionContainer.value) return;
  observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === "style") {
        const style = (mutation.target as HTMLElement).style;
        if (style.display === "block") {
          isRevisionHistoryVisible.value = true;
          toc.value!.style.display = "none";
          const revSidebar = document.getElementsByClassName(
            "ck-revision-history-sidebar"
          );
          if (revSidebar.length > 0) {
            sidebarForRevision.value?.appendChild(revSidebar[0]);
            sidebarForRevision.value!.style.display = "block";
            props.allFormIds.forEach((id) => {
              if (id !== props.item.idFormEditor) {
                const container = document.getElementById(
                  `editorContainer-${id}`
                ) as HTMLElement;
                container.classList.add("editor-disabled");
                container.style.position = "relative";
                container.style.pointerEvents = "none";
              }
            });
          }
        } else {
          isRevisionHistoryVisible.value = false;
          toc.value!.style.display = "block";
          sidebarForRevision.value!.style.display = "none";
          props.allFormIds.forEach((id) => {
            const container = document.getElementById(
              `editorContainer-${id}`
            ) as HTMLElement;
            container.classList.remove("editor-disabled");
            container.style.pointerEvents = "auto";
          });
        }
      }
    });
  });

  observer.observe(revisionContainer.value, {
    attributes: true,
    attributeFilter: ["style"],
  });
};

onMounted(() => observeStyleChanges());
onBeforeMount(() => {
  if (observer) observer.disconnect();
});

//==================================Revision History Variable================================\\
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
.track-changes-badge {
  background-color: rgb(255, 238, 202);
  color: rgb(144, 110, 44);
  font-weight: 500;
  animation: pulse 2s infinite;
  font-weight: bold;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.editor-disabled::before {
  content: "Read only - Revision History Opened";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  background: rgba(0, 0, 0, 0.6);
  padding: 8px 16px;
  border-radius: 8px;
  z-index: 10;
  font-weight: bold;
  pointer-events: none;
}

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
