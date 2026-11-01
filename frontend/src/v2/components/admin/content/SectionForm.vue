<template>
  <hr class="line" />
  <div class="section-form">
    <div class="doc-title">
      <p>{{ docName }}</p>
    </div>
    <div
      class="d-flex mb-3"
      v-for="(section, sectionIdx) in formData.arraySection"
      :key="sectionIdx"
    >
      <div class="section">
        <p class="sectionName-label">
          Section Title <span class="text-redTheme">*</span>
        </p>
        <div class="sectionName-field">
          <v-text-field
            variant="outlined"
            v-model="section.sectionName"
            class="border-radius-dwp"
            placeholder="Input section title"
            :error-messages="
              validator.$dirty
                ? getErrorMessages(
                    validator.arraySection.$each.$response.$errors[sectionIdx]
                      .sectionName[0],
                    {
                      required: 'Required',
                    }
                  )
                : ''
            "
          />
        </div>
        <p class="sectionName-label" v-if="isShowSector">
          Sector <span class="text-redTheme">*</span>
        </p>
        <v-radio-group
          v-if="isShowSector"
          inline
          class="sector-radio-group"
          v-model="section.idMSector"
          :error-messages="
            validator.$dirty
              ? getErrorMessages(
                  validator.arraySection.$each.$response.$errors[sectionIdx]
                    .idMSector[0],
                  {
                    required: 'Required',
                  }
                )
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
      <div class="item-actions">
        <v-btn
          color="#CB3A31"
          variant="outlined"
          icon="mdi-delete"
          size="large"
          class="item-remove-btn"
          @click="emit('onRemoveItem', sectionIdx)"
          v-if="formData.arraySection.length > 1"
        ></v-btn>
        <v-btn
          variant="elevated"
          class="item-add-btn"
          icon="mdi-plus"
          size="x-large"
          @click="
            () => {
              validator.$reset();
              emit('onAddItem');
            }
          "
          v-if="sectionIdx == formData.arraySection.length - 1"
        ></v-btn>
      </div>
    </div>
  </div>
  <div class="form-action">
    <v-btn @click="emit('toggleDialog', true)" style="color: #065695">
      Cancel
    </v-btn>
    <v-btn variant="elevated" class="submit-btn" @click="emit('onConfirm')">
      Create
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { getErrorMessages } from "@/v2/helpers/validation";
import { ref, onMounted } from "vue";
import { useStore } from "vuex";

const emit = defineEmits([
  "toggleDialog",
  "onConfirm",
  "onAddItem",
  "onRemoveItem",
]);
const props = defineProps({
  isShowSector: { type: Boolean, default: false },
  docName: { type: String, default: "" },
  docId: { type: Number, default: 0 },
  formData: { type: Object, default: () => ({}) },
  validator: { type: Object, default: () => ({}) },
});

const store = useStore();
const listSector = ref<any[]>([]);

store.dispatch("eFormStore/getListSectorPredefine").then(({ responseData }) => {
  listSector.value = responseData.filter(
    (item: any) => item.type === props.docId
  );
});

onMounted(() => {
  if (props.formData.arraySection.length == 0) {
    emit("onAddItem");
  }
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
.section-form {
  width: 100%;
  padding: 1.5rem;
  padding-right: 0px !important;
  border-radius: 0.5rem;
  border: 1px solid #babcca;
}
.sector-radio-group {
  padding-left: 0.2rem;
  margin-left: -8px;
  font-size: 14px;
}
:deep(.sector-radio-group .v-label) {
  font-size: 14px !important;
}
.doc-title {
  width: 98%;
  height: 2rem;
  position: relative;
  margin-top: -1.5rem;
  p {
    width: 100%;
    font-weight: 600;
    background: #fff;
    position: absolute;
    margin-top: -0.8rem;
    padding: 0 0.5rem;
    top: 0;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
.section {
  padding: 1rem;
  flex: 0 0 90%;
  border-radius: 0.75rem;
  border: 1px solid #babcca;
}
.sectionName-label {
  font-size: 15px !important;
  font-weight: 700 !important;
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
  gap: 1rem;
  flex: 0 0 10%;
  display: flex;
  padding: 0.25rem;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  button {
    border-radius: 0.5rem !important;
  }
}
button {
  height: 45px !important;
  font-size: 15px !important;
}
.item-add-btn,
.item-remove-btn {
  width: 41px !important;
  height: 41px !important;
}
.submit-btn,
.item-add-btn,
.item-remove-btn {
  color: #fff;
}
.submit-btn,
.item-add-btn {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}
.form-action {
  gap: 1rem;
  display: flex;
  justify-content: end;
  align-items: center;
  margin-top: 1rem;
  button {
    border-radius: 10px !important;
  }
}
</style>
