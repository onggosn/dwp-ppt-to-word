<template>
  <div v-if="!isEditMode">
    <p class="mt-2 font-weight-regular">Output mapping</p>
    <div class="py-2">
      <v-chip
        class="chip-text"
        v-for="(items, index) in props.item"
        :key="index"
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
            <strong>{{ items.documentName }}</strong> - {{ items.title }}
          </span>
        </span>
      </v-chip>
    </div>
  </div>
  <div v-else>
    <div v-for="(items, index) in props.item" :key="index">
      <p class="mt-2 font-weight-regular">Output mapping {{ index + 1 }}</p>
      <div v-if="!items.isDelete" class="py-2">
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
              {{ items.documentName }}
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
              {{ items.sectionTitle }}
            </span>
          </span>
        </v-chip>

        <div class="d-flex">
          <v-chip
            class="chip-text"
            :class="['border-radius-dwp py-7 px-4 text-truncate mb-2']"
            style="flex-grow: 1"
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
                {{ items.subSectionTitle }}
              </span>
            </span>
          </v-chip>
          <div class="d-flex pl-2" :style="{ gap: '10px' }">
            <v-btn
              v-if="items.isDelete"
              class="rounded-lg"
              min-width="0"
              height="55"
              width="55"
            >
              <v-icon icon="mdi-delete" color="red"></v-icon
            ></v-btn>
            <v-btn
              v-if="index === props.item.length - 1"
              class="p-2 primary-gradient rounded-lg btn-icon"
              height="55"
              width="55"
              @click="$emit('add-output-mapping')"
            >
              <v-icon icon="mdi-plus"></v-icon>
            </v-btn>
          </div>
        </div>
      </div>
      <div v-else class="py-2">
        <v-autocomplete
          style="width: 100%"
          variant="solo"
          placeholder="Choose Tahapan"
          v-model="items.tahapan"
          :item-title="'Value'"
          :item-value="'id'"
          :items="ListTahapan"
          :disabled="props.itemAll.idEformSource == null"
          @update:modelValue="handleTahapanChange"
          clearable
        ></v-autocomplete>
        <v-autocomplete
          style="width: 100%"
          variant="solo"
          placeholder="Choose Content"
          v-model="items.documentName"
          :item-title="'Value'"
          :item-value="'id'"
          :items="ListContent"
          :disabled="!items.tahapan"
          clearable
          @update:modelValue="handleContentChange"
        ></v-autocomplete>
        <v-autocomplete
          style="width: 100%"
          variant="solo"
          placeholder="Choose Section"
          v-model="items.sectionTitle"
          :item-title="'Value'"
          :item-value="'IdSection'"
          :items="ListSection"
          :disabled="!items.tahapan || !items.documentName"
          clearable
          @update:modelValue="handleSectionChange"
        ></v-autocomplete>
        <div class="d-flex">
          <v-autocomplete
            style="width: 100%"
            variant="solo"
            placeholder="Choose Sub Section"
            v-model="items.subSectionTitle"
            :items="ListSubsection"
            :item-title="'Value'"
            :item-value="'Id'"
            :disabled="
              !items.tahapan || !items.documentName || !items.sectionTitle
            "
            clearable
          ></v-autocomplete>
          <div class="d-flex pl-2" :style="{ gap: '10px' }">
            <v-btn
              v-if="items.isDelete && props.item.length > 1"
              class="rounded-lg"
              min-width="0"
              height="55"
              width="55"
            >
              <v-icon icon="mdi-delete" color="red"></v-icon
            ></v-btn>
            <v-btn
              v-if="index === props.item.length - 1"
              class="p-2 primary-gradient rounded-lg btn-icon"
              height="55"
              width="55"
              :disabled="
                !items.tahapan || !items.sectionTitle || !items.subSectionTitle
              "
              @click="$emit('add-output-mapping')"
            >
              <v-icon icon="mdi-plus"></v-icon>
            </v-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, watch } from "vue";
import { TFormInputMapping, TFormOutputMapping } from "@/v2/Type";

import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { di } from "@fullcalendar/core/internal-common";

const props = defineProps<{
  item: TFormOutputMapping[];
  isEditMode: boolean;
  isEformSource: null | string;
  itemAll: TFormInputMapping;
}>();

const route = useRoute();
const store = useStore();
const formData = ref<TFormOutputMapping[]>([]);
const ListTahapan = ref<any[]>([]);
const ListContent = ref<any[]>([]);
const ListSection = ref<any[]>([]);
const ListSubsection = ref<any[]>([]);
watch(
  () => props.isEditMode,
  (newVal) => {
    if (newVal == true) {
      formData.value = [...props.item];
      getTahapanList();
      console.log(props.item, props.itemAll, "hahahahahahah");
    }
  },
  { immediate: true }
);

function getTahapanList() {
  console.log("get tahapan list", route.params);
  store
    .dispatch("contentStore/getBpList", {
      idEvent: route.params.idEvent,
      idSector: store.getters["documentStore/getSectorId"],
    })
    .then((res) => {
      console.log(res, "res tahapan");
      ListTahapan.value = Array.isArray(res)
        ? res.map((section: any) => ({
            Value: section.Value || "",
            id: section.Id || "",
          }))
        : [];
    });
}

function handleTahapanChange(value: string) {
  console.log("Tahapan changed to:", value);
  getListContent(value);
}

function getListContent(idTahapan: string) {
  const payload = {
    IdEFormSource: props.isEformSource,
    idBP: idTahapan,
  };
  console.log(payload, "payload content");
  console.log(props.item, "wewewewewe");
  store.dispatch("contentStore/getBpDocMappingList", payload).then((res) => {
    console.log(res, "res content", payload);
    ListContent.value = Array.isArray(res)
      ? res.map((section: any) => ({
          Value: section.Value || "",
          id: section.Id || "",
        }))
      : [];
  });
}

function handleContentChange(value: string) {
  console.log("Content changed to:", value);
  getListSection();
}

function getListSection() {
  store
    .dispatch("contentStore/getBpDocSectionMappingList", {
      idBPDoc: route.params.idDoc,
    })
    .then((res) => {
      console.log(res, "res section");
      ListSection.value = Array.isArray(res)
        ? res.map((section: any) => ({
            Value: section.Value || "",
            IdSection: section.IdSection || "",
          }))
        : [];
    });
}

function handleSectionChange(value: string) {
  console.log("Section changed to:", value);
  getListSubSection(value);
}

function getListSubSection(idSection: string) {
  store
    .dispatch("contentStore/getBpDocSubSectionMappingList", {
      idBPSection: idSection,
    })
    .then((res) => {
      console.log(res, "res sub section");
      ListSubsection.value = Array.isArray(res)
        ? res.map((subSection: any) => ({
            Value: subSection.Value || "",
            Id: subSection.Id || "",
          }))
        : [];
    });
}
</script>
