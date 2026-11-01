<template>
  <div>
    <v-expansion-panels
      class="mb-2"
      :readonly="section.isAnySubSection === false"
      v-model="panel"
    >
      <v-expansion-panel :value="section.idBPSection">
        <div class="d-flex align-center section-panel-header">
          <v-expansion-panel-title
            :hide-actions="true"
            class="section-panel-title"
            style="flex: 0 1 65%"
          >
            <div class="w-100 d-flex justify-space-between align-center">
              <div class="section-name-col" style="flex: 0 1 60%">
                <div class="text-truncate-1" :title="section.sectionName">
                  <img
                    :src="require(`@/v2/assets/icon/drag2.svg`)"
                    v-if="parentDragging"
                  />
                  {{ section.sectionName }}
                </div>
              </div>
              <div
                class="d-flex align-center justify-center section-chip-col"
                style="flex: 0 1 40%"
              >
                <v-chip
                  v-if="!!section.sectorName && isShowSector"
                  :style="(getColorChipTypeRdg('bulanan') as StyleValue)"
                  >{{ section.sectorName }}</v-chip
                >
                <v-chip v-if="section.isHeader" class="header-section"
                  >Header</v-chip
                >
              </div>
            </div>
            <span
              class="important-whitespace"
              v-if="section.isAnySubSection === false"
              style="width: 22px"
            ></span>
          </v-expansion-panel-title>
          <div
            class="d-flex justify-end align-center section-actions py-2"
            style="flex: 0 1 30%"
          >
            <btn-delete
              :dialog-width="640"
              btn-color="#CB3A31"
              btn-class="section-btn icon-only"
              btn-size="default"
              v-if="!!section.buttonDelete"
              :title="'Delete Section'"
              :is-icon-button="true"
              :hide-icon="true"
              :subtitle="'Are you sure delete this section? Deleting the section will delete subsections, mappings, and permissions on this document.'"
              :description="''"
              :append-icon="true"
              :btn-icon-color="'#d6212a'"
              :count-down="0"
              :btn-density="'compact'"
              positive-text-button="Yes"
              :positive-button-timer="10"
              warning-title="Are you sure you want to make changes?"
              warning-message="The changes you make will not affect the Pre-Defined Content"
              @update="confirmDelete"
              @on-confirmed="
                  (e) => deleteSection({ idEForm: section.idEForm as string })
                "
            >
              <v-icon>mdi-delete-outline</v-icon>
            </btn-delete>
            <v-btn
              v-if="!!section.buttonEditName"
              variant="outlined"
              color="#065695"
              class="section-btn icon-only"
              @click="toggleEditDialog"
            >
              <v-icon>mdi-pencil-outline</v-icon>
            </v-btn>
            <div class="d-flex" v-if="dragging">
              <v-btn
                class="mr-2 rounded-lg font-weight-bold btn-white-text"
                color="#D6212A"
                min-width="90px"
                @click="cancelDragParent"
              >
                Cancel
              </v-btn>
              <v-btn
                class="mr-2 rounded-lg font-weight-bold btn-white-text"
                color="#065695"
                min-width="90px"
                @click="handleShowChangeOrderWarning"
              >
                Save
              </v-btn>
            </div>
            <v-btn
              v-if="!!section.buttonChangeOrderSubSection && !dragging"
              variant="outlined"
              color="#065695"
              class="section-btn icon-only"
              @click="dragParent"
            >
              <v-icon>mdi-swap-vertical</v-icon>
            </v-btn>
            <custom-dialog
              variant="outlined"
              title="Add Sub Section"
              :button-class="['btn-add']"
              prepend-icon="mdi-plus"
              v-if="!!section.buttonAddSubsection"
              button-label="Add Sub Section"
              :showDialogProps="showAddDialog"
              dialog-class="add-section-dialog"
              @handle-show-dialog="() => toggleAddDialog(true)"
            >
              <sub-section-form
                :validator="$v"
                :section="section"
                :isShowSector="isShowSector"
                :form-data="formData"
                :docId="document.idDocumentType"
                @on-add-item="addItem"
                :docName="document.docName"
                @on-remove-item="removeItem"
                @toggle-dialog="toggleAddDialog"
                @on-confirm="handleShowWarning"
              />
            </custom-dialog>
          </div>
          <v-expansion-panel-title
            :hide-actions="section.isAnySubSection === false"
            class="section-panel-chevron"
            style="flex: 0 1 3%"
          >
            <template v-if="!!loading" v-slot:actions="">
              <v-progress-circular width="1" size="18" indeterminate />
            </template>
            <span
              class="important-whitespace"
              v-if="section.isAnySubSection === false"
              style="width: 22px"
            ></span>
          </v-expansion-panel-title>
        </div>
        <v-expansion-panel-text v-if="!loading">
          <!-- Section Content -->
          <draggable
            item-key="idEForm"
            v-model="subItems"
            :disabled="!dragging"
            @start="drag = true"
            @end="drag = false"
            animation="200"
          >
            <template #item="{ element }">
              <SubSectionItem
                :sub-section="element"
                :section="section"
                :isShowSector="isShowSector"
                :document="document"
                :dragging="dragging"
                @updateList="getSubSection(section.idBPSection as string)"
                @delete-section="deleteSection"
                @confirm-delete="confirmDelete"
              />
            </template>
          </draggable>
          <!-- /Section Content -->
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <teleport to="body">
      <ModalConfirm
        ref="warningDialog"
        :form-config="{
          title: 'Are you sure you want to make changes?',
          message:
            'The changes you make will not affect the Pre-Defined Content',
        }"
      >
        <template v-slot:icon-img>
          <v-avatar color="white" size="80" style="margin-top: -60px">
            <img :src="'/images/warningAlert.png'" style="width: 75px" />
          </v-avatar>
        </template>
        <template v-slot:btn-action>
          <div>
            <v-btn
              @click="handleCloseWarning"
              variant="outlined"
              color="#065695"
              class="mr-2 rounded-lg btn"
            >
              Close
            </v-btn>
            <v-btn
              @click="storeSubSection"
              class="mr-2 rounded-lg btn primary-gradient"
            >
              Yes
            </v-btn>
          </div>
        </template>
      </ModalConfirm>
    </teleport>

    <teleport to="body">
      <ModalConfirm
        ref="warningChangeOrderDialog"
        :form-config="{
          title: 'Are you sure you want to make changes?',
          message:
            'The changes you make will not affect the Pre-Defined Content',
        }"
      >
        <template v-slot:icon-img>
          <v-avatar color="white" size="80" style="margin-top: -60px">
            <img :src="'/images/warningAlert.png'" style="width: 75px" />
          </v-avatar>
        </template>
        <template v-slot:btn-action>
          <div>
            <v-btn
              @click="handleCloseChangeOrderWarning"
              variant="outlined"
              color="#065695"
              class="mr-2 rounded-lg btn"
            >
              Close
            </v-btn>
            <v-btn
              @click="saveNewOrder"
              class="mr-2 rounded-lg btn primary-gradient"
            >
              Yes
            </v-btn>
          </div>
        </template>
      </ModalConfirm>
    </teleport>

    <teleport to="body">
      <SectionEditDialog
        :showDialog="showEditDialog"
        :isShowSector="isShowSector"
        :document="document"
        :section="section"
        @toggle-dialog="toggleEditDialog"
        @update-list="() => emit('updateList')"
      />
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { useStore } from "vuex";
import draggable from "vuedraggable";
import useVuelidate from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import { getCurrentInstance, ref, StyleValue, watch } from "vue";

import SubSectionForm from "./SubSectionForm.vue";
import SectionEditDialog from "./SectionEditDialog.vue";
import SubSectionItem from "./SubSectionItem.vue";
import BtnDelete from "@/v2/components/utils/dialog/DeleteDialog.vue";
import CustomDialog from "@/v2/components/utils/dialog/CustomDialog.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { getColorChipTypeRdg } from "@/v2/helpers/color";

const emit = defineEmits(["updateList"]);
const props = defineProps({
  isShowSector: { type: Boolean, default: false },
  document: { type: Object, default: () => ({}) },
  section: { type: Object, default: () => ({}) },
  parentDragging: { type: Boolean, default: false },
});

interface SubSectionProps {
  id: string;
  value: string;
  isDelete: boolean;
  isEdit: boolean;
  sector: string;
}

const subItems = ref<SubSectionProps[]>([]);
const drag = ref(false);
const dragging = ref(false);
const dragParent = () => {
  dragging.value = true;
};
const cancelDragParent = () => {
  dragging.value = false;
  subItems.value = [...subSections.value];
};

const store = useStore();
const panel = ref<string | undefined>(undefined);
const loading = ref<boolean>(false);
const subSections = ref<SubSectionProps[]>([]);
const instance = ref<any>(getCurrentInstance()?.root.refs);
const showAddDialog = ref<boolean>(false);
const showEditDialog = ref<boolean>(false);
const toggleAddDialog = (reset = false) => {
  $v.value.$reset();
  if (reset) formData.value.arraySubSection = [];
  showAddDialog.value = !showAddDialog.value;
};
const toggleEditDialog = () => {
  showEditDialog.value = !showEditDialog.value;
};

const newSubSection = {
  eformName: "",
  idMSector: null,
};
const formData = ref({
  idBPSection: props.section.idBPSection,
  idBPDocument: props.document.docID,
  arraySubSection: [] as any,
});
const rules = {
  idBPDocument: { required },
  idBPSection: { required },
  arraySubSection: {
    $each: helpers.forEach({
      eformName: { required },
      idMSector: props.isShowSector ? { required } : {},
    }),
  },
};
const $v = useVuelidate(rules, formData);

watch(panel, async (idBPSection) => {
  if (idBPSection && !subSections.value.length) {
    getSubSection(idBPSection);
  }
});

const getSubSection = async (idBPSection: string) => {
  loading.value = true;
  await store
    .dispatch("adminStore/GetSubSectionBPDocOnGoing", {
      idBPSection: idBPSection,
    })
    .then((res) => {
      subItems.value = res.responseData;
      subSections.value = res.responseData;
    });
  loading.value = false;
};

// @TODO : refactor DeleteDialog, make it efficient
const confirmDelete = (e: any) => {
  const { dialog, modalWarning } = e;
  dialog.value = false;
  modalWarning.value.show();
};

/**
 * Delete Section or Sub Section
 * @param idEForm section's ID or sub section's ID
 */
const deleteSection = async (args: {
  idEForm: string;
  idBPSection?: string;
}) => {
  await store
    .dispatch("adminStore/DeleteEFormByIdEForm", {
      idEForm: args.idEForm,
    })
    .then((res) => {
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully deleted",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: "Failed to delete section",
          color: "error",
          timeout: 3000,
          icon: "mdi-close",
        });
      }
    })
    .catch((e) => {
      instance.value.toast.show({
        message:
          e.response?.data?.responseMessage ??
          "An error occurred while deleting",
        color: "error",
        timeout: 3000,
        icon: "mdi-close",
      });
    })
    .finally(() => {
      if (args.idBPSection) getSubSection(args.idBPSection);
      if (args.idBPSection == undefined) emit("updateList");
    });
};

const addItem = () => formData.value.arraySubSection.push({ ...newSubSection });
const removeItem = (idx: number) =>
  formData.value.arraySubSection.splice(idx, 1);
const warningDialog = ref();
const handleShowWarning = async () => {
  const valid = await $v.value.$validate();
  if (!valid) return;

  toggleAddDialog();
  warningDialog.value.show();
};
const handleCloseWarning = () => {
  $v.value.$reset();
  toggleAddDialog();
  warningDialog.value.hide();
};
const warningChangeOrderDialog = ref();
const handleShowChangeOrderWarning = async () => {
  warningChangeOrderDialog.value.show();
};
const handleCloseChangeOrderWarning = () => {
  warningChangeOrderDialog.value.hide();
};

const storeSubSection = () => {
  const payload = {
    ...formData.value,
    arraySubSection: formData.value.arraySubSection.map((item: any) => ({
      ...item,
      idMSector: item.idMSector ?? 0,
    })),
  };
  store
    .dispatch("adminStore/AddEFormOnGoingByIdBPSection", payload)
    .then((res) => {
      handleCloseWarning();
      emit("updateList");
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully create sub section",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: "Failed to create sub section",
          color: "error",
          timeout: 3000,
          icon: "mdi-close",
        });
      }
    })
    .catch((e) => {
      instance.value.toast.show({
        message:
          e.response?.data?.responseMessage ??
          "An error occurred while creating",
        color: "error",
        timeout: 3000,
        icon: "mdi-close",
      });
    })
    .finally(() => {
      if (formData.value.idBPSection) getSubSection(formData.value.idBPSection);
    });
};

const saveNewOrder = () => {
  const payload = {
    idBPDocument: props.document.docID,
    data: subItems.value.map((item: any, order) => ({
      idEform: item.id,
      eFormOrder: order + 1,
    })),
  };
  store
    .dispatch("adminStore/ChangeOrderSubSectionOnGoing", payload)
    .then((res) => {
      dragging.value = false;
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully saved",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
        getSubSection(props.section.idBPSection as string);
        handleCloseChangeOrderWarning();
      } else {
        instance.value.toast.show({
          message: "Failed to change order",
          color: "error",
          timeout: 3000,
          icon: "mdi-close",
        });
      }
    })
    .catch((e) => {
      instance.value.toast.show({
        message:
          e.response?.data?.responseMessage ??
          "An error occurred while changing order",
        color: "error",
        timeout: 3000,
        icon: "mdi-close",
      });
    });
};
</script>

<style scoped>
.section-panel-header {
  overflow: hidden;
}

.section-panel-title,
.section-panel-chevron {
  min-width: 0;
}

.section-name-col {
  min-width: 0;
  overflow: hidden;
}

.section-chip-col {
  gap: 1rem;
  min-width: 0;
  overflow: hidden;
}

.section-actions {
  min-width: 0;
  flex-wrap: wrap;
}

.btn-white-text {
  color: white;
}

.header-section {
  background-color: rgba(255, 238, 202, 1);
  color: rgba(144, 110, 44, 1);
}

.text-truncate-1 {
  display: -webkit-box;
  line-clamp: 1;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Remove black overlay on hover */
:deep(.v-expansion-panel-title:hover > .v-expansion-panel-title__overlay) {
  opacity: 0;
}
</style>
