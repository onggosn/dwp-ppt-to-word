<template>
  <v-sheet class="my-3">
    <v-row v-if="props.isLoading">
      <v-col cols="12">
        <free-style-shimmer
          width="100%"
          height="32px"
          border-radius="10px"
          color="#d3d3d3"
        />
      </v-col>
    </v-row>
    <v-expansion-panels v-model="panel" :readonly="!canExpand || isDisable">
      <v-expansion-panel :value="item.idMBPDocumentTemplate">
        <v-expansion-panel-title :hide-actions="!canExpand">
          <v-row align="center" style="cursor: pointer !important">
            <v-col cols="5" style="padding: 0 !important">
              <div class="d-flex align-center">
                <img
                  :src="require(`@/v2/assets/icon/drag2.svg`)"
                  v-if="isDragParent"
                />

                <span
                  class="font-weight-bold text-truncate-2 ellipsis-1"
                  :class="[isDisable ? 'text-disable ' : '']"
                  :title="filterHTMLTag(item.bPEFormLabel) || '-'"
                  v-text="filterHTMLTag(item.bPEFormLabel) || '-'"
                ></span>
              </div>
            </v-col>
            <v-col cols="1" style="padding: 0 !important">
              <v-chip
                v-if="item?.isHeader"
                :class="[!isDisable ? 'chip-header' : 'chip-sector--disabled']"
              >
                Header
              </v-chip>
            </v-col>
            <v-col cols="2" class="chip-column">
              <v-chip
                v-if="item?.sectorName"
                :class="[!isDisable ? 'chip-sector' : 'chip-sector--disabled']"
              >
                {{ item.sectorName }}
              </v-chip>
            </v-col>
            <v-col cols="4" style="padding: 0 !important">
              <div
                class="d-flex flex-wrap ml-auto mr-5"
                style="justify-content: flex-end; gap: 10px"
              >
                <div class="d-flex align-center" v-if="isDragChild">
                  <v-btn
                    size="small"
                    class="mr-2 rounded-lg font-weight-bold"
                    color="#D6212A"
                    min-width="90px"
                    style="color: white"
                    @click.stop="cancelDrag"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    size="small"
                    class="mr-2 rounded-lg font-weight-bold"
                    color="#065695"
                    min-width="90px"
                    style="color: white"
                    @click.stop="saveDrag"
                  >
                    Save
                  </v-btn>
                </div>
                <btn-delete
                  v-if="item.isDelete && !isDisable"
                  :title="'Delete Section'"
                  :is-icon-button="true"
                  :subtitle="'Are you sure delete this section ?'"
                  :description="'Deleting the section will delete subsections, mappings, and permissions on this document'"
                  :append-icon="true"
                  :btn-color="'#d6212a'"
                  :btn-icon-color="'#d6212a'"
                  :disabled-delete-last-item="itemCount === 1"
                  @update="deleteSectionContent(item)"
                >
                  <v-tooltip activator="parent" location="bottom">
                    Delete
                  </v-tooltip>
                </btn-delete>

                <v-btn
                  v-if="item.isEdit && !isDisable"
                  class="rounded-lg px-2 py-2"
                  min-width="0"
                  color="#065695"
                  variant="outlined"
                  @click.stop="emit('onEdit', true)"
                >
                  <img :src="require('@/v2/assets/icon/edit.svg')" />
                  <v-tooltip activator="parent" location="bottom">
                    Edit Section
                  </v-tooltip>
                </v-btn>
                <v-btn
                  v-if="!canExpand && !item.disabledRow && isDisablePpt"
                  class="rounded-lg px-2 py-2"
                  min-width="0"
                  color="#065695"
                  variant="outlined"
                  @click.stop="emit('onAddMapping', item, null)"
                >
                  <img :src="require('@/v2/assets/icon/paperupload.svg')" />
                  <v-tooltip activator="parent" location="bottom">
                    Mapping Section PPT
                  </v-tooltip>
                </v-btn>
                <v-btn
                  v-if="item.isMappingAccess && !canExpand && !isDisable"
                  class="rounded-lg px-2"
                  min-width="0"
                  color="#065695"
                  variant="outlined"
                  @click="emit('onAddStp', true)"
                >
                  <v-icon color="#065695" small style="cursor: pointer">
                    mdi-share-variant
                  </v-icon>
                  <v-tooltip activator="parent" location="bottom">
                    Mapping STP
                  </v-tooltip>
                </v-btn>
                <EditAccessSection
                  v-if="!props.item.childSection?.length && !isDisable"
                  :sectionName="props.item.bPEFormLabel"
                  :idMEform="props.item.idMEFormTemplate"
                  :title="
                    props.item.isSection
                      ? 'Edit Access Section'
                      : 'Edit Access Sub Section'
                  "
                  :key="
                    store.getters['collaborationStore/getDocumentFlowCheck']
                  "
                />
                <v-btn
                  v-if="!isDragChild && canExpand && props.item.isSectionOrder"
                  :disabled="isDragParent"
                  size="reguler"
                  variant="outlined"
                  class="rounded-lg font-weight-bold px-2 py-2"
                  color="#065695"
                  @click.stop="startDragChild()"
                >
                  <v-icon
                    color="#065695"
                    small
                    style="cursor: pointer; transform: rotateY(180deg)"
                  >
                    mdi-swap-vertical
                  </v-icon>
                  <v-tooltip activator="parent" location="bottom">
                    Change Order
                  </v-tooltip>
                </v-btn>

                <v-btn
                  v-if="
                    item.isAddSection &&
                    canAddSubsection &&
                    !isDisable &&
                    !item?.isHeader
                  "
                  class="rounded-lg px-2 font-weight-bold"
                  min-width="0"
                  color="#065695"
                  variant="outlined"
                  @click.stop="emit('onAddSubSection', true)"
                >
                  + Add Sub Section
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div>
            <draggable
              v-model="childListPanel"
              :disabled="!isDragChild"
              @start="drag = true"
              @end="drag = false"
              animation="200"
              item-key="id"
            >
              <template #item="{ element: item }">
                <v-card class="mb-3 pa-5 rounded-lg item-card">
                  <v-row
                    align="center"
                    style="cursor: pointer !important"
                    class="py-1 px-2"
                  >
                    <v-col cols="6" style="padding: 0 !important">
                      <div class="d-flex align-center">
                        <img
                          :src="require(`@/v2/assets/icon/drag2.svg`)"
                          v-if="isDragChild"
                        />
                        <span
                          :class="[
                            item.disabledRow
                              ? 'font-weight-bold text-disable text-truncate-2'
                              : 'font-weight-bold text-truncate-2',
                          ]"
                          style="
                            color: #4b4b4b;
                            overflow-wrap: break-word;
                            word-break: break-word;
                            white-space: normal;
                            display: block;
                            max-width: 100%;
                            padding-right: 32px;
                          "
                          :title="filterHTMLTag(item.bPEFormLabel) || '-'"
                          v-text="filterHTMLTag(item.bPEFormLabel) || '-'"
                        >
                        </span>
                      </div>
                    </v-col>
                    <v-col cols="3" class="chip-column">
                      <v-chip
                        v-if="item?.sectorName"
                        :class="[
                          !item.disabledRow
                            ? 'chip-sector'
                            : 'chip-sector--disabled',
                        ]"
                      >
                        {{ item.sectorName }}
                      </v-chip>
                    </v-col>
                    <v-col cols="3" style="padding: 0 !important">
                      <div
                        class="d-flex flex-wrap ml-auto mr-5"
                        style="justify-content: flex-end; gap: 10px"
                      >
                        <btn-delete
                          v-if="item.isDelete && !item.disabledRow"
                          :title="'Delete Section'"
                          :is-icon-button="true"
                          :subtitle="'Are you sure delete this section ?'"
                          :description="'Deleting the section will delete subsections, mappings, and permissions on this document'"
                          :append-icon="true"
                          :btn-color="'#d6212a'"
                          :btn-icon-color="'#d6212a'"
                          :disabled-delete-last-item="itemChildCount === 0"
                          @update="deleteSectionContent(item)"
                        >
                          <v-tooltip activator="parent" location="bottom">
                            Delete
                          </v-tooltip>
                        </btn-delete>

                        <v-btn
                          v-if="item.isEdit && !item.disabledRow"
                          class="rounded-lg px-2 py-2"
                          min-width="0"
                          color="#065695"
                          variant="outlined"
                          @click.stop="emit('onEditSubsection', item)"
                        >
                          <img :src="require('@/v2/assets/icon/edit.svg')" />
                        </v-btn>
                        <v-btn
                          v-if="isDisablePpt && !item.disabledRow"
                          class="rounded-lg px-2 py-2"
                          min-width="0"
                          color="#065695"
                          variant="outlined"
                          @click.stop="emit('onAddMapping', item, props.item)"
                        >
                          <img
                            :src="require('@/v2/assets/icon/paperupload.svg')"
                          />
                          <v-tooltip activator="parent" location="bottom">
                            Mapping Section PPT
                          </v-tooltip>
                        </v-btn>
                        <v-btn
                          v-if="item.isMappingAccess && !item.disabledRow"
                          class="rounded-lg px-2"
                          min-width="0"
                          color="#065695"
                          variant="outlined"
                          @click="emit('onAddStpSubsection', item)"
                        >
                          <v-icon color="#065695" small style="cursor: pointer">
                            mdi-share-variant
                          </v-icon>
                        </v-btn>
                        <EditAccessSection
                          v-if="item.isAccess && !item.disabledRow"
                          :sectionName="item.bPEFormLabel"
                          :idMEform="item.idMEFormTemplate"
                          :title="'Edit Access Sub Section'"
                          :key="
                            store.getters[
                              'collaborationStore/getDocumentFlowCheck'
                            ]
                          "
                        />
                      </div>
                    </v-col>
                  </v-row>
                </v-card>
              </template>
            </draggable>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, onMounted } from "vue";
import { useStore } from "vuex";
import EditAccessSection from "../../collaboration/EditAccessSection.vue";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
import { filterHTMLTag } from "@/v2/helpers/utils";
import draggable from "vuedraggable";
const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  childItems: {
    type: Object,
    default: () => {
      return {};
    },
  },
  canAddSubsection: {
    type: Boolean,
    default: false,
  },
  canExpand: {
    type: Boolean,
    default: true,
  },
  isDisable: {
    type: Boolean,
    default: false,
  },
  isDragParent: {
    type: Boolean,
    default: false,
  },
  itemCount: {
    type: Number,
    default: 0,
  },
  itemChildCount: {
    type: Number,
    default: 0,
  },
  isDisablePpt: {
    type: Boolean,
    default: false,
  },
});
const emit = defineEmits([
  "onAddStp",
  "onAddStpSubsection",
  "onAddSubSection",
  "onEdit",
  "onAddMapping",
  "onDeleteSection",
  "onExportSectionPpt",
  "onEditSubsection",
  "onStartDragChild",
]);

const originalChildList = ref<any>([]);
const childListPanel = ref<any>(props.childItems);

onMounted(() => {
  originalChildList.value = [...childListPanel.value];
});

const isDragChild = ref(false);
const drag = ref(false);
const startDragChild = () => {
  isDragChild.value = true;
  emit("onStartDragChild", true);
};
const saveDrag = () => {
  isDragChild.value = false;
  originalChildList.value = [...childListPanel.value];

  let payload = [
    ...childListPanel.value.map((item, index) => {
      return {
        idMEFormTemplate: item.idMEFormTemplate,
        eFormOrder: index,
      };
    }),
  ];

  store
    .dispatch("adminStore/updateSubSectionOrder", {
      idMBPSectionTemplate: props.item.idMBPSectionTemplate,
      data: payload,
    })
    .then((res) => {
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Sucessfully saved",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      }
    })
    .catch(() => {
      instance.value.toast.show({
        message: "Failed to save changes",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      emit("onStartDragChild", false);
    });
};

const cancelDrag = () => {
  isDragChild.value = false;
  childListPanel.value = [...originalChildList.value];
  emit("onStartDragChild", false);
};

const panel = ref<number[]>([]);

const store = useStore();
const instance = ref<any>(getCurrentInstance()?.root.refs);
const reloadSection = () => {
  emit("onDeleteSection");
};

const deleteSectionContent = (item: any) => {
  const payload = {
    idMBPSectionTemplate: item.idMBPSectionTemplate,
    idMEFormTemplate: item.idMEFormTemplate,
  };
  store
    .dispatch("adminStore/deleteSectionContent", payload)
    .then((res) => {
      if (res.responseCode == "011000") {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: res.responseMessage,
          color: "error",
          timeout: 3000,
          icon: "mdi-check",
        });
      }
    })
    .catch(() => {
      instance.value.toast.show({
        message: "Fail deleting section/subsection",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      reloadSection();
    });
};
</script>

<style scoped>
.item-card {
  padding: 30px 36px;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 1);

  /* Shadow 1 */
  box-shadow: 0px 2px 4px 2px rgba(0, 0, 0, 0.12);
}
.item-card:hover {
  background-color: rgba(150, 150, 150, 0.1);
  transition: background-color 0.1s ease-in-out;
}
.chip-sector {
  background-color: #e9f5ff;
  color: #2279bd;
}

.chip-header {
  background-color: #ffeeca;
  color: #906e2c;
}

.chip-sector--disabled {
  background-color: #dfdfdf !important;
  color: #aeaeb1 !important;
}

.text-disable {
  color: #babcca !important;
}

.disable-action:hover {
  pointer-events: none !important;
  background-color: transparent;
}

.text-truncate-2 {
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.chip-column {
  padding: 0 !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
