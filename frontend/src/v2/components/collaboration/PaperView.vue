<template>
  <div class="paper-view">
    <HeaderPaperView />
    <div class="body-paper">
      <template v-for="item in listForm" :key="item.id">
        <p
          v-if="item.isView"
          class="text-left font-weight-bold"
          style="font-size: 0.9167em"
          :style="{
            fontFamily: `'${getFontFace(documentType)}'`,
          }"
          :id="`section-form-${item.idBpSection}`"
          v-html="formattedSectionName(item.sectionName)"
        />

        <div class="form-item">
          <template v-for="childItem in item.children" :key="childItem">
            <p
              class="text-left font-weight-bold"
              style="font-size: 0.9167em"
              :style="{
                marginLeft: getTitleTab(childItem.bPEFormLabel),
                fontFamily: `'${getFontFace(documentType)}'`,
              }"
              v-if="childItem.isLabelVisible"
              v-html="formattedSectionName(childItem.bPEFormLabel)"
            />

            <PaperFormEditor
              v-if="childItem.isView && childItem.idFormEditor"
              :item="childItem"
              :allFormIds="allFormIds"
            />
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import HeaderPaperView from "./HeaderPaperView.vue";
import { computed } from "vue";
import { useStore } from "vuex";
import {
  formattedSectionName,
  getFontFace,
  getTitleTab,
} from "@/v2/helpers/utils";

import PaperFormEditor from "./editor/PaperFormEditor.vue";

const store = useStore();
const listForm = computed(
  () => store.getters["collaborationStore/getListForm"]
);

const allFormIds = computed(() =>
  store.getters["collaborationStore/getListForm"].flatMap((item) =>
    item.children
      .filter((child) => child.isView && child.idFormEditor)
      .map((child) => child.idFormEditor)
  )
);

const documentType = computed(
  () => store.getters["collaborationStore/getDocumentTypeId"]
);
</script>

<style scoped>
.paper-view {
  text-align: left;
}

.body-paper {
  margin-top: 20px;
}

:deep(.page-break > .page-break__label) {
  visibility: hidden;
}
</style>
