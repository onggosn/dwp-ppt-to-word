<template>
  <v-sheet class="px-5 py-2 child-container">
    <div
      class="d-flex flex-wrap ml-auto ga-2"
      style="justify-content: flex-end"
    >
      <v-btn
        v-if="perentItem.isImportPPT"
        @click="downloadMappingSectionPpt"
        size="small"
        variant="outlined"
        prepend-icon="mdi-file-upload"
        class="mr-2"
        color="#065695"
        rounded="lg"
      >
        Export Mapping
      </v-btn>
      <div class="d-flex" v-if="isDragParent">
        <v-btn
          size="small"
          class="mr-2 rounded-lg font-weight-bold"
          color="#D6212A"
          min-width="90px"
          style="color: white"
          @click="cancelDrag()"
        >
          Cancel
        </v-btn>
        <v-btn
          size="small"
          class="mr-2 rounded-lg font-weight-bold"
          color="#065695"
          min-width="90px"
          style="color: white"
          @click="saveDrag()"
        >
          Save
        </v-btn>
      </div>
      <div class="pr-2" v-if="perentItem.isDelete">
        <btn-delete
          :title="'Delete Content'"
          :btn-title="'Delete Content'"
          :subtitle="'Are you sure delete this Content ?'"
          :description="'Deleting the content will delete sections, subsections, mappings, and permissions on this content'"
          :append-icon="true"
          :btn-color="'#d6212a'"
          :btn-icon-color="'#d6212a'"
          :btn-density="'comfortable'"
          btn-class="font-weight-bold text-12"
          @update="deleteContent(perentItem)"
        />
      </div>

      <v-btn
        v-if="!isDragParent && perentItem.isSectionOrder"
        :disabled="isDragChild"
        size="small"
        variant="outlined"
        prepend-icon="mdi-swap-vertical"
        class="mr-2 rounded-lg font-weight-bold"
        color="#065695"
        @click="makeParentDraggable()"
      >
        Change Order
      </v-btn>
      <FormEditContent
        v-if="perentItem.isEdit"
        :id="perentItem.idMBPDocumentTemplate"
      />
      <div v-if="perentItem.isAccess">
        <edit-access-form
          :is-admin="true"
          :isRisalahDoc="props.perentItem.isRisalahRDG"
          :from-admin="props.perentItem"
        />
      </div>
      <v-btn
        v-if="perentItem.isAddSection"
        class="rounded-lg px-2 font-weight-bold"
        size="small"
        min-width="0"
        color="#065695"
        variant="outlined"
        @click="addSection.openDialog()"
        style="border-radius: 8px !important"
      >
        + Add Section
      </v-btn>
    </div>

    <draggable
      v-model="listPanel"
      :disabled="!isDragParent"
      @start="drag = true"
      @end="drag = false"
      animation="200"
      item-key="idMEFormTemplate"
    >
      <template #item="{ element }">
        <ChildItem
          can-add-subsection
          @onAddStp="
            stp_mapping_form.openDialog(
              element.idMEFormTemplate,
              element.childSection.length
            )
          "
          @onAddStpSubsection="
            (value) => {
              stp_mapping_form.openDialog(
                value.idMEFormTemplate,
                element.childSection.length
              );
            }
          "
          @onAddSubSection="addSection.openDialog(element)"
          @on-edit="edit_subsection.openDialog(element)"
          @on-edit-subsection="
            (value) => {
              edit_subsection.openDialog(value, element.bPEFormLabel);
            }
          "
          @on-delete-section="reloadSection"
          @onAddMapping="
            (value, section) => {
              MappingPPTSection.handleOpenModal(value, section);
            }
          "
          :can-expand="element.childSection?.length !== 0"
          :item="element"
          :itemCount="item.length"
          :itemChildCount="element.childSection.length"
          :is-disable-ppt="perentItem.isImportPPT"
          :is-disable="isDisableRow(element)"
          :is-drag-parent="isDragParent"
          :is-parent="true"
          :child-items="element.childSection"
          @on-start-drag-child="
            (value) => {
              isDragChild = value;
            }
          "
        >
          <!-- <draggable
            v-model="element.childSection"
            :disabled="isDragParent"
            @start="drag = true"
            @end="drag = false"
            item-key="id"
          >
            <template #item="{ element: item }">
              <ChildItem
                @onAddStp="
                  stp_mapping_form.openDialog(
                    item.idMEFormTemplate,
                    element.childSection.length
                  )
                "
                @on-edit="
                  edit_subsection.openDialog(item, element.bPEFormLabel)
                "
                @on-delete-section="reloadSection"
                :can-expand="false"
                :is-disable="item.disabledRow"
                :item="item"
                :is-drag-child="dragChild"
              >
              </ChildItem>
            </template>
          </draggable> -->
          <!-- <template
            v-for="item in element.childSection"
            :key="item.idMEFormTemplate"
          >
          </template> -->
        </ChildItem>
      </template>
    </draggable>

    <!-- <div v-for="list in props.item" :key="list.idMEFormTemplate">
      <ChildItem
        can-add-subsection
        @onAddStp="
          stp_mapping_form.openDialog(
            list.idMEFormTemplate,
            list.childSection.length
          )
        "
        @onAddSubSection="addSection.openDialog(list)"
        @on-edit="edit_subsection.openDialog(list)"
        @on-delete-section="reloadSection"
        @onAddMapping="MappingPPTSection.handleOpenModal(list)"
        :can-expand="list.childSection?.length !== 0"
        :item="list"
        :itemCount="item.length"
        :is-disable="isDisableRow(list)"
      >
        <template
          v-for="item in list.childSection"
          :key="item.idMEFormTemplate"
        >
          {{ item }}
          <ChildItem
            @onAddStp="
              stp_mapping_form.openDialog(
                item.idMEFormTemplate,
                list.childSection.length
              )
            "
            @on-edit="edit_subsection.openDialog(item, list.bPEFormLabel)"
            @on-delete-section="reloadSection"
            :can-expand="false"
            :is-disable="item.disabledRow"
            :item="item"
          ></ChildItem>
        </template>
      </ChildItem>
    </div> -->
  </v-sheet>
  <StpMapping ref="stp_mapping_form" />
  <AddSection ref="addSection" @onSuccess="reloadSection" :item="perentItem" />
  <EditSubsection
    ref="edit_subsection"
    @onSuccess="reloadSection"
    :item="perentItem"
  />
  <FormMappingSection
    :item="perentItem"
    :id-mbp-document-template="idMbpDocumentTemplate"
    ref="MappingPPTSection"
  />
</template>

<script setup lang="ts">
import { ref, getCurrentInstance, onMounted } from "vue";
import { useStore } from "vuex";

import draggable from "vuedraggable";

import { downloadFileHelper } from "@v2/helpers/DownloadFileHelper";

import EditAccessForm from "@v2/components/collaboration/EditAccessForm.vue";
import FormEditContent from "@/v2/components/admin/content/FormEdit.vue";
import ChildItem from "@/v2/components/admin/children/ChildItem.vue";
// import DraggableChildItem from "@/v2/components/admin/children/DraggableChildItem.vue";
import BtnDelete from "@/v2/components/utils/dialog/DeleteEventDialog.vue";
import StpMapping from "@/v2/components/admin/content/StpMapping.vue";
import AddSection from "@/v2/components/admin/content/FormAddSection.vue";
import EditSubsection from "@/v2/components/admin/content/EditSubsection.vue";
import FormMappingSection from "@/v2/components/admin/content/FormMappingSection.vue";

const drag = ref(false);
const isDragParent = ref(false);
const isDragChild = ref(false);
// const dragChild = ref(true);
const store = useStore();
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
  perentItem: {
    type: Object,
    default: () => {
      return {};
    },
  },
  idMbpDocumentTemplate: {
    type: Number,
    default: 0,
  },
  bpDocumentName: {
    type: String,
    default: "",
  },
});

const originalList = ref<any>([]);
const listPanel = ref<any>(props.item);

onMounted(() => {
  originalList.value = [...listPanel.value];
});

const emit = defineEmits(["onDeleteSection", "onDeleteContent"]);
const instance = ref<any>(getCurrentInstance()?.root.refs);
const stp_mapping_form = ref();
const edit_subsection = ref();
const MappingPPTSection = ref();

function isDisableRow(item) {
  if (item.disabledRow && item.childSection.length === 0) return true;

  return false;
}
const addSection = ref();

const reloadSection = () => {
  emit("onDeleteSection");
};

const reloadContent = () => {
  emit("onDeleteContent");
};

const downloadMappingSectionPpt = () => {
  const { idMbpDocumentTemplate: idBpDocumentTemplate } = props;

  const payload = {
    idBpDocumentTemplate,
  };

  store
    .dispatch("adminStore/mappingSectionPptDownload", payload)
    .then((res) => {
      downloadFileHelper(res, props.bpDocumentName);
    });
};

const makeParentDraggable = () => {
  isDragParent.value = true;
};

const saveDrag = () => {
  let payload = [
    ...listPanel.value.map((item, index) => {
      return {
        idMBPSectionTemplate: item.idMBPSectionTemplate,
        bpSectionOrder: index,
      };
    }),
  ];

  store
    .dispatch("adminStore/updateSectionOrder", {
      idMBPDocumentTemplate: props.perentItem.idMBPDocumentTemplate,
      data: payload,
    })
    .then((res) => {
      if (res.responseCode === "011000") {
        isDragParent.value = false;
        originalList.value = [...listPanel.value];
        instance.value.toast.show({
          message: "Successfully Saved",
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
    });
};

const cancelDrag = () => {
  isDragParent.value = false;
  listPanel.value = [...originalList.value];
};

const deleteContent = (item) => {
  const payload = {
    idMBPDoc: item.idMBPDocumentTemplate,
  };
  store
    .dispatch("adminStore/deleteContent", payload)
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
        message: "Fail deleting content",
        color: "error",
        timeout: 3000,
        icon: "mdi-check",
      });
    })
    .finally(() => {
      reloadContent();
    });
};
</script>

<style scoped lang="css">
.btn-create {
  color: #065695;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
.btn-delete {
  color: #d6212a;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}
</style>
