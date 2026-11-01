<template>
  <v-sheet class="mb-3 d-flex">
    <template v-if="!disabledCondition">
      <v-btn
        size="small"
        variant="outlined"
        style="border-radius: 10px"
        class="mr-2"
        color="#065695"
        prepend-icon="mdi-pencil"
        @click="startCollaboration"
        :disabled="
          collabMode || isInitializing || !buttonState || isApprovalInProgress
        "
        :loading="isInitializing"
      >
        Edit Section
      </v-btn>
    </template>

    <template v-if="!disabledCondition">
      <BtnMngMapping :formSource="item.idEForm" v-if="item.isMapping" />
    </template>

    <template v-if="item.isButtonAccess">
      <template v-if="!disabledCondition">
        <EditAccessSection
          :sectionName="item.bPEFormLabel"
          :idDoc="item.idFormEditor"
          :idEform="item.idEForm"
          :key="store.getters['collaborationStore/getDocumentFlowCheck']"
        />
      </template>
    </template>
  </v-sheet>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { TFormEditor } from "@v2/Type.d";
import EditAccessSection from "../EditAccessSection.vue";
import BtnMngMapping from "@v2/components/collaboration/MngMappingSection.vue";
import { useStore } from "vuex";

const props = defineProps({
  collabMode: {
    type: Boolean,
    default: false,
  },
  isInitializing: {
    type: Boolean,
    default: false,
  },
  item: {
    type: Object as () => TFormEditor,
    required: true,
  },
});
const emit = defineEmits(["startCollaboration"]);
const store = useStore();
const startCollaboration = () => {
  emit("startCollaboration");
};

const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);
const isApprovalInProgress = computed(
  (): boolean => store.getters["collaborationStore/getDocumentStatusId"] == "49"
);

// const disabledCondition = ref(
//   [29].includes(store.getters["collaborationStore/getDocumentStatusId"])
//     ? true
//     : store.getters["collaborationStore/getDisableAllForm"]
//     ? true
//     : !props.item.isEdit
// );

const disabledCondition = computed(() => {
  return [29].includes(store.getters["collaborationStore/getDocumentStatusId"])
    ? true
    : store.getters["collaborationStore/getDisableAllForm"]
    ? true
    : !props.item.isEdit;
});
</script>
