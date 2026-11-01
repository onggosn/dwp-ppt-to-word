<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="1100" persistent>
      <v-card class="border-radius-dwp h-100">
        <!-- ini title atas -->
        <v-card-title class="text-center my-2">
          <p class="text-18 fw-500">Submit Document</p>
          <v-btn
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onclose"
          />
        </v-card-title>
        <hr class="line my-3 d-block mb-5 pb-1" />

        <!-- ini awal mula load data -->
        <div class="mx-12">
          <template v-if="isLoading">
            <v-row>
              <v-col cols="12" v-for="idx in 6" :key="idx">
                <free-style-shimmer
                  :is-loading="true"
                  width="100%"
                  height="4.3rem"
                  border-radius="10px"
                />
              </v-col>
            </v-row>
          </template>
          <template v-if="!formTempInputGroup.length && !isLoading">
            <v-img
              :src="require('@/v2/assets/empty/no_available_state.svg')"
              style="
                display: block;
                margin: 0 auto;
                width: 300px;
                margin-top: 80px;
                margin-bottom: 40px;
                padding-bottom: 40px;
              "
            />
            <div class="text-center mb-10">
              <v-btn
                class="rounded-lg px-2 font-weight-bold"
                min-width="0"
                color="#065695"
                variant="outlined"
                @click="handleAddNewMapping()"
              >
                + Add Mapping
              </v-btn>
            </div>
          </template>
          <template v-if="formTempInputGroup.length && !isLoading">
            <p class="mt-2 font-weight-regular my-3 ml-2 label-form">
              Select Section to Submit
            </p>
            <v-row>
              <v-col cols="1" class="py-0">
                <v-checkbox
                  v-model="selectAll"
                  :value="true"
                  :error="v$.listIdEform.$error"
                  color="#065391"
                  style="height: 50px"
                  class="mt-n2"
                  @update:model-value="selectAllCheckbox"
                />
              </v-col>
              <v-col cols="5" class="py-0 pl-0">
                <p class="mt-2 font-weight-regular label-form">Select All</p>
              </v-col>
            </v-row>
            <v-form>
              <div
                v-for="(item, idx) in formTempInputGroup"
                :key="item.idEformSource"
              >
                <v-row>
                  <v-col cols="1" class="py-0">
                    <v-checkbox
                      v-model="listIdEform"
                      color="#065391"
                      :value="item.idEformSource"
                      :error="v$.listIdEform.$error"
                      class="mt-n2"
                    />
                  </v-col>
                  <v-col cols="12" sm="5" class="py-0 pl-0">
                    <p class="mt-2 font-weight-regular label-form">
                      {{ item.isEdited ? "Input Mapping" : "SubSection Title" }}
                    </p>
                    <template v-if="!item.isEdited">
                      <div class="py-2">
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
                            >{{
                              item.subSectionTitle
                                ? item.subSectionTitle
                                : item.sectionTitle
                            }}</span
                          >
                        </v-chip>
                      </div>
                    </template>
                    <template v-else>
                      <div v-if="!item.isDelete" class="py-2">
                        <v-chip
                          class="chip-text"
                          :class="[
                            'border-radius-dwp py-7 px-4 text-truncate mb-2',
                          ]"
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
                            <span
                              style="
                                word-break: break-word;
                                white-space: normal;
                              "
                            >
                              {{ item.sectionTitle }}
                            </span>
                          </span>
                        </v-chip>
                        <v-chip
                          v-if="item.subSectionTitle"
                          class="chip-text"
                          :class="[
                            'border-radius-dwp py-7 px-4 text-truncate mb-2',
                          ]"
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
                            <span
                              style="
                                word-break: break-word;
                                white-space: normal;
                              "
                            >
                              {{ item.subSectionTitle }}
                            </span>
                          </span>
                        </v-chip>
                      </div>
                      <div v-else>
                        <v-autocomplete
                          style="width: 100%"
                          variant="solo"
                          placeholder="Choose Section"
                          v-model="item.sectionTitle"
                          :loading="item.isLoadingSection"
                          loading-text="Loading..."
                          :items="item.listSection"
                          :item-title="'name'"
                          :item-value="'name'"
                          :disabled="!item.isDelete"
                          :no-data-text="
                            item.isLoadingSection ? '' : 'No data available'
                          "
                          clearable
                          @focus="getListSection(idx)"
                          @update:modelValue="
                            handleSectionChangeInput($event, idx)
                          "
                          return-object
                          @click:clear="
                            (item.sectionTitle = null),
                              (item.subSectionTitle = null),
                              (item.idSubSection = null),
                              (item.idEformSource = null),
                              (item.idSection = null)
                          "
                        ></v-autocomplete>
                        <v-autocomplete
                          style="width: 100%"
                          variant="solo"
                          placeholder="Choose Sub Section"
                          item-title="Value"
                          item-value="Value"
                          v-model="item.subSectionTitle"
                          :loading="item.isLoadingSubSection"
                          loading-text="Loading..."
                          :items="item.listSubSection"
                          :disabled="!item.sectionTitle"
                          @update:modelValue="
                            handleSubSectionChangeInput($event, idx)
                          "
                          @focus="getListSubSectionInput(idx)"
                          return-object
                          :no-data-text="
                            item.isLoadingSection ? '' : 'No data available'
                          "
                          @clear="
                            (item.subSectionTitle = null),
                              (item.idSubSection = null)
                          "
                        ></v-autocomplete>
                      </div>
                    </template>
                  </v-col>
                  <v-col cols="12" sm="6" class="py-0 pl-0">
                    <template v-if="!item.isEdited">
                      <div>
                        <p class="font-weight-regular label-form">
                          Output mapping
                        </p>
                        <div class="py-2">
                          <v-chip
                            class="chip-text"
                            v-for="(items, index) in item.outputMappings"
                            :key="index"
                            :class="[
                              'border-radius-dwp py-7 px-4 text-truncate mb-2',
                            ]"
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
                              <span
                                style="
                                  word-break: break-word;
                                  white-space: normal;
                                "
                              >
                                <strong>{{ items.documentName }}</strong> -
                                {{ items.title }}
                              </span>
                            </span>
                          </v-chip>
                        </div>
                      </div>
                    </template>
                    <template v-else>
                      <div
                        v-for="(items, index) in item.outputMappings"
                        :key="index"
                      >
                        <p class="my-2 font-weight-regular label-form">
                          Output mapping {{ index + 1 }}
                        </p>
                        <div v-if="!items.isDelete" class="py-2">
                          <v-chip
                            class="chip-text"
                            :class="[
                              'border-radius-dwp py-7 px-4 text-truncate mb-2',
                            ]"
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
                              <span
                                style="
                                  word-break: break-word;
                                  white-space: normal;
                                "
                              >
                                {{ items.documentName }}
                              </span>
                            </span>
                          </v-chip>
                          <div
                            v-if="
                              items.condisionalSubsection !== items.sectionTitle
                            "
                          >
                            <v-chip
                              class="chip-text"
                              :class="[
                                'border-radius-dwp py-7 px-4 text-truncate mb-2',
                              ]"
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
                                <span
                                  style="
                                    word-break: break-word;
                                    white-space: normal;
                                  "
                                >
                                  {{ items.sectionTitle }}
                                </span>
                              </span>
                            </v-chip>
                            <div class="d-flex">
                              <v-chip
                                class="chip-text"
                                :class="[
                                  'border-radius-dwp py-7 px-4 text-truncate mb-2',
                                ]"
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
                                  <span
                                    style="
                                      word-break: break-word;
                                      white-space: normal;
                                    "
                                  >
                                    {{ items.condisionalSubsection }}
                                  </span>
                                </span>
                              </v-chip>
                              <div class="d-flex pl-2" :style="{ gap: '10px' }">
                                <v-btn
                                  v-if="items.isDelete"
                                  class="rounded-lg"
                                  min-width="0"
                                  height="40"
                                  width="40"
                                >
                                  <v-icon icon="mdi-delete" color="red"></v-icon
                                ></v-btn>
                                <v-btn
                                  v-if="
                                    index === item.outputMappings.length - 1
                                  "
                                  class="p-2 primary-gradient rounded-lg btn-icon"
                                  height="40"
                                  width="40"
                                  min-width="0"
                                  @click="handleAddOutputMapping(idx)"
                                >
                                  <v-icon icon="mdi-plus"></v-icon>
                                </v-btn>
                              </div>
                            </div>
                          </div>

                          <div v-else class="d-flex">
                            <v-chip
                              class="chip-text"
                              :class="[
                                'border-radius-dwp py-7 px-4 text-truncate mb-2',
                              ]"
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
                                <span
                                  style="
                                    word-break: break-word;
                                    white-space: normal;
                                  "
                                >
                                  {{ items.sectionTitle }}
                                </span>
                              </span>
                            </v-chip>
                            <div class="d-flex pl-2" :style="{ gap: '10px' }">
                              <v-btn
                                v-if="items.isDelete"
                                class="rounded-lg"
                                min-width="0"
                                height="40"
                                width="40"
                              >
                                <v-icon icon="mdi-delete" color="red"></v-icon
                              ></v-btn>
                              <v-btn
                                v-if="index === item.outputMappings.length - 1"
                                class="p-2 primary-gradient rounded-lg btn-icon"
                                height="40"
                                width="40"
                                min-width="0"
                                @click="handleAddOutputMapping(idx)"
                              >
                                <v-icon icon="mdi-plus"></v-icon>
                              </v-btn>
                            </div>
                          </div>
                        </div>
                        <div v-else :key="listKey">
                          <v-autocomplete
                            style="width: 100%"
                            variant="solo"
                            placeholder="Choose Tahapan"
                            v-model="items.tahapan"
                            :loading="items.isLoadingTahapan"
                            loading-text="Loading..."
                            :item-title="'Value'"
                            :item-value="'Value'"
                            :items="items.listTahapan"
                            :disabled="item.idEformSource == null"
                            @update:modelValue="
                              handleTahapanChange($event, idx, index)
                            "
                            :no-data-text="
                              items.isLoadingTahapan ? '' : 'No data available'
                            "
                            return-object
                            @focus="getTahapanList(idx, index)"
                          ></v-autocomplete>
                          <v-autocomplete
                            style="width: 100%"
                            variant="solo"
                            placeholder="Choose Content"
                            v-model="items.documentName"
                            :loading="items.isLoadingContent"
                            loading-text="Loading..."
                            :item-title="'Value'"
                            :item-value="'Value'"
                            :items="items.listContent"
                            :disabled="!items.tahapan"
                            clearable
                            return-object
                            @update:modelValue="
                              handleContentChange($event, idx, index)
                            "
                            :no-data-text="
                              items.isLoadingContent ? '' : 'No data available'
                            "
                            @focus="getContentList(idx, index)"
                            @click:clear="
                              (items.documentName = null),
                                (items.sectionTitle = null),
                                (items.subSectionTitle = null),
                                (items.idSubSection = null),
                                (items.idBpSection = null),
                                (items.idEformSource = null),
                                (items.idBpDocument = null)
                            "
                          ></v-autocomplete>
                          <v-autocomplete
                            style="width: 100%"
                            variant="solo"
                            placeholder="Choose Section"
                            v-model="items.sectionTitle"
                            :loading="items.isLoadingSection"
                            loading-text="Loading..."
                            :item-title="'name'"
                            :item-value="'idEformSource'"
                            :items="items.listSection"
                            :disabled="!items.tahapan || !items.documentName"
                            clearable
                            return-object
                            @update:modelValue="
                              handleSectionOutputChange($event, idx, index)
                            "
                            :error-messages="
                              v$.formTempInputGroup.$each.$response.$data[idx]
                                .outputMappings.$each.$data[index].idBpSection
                                .uniqueComb
                                ? ''
                                : 'Duplicate section selected.'
                            "
                            :no-data-text="
                              items.isLoadingSection ? '' : 'No data available'
                            "
                            @focus="getListSectionOutput(idx, index)"
                            @click:clear="
                              (items.sectionTitle = null),
                                (items.subSectionTitle = null),
                                (items.idSubSection = null),
                                (items.idBpSection = null),
                                (items.idEformSource = null)
                            "
                          ></v-autocomplete>
                          <div class="d-flex">
                            <div class="text-left" style="width: 100%">
                              <v-autocomplete
                                style="width: 100%"
                                variant="solo"
                                placeholder="Choose Sub Section (Opsional)"
                                v-model="items.subSectionTitle"
                                :loading="items.isLoadingSubSection"
                                loading-text="Loading..."
                                :items="items.listSubSection"
                                :item-title="'Value'"
                                :item-value="'Id'"
                                :disabled="!items.sectionTitle"
                                clearable
                                return-object
                                @click:clear="
                                  (items.subSectionTitle = null),
                                    (items.idSubSection = null)
                                "
                                @update:modelValue="
                                  handleSubSectionChangeOutput(
                                    $event,
                                    idx,
                                    index
                                  )
                                "
                                :no-data-text="
                                  items.isLoadingSubSection
                                    ? ''
                                    : 'No data available'
                                "
                                :error-messages="
                                  v$.formTempInputGroup.$each.$response.$data[
                                    idx
                                  ].outputMappings.$each.$data[index]
                                    .idSubSection.uniqueSub
                                    ? ''
                                    : 'Duplicate Subsection selected.'
                                "
                                @focus="getListOutputSubSection(idx, index)"
                              ></v-autocomplete>
                            </div>
                            <div class="d-flex ma-2" :style="{ gap: '10px' }">
                              <v-btn
                                v-if="
                                  items.isDelete &&
                                  item.outputMappings.length > 1
                                "
                                class="rounded-lg"
                                min-width="0"
                                height="40"
                                width="40"
                                @click="item.outputMappings.splice(index, 1)"
                              >
                                <v-icon icon="mdi-delete" color="red"></v-icon
                              ></v-btn>
                              <v-btn
                                v-if="index === item.outputMappings.length - 1"
                                class="p-2 primary-gradient rounded-lg btn-icon"
                                height="40"
                                width="40"
                                min-width="0"
                                :disabled="
                                  !items.sectionTitle ||
                                  v$.formTempInputGroup.$each.$response.$data[
                                    idx
                                  ].outputMappings.$invalid
                                "
                                @click="handleAddOutputMapping(idx)"
                              >
                                <v-icon icon="mdi-plus"></v-icon>
                              </v-btn>
                            </div>
                          </div>
                        </div>
                      </div>
                    </template>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="1">
                    <v-btn
                      v-if="!item.isEdited"
                      class="rounded-lg px-2 font-weight-bold"
                      min-width="0"
                      color="#065695"
                      variant="outlined"
                      :disabled="isEditMode"
                      @click="handleEditItemMapping(idx)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                      Edit
                    </v-btn>
                  </v-col>
                  <v-col cols="12" sm="5">
                    <div v-if="item.isEdited" class="d-flex">
                      <div v-if="item.isDelete">
                        <v-btn
                          class="rounded-lg px-2 py-2 font-weight-bold text-12"
                          min-width="0"
                          color="#d6212a"
                          variant="outlined"
                          :loading="isLoadingTemp"
                          @click="handleDeleteAllMapping(idx)"
                        >
                          <v-icon>mdi-delete</v-icon>
                          Delete
                        </v-btn>
                      </div>
                      <div class="ps-2">
                        <v-btn
                          class="rounded-lg px-2 font-weight-bold"
                          min-width="0"
                          :loading="isLoadingTemp"
                          color="#065695"
                          variant="outlined"
                          :disabled="
                            !formTempInputGroup[idx].idEformSource ||
                            !formTempInputGroup[idx].sectionTitle ||
                            v$.formTempInputGroup.$each.$response.$data[idx]
                              .outputMappings.$invalid
                          "
                          @click="handleSaveItemMapping(idx)"
                        >
                          <v-icon>mdi-folder-open-outline</v-icon>
                          Save
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </div>
              <div class="pt-4">
                <v-btn
                  class="rounded-lg px-2 font-weight-bold"
                  min-width="0"
                  color="#065695"
                  variant="outlined"
                  :disabled="
                    isEditMode ||
                    formTempInputGroup.some((item) => !item.idEformSource)
                  "
                  @click="handleAddMappingOnly()"
                >
                  + Add Mapping
                </v-btn>
              </div>
            </v-form>
            <div class="my-5">
              <p class="font-weight-regular label-form">
                Should the updated data be appended or replaced?<span
                  class="text-red"
                  >*</span
                >
              </p>
              <v-radio-group v-model="isAppend" class="w-50">
                <div class="d-flex">
                  <v-radio label="Append" :value="true" color="#065391" />
                  <v-radio label="Replace" :value="false" color="#065391" />
                </div>
              </v-radio-group>
            </div>
          </template>
        </div>
        <v-card-actions
          v-if="formTempInputGroup.length"
          class="justify-end pb-5 pr-8 pt-5"
          style="
            padding-top: 0px;
            background: white;
            border-radius: 0px 0px 10px 10px;
            box-shadow: 10px 10px;
          "
        >
          <v-spacer />
          <v-btn
            variant="flat"
            elevation="3"
            width="6vw"
            class="rounded-lg font-weight-bold"
            style="
              background: linear-gradient(#fff -46.47%, #fff 157.9%);
              border-radius: 10px;
              padding-left: 15px;
              padding-right: 15px;
              font-weight: 800;
              color: #065695;
            "
            :loading="isLoading"
            @click="onclose"
          >
            Cancel
          </v-btn>
          <v-btn
            variant="flat"
            color="#065695"
            width="6vw"
            elevation="3"
            class="ml-5 rounded-lg font-weight-bold"
            style="color: #fdfdfd"
            :loading="isLoading"
            :disabled="isEditMode || listIdEform.length === 0"
            @click="submit"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength, helpers } from "@vuelidate/validators";
import {
  TDetailSubmit,
  TListEForm,
  TFormInputMapping,
  TFormOutputMapping,
} from "@/v2/Type";

const dialog = ref(false);
const isEditMode = ref(false);
const isLoading = ref(false);
const isLoadingTemp = ref(false);
const route = useRoute();
const store = useStore();
let formTempInputGroup = ref<TFormInputMapping[]>([]);
let formTempOutputGroup = ref<TFormOutputMapping[]>([]);
const instance = ref<any>(getCurrentInstance()?.root.refs);
const items = ref<TDetailSubmit[]>([]);
const listIdEform = ref<string[]>([]);
const selectAll = ref(false);
const listKey = ref(0);
const isAppend = ref(false);

const emit = defineEmits<{
  (e: "submit", value: TListEForm): void;
  (e: "close", value: boolean): void;
}>();

function setDataDetail(temp) {
  formTempInputGroup.value = [];
  temp.forEach((element: TFormInputMapping, index: number) => {
    const inputMapping: TFormInputMapping = {
      id: index + 1,
      idEformSource: element.idEformSource || null,
      isEdited: false,
      isDelete: element.isDelete || false,

      subSectionTitle:
        element.sectionTitle === element.subSectionTitle
          ? null
          : element.subSectionTitle,
      sectionTitle: element.sectionTitle || null,
      listSection: [],
      listSubSection: [],
      isLoadingSection: false,
      isLoadingSubSection: false,
      idSection: element.idSection || null,
      idSubSection: element.idSubSection || null,
      IdEformSourceOriginal: element.idEformSource || null,
      outputMappings: [],
    };
    element.outputMappings.forEach((outMapping) => {
      const outputMapping: TFormOutputMapping = {
        documentName: outMapping.documentName,
        isDelete: outMapping.isDelete || false,
        isEdited: false,
        tahapan: outMapping.tahapan || null,
        sectionTitle: outMapping.sectionTitle || null,
        subSectionTitle:
          outMapping.subSectionTitle == outMapping.sectionTitle
            ? null
            : outMapping.subSectionTitle,
        condisionalSubsection: outMapping.subSectionTitle,
        isLoadingContent: false,
        isLoadingSection: false,
        isLoadingSubSection: false,
        isLoadingTahapan: false,
        listTahapan: [],
        listContent: [],
        listSection: [],
        listSubSection: [],
        title: outMapping.title || null,
        idBp: outMapping.idBp || null,
        idBpDocument: outMapping.idBpDocument || null,
        idBpSection: outMapping.idBpSection || null,
        idSubSection: outMapping.idSubSection || null,
        idEformSource: outMapping.idEformSource || null,
      };
      inputMapping.outputMappings.push(outputMapping);
    });
    formTempInputGroup.value.push(inputMapping);
  });
}

async function getSubmitDetail() {
  isLoading.value = true;
  try {
    const reqData = { idBpDocument: route.params.idDoc };
    const response = await store.dispatch("eFormStore/getSubmitDetail", {
      idBpDocument: reqData.idBpDocument,
    });
    isLoading.value = false;
    isLoadingTemp.value = false;
    if (Array.isArray(response.responseData)) {
      setDataDetail(response.responseData);
    } else {
      formTempInputGroup.value = [];
    }
  } catch (error) {
    formTempInputGroup.value = [];
    isLoading.value = false;
  }
}

function handleAddNewMapping() {
  handleNewMapping();
}

function handleNewMapping() {
  const newOutput: TFormOutputMapping = {
    documentName: null,
    isDelete: true,
    isEdited: true,
    tahapan: null,
    sectionTitle: null,
    subSectionTitle: null,
    condisionalSubsection: "",
    isLoadingContent: false,
    isLoadingSection: false,
    isLoadingSubSection: false,
    isLoadingTahapan: false,
    listTahapan: [],
    listContent: [],
    listSection: [],
    listSubSection: [],
    title: null,
    idBp: null,
    idBpDocument: null,
    idBpSection: null,
    idSubSection: null,
    idEformSource: null,
  };
  const newInput: TFormInputMapping = {
    id: null,
    idEformSource: null,
    isEdited: true,
    isDelete: true,
    subSectionTitle: null,
    sectionTitle: null,
    isLoadingSection: false,
    isLoadingSubSection: false,
    listSection: [],
    listSubSection: [],
    outputMappings: [newOutput],
    idSection: null,
    idSubSection: null,
    IdEformSourceOriginal: null,
  };
  formTempInputGroup.value.push(newInput);
}

function getTahapanList(indexInput: number, indexOutput: number) {
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].isLoadingTahapan = true;
  store
    .dispatch("contentStore/getBpList", {
      idEvent: route.params.idEvent,
      idSector: store.getters["documentStore/getSectorId"],
    })
    .then((res) => {
      if (Array.isArray(res)) {
        formTempInputGroup.value[indexInput].outputMappings[
          indexOutput
        ].listTahapan = res.map((section: any) => ({
          Value: section.Value || "",
          id: section.Id || "",
        }));
        // formTempInputGroup.value.map((item) => {
        //   item.outputMappings.map((x) => {
        //     x.listTahapan = res.map((section: any) => ({
        //       Value: section.Value || "",
        //       id: section.Id || "",
        //     }));
        //   });
        // });
      }
      formTempInputGroup.value[indexInput].outputMappings[
        indexOutput
      ].isLoadingTahapan = false;
    });
}

function getListSection(indexInput: number) {
  formTempInputGroup.value[indexInput].isLoadingSection = true;
  formTempInputGroup.value[indexInput].listSection = [];
  store
    .dispatch("contentStore/getBpDocSectionMappingList", {
      idBPDoc: route.params.idDoc,
      isSource: true,
    })
    .then((res) => {
      formTempInputGroup.value[indexInput].listSection = Array.isArray(res)
        ? res.map((section: any) => ({
            name: section.Value || "",
            idSection: section.IdSection || "",
            idEformSource: section.IdEForm || "",
          }))
        : [];
      formTempInputGroup.value[indexInput].isLoadingSection = false;
    });
}

function handleSectionChangeInput(newValue: any, index: number) {
  formTempInputGroup.value[index].idSection = newValue?.idSection;
  formTempInputGroup.value[index].idEformSource = newValue?.idEformSource;

  formTempInputGroup.value[index].idSubSection = null;
  formTempInputGroup.value[index].subSectionTitle = null;
}

function handleSubSectionChangeInput(newValue: any, index: number) {
  formTempInputGroup.value[index].idSubSection = newValue?.Id;
}

function getListSubSectionInput(index) {
  formTempInputGroup.value[index].listSubSection = [];
  formTempInputGroup.value[index].isLoadingSubSection = true;
  const idSection = formTempInputGroup.value[index].idSection;

  store
    .dispatch("contentStore/getBpDocSubSectionMappingList", {
      idBPSection: idSection,
      isSource: true,
    })
    .then((res) => {
      formTempInputGroup.value[index].listSubSection = Array.isArray(res)
        ? res.map((section: any) => ({
            Value: section.Value || "",
            Id: section.Id || "",
          }))
        : [];
      formTempInputGroup.value[index].isLoadingSubSection = false;
    });
}

function getContentList(indexInput: number, indexOutput: number) {
  formTempInputGroup.value[indexInput].outputMappings[indexOutput].listContent =
    [];
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].isLoadingContent = true;
  const idTahapan =
    formTempInputGroup.value[indexInput].outputMappings[indexOutput].idBp;
  const payload = {
    IdEFormSource: formTempInputGroup.value[indexInput].idEformSource,
    idBP: idTahapan,
  };
  store.dispatch("contentStore/getBpDocMappingList", payload).then((res) => {
    formTempInputGroup.value[indexInput].outputMappings[
      indexOutput
    ].listContent = Array.isArray(res)
      ? res.map((section: any) => ({
          Value: section.Value || "",
          id: section.Id || "",
        }))
      : [];
    formTempInputGroup.value[indexInput].outputMappings[
      indexOutput
    ].isLoadingContent = false;
  });
}

function handleAddOutputMapping(idxInput: number) {
  const newOutput: TFormOutputMapping = {
    documentName: null,
    isDelete: true,
    isEdited: true,
    tahapan: null,
    sectionTitle: null,
    subSectionTitle: null,
    isLoadingContent: false,
    condisionalSubsection: "",
    isLoadingSection: false,
    isLoadingSubSection: false,
    isLoadingTahapan: false,
    listTahapan: [],
    listContent: [],
    listSection: [],
    listSubSection: [],
    title: null,
    idBp: null,
    idBpDocument: null,
    idBpSection: null,
    idSubSection: null,
    idEformSource: null,
  };

  formTempInputGroup.value[idxInput].outputMappings.push(newOutput);
}

watch(
  [
    formTempInputGroup,
    () => formTempInputGroup.value.map((i) => i.outputMappings),
  ],
  () => {
    const editedInput = formTempInputGroup.value.some((item) => item.isEdited);
    const editedOutput = formTempInputGroup.value.some(
      (item) =>
        Array.isArray(item.outputMappings) &&
        item.outputMappings.some((out: any) => out.isEdited)
    );
    isEditMode.value = editedInput || editedOutput;
  },
  { deep: true }
);

function handleEditItemMapping(idx: number) {
  formTempInputGroup.value[idx].isEdited = true;
}
function handleDeleteAllMapping(idx: number) {
  isLoadingTemp.value = true;
  const req = {
    IdEFormSource: formTempInputGroup.value[idx].idEformSource,
    IdEformSourceOriginal: formTempInputGroup.value[idx].IdEformSourceOriginal,
    IdEformDestination: [] as string[],
  };
  if (!formTempInputGroup.value[idx].id) {
    formTempInputGroup.value.splice(idx, 1);
    isLoadingTemp.value = false;
    return;
  }
  store
    .dispatch("contentStore/mappingSection", req)
    .then((res) => {
      if (res.responseCode === "011000") {
        instance.value.toast.show({
          message: res.responseMessage,
          timeout: 1000,
          color: "success",
        });
        formTempInputGroup.value.splice(idx, 1);
        dialog.value = true;
      } else {
        instance.value.toast.show({
          message: res.responseMessage,
          timeout: 1000,
          color: "warning",
        });
      }
    })
    .finally(() => {
      clearState();
      isLoadingTemp.value = false;
    });
}
function handleSaveItemMapping(idx: number) {
  handleSaveClearItemMapping(formTempInputGroup.value[idx]);
}

function handleSaveClearItemMapping(payload: any) {
  isLoadingTemp.value = true;
  let req = {
    IdEFormSource: payload.idSubSection ?? payload.idEformSource,
    IdEformSourceOriginal: payload.IdEformSourceOriginal,
    IdEformDestination: [] as string[],
  };
  payload.outputMappings.map((item) => {
    if (item.idSubSection == null) {
      if (item.idEformSource != null) {
        req.IdEformDestination.push(item.idEformSource);
      }
    } else {
      req.IdEformDestination.push(item.idSubSection);
    }
  });
  store.dispatch("contentStore/mappingSection", req).then((res) => {
    if (res.responseCode === "011000") {
      instance.value.toast.show({
        message: res.responseMessage,
        timeout: 1000,
        color: "success",
      });
      isLoadingTemp.value = false;
      clearState();
      getSubmitDetail();
      dialog.value = true;
    } else {
      instance.value.toast.show({
        message: res.responseMessage,
        timeout: 1000,
        color: "warning",
      });
      isLoadingTemp.value = false;
    }
    isLoadingTemp.value = false;
  });
}

function handleAddMappingOnly() {
  handleNewMapping();
}

function handleClearMapping() {
  formTempInputGroup.value = [];
  formTempOutputGroup.value = [];
  items.value = [];
  isEditMode.value = false;
}

// start logic validate untuk STP
const findSiblingList = (itemObject) => {
  if (itemObject) {
    for (const parent of formTempInputGroup.value) {
      if (parent.outputMappings.includes(itemObject)) {
        return parent.outputMappings;
      }
    }
  }
  return [];
};
const isCombinationUnique = (value, object) => {
  if (value == null) {
    return true;
  } else {
    if (object) {
      const siblingList = findSiblingList(object);
      const currentSubId = object.idSubSection;
      let count = 0;

      for (let index = 0; index < siblingList.length; index++) {
        if (siblingList[index].idBpSection === value) {
          if (currentSubId != null) {
            if (siblingList[index].idSubSection === currentSubId) {
              count++;
            }
          } else {
            count++;
          }
        }
      }
      return count <= 1;
    } else {
      return true;
    }
  }
};

const isSubSectionUnique = (value, object) => {
  if (value == null) {
    return true;
  } else {
    if (object) {
      const siblingList = findSiblingList(object);

      const count = siblingList.filter(
        (item) => item.idSubSection === value
      ).length;
      return count <= 1;
    } else {
      return true;
    }
  }
};

const rules = {
  listIdEform: {
    required: helpers.withMessage(
      "Please select at least one section.",
      required
    ),
    minLength: helpers.withMessage(
      "You must select at least one section.",
      minLength(1)
    ),
  },
  formTempInputGroup: {
    $each: helpers.forEach({
      // --- VALIDASI LEVEL 2 ---
      outputMappings: {
        $each: helpers.forEach({
          // Validasi item di dalam outputMappings
          idBp: { required }, // <-- TAMBAH: idBp
          idBpDocument: { required },
          idBpSection: {
            required,
            uniqueComb: helpers.withMessage(
              "Kombinasi Section dan Sub Section ini sudah ada.",
              isCombinationUnique
            ),
          },
          idSubSection: {
            uniqueSub: helpers.withMessage(
              "Sub Section ini sudah digunakan.",
              isSubSectionUnique
            ),
          },
        }),
      },
    }),
  },
};
const v$ = useVuelidate(rules, { listIdEform, formTempInputGroup });

function showDialog() {
  clearState();
  getSubmitDetail();
  dialog.value = true;
}
function onclose() {
  handleClearMapping();
  dialog.value = false;
  emit("close", true);
}
function clearState() {
  listIdEform.value = [];
  isAppend.value = false;
}

function selectAllCheckbox(val: boolean) {
  if (val)
    listIdEform.value = formTempInputGroup.value.map(
      (item: TDetailSubmit) => item.idEformSource
    );
  else listIdEform.value = [];
}

watch(listIdEform, (val) => {
  selectAll.value =
    formTempInputGroup.value.length > 0 &&
    val.length === formTempInputGroup.value.length;
});

async function submit() {
  const result = await v$.value.$validate();
  if (!result) return;
  emit("submit", { isAppend: isAppend.value, listIdEform: listIdEform.value });
}

function handleTahapanChange(
  value: any,
  indexInput: number,
  indexOutput: number
) {
  // forceRerender();
  formTempInputGroup.value[indexInput].outputMappings[indexOutput].idBp =
    value?.id;

  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].documentName = null;

  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idSubSection = null;

  formTempInputGroup.value[indexInput].outputMappings[indexOutput].idBpSection =
    null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idEformSource = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].sectionTitle = null;
}

function handleContentChange(value: any, indexInput, indexOutput) {
  // forceRerender();
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idBpDocument = value?.id;

  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idSubSection = null;

  formTempInputGroup.value[indexInput].outputMappings[indexOutput].idBpSection =
    null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idEformSource = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].sectionTitle = null;
}

function getListSectionOutput(indexInput: number, indexOutput: number) {
  formTempInputGroup.value[indexInput].outputMappings[indexOutput].listSection =
    [];
  const data =
    formTempInputGroup.value[indexInput].outputMappings[indexOutput]
      .idBpDocument;
  store
    .dispatch("contentStore/getBpDocSectionMappingList", {
      idBPDoc: data,
    })
    .then((res) => {
      formTempInputGroup.value[indexInput].outputMappings[
        indexOutput
      ].listSection = Array.isArray(res)
        ? res.map((section: any) => ({
            name: section.Value || "",
            idSection: section.IdSection || "",
            idEformSource: section.IdEForm || "",
          }))
        : [];
    });
}

function handleSubSectionChangeOutput(
  value: any,
  indexInput: number,
  indexOutput: number
) {
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idSubSection = value?.Id;
}

function handleSectionOutputChange(
  value: any,
  indexInput: number,
  indexOutput: number
) {
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idSubSection = null;

  //ini batas
  formTempInputGroup.value[indexInput].outputMappings[indexOutput].idBpSection =
    value?.idSection;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idEformSource = value?.idEformSource;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
}

function getListOutputSubSection(indexInput: number, indexOutput: number) {
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].listSubSection = [];
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].isLoadingSubSection = true;
  const idSection =
    formTempInputGroup.value[indexInput].outputMappings[indexOutput]
      .idBpSection;
  store
    .dispatch("contentStore/getBpDocSubSectionMappingList", {
      idBPSection: idSection,
    })
    .then((res) => {
      formTempInputGroup.value[indexInput].outputMappings[
        indexOutput
      ].listSubSection = Array.isArray(res)
        ? res.map((subSection: any) => ({
            Value: subSection.Value || "",
            Id: subSection.Id || "",
          }))
        : [];
      formTempInputGroup.value[indexInput].outputMappings[
        indexOutput
      ].isLoadingSubSection = false;
    });
}

defineExpose({ showDialog, onclose });
</script>

<style scoped>
.line {
  border: none;
  height: 3px;
  margin: 16px 0;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}
:deep(.v-btn--disabled) {
  background-color: #a6abc7 !important;
}
:deep(.v-btn--disabled .v-btn__content) {
  color: #000 !important;
}
:deep(.v-chip.v-chip--size-default) {
  height: auto !important;
  padding: 10px !important;
}
:deep(.v-field.v-field--appended) {
  border-radius: 18px !important;
}
:deep(
    .v-input--disabled .v-field--variant-solo,
    .v-field--variant-solo-filled
  ) {
  background: #b3b0b0 !important;
}
.label-form {
  font-weight: 500;
  font-size: 15px;
  color: #3a416f;
}
</style>
