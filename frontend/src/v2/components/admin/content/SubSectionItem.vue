<template>
  <div>
    <v-expansion-panels class="mb-4">
      <v-expansion-panel>
        <v-expansion-panel-title :hide-actions="true">
          <div
            class="w-100 d-flex justify-space-between align-center subsection-header"
          >
            <div class="subsection-name-col" style="flex: 0 1 60%">
              <div class="section-title" :title="subSection.value">
                <img
                  :src="require(`@/v2/assets/icon/drag2.svg`)"
                  v-if="dragging"
                />
                {{ subSection.value }}
              </div>
            </div>
            <div
              class="d-flex align-center justify-center subsection-chip-col"
              style="flex: 0 1 20%"
            >
              <v-chip
                v-if="!!subSection.sector"
                :style="(getColorChipTypeRdg('bulanan') as StyleValue)"
                :title="subSection.sector"
                class="chip-ellipsis"
                >{{ subSection.sector }}</v-chip
              >
            </div>
            <div
              class="d-flex justify-end section-actions"
              style="flex: 0 1 20%"
            >
              <btn-delete
                :dialog-width="640"
                btn-color="#CB3A31"
                btn-class="section-btn icon-only"
                btn-size=""
                v-if="!!subSection.isDelete"
                :title="'Delete Sub Section'"
                :is-icon-button="true"
                :hide-icon="true"
                :subtitle="'Are you sure delete this sub section? Deleting the sub section will delete mappings and permissions on this document.'"
                :description="''"
                :append-icon="true"
                :btn-icon-color="'#d6212a'"
                :count-down="0"
                :btn-density="'compact'"
                positive-text-button="Yes"
                :positive-button-timer="10"
                warning-title="Are you sure you want to make changes?"
                warning-message="The changes you make will not affect the Pre-Defined Content"
                @update="(e) => emit('confirmDelete', e)"
                @on-confirmed="
                  () =>
                    emit('deleteSection', {
                      idEForm: subSection.id,
                      idBPSection: section.idBPSection,
                    })
                "
              >
                <v-icon>mdi-delete-outline</v-icon>
              </btn-delete>
              <v-btn
                v-if="!!subSection.isEdit"
                variant="outlined"
                color="#065695"
                class="section-btn icon-only"
                @click="toggleSubSectionEditDialog"
              >
                <v-icon>mdi-pencil-outline</v-icon>
              </v-btn>
            </div>
          </div>
        </v-expansion-panel-title>
      </v-expansion-panel>
    </v-expansion-panels>

    <sub-section-edit-dialog
      :sub-section="subSection"
      :section="section"
      :isShowSector="isShowSector"
      :document="document"
      @updateList="$emit('updateList')"
      @toggleDialog="toggleSubSectionEditDialog"
      :showDialog="showDialog"
    />
  </div>
</template>

<script setup lang="ts">
import { StyleValue, ref } from "vue";
import { getColorChipTypeRdg } from "@/v2/helpers/color";
import BtnDelete from "@/v2/components/utils/dialog/DeleteDialog.vue";
import SubSectionEditDialog from "./SubSectionEditDialog.vue";

const emit = defineEmits(["updateList", "deleteSection", "confirmDelete"]);
defineProps({
  subSection: { type: Object, required: true },
  section: { type: Object, required: true },
  isShowSector: { type: Boolean, required: true },
  document: { type: Object, required: true },
  dragging: { type: Boolean, default: false },
});

const showDialog = ref(false);
const toggleSubSectionEditDialog = () => {
  showDialog.value = !showDialog.value;
};
</script>

<style lang="scss" scoped>
.subsection-header {
  overflow: hidden;
}

.subsection-name-col,
.subsection-chip-col {
  min-width: 0;
  overflow: hidden;
}

.section-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.chip-ellipsis) {
  max-width: 100%;
}

:deep(.chip-ellipsis .v-chip__content) {
  display: -webkit-box;
  line-clamp: 1;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.section-actions {
  min-width: 0;
  flex-wrap: wrap;
  padding-right: 2.5%;
}

:deep(.v-expansion-panel-title:hover > .v-expansion-panel-title__overlay) {
  opacity: 0;
}
</style>
