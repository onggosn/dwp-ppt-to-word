<template>
  <!-- List Section -->
  <v-row class="section-list">
    <v-col cols="12" class="">
      <h3 v-if="hasSectionItems" style="font-weight: 600">List Section</h3>
    </v-col>
    <v-col cols="12" class="d-flex justify-end section-actions pb-1">
      <div class="d-flex" v-if="dragging && hasSectionItems">
        <v-btn
          class="mr-2 rounded-lg font-weight-bold"
          color="#D6212A"
          min-width="90px"
          style="color: white"
          @click="cancelDrapParent"
        >
          Cancel
        </v-btn>
        <v-btn
          class="mr-2 rounded-lg font-weight-bold"
          color="#065695"
          min-width="90px"
          style="color: white"
          @click="handleShowChangeOrderWarning"
        >
          Save
        </v-btn>
      </div>
      <v-btn
        v-if="!!buttonChangeOrderSection && !dragging && hasSectionItems"
        variant="outlined"
        color="#065695"
        class="section-btn"
        @click="dragParent"
      >
        <v-icon>mdi-swap-vertical</v-icon>
        Change Order
      </v-btn>
      <add-dialog
        variant="outlined"
        title="Add Section"
        max-width="900"
        :button-class="['btn-add']"
        prepend-icon="mdi-plus"
        v-if="!!buttonAddSection && sectionItems.length > 0"
        button-label="Add Section"
        :showDialogProps="showAddDialog"
        dialog-class="add-section-dialog"
        @handle-show-dialog="() => toggleDialog(true)"
      >
        <section-form
          :isShowSector="document.isShowSector"
          :docName="document.docName"
          :docId="document.idDocumentType"
          :form-data="formData"
          @on-add-item="addItem"
          @on-remove-item="removeItem"
          @on-confirm="handleShowWarning"
          @toggle-dialog="toggleDialog"
          :validator="$v"
        />
      </add-dialog>
    </v-col>
    <v-col cols="12" class="pt-1">
      <v-sheet class="my-1 section-item">
        <draggable
          item-key="idEForm"
          v-model="sectionItems"
          :disabled="!dragging"
          @start="drag = true"
          @end="drag = false"
          animation="200"
        >
          <template #item="{ element }">
            <SectionItem
              :parent-dragging="dragging"
              :section="element"
              :document="document"
              :isShowSector="document.isShowSector"
              @update-list="() => emit('updateList')"
            />
          </template>
        </draggable>
      </v-sheet>
    </v-col>
  </v-row>
  <!-- / List Section -->
  <teleport to="body">
    <ModalConfirm
      ref="warningDialog"
      :form-config="{
        title: 'Are you sure you want to make changes?',
        message: 'The changes you make will not affect the Pre-Defined Content',
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
            @click="storeSection"
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
        message: 'The changes you make will not affect the Pre-Defined Content',
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
</template>

<script setup lang="ts">
import { getCurrentInstance, ref, computed } from "vue";
import { useStore } from "vuex";
import SectionItem from "./SectionItem.vue";
import SectionForm from "./SectionForm.vue";
import AddDialog from "@/v2/components/utils/dialog/CustomDialog.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { helpers, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import draggable from "vuedraggable";

const emit = defineEmits(["updateList"]);
const instance = ref<any>(getCurrentInstance()?.root.refs);
const props = defineProps({
  document: { type: Object, default: () => ({}) },
  items: { type: Array, default: () => [] },
  buttonAddSection: { type: Boolean, default: () => false },
  buttonChangeOrderSection: { type: Boolean, default: () => false },
});

const drag = ref(false);
const dragging = ref(false);
const hasSectionItems = computed(() => sectionItems.value.length > 0);
const dragParent = () => {
  dragging.value = true;
};
const cancelDrapParent = () => {
  dragging.value = false;
  sectionItems.value = [...props.items];
};
const sectionItems = ref([...props.items]);
const store = useStore();
const showAddDialog = ref<boolean>(false);
const toggleDialog = (reset = false) => {
  $v.value.$reset();
  if (reset) formData.value.arraySection = [];
  showAddDialog.value = !showAddDialog.value;
};
const newSection = {
  sectionName: "",
  isHeader: false,
  idMSector: null,
};

const formData = ref({
  idBPDocument: props.document.docID,
  arraySection: [] as any,
});
const rules = {
  idBPDocument: { required },
  arraySection: {
    $each: helpers.forEach({
      sectionName: { required },
      idMSector: props.document.isShowSector ? { required } : {},
    }),
  },
};
const $v = useVuelidate(rules, formData);

const warningDialog = ref();
const warningChangeOrderDialog = ref();
const handleShowWarning = async () => {
  const valid = await $v.value.$validate();

  if (!valid) return;

  toggleDialog();
  warningDialog.value.show();
};
const handleCloseWarning = () => {
  toggleDialog();
  warningDialog.value.hide();
};
const handleShowChangeOrderWarning = async () => {
  warningChangeOrderDialog.value.show();
};
const handleCloseChangeOrderWarning = () => {
  warningChangeOrderDialog.value.hide();
};

const storeSection = () => {
  const payload = {
    ...formData.value,
    arraySection: formData.value.arraySection.map((item) => {
      return {
        ...item,
        idMSector: item.idMSector == null ? 0 : item.idMSector,
      };
    }),
  };
  store
    .dispatch("adminStore/AddBPSectionOnGoingByIdBPDocument", payload)
    .then((res) => {
      handleCloseWarning();
      emit("updateList");
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully created",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: "Failed to create section",
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
    });
};

const saveNewOrder = () => {
  const payload = {
    idBPDocument: props.document.docID,
    data: sectionItems.value.map((item: any, order) => ({
      idBPSection: item.idBPSection,
      bpSectionOrder: order + 1,
    })),
  };
  store
    .dispatch("adminStore/ChangeOrderSectionOnGoing", payload)
    .then((res) => {
      dragging.value = false;
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully saved",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
        emit("updateList");
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

const addItem = () => formData.value.arraySection.push({ ...newSection });
const removeItem = (idx: number) => formData.value.arraySection.splice(idx, 1);
</script>

<style scoped>
:deep(.btn-add) {
  margin-inline: 0 !important;
  border-radius: 0.5rem !important;
  border-color: #d9d9d9 !important;
}
.section-list,
:deep(.section-list) {
  .section-actions,
  :deep(.section-actions) {
    gap: 1rem;
  }

  .section-actions .section-btn,
  :deep(.section-actions .section-btn) {
    margin-top: 0 !important;
    border-radius: 0.5rem !important;
    border-color: #d9d9d9 !important;
  }

  .section-actions .section-btn.icon-only .v-btn__prepend,
  :deep(.section-actions .section-btn.icon-only .v-btn__prepend) {
    margin: 0 !important;
  }
  .section-actions .section-btn.icon-only,
  :deep(.section-actions .section-btn.icon-only) {
    min-width: 44px !important;
    padding: 0px !important;
  }

  .section-item .section-title,
  :deep(.section-item .section-title) {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 500;
    font-size: 1rem;
  }
}
</style>
