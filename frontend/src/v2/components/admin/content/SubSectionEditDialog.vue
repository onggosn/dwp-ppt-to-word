<template>
  <v-dialog v-model="dialog" max-width="800" persistent>
    <v-card class="py-3 px-6 rounded-lg edit-subsection-dialog">
      <div
        class="d-flex justify-space-between align-center border-bottom header dialog-header"
      >
        <div class="w-100 font-weight-bold text-center dialog-title">
          Edit Sub Section Title
        </div>
        <v-btn
          class="close-button"
          icon="mdi-close"
          variant="plain"
          @click="closeDialog"
        ></v-btn>
      </div>
      <div class="pt-3">
        <hr class="line" />
        <div class="edit-section-form">
          <div class="content">
            <p class="sectionName-label">Content Title</p>
            <div class="sectionName-field">
              <v-text-field
                disabled
                variant="outlined"
                :model-value="document.docName"
                class="border-radius-dwp"
              />
            </div>
          </div>
          <div class="section">
            <p class="sectionName-label">
              Section Title <span class="text-redTheme">*</span>
            </p>
            <div class="sectionName-field">
              <v-text-field
                disabled
                variant="outlined"
                :model-value="section.sectionName"
                class="border-radius-dwp"
              />
            </div>
          </div>
          <div class="sub-section">
            <p class="sectionName-label">
              Section Title <span class="text-redTheme">*</span>
            </p>
            <div class="sectionName-field">
              <v-text-field
                variant="outlined"
                v-model="formData.name"
                class="border-radius-dwp"
                placeholder="Input section title"
                :error-messages="
                  $validator.$dirty
                    ? getErrorMessages($validator.name, {
                        required: 'Required',
                      })
                    : ''
                "
              />
            </div>
            <p
              class="sectionName-label"
              v-if="isBuku2D && section.isAnySubSection === false"
            >
              Sector <span class="text-redTheme">*</span>
            </p>
            <v-radio-group
              v-if="isBuku2D"
              inline
              style="margin-left: -8px"
              v-model="formData.idSector"
              :error-messages="
                $validator.$dirty
                  ? getErrorMessages($validator.idSector, {
                      required: 'Required',
                    })
                  : ''
              "
            >
              <v-radio
                v-for="(option, index) in listSector"
                :key="index"
                :value="option.id"
                :label="option.value"
                color="#065391"
              />
            </v-radio-group>
          </div>
        </div>
        <div class="form-action">
          <v-btn style="color: #065695" @click="closeDialog">Cancel</v-btn>
          <v-btn
            variant="elevated"
            class="submit-btn"
            @click="handleShowEditWarning"
          >
            Save
          </v-btn>
        </div>
      </div>
    </v-card>
  </v-dialog>

  <ModalConfirm
    ref="confirmDialog"
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
          @click="handleCloseEditWarning"
          variant="outlined"
          color="#065695"
          class="mr-2 rounded-lg btn"
        >
          Close
        </v-btn>
        <v-btn
          :loading="isLoading"
          @click="updateSection"
          class="mr-2 rounded-lg btn primary-gradient"
        >
          Yes
        </v-btn>
      </div>
    </template>
  </ModalConfirm>
</template>

<script setup lang="ts">
import { required } from "@vuelidate/validators";
import { getErrorMessages } from "@/v2/helpers/validation";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { computed, onMounted, ref, watch } from "vue";
import useVuelidate from "@vuelidate/core";
import { useStore } from "vuex";
import { getCurrentInstance } from "vue";
const emit = defineEmits(["toggleDialog", "onConfirm", "updateList"]);
const props = defineProps({
  showDialog: { type: Boolean, default: false },
  isBuku2D: { type: Boolean, default: false },
  document: { type: Object, default: () => ({}) },
  section: { type: Object, default: () => ({}) },
  subSection: { type: Object, default: () => ({}) },
});
const store = useStore();
const instance = ref<any>(getCurrentInstance()?.root.refs);
const listSector = ref<any[]>([]);
store.dispatch("eFormStore/getListSectorPredefine").then(({ responseData }) => {
  listSector.value = responseData.filter(
    (item: any) => item.type === props.document.idDocumentType
  );
});
const dialog = ref(false);
watch(
  () => props.showDialog,
  (val) => {
    dialog.value = val;
  }
);
const confirmDialog = ref(); // @TODO : refactor ModalConfirm, make it efficient
const handleShowEditWarning = async () => {
  const valid = await $validator.value.$validate();
  if (!valid) return;

  emit("toggleDialog");
  confirmDialog.value.show();
};
const handleCloseEditWarning = () => {
  $validator.value.$reset();
  emit("toggleDialog");
  confirmDialog.value.hide();
};
const formData = ref<any>({});
const resetFormData = () => {
  formData.value = {
    idEform: props.subSection.id,
    name: props.subSection.value,
    isSection: false,
    isHeader: props.subSection.isHeader ?? false,
    idSector: props.subSection.idMSector,
    idBPDocument: props.document.docID,
  };
};
const closeDialog = () => {
  resetFormData();
  emit("toggleDialog");
};
const Editrules = computed(() => ({
  idEform: { required },
  name: { required },
  isSection: { required },
  isHeader: { required },
  idSector: !props.isBuku2D ? {} : { required },
  idBPDocument: { required },
}));

const $validator = useVuelidate(Editrules, formData);

const isLoading = ref(false);
const updateSection = () => {
  isLoading.value = true;
  store
    .dispatch("adminStore/updateEForm", formData.value)
    .then((res) => {
      handleCloseEditWarning();
      emit("updateList");
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: "Successfully update section",
          color: "success",
          timeout: 3000,
          icon: "mdi-check",
        });
      } else {
        instance.value.toast.show({
          message: "Failed to update section",
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
          "An error occurred while updating",
        color: "error",
        timeout: 3000,
        icon: "mdi-close",
      });
    })
    .finally(() => {
      isLoading.value = false;
    });
};

onMounted(() => {
  resetFormData();
});
</script>

<style scoped>
:global(.add-section-dialog .dialog-header) {
  padding: 1rem 0 !important;
}
:global(.add-section-dialog .dialog-title) {
  font-size: 20px;
  font-weight: 600;
}
.line {
  margin-bottom: 1.5rem;
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
:deep(.content .v-field),
:deep(.section .v-field) {
  background-color: #dfdfdf !important;
}
.sub-section {
  padding: 1rem;
  flex: 0 0 90%;
  border-radius: 0.75rem;
  border: 1px solid #babcca;
}
.sectionName-label {
  font-size: 15px !important;
  font-weight: 500 !important;
  color: #3a416f !important;
}
:deep(.sectionName-field .v-field) {
  border-radius: 12px !important;
  border-color: #e0e0e0 !important;
}
.sectionName-field,
.item-actions {
  padding: 0.25rem;
}
.item-actions {
  display: flex;
  align-items: center;
  flex: 0 0 10%;
  padding: 0.25rem;
  button {
    border-radius: 0.5rem !important;
  }
}
.edit-subsection-dialog button {
  height: 45px !important;
}
.submit-btn {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}
.submit-btn,
.item-add-btn,
.item-remove-btn {
  color: #fff;
}
.submit-btn,
.item-add-btn {
  background: linear-gradient(#267dc2, #065695e0);
}
.form-action {
  gap: 1rem;
  display: flex;
  justify-content: end;
  align-items: center;
  margin-top: 1rem;
  button {
    border-radius: 0.5rem !important;
  }
}
</style>
