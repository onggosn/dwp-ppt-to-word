<template>
  <v-dialog v-model="dialog" :max-width="800" persistent>
    <v-card class="mb-5 border-radius-dwp">
      <v-card-title class="d-flex justify-center align-center">
        <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
          Mapping Section PPT
        </div>
        <v-btn
          @click="handleCloseModal"
          class="mr-2"
          style="position: absolute; right: 0"
          variant="text"
          icon="mdi-close"
        />
      </v-card-title>
      <v-card-text>
        <hr class="line mt-3" />
        <v-col cols="12" class="pb-0">
          <p class="pb-2 text-left text-darkBlue font-weight-bold">
            Content Title
          </p>
          <v-text-field
            v-model="inputMappingDetail.contentTitle"
            placeholder="Insert Section Title"
            disabled
          ></v-text-field>
        </v-col>
        <v-col cols="12" class="pb-0">
          <p class="pb-2 text-left text-darkBlue font-weight-bold">
            Section Title
          </p>
          <v-text-field
            v-model="inputMappingDetail.sectionTitle"
            placeholder="Insert Section Title"
            disabled
          ></v-text-field>
        </v-col>
        <v-col cols="12" class="pb-0">
          <p class="pb-2 text-left text-darkBlue font-weight-bold">
            Sub Section Title
          </p>
          <v-text-field
            v-model="inputMappingDetail.subSectionTitle"
            placeholder="Insert Section Title"
            disabled
          ></v-text-field>
        </v-col>
        <v-row
          v-for="(section, index) in visibleSections"
          :key="`section-${index}`"
          class="rounded-lg px-2 mt-2 pb-5 mx-2 mb-5"
          style="border: 2px #babcca solid"
        >
          <span class="text-darkBlue font-weight-bold form-title">
            Input {{ index + 1 }}
          </span>
          <v-col cols="12 d-flex" class="pb-0" style="gap: 10px">
            <v-text-field
              v-model="section.sectionName"
              :error="Boolean(validationErrors[index])"
              :error-messages="
                validationErrors[index] ? [validationErrors[index]] : []
              "
              @update:modelValue="handleInput(index)"
              variant="solo"
              placeholder="Insert Title"
            ></v-text-field>
            <v-btn
              @click="handleDeleteInput(section.id || 0, index)"
              class="rounded-lg px-4 py-4"
              min-width="0"
              min-height="55"
            >
              <v-icon icon="mdi-delete" color="#D6212A" size="18" />
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="d-flex justify-start px-6 py-4">
        <v-btn
          @click="handleAddInput"
          elevation="3"
          class="primary-gradient rounded-lg"
        >
          + Add Input
        </v-btn>
      </v-card-actions>
      <v-card-actions class="d-flex justify-end px-6 py-4">
        <v-btn
          @click="handleCloseModal"
          elevation="3"
          class="rounded-lg text-light-blue-darken-4"
        >
          Cancel
        </v-btn>
        <v-btn
          @click="handleAddNewSection(idMbpDocumentTemplate)"
          elevation="3"
          class="primary-gradient rounded-lg"
          :loading="onLoadingAdd"
          :disabled="isSectionsNotAdded"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { defineExpose, defineProps } from "vue";
import { watch } from "vue";
import useMappingSection from "@/v2/composables/useMappingSection";

const props = defineProps({
  idMbpDocumentTemplate: {
    type: Number,
    default: 0,
  },
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});

const {
  dialog,
  inputMappingDetail,
  visibleSections,
  onLoadingAdd,
  validationErrors,
  isSectionsNotAdded,
  rootInstance,
  showToast,
  handleAddInput,
  handleOpenModal,
  handleCloseModal,
  handleDeleteInput,
  handleInput,
  handleAddNewSection,
} = useMappingSection(props.item);

defineExpose({ handleOpenModal });

watch(
  showToast,
  () => {
    rootInstance.refs.toast?.show({
      message: "Successfully Saved",
      color: "success",
      timeout: 3000,
    });
  },
  {
    deep: true,
  }
);
</script>

<style scoped>
.form-title {
  margin-top: -15px;
  margin-left: 20px;
  background-color: white;
  width: fit-content;
}

.line {
  margin-top: -10px !important;
  margin-bottom: 40px;
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

:deep(.v-field--disabled .v-field__field) {
  background-color: rgba(133, 133, 133, 0.25) !important;
  border-radius: 6px;
  color: #4b4b4b;
}
</style>
