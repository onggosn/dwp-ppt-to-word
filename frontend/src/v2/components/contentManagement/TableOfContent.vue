<template>
  <template v-if="isLoading">
    <div class="d-flex ml-4 mt-4" v-for="i in 12" :key="i">
      <div>
        <free-style-shimmer
          height="25px"
          width="25px"
          border-radius="5px"
          color="#DCDCDC"
        />
      </div>
      <div class="ml-8">
        <free-style-shimmer
          height="10px"
          width="250px"
          border-radius="5px"
          color="#DCDCDC"
          class="mb-1"
        />
        <paragraph-shimmer :lines="1" :random-size="true" color="#DCDCDC" />
      </div>
    </div>
  </template>
  <template v-else>
    <v-expansion-panels
      v-if="listOutline.content"
      :model-value="panelContent"
      class="mt-3"
      elevation="0"
      :multiple="true"
    >
      <v-expansion-panel
        v-for="item in listOutline.content"
        :key="item.bpName"
        :value="item.bpName"
        style="margin-top: 0px"
      >
        <v-expansion-panel-title expand-icon="mdi-menu-down">
          <v-list-item
            class="text-black font-weight-bold head"
            prepend-icon="mdi-folder-open-outline"
          >
            {{ item.bpName }}
          </v-list-item>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-expansion-panels
            :model-value="panelDoc"
            elevation="0"
            :multiple="true"
          >
            <v-expansion-panel
              v-for="child in item.dataDocument"
              :key="child.idBpDocument"
              :value="child.idBpDocument"
              :disabled="!child.isView"
              style="margin-top: 0px"
              @click="handleRoute(child)"
            >
              <v-expansion-panel-title
                :expand-icon="
                  child.dataSection && child.dataSection.length
                    ? 'mdi-menu-down'
                    : 'none'
                "
                :collapse-icon="
                  child.dataSection && child.dataSection.length
                    ? 'mdi-menu-up'
                    : 'none'
                "
                class="child-title my-1"
              >
                <v-list-item style="width: 100%; padding: 4px 16px">
                  <div
                    class="d-flex flex-row justify-space-between align-center my-2"
                  >
                    <div
                      class="text-black"
                      :class="
                        panelDocActive === child.idBpDocument
                          ? 'text-red font-weight-bold text-split '
                          : ''
                      "
                    >
                      <!-- tooltip -->
                      <tooltipDialog :name="child.bpDocumentName" />
                    </div>
                    <!-- icon -->
                    <div
                      v-if="panelDocActive === child.idBpDocument"
                      class="ml-2"
                    >
                      <v-btn
                        icon
                        class="custom-small"
                        size="x-small"
                        :color="iconDoc['background-color']"
                      >
                        <v-icon
                          :icon="iconDoc.icon"
                          :color="iconDoc.color"
                        ></v-icon>
                      </v-btn>
                    </div>
                  </div>
                </v-list-item>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="child-panel">
                <v-list-item
                  class="text-black"
                  v-for="grandchild in child.dataSection"
                  :key="grandchild.idBpSection"
                >
                  <p
                    style="cursor: pointer"
                    class="text-black"
                    @click="handleSection(grandchild)"
                    v-html="formattedSectionName(grandchild.bpSectionName)"
                  ></p>

                  <!-- {{ grandchild.title }} -->
                </v-list-item>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-expansion-panel-text>
      </v-expansion-panel>
      <hr
        style="
          border: none;
          border-top: 2px solid #065695;
          width: 100%;
          margin: 15px 10px;
        "
      />
    </v-expansion-panels>
    <template v-if="listOutline.reference">
      <div class="mx-2 mb-4">
        <div class="font-weight-bold head" style="color: #000">Reference</div>
      </div>
      <v-expansion-panels
        :model-value="panelContent"
        :multiple="true"
        class="mt-3"
        elevation="0"
      >
        <v-expansion-panel
          v-for="item in listOutline.reference"
          :key="item.bpName"
          :value="item.bpName"
          style="margin-top: 0px"
          @click="handleBPReference(item)"
        >
          <v-expansion-panel-title expand-icon="mdi-menu-down">
            <v-list-item
              class="text-black font-weight-bold head"
              prepend-icon="mdi-folder-open-outline"
            >
              {{ item.bpName }}
            </v-list-item>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-expansion-panels
              :model-value="panelSector"
              elevation="0"
              :multiple="true"
            >
              <v-expansion-panel
                v-for="sector in item.dataSector"
                :key="sector.sectorName"
                :value="item.bpName + '' + sector.sectorName"
                style="margin-top: 0px"
              >
                <v-expansion-panel-title
                  expand-icon="mdi-menu-down"
                  class="child-title my-1"
                >
                  <v-list-item style="width: 100%; padding: 4px 0px">
                    <v-list-item class="head">
                      {{ sector.sectorName }}
                    </v-list-item>
                  </v-list-item>
                </v-expansion-panel-title>
                <v-expansion-panel-text class="child-panel">
                  <v-expansion-panels
                    :model-value="panelDoc"
                    class="my-0"
                    elevation="0"
                    :multiple="true"
                  >
                    <v-expansion-panel
                      v-for="doc in sector.dataDocument"
                      :key="doc.idBpDocument"
                      :value="doc.idBpDocument"
                      :disabled="!doc.isView"
                      @click="handleRoute(doc)"
                      style="margin-top: 0px"
                    >
                      <v-expansion-panel-title
                        expand-icon="mdi-menu-down"
                        class="child-title my-1"
                      >
                        <v-list-item style="width: 100%; padding: 0px 16px">
                          <div
                            class="d-flex flex-row justify-space-between align-center my-2"
                          >
                            <div
                              class="text-black"
                              :class="
                                panelDocActive === doc.idBpDocument
                                  ? 'text-red font-weight-bold text-split'
                                  : ''
                              "
                            >
                              <tooltip-dialog
                                :name="doc.bpDocumentName"
                              ></tooltip-dialog>
                            </div>
                            <!-- icon -->
                            <div
                              v-if="panelDocActive === doc.idBpDocument"
                              class="ml-2"
                            >
                              <v-btn
                                icon
                                class="custom-small"
                                size="x-small"
                                :color="iconDoc['background-color']"
                              >
                                <v-icon
                                  :icon="iconDoc.icon"
                                  :color="iconDoc.color"
                                ></v-icon>
                              </v-btn>
                            </div>
                          </div>
                        </v-list-item>
                      </v-expansion-panel-title>
                      <v-expansion-panel-text class="child-panel">
                        <v-list-item
                          class="text-black"
                          v-for="grandchild in doc.dataSection"
                          :key="grandchild.idBpSection"
                        >
                          <p
                            style="cursor: pointer"
                            class="text-black"
                            @click="handleSection(grandchild)"
                          >
                            {{ grandchild.bpSectionName }}
                          </p>
                        </v-list-item>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </template>
    <template v-if="listOutline.publikasi">
      <!-- <div class="mx-2 mb-2 mt-4">
        <div class="font-weight-bold head" style="color: #000">Publikasi</div>
      </div> -->
      <v-expansion-panels
        v-if="listOutline.publikasi"
        :model-value="listOutline.publikasi.map((s) => s.bpName)"
        class="mb-6"
        elevation="0"
        :multiple="true"
        :readonly="true"
      >
        <template v-for="item in listOutline.publikasi" :key="item.bpName">
          <v-expansion-panel :value="item.bpName" style="margin-top: 0px">
            <v-expansion-panel-title expand-icon="none" collapse-icon="none">
              <div class="text-black font-weight-bold head ml-2">
                {{ item.bpName }}
              </div>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-expansion-panels
                :model-value="panelDoc"
                elevation="0"
                :multiple="true"
              >
                <v-expansion-panel
                  v-for="child in item.dataDocument"
                  :key="child.idBpDocument"
                  :value="child.idBpDocument"
                  :disabled="!child.isView"
                  style="margin-top: 0px"
                  @click="handleRoute(child)"
                >
                  <v-expansion-panel-title
                    expand-icon="mdi-menu-down"
                    class="child-title my-1"
                  >
                    <v-list-item style="width: 100%; padding: 4px 16px">
                      <div
                        class="d-flex flex-row justify-space-between align-center my-2"
                      >
                        <div
                          class="text-black"
                          :class="
                            panelDocActive === child.idBpDocument
                              ? 'text-red font-weight-bold text-split'
                              : ''
                          "
                        >
                          <tooltip-dialog
                            :name="child.bpDocumentName"
                          ></tooltip-dialog>
                        </div>
                        <!-- icon -->
                        <div
                          v-if="panelDocActive === child.idBpDocument"
                          class="ml-2"
                        >
                          <v-btn
                            icon
                            class="custom-small"
                            size="x-small"
                            :color="iconDoc['background-color']"
                          >
                            <v-icon
                              :icon="iconDoc.icon"
                              :color="iconDoc.color"
                            ></v-icon>
                          </v-btn>
                        </div>
                      </div>
                    </v-list-item>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text class="child-panel">
                    <v-list-item
                      class="text-black"
                      v-for="grandchild in child.dataSection"
                      :key="grandchild.idBpSection"
                    >
                      <p
                        style="cursor: pointer"
                        class="text-black"
                        @click="handleSection(grandchild)"
                        v-html="formattedSectionName(grandchild.bpSectionName)"
                      ></p>

                      <!-- {{ grandchild.title }} -->
                    </v-list-item>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </template>
      </v-expansion-panels>
    </template>
  </template>
  <modal-warning ref="modal" :modal-config="modalConfig" />
</template>

<script lang="ts" setup>
/* eslint-disable */
import ModalWarning from "@/v2/components/utils/modal/ModalWarning.vue";
import { useRouter, useRoute } from "vue-router";
import {
  TModalWarning,
  TRequestTOC,
  TTOC,
  TTOCDoc,
  TTOCSector,
  TTOCReference,
  TTOCSection,
} from "@/v2/Type";
import { ref, onMounted, computed, watch, onBeforeMount } from "vue";
import { getColorChipEditor } from "@v2/helpers/color";
import { useStore } from "vuex";
import { formattedSectionName } from "@/v2/helpers/utils";
import tooltipDialog from "@/v2/components/utils/dialog/TooltipDialog.vue";

const props = defineProps<{
  isApproved?: boolean;
  onRegisterRefresh: (refreshFunction: () => void) => void;
}>();

const router = useRouter();
const route = useRoute();
const store = useStore();

const panelContent = ref<string>("");
const panelDocActive = ref<string>("");
const panelDoc = ref<string[]>([]);

const panelSector = ref<string>("");
const isRevision = ref(false);

const needRefreshTOC = computed(
  () => store.getters["globalStore/getNeedRefreshTOC"]
);
const listOutline = computed((): TTOC => store.getters["contentStore/getTOC"]);
const idEvent = computed((): string => {
  const segments = route.path.split("/");
  const docIndex = segments.indexOf("doc");
  return docIndex > 0 ? segments[docIndex - 1] : "";
});
const idDoc = computed(
  (): string => (route.params.idDoc as string) ?? route.hash.split("#")[1]
);
const iconDoc = computed(() => {
  return getColorChipEditor(
    store.getters["collaborationStore/getDocumentStatus"]
  );
});
const modal = ref();
const modalConfig = ref<TModalWarning>({
  img: {
    location: "workspace/access-denied.svg",
    width: "395px",
    height: "311px",
  },
  title: "Access Denied",
  description:
    "You can't open this document. Speak to your administrator to open this document.",
  btnBackgroundStyle: "linear-gradient(to right, #065695, #267DC2)",
  textBtn: "Close",
  textWeight: 400,
  textStyle: "normal",
});
const emit = defineEmits(["refreshToc", "updateIsRevision"]);
const isLoading = ref(false);

function handleRoute(item: TTOCDoc) {
  if (item.isView) {
    if (props.isApproved) {
      router.replace({ hash: `#${item.idBpDocument}` });
    } else {
      store.commit("collaborationStore/setSectionActive", null);
      router.replace({ params: { idDoc: item.idBpDocument } });
    }
  } else {
    modalConfig.value = {
      img: {
        location: "workspace/access-denied.svg",
        width: "395px",
        height: "311px",
      },
      title: "Access Denied",
      description:
        "You can't open this document. Speak to your administrator to open this document.",
      btnBackgroundStyle: "linear-gradient(to right, #065695, #267DC2)",
      textBtn: "Close",
      textWeight: 400,
      textStyle: "normal",
    };
    modal.value.show();
  }
}

function handleSection(section: TTOCSection) {
  const status = store.getters["collaborationStore/getDocumentStatus"];
  if (status?.toLowerCase() == "approved") {
    store.commit("collaborationStore/setSectionActive", section.bpSectionName);
  } else {
    store.commit("collaborationStore/setSectionActive", section.idBpSection);
  }
}

function handleBPReference(item: TTOCReference) {
  if (item.dataSector.length == 0) {
    showModalFormIsEmpty();
  }
}

function getTableOfContent() {
  isLoading.value = true;
  const req: TRequestTOC = {
    idEvent: idEvent.value,
  };
  store
    .dispatch("contentStore/getTableOfContent", req)
    .then(() => {
      store.commit("globalStore/setNeedRefreshTOC", false);
      isLoading.value = false;
      setPannelActive();
      setIsRevisionFromListOutline(idDoc.value);
    })
    .catch((error) => {
      if (error.response.status === 403)
        router.push({ path: "/app/v2/workspace-management/rdgb" });
    });
}

function showModalFormIsEmpty() {
  modalConfig.value = {
    img: {
      location: "workspace/access-denied.svg",
      width: "395px",
      height: "311px",
    },
    title: "Don't Have Any Document",
    description:
      "You don't have any document. Speak to your administrator to open this document.",
    btnBackgroundStyle: "linear-gradient(to right, #065695, #267DC2)",
    textBtn: "Close",
    textWeight: 400,
    textStyle: "normal",
  };
  modal.value.show();
}

// handle active panel
function setPannelActive() {
  // set sector
  panelSector.value = "";
  const sectors: TTOCSector[] = [].concat.apply(
    [],
    listOutline.value.reference.map((reff) => reff.dataSector) as Array<any>
  );
  const sector = sectors.find(
    (sec) =>
      sec.dataDocument.filter((doc) => doc.idBpDocument === idDoc.value)
        .length > 0
  )?.sectorName as string;

  if (sector) {
    const content = listOutline.value.reference.find((reff) =>
      reff.dataSector.find((sec) =>
        sec.dataDocument.find((doc) => doc.idBpDocument === idDoc.value)
      )
    )?.bpName as string;
    panelContent.value = content;
    panelSector.value = content + "" + sector;
  } else {
    panelContent.value = listOutline.value.content.find((content) =>
      content.dataDocument?.find((doc) => doc.idBpDocument === idDoc.value)
    )?.bpName as string;
  }

  if (["00000000-0000-0000-0000-000000000000"].includes(idDoc.value)) {
    showModalFormIsEmpty();
  }
}

function loadTOC() {
  emit("refreshToc");
  panelDocActive.value = idDoc.value as string;
  getTableOfContent();
  props.onRegisterRefresh(getTableOfContent);
}

onBeforeMount(() => {
  panelDoc.value.push(idDoc.value as string);
});

onMounted(() => {
  loadTOC();
});

watch(
  () => needRefreshTOC.value,
  (newVal) => {
    if (newVal) {
      store.commit("globalStore/setNeedRefreshTOC", false);
      setTimeout(() => {
        loadTOC();
      }, 200);
    }
  }
);

watch(
  () => route.hash,
  (hash) => {
    setPannelActive();
    panelDocActive.value = hash.split("#")[1];
    panelDoc.value.push(hash.split("#")[1]);
    setIsRevisionFromListOutline(hash.split("#")[1]);
  }
);

watch(idDoc, (newVal) => {
  panelDocActive.value = newVal;
  setIsRevisionFromListOutline(newVal);
});

function setIsRevisionFromListOutline(docId: string) {
  isRevision.value = false;

  // Search in content
  if (listOutline.value.content) {
    for (const content of listOutline.value.content) {
      const doc = content.dataDocument?.find(
        (doc) => doc.idBpDocument === docId
      );
      if (doc && doc.isRevision !== undefined) {
        isRevision.value = doc.isRevision;
        emit("updateIsRevision", doc.isRevision);
        return;
      }
    }
  }

  // Search in reference
  if (listOutline.value.reference) {
    for (const reference of listOutline.value.reference) {
      for (const sector of reference.dataSector) {
        const doc = sector.dataDocument?.find(
          (doc) => doc.idBpDocument === docId
        );
        if (doc && doc.isRevision !== undefined) {
          isRevision.value = doc.isRevision;
          emit("updateIsRevision", doc.isRevision);
          return;
        }
      }
    }
  }

  // Search in publikasi
  if (listOutline.value.publikasi) {
    for (const publikasi of listOutline.value.publikasi) {
      const doc = publikasi.dataDocument?.find(
        (doc) => doc.idBpDocument === docId
      );
      if (doc && doc.isRevision !== undefined) {
        isRevision.value = doc.isRevision;
        emit("updateIsRevision", doc.isRevision);
        return;
      }
    }
  }

  emit("updateIsRevision", isRevision.value);
}
</script>
<style></style>
<style scoped>
.text-split {
  /* max-width: 225px; */
  overflow-wrap: break-word;
  word-wrap: break-word;
  /* line-break: anywhere; */
  /* hyphens: auto; */
}
:deep(.v-expansion-panel-title) {
  padding: 0px !important;
  padding-right: 15px !important;
}

:deep(.v-expansion-panel:not(:first-child)::after) {
  border-top-style: none;
  border-top-width: 0px;
}

:deep(.v-expansion-panel--active > .v-expansion-panel-title) {
  min-height: 40px !important;
}

:deep(.v-expansion-panel-title.child-title) {
  padding: 0px !important;
  padding-right: 5px !important;
  width: 95% !important;
  height: 50px !important;
}

:deep(.v-expansion-panel__shadow) {
  box-shadow: none !important;
}

:deep(.v-expansion-panel-title__overlay) {
  background-color: transparent !important;
}

:deep(.v-expansion-panel-text) {
  border-left: 3px solid #065695;
  margin-left: 25px;
}

:deep(.v-expansion-panel-text.child-panel) {
  border-left: 0px !important;
  margin-left: 20px;
}

:deep(.v-expansion-panel-text__wrapper) {
  padding: 0px !important;
}

:deep(.v-list-item__content) {
  color: #1a6eb1 !important;
}
:deep(.v-list-item__content .child-title) {
  color: black !important;
}

:deep(.custom-small.v-btn--size-x-small) {
  --v-btn-height: 10px;
}
</style>
