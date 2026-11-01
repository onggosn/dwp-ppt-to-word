<template>
  <div v-if="!isEditMode" class="py-2">
    <v-chip
      class="chip-text border-radius-dwp py-7 px-4 text-truncate"
      style="width: 100%"
    >
      <span
        style="
          display: block;
          width: 100%;
          word-break: break-word;
          white-space: normal;
        "
        >{{ props.item.sectionTitle }}</span
      >
    </v-chip>
  </div>
  <div v-else class="py-2">
    <div v-if="!props.item.isDelete">
      <v-chip
        class="chip-text"
        :class="['border-radius-dwp py-7 px-4 text-truncate mb-2']"
        style="width: 100%"
      >
        <span
          style="
            display: block;
            width: 100%;
            word-break: break-word;
            white-space: normal;
          "
          class="px-2"
        >
          <span style="word-break: break-word; white-space: normal">
            {{ formData.sectionTitle }}
          </span>
        </span>
      </v-chip>
      <v-chip
        class="chip-text"
        :class="['border-radius-dwp py-7 px-4 text-truncate mb-2']"
        style="width: 100%"
      >
        <span
          style="
            display: block;
            width: 100%;
            word-break: break-word;
            white-space: normal;
          "
          class="px-2"
        >
          <span style="word-break: break-word; white-space: normal">
            {{ formData.subSectionTitle }}
          </span>
        </span>
      </v-chip>
    </div>
    <div v-else>
      <v-autocomplete
        style="width: 100%"
        variant="solo"
        placeholder="Choose Section"
        v-model="formData.sectionTitle"
        :items="ListSection"
        :item-title="'name'"
        :item-value="'idSection'"
        :disabled="!formData.isDelete"
        @update:modelValue="handleSectionChange"
        clearable
        @click:clear="formData.subSectionTitle = null"
      ></v-autocomplete>
      <v-autocomplete
        style="width: 100%"
        variant="solo"
        placeholder="Choose Sub Section"
        item-title="Value"
        item-value="Id"
        v-model="formData.subSectionTitle"
        :items="ListSubSection"
        :disabled="!formData.sectionTitle"
      ></v-autocomplete>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, watch, defineEmits } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { TFormInputMapping } from "@/v2/Type";

const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
  isEditMode: {
    type: Boolean,
    default: false,
  },
  index: {
    type: Number,
    default: 0,
  },
});
const route = useRoute();
const store = useStore();
let ListSubSection = ref<{ Value: any; Id: any }[]>([]);
const ListSection = ref<{ name: any; idSection: any }[]>([]);
let formData = ref<TFormInputMapping>({
  idEformSource: "",
  sectionTitle: null,
  subSectionTitle: null,
  isEdited: false,
  isDelete: false,
  outputMappings: [],
  idSection: null,
});
const emits = defineEmits(["update-input-mapping"]);
watch(
  () => props.isEditMode,
  (newVal) => {
    if (newVal == true) {
      formData.value.sectionTitle = props.item.sectionTitle || null;
      formData.value.subSectionTitle = props.item.subSectionTitle || null;
      formData.value.isDelete = props.item.isDelete || false;
      getListSectiion();
    }
  },
  { immediate: true }
);

watch(
  () => formData.value.subSectionTitle,
  (newVal) => {
    if (newVal) {
      console.log(newVal);
      const data = {
        idx: props.index,
        ...formData.value,
      };
      emits("update-input-mapping", data);
    }
  }
);

function getListSectiion() {
  store
    .dispatch("contentStore/getBpDocSectionMappingList", {
      idBPDoc: route.params.idDoc,
    })
    .then((res) => {
      console.log(res, "res section");
      ListSection.value = Array.isArray(res)
        ? res.map((section: any) => ({
            name: section.Value || "",
            idSection: section.IdSection || "",
            idEformSource: section.IdEForm || "",
          }))
        : [];
    });
}

function handleSectionChange(newValue: any) {
  const foundObject: any = ListSection.value.find(
    (item) => item.idSection === newValue
  );
  formData.value.idEformSource = foundObject ? foundObject.idEformSource : null;
  // updateFormData();
  if (newValue) {
    getListSubSection(newValue);
  }
}

function getListSubSection(newValue) {
  store
    .dispatch("contentStore/getBpDocSubSectionMappingList", {
      idBPSection: newValue,
    })
    .then((res) => {
      console.log(res, "res section");
      ListSubSection.value = Array.isArray(res)
        ? res.map((section: any) => ({
            Value: section.Value || "",
            Id: section.Id || "",
          }))
        : [];
      if (ListSubSection.value.length == 0) {
        const foundObject: any = ListSection.value.find(
          (item) => item.idSection === newValue
        );
        formData.value.subSectionTitle = foundObject.name;
      } else {
        formData.value.subSectionTitle = null;
      }
    });
}
</script>
