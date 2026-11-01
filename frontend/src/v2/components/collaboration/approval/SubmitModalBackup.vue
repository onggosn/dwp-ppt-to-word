<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="1100" persistent>
      <v-card class="border-radius-dwp h-100">
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
        <div class="mx-12">
          <p
            v-if="formTempInputGroup.length && !isLoading"
            class="mt-2 font-weight-regular my-3 ml-2"
          >
            Select Section to Submit
          </p>
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
            <div>
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
            </div>
          </template>
          <template v-if="formTempInputGroup.length && !isLoading">
            <v-row>
              <v-col cols="1">
                <v-checkbox
                  v-model="selectAll"
                  :value="true"
                  :error="v$.listIdEform.$error"
                  color="#065391"
                  style="height: 50px"
                  class="mt-n2"
                />
              </v-col>
              <v-col cols="5">
                <p class="mt-2 font-weight-regular">Select All</p>
              </v-col>
            </v-row>
            <v-form>
              <div
                v-for="(item, idx) in formTempInputGroup"
                :key="item.idEformSource"
              >
                <v-row>
                  <v-col cols="1">
                    <v-checkbox
                      v-model="listIdEform"
                      color="#065391"
                      :value="item.idEformSource"
                      :error="v$.listIdEform.$error"
                      class="mt-n2"
                    />
                  </v-col>
                  <v-col cols="12" sm="5">
                    <p class="mt-2 font-weight-regular">
                      {{ item.isEdited ? "Input Mapping" : "SubSection Title" }}
                    </p>
                    <!-- section input -->
                    <div>
                      <div v-if="!item.isEdited" class="py-2">
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
                      <div v-else class="py-2">
                        <div v-if="!item.isDelete">
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
                            :items="item.listSection"
                            :item-title="'name'"
                            :item-value="'idSection'"
                            :disabled="!item.isDelete"
                            @update:modelValue="
                              handleSectionChangeInput($event, idx)
                            "
                            clearable
                            @click:clear="handleClearTempSection(idx)"
                          ></v-autocomplete>
                          <v-autocomplete
                            style="width: 100%"
                            variant="solo"
                            placeholder="Choose Sub Section"
                            item-title="Value"
                            item-value="Id"
                            v-model="item.subSectionTitle"
                            :items="item.listSubSection"
                            :disabled="!item.sectionTitle"
                            @update:modelValue="
                              handleSubSectionChangeInput($event, idx)
                            "
                          ></v-autocomplete>
                        </div>
                      </div>
                    </div>
                    <!-- <item-input-stp
                      :item="item"
                      :index="idx"
                      :is-edit-mode="item.isEdited"
                      @update-input-mapping="handleUpdateTempInput($event)"
                    /> -->
                  </v-col>
                  <v-col cols="12" sm="6">
                    <!-- bagian mapping output -->
                    <div>
                      <div v-if="!item.isEdited">
                        <p class="mt-2 font-weight-regular">Output mapping</p>
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
                      <div v-else>
                        <div
                          v-for="(items, index) in item.outputMappings"
                          :key="index"
                        >
                          <p class="mt-2 font-weight-regular">
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
                              v-if="items.subSectionTitle != items.sectionTitle"
                              class="d-flex"
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
                                  v-if="
                                    index === item.outputMappings.length - 1
                                  "
                                  class="p-2 primary-gradient rounded-lg btn-icon"
                                  height="55"
                                  width="55"
                                  @click="handleAddOutputMapping(idx)"
                                >
                                  <v-icon icon="mdi-plus"></v-icon>
                                </v-btn>
                              </div>
                            </div>

                            <div v-else class="d-flex">
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
                                  v-if="
                                    index === item.outputMappings.length - 1
                                  "
                                  class="p-2 primary-gradient rounded-lg btn-icon"
                                  height="55"
                                  width="55"
                                  @click="handleAddOutputMapping(idx)"
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
                              :items="items.listTahapan"
                              :disabled="item.idEformSource == null"
                              clearable
                              @update:modelValue="
                                handleTahapanChange($event, idx, index)
                              "
                              @click:clear="
                                (items.tahapan = null),
                                  (items.documentName = null),
                                  (items.sectionTitle = null),
                                  (items.subSectionTitle = null)
                              "
                            ></v-autocomplete>
                            <v-autocomplete
                              style="width: 100%"
                              variant="solo"
                              placeholder="Choose Content"
                              v-model="items.documentName"
                              :item-title="'Value'"
                              :item-value="'id'"
                              :items="items.listContent"
                              :disabled="!items.tahapan"
                              clearable
                              @update:modelValue="
                                handleContentChange($event, idx, index)
                              "
                              @click:clear="
                                (items.documentName = null),
                                  (items.sectionTitle = null),
                                  (items.subSectionTitle = null)
                              "
                            ></v-autocomplete>
                            <v-autocomplete
                              style="width: 100%"
                              variant="solo"
                              placeholder="Choose Section"
                              v-model="items.sectionTitle"
                              :item-title="'name'"
                              :item-value="'idEformSource'"
                              :items="items.listSection"
                              :disabled="!items.tahapan || !items.documentName"
                              clearable
                              @update:modelValue="
                                handleSectionOutputChange($event, idx, index)
                              "
                              @click:clear="
                                (items.sectionTitle = null),
                                  (items.subSectionTitle = null)
                              "
                            ></v-autocomplete>
                            <div class="d-flex">
                              <v-autocomplete
                                style="width: 100%"
                                variant="solo"
                                placeholder="Choose Sub Section (Opsional)"
                                v-model="items.subSectionTitle"
                                :items="items.listSubSection"
                                :item-title="'Value'"
                                :item-value="'Id'"
                                :disabled="
                                  !items.tahapan ||
                                  !items.documentName ||
                                  !items.sectionTitle
                                "
                                clearable
                                @click:clear="items.subSectionTitle = null"
                                @update:modelValue="
                                  handleSubSectionChangeOutput(
                                    $event,
                                    idx,
                                    index
                                  )
                                "
                              ></v-autocomplete>
                              <div class="d-flex pl-2" :style="{ gap: '10px' }">
                                <v-btn
                                  v-if="
                                    items.isDelete &&
                                    item.outputMappings.length > 1
                                  "
                                  class="rounded-lg"
                                  min-width="0"
                                  height="55"
                                  width="55"
                                  @click="item.outputMappings.splice(index, 1)"
                                >
                                  <v-icon icon="mdi-delete" color="red"></v-icon
                                ></v-btn>
                                <v-btn
                                  v-if="
                                    index === item.outputMappings.length - 1
                                  "
                                  class="p-2 primary-gradient rounded-lg btn-icon"
                                  height="55"
                                  width="55"
                                  :disabled="
                                    !items.tahapan || !items.sectionTitle
                                  "
                                  @click="handleAddOutputMapping(idx)"
                                >
                                  <v-icon icon="mdi-plus"></v-icon>
                                </v-btn>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- <item-output-stp
                      :item="item.outputMappings"
                      :item-all="item"
                      :is-edit-mode="item.isEdited"
                      :is-eform-source="item.idEformSource"
                      @add-output-mapping="handleAddOutputMapping(idx)"
                      @remove-output-mapping="
                        item.outputMappings.splice($event, 1)
                      "
                    /> -->
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
                            formTempInputGroup[idx].outputMappings.some(
                              (output) =>
                                !output.documentName ||
                                !output.tahapan ||
                                !output.sectionTitle
                            )
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
                  @click="handleAddMapping('add', 0, 0)"
                >
                  + Add Mapping
                </v-btn>
              </div>
            </v-form>
            <div class="my-5">
              <p class="font-weight-regular">
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
        <div
          v-if="!formTempInputGroup.length && !isLoading"
          class="text-center mb-10"
        >
          <v-btn
            class="rounded-lg px-2 font-weight-bold"
            min-width="0"
            color="#065695"
            variant="outlined"
            @click="handleAddMapping('new', 0, 0)"
          >
            + Add Mapping
          </v-btn>
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
import ItemOutputStp from "./ItemOutputStp.vue";
import ItemInputStp from "./ItemInputStp.vue";
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
let ListSubSection = ref<{ Value: any; Id: any }[]>([]);
let ListOutputSubsection = ref<{ Value: any; Id: any }[]>([]);
let ListSection = ref<{ name: any; idSection: any }[]>([]);
let ListTahapan = ref<any[]>([]);
const instance = ref<any>(getCurrentInstance()?.root.refs);
let ListContent = ref<any[]>([]);
const items = ref<TDetailSubmit[]>([]);
const listIdEform = ref<string[]>([]);
const selectAll = ref(false);
const isAppend = ref(false);
const defaultFormData = ref({
  idEformSource: null,
  isEdited: true,
  idSubSection: null,
  isDelete: true,
  subSectionTitle: null,
  sectionTitle: null,
  listSection: [],
  listSubSection: [],
  idSection: null,
  IdEformSourceOriginal: null,
  outputMappings: [
    {
      documentName: null,
      isDelete: true,
      isEdited: true,
      tahapan: null,
      sectionTitle: null,
      subSectionTitle: null,
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
    },
  ],
});

const emit = defineEmits<{
  (e: "submit", value: TListEForm): void;
  (e: "close", value: boolean): void;
}>();

function handleAddMapping(
  stat: string,
  indexInput: number,
  indexOutput: number
) {
  if (stat === "new") {
    handleNewMapping(indexInput, indexOutput);
  } else if (stat === "add") {
    handleAddMappingOnly(indexInput, indexOutput);
  }
  isEditMode.value = false;
  getTahapanList();
}

function handleSubSectionChangeInput(newValue: any, index: number) {
  if (formTempInputGroup.value[index].listSubSection.length !== 0) {
    const foundObject = formTempInputGroup.value[index].listSubSection.find(
      (item) => item.Id === newValue
    );
    if (foundObject) {
      formTempInputGroup.value[index].idSubSection = foundObject.Id;
      formTempInputGroup.value[index].subSectionTitle = foundObject.Value;
    }
  }
  // const foundObject = formTempInputGroup.value[
  //   index
  // ].listSubSection.find((item) => item.Id === newValue);
  // if (foundObject) {
  //   formTempInputGroup.value[index].idSubSection = foundObject.Id;
  // }
}

function getListSection(indexInput: number) {
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
    });
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
  store.dispatch("contentStore/mappingSection", req).then((res) => {
    isLoadingTemp.value = false;
    dialog.value = true;
  });
  clearState();
  getSubmitDetail();
  isLoadingTemp.value = false;
}
function handleSaveItemMapping(idx: number) {
  handleSaveClearItemMapping(formTempInputGroup.value[idx]);
}

function handleRefreshSaveItemMapping(idx: number) {
  formTempInputGroup.value[idx].isEdited = false;
}

function handleSaveClearItemMapping(payload: any) {
  isLoadingTemp.value = true;
  let req = {
    IdEFormSource: payload.idSubSection ?? payload.idEformSource,
    IdEformSourceOriginal: payload.idEformSource,
    IdEformDestination: [] as string[],
  };
  payload.outputMappings.map((item) => {
    req.IdEformDestination.push(item.idSubSection);
  });
  store.dispatch("contentStore/mappingSection", req).then((res) => {
    if (res.responseCode === "011002") {
      isLoadingTemp.value = false;
      instance.value.toast.show({
        message: res.responseMessage,
        color: "warning",
        timeout: 3000,
      });
    } else {
      isLoadingTemp.value = false;
      instance.value.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
        icon: "mdi-check",
      });
      clearState();
      getSubmitDetail();
      dialog.value = true;
      isLoadingTemp.value = false;
      console.log(req, res);
    }
  });
}
function handleNewMapping(indexInput: number, indexOutput: number) {
  formTempInputGroup.value = [];
  formTempOutputGroup.value = [];
  formTempOutputGroup.value.push({
    documentName: null,
    isDelete: true,
    isEdited: true,
    tahapan: null,
    sectionTitle: null,
    subSectionTitle: null,
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
  });
  formTempInputGroup.value.push({
    idEformSource: null,
    isEdited: true,
    isDelete: true,
    subSectionTitle: null,
    sectionTitle: null,
    listSection: [],
    listSubSection: [],
    outputMappings: formTempOutputGroup.value,
    idSection: null,
    idSubSection: null,
    IdEformSourceOriginal: null,
  });
  getListSection(indexInput);
}

function handleAddMappingOnly(indexInput: number, indexOutput: number) {
  formTempInputGroup.value.push({
    idEformSource: null,
    isEdited: true,
    isDelete: true,
    subSectionTitle: null,
    sectionTitle: null,
    IdEformSourceOriginal: null,
    listSection: [],
    listSubSection: [],
    outputMappings: [
      {
        documentName: null,
        isDelete: true,
        isEdited: true,
        tahapan: null,
        sectionTitle: null,
        subSectionTitle: null,
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
      },
    ],
    idSection: null,
    idSubSection: null,
  });
  getListSection(formTempInputGroup.value.length - 1);
}

function handleAddOutputMapping(idxInput: number) {
  formTempInputGroup.value[idxInput].outputMappings.push({
    documentName: null,
    isDelete: true,
    isEdited: true,
    tahapan: null,
    sectionTitle: null,
    subSectionTitle: null,
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
  });
  isEditMode.value = true;
  getTahapanList();
}

function handleClearMapping() {
  formTempInputGroup.value = [];
  formTempOutputGroup.value = [];
  items.value = [];
  isEditMode.value = false;
}
function getSubmitDetail() {
  v$.value.$reset();
  isLoading.value = true;
  const reqData = { idBpDocument: route.params.idDoc };
  store
    .dispatch("eFormStore/getSubmitDetail", reqData)
    .then((response) => {
      items.value = response.responseData;
      formTempInputGroup.value = [];
      formTempOutputGroup.value = [];

      // Populate input/output mappings from response
      if (Array.isArray(response.responseData)) {
        response.responseData.forEach((item: any) => {
          // Output mapping
          const outputMappings = Array.isArray(item.outputMappings)
            ? item.outputMappings.map((out: any) => ({
                // ...out,
                documentName: out.documentName || null,
                isDelete: out.isDelete || false,
                isEdited: false,
                tahapan: out.tahapan || null,
                sectionTitle: out.sectionTitle || null,
                subSectionTitle:
                  out.sectionTitle == out.subSectionTitle
                    ? null
                    : out.subSectionTitle,
                listTahapan: [],
                listContent: [],
                listSection: [],
                listSubSection: [],
                title: out.title || null,
                idBp: out.idBp || null,
                idBpDocument: out.idBpDocument || null,
                idBpSection: out.idBpSection || null,
                idSubSection: out.idSubSection || null,
              }))
            : [];
          formTempInputGroup.value.push({
            idEformSource: item.idEformSource || null,
            isEdited: false,
            idSubSection: item.idEformSource,
            isDelete: item.isDelete || false,
            subSectionTitle:
              item.subSectionTitle == item.sectionTitle
                ? null
                : item.subSectionTitle,
            sectionTitle: item.sectionTitle || null,
            listSection: [],
            listSubSection: [],
            idSection: item.idSection || null,
            IdEformSourceOriginal: item.IdEformSourceOriginal || null,
            outputMappings: outputMappings,
          });
          // Optionally, collect all output mappings
          // formTempOutputGroup.value.push(...outputMappings);
        });
        getTahapanList();

        response.responseData.forEach((item: any, indexInput: any) => {
          item.outputMappings.forEach((out: any, indexOutput: any) => {
            //get list content
            getListContent(out.idBp, indexInput, indexOutput);
            //get list section
            getListSectionOutput(out.idBpDocument, indexInput, indexOutput);
            // get list sub section
            getListOutputSubSection(
              out.idBpSection,
              indexInput,
              indexOutput,
              true
            );
          });
        });
      }
    })
    .finally(() => {
      isLoading.value = false;
    });
}

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
};
const v$ = useVuelidate(rules, { listIdEform });

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

watch(selectAll, (val) => {
  if (val) {
    listIdEform.value = items.value.map(
      (item: TDetailSubmit) => item.idEformSource
    );
  } else {
    listIdEform.value = [];
  }
});
watch(listIdEform, (val) => {
  selectAll.value = items.value.length > 0 && val.length === items.value.length;
});

async function submit() {
  const result = await v$.value.$validate();
  if (!result) return;
  emit("submit", { isAppend: isAppend.value, listIdEform: listIdEform.value });
}
function isValidMapping(idx: number): boolean {
  const item = formTempInputGroup.value[idx];
  if (!item) return false;

  // Validate input mapping
  if (!item.idEformSource) return false;

  // Validate output mappings
  if (!Array.isArray(item.outputMappings) || item.outputMappings.length === 0)
    return false;

  for (const output of item.outputMappings) {
    if (
      !output.documentName ||
      !output.tahapan ||
      !output.sectionTitle ||
      !output.subSectionTitle ||
      !output.title
    ) {
      return false;
    }
  }

  return true;
}

// temp wip mapping
function getTahapanList() {
  ListTahapan.value = [];
  store
    .dispatch("contentStore/getBpList", {
      idEvent: route.params.idEvent,
      idSector: store.getters["documentStore/getSectorId"],
    })
    .then((res) => {
      ListTahapan.value = Array.isArray(res)
        ? res.map((section: any) => ({
            Value: section.Value || "",
            id: section.Id || "",
          }))
        : [];
      formTempInputGroup.value.map((item) => {
        item.outputMappings.map((x) => {
          x.listTahapan = ListTahapan.value;
        });
      });
    });
}

function handleSectionChangeInput(newValue: any, index: number) {
  const foundObject: any = formTempInputGroup.value[index].listSection.find(
    (item) => item.idSection === newValue
  );
  if (foundObject) {
    formTempInputGroup.value[index].idSection = foundObject.idSection;
    formTempInputGroup.value[index].idEformSource = foundObject.idEformSource;
  }
  const tempClearSection = {
    documentName: null,
    isDelete: true,
    isEdited: true,
    tahapan: null,
    sectionTitle: null,
    subSectionTitle: null,
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
  formTempInputGroup.value[index].outputMappings = [tempClearSection];
  getListSubSectionInput(newValue, index);
}

function getListSubSectionInput(newValue, index) {
  formTempInputGroup.value[index].listSubSection = [];
  store
    .dispatch("contentStore/getBpDocSubSectionMappingList", {
      idBPSection: newValue,
      isSource: true,
    })
    .then((res) => {
      formTempInputGroup.value[index].listSubSection = Array.isArray(res)
        ? res.map((section: any) => ({
            Value: section.Value || "",
            Id: section.Id || "",
          }))
        : [];

      formTempInputGroup.value[index].subSectionTitle = null;
      getTahapanList();
      // if (formTempInputGroup.value[index].listSubSection.length === 0) {
      //   const foundObject: any = formTempInputGroup.value[
      //     index
      //   ].listSection.find((item) => item.idSection === newValue);
      //   if (foundObject) {
      //     formTempInputGroup.value[index].idSubSection =
      //       foundObject.idEformSource;
      //     formTempInputGroup.value[index].idSection = foundObject.idSection;
      //     formTempInputGroup.value[index].idEformSource =
      //       foundObject.idEformSource;
      //   }
      // }
    });
}

function handleClearTempSection(index: number) {
  formTempInputGroup.value[index] = {
    ...defaultFormData.value,
  };
  getTahapanList();
  getListSection(index);
}

function handleTahapanChange(
  value: string,
  indexInput: number,
  indexOutput: number
) {
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].documentName = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].sectionTitle = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
  getListContent(value, indexInput, indexOutput);
}

function getListContent(idTahapan: string, indexInput: number, indexOutput) {
  const payload = {
    IdEFormSource: formTempInputGroup.value[indexInput].idEformSource,
    idBP: idTahapan,
  };
  formTempInputGroup.value[indexInput].outputMappings[indexOutput].listContent =
    [];
  store.dispatch("contentStore/getBpDocMappingList", payload).then((res) => {
    formTempInputGroup.value[indexInput].outputMappings[
      indexOutput
    ].listContent = Array.isArray(res)
      ? res.map((section: any) => ({
          Value: section.Value || "",
          id: section.Id || "",
        }))
      : [];
  });
}

function handleContentChange(value: string, indexInput, indexOutput) {
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].sectionTitle = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
  getListSectionOutput(value, indexInput, indexOutput);
}

function getListSectionOutput(
  value: string,
  indexInput: number,
  indexOutput: number
) {
  formTempInputGroup.value[indexInput].outputMappings[indexOutput].listSection =
    [];
  store
    .dispatch("contentStore/getBpDocSectionMappingList", {
      idBPDoc: value,
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
  value: string,
  indexInput: number,
  indexOutput: number
) {
  if (
    formTempInputGroup.value[indexInput].outputMappings[indexOutput]
      .listSubSection.length !== 0
  ) {
    // return;
    const foundObject = formTempInputGroup.value[indexInput].outputMappings[
      indexOutput
    ].listSubSection.find((item) => item.Id === value);
    if (foundObject) {
      formTempInputGroup.value[indexInput].outputMappings[
        indexOutput
      ].idSubSection = foundObject.Id;
      formTempInputGroup.value[indexInput].outputMappings[
        indexOutput
      ].subSectionTitle = foundObject.Value;
    }
  }
}

function handleSectionOutputChange(
  value: string,
  indexInput: number,
  indexOutput: number
) {
  let tempData = value;
  const foundObject: any = formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].listSection.find((item) => item.idEformSource === value);

  if (foundObject) {
    formTempInputGroup.value[indexInput].outputMappings[
      indexOutput
    ].idBpSection = foundObject.idSection;
    formTempInputGroup.value[indexInput].outputMappings[
      indexOutput
    ].idEformSource = foundObject.idEformSource;
    tempData = foundObject.idSection;
  }
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].subSectionTitle = null;
  formTempInputGroup.value[indexInput].outputMappings[
    indexOutput
  ].idSubSection = foundObject.idEformSource;
  getListOutputSubSection(tempData, indexInput, indexOutput, false);
}

function getListOutputSubSection(
  idSection: any,
  indexInput: number,
  indexOutput: number,
  isEdit: boolean
) {
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

      if (!isEdit) {
        formTempInputGroup.value[indexInput].outputMappings[
          indexOutput
        ].subSectionTitle = null;
      }
      // if (
      //   formTempInputGroup.value[indexInput].outputMappings[indexOutput]
      //     .listSubSection.length === 0
      // ) {
      //   const foundObject: any = formTempInputGroup.value[
      //     indexInput
      //   ].outputMappings[indexOutput].listSection.find(
      //     (item) => item.idSection === idSection
      //   );
      //   if (foundObject) {
      //     formTempInputGroup.value[indexInput].outputMappings[
      //       indexOutput
      //     ].idSubSection = foundObject.idEformSource;

      //     formTempInputGroup.value[indexInput].outputMappings[
      //       indexOutput
      //     ].idBpSection = foundObject.idSection;

      //     formTempInputGroup.value[indexInput].outputMappings[
      //       indexOutput
      //     ].idEformSource = foundObject.idEformSource;
      //   }
      // }
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
</style>
