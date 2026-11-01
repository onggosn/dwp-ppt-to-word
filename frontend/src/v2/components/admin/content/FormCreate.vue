<template>
  <v-btn
    prepend-icon="mdi-plus"
    class="bg-gradient-darkblue font-weight-bold"
    elevation="4"
    style="color: white; border-radius: 10px"
    @click="onOpen()"
  >
    Add Content
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="1000" persistent>
      <v-card class="border-radius-dwp">
        <v-card-title class="text-center mt-3">
          <h3 class="text-h6 font-weight-regular">Add Content</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onClose()"
          />
        </v-card-title>
        <hr class="line mt-3" />
        <v-form ref="form">
          <Steppy
            v-model:step="step"
            nextText="Next"
            backText="Back"
            doneText="Create"
            :tabs="tabs"
          >
            <template #1>
              <v-row no-gutters>
                <v-col :cols="12" class="mb-2">
                  <p class="pb-3 text-left text-darkBlue font-weight-bold">
                    Event Type<span class="text-redTheme">*</span>
                  </p>
                  <v-autocomplete
                    v-model="formInput.event_type"
                    :loading="store.getters['eventStore/getLoading']"
                    :items="formList.event_types"
                    variant="solo"
                    placeholder="Choose Event Type"
                    class="mb-3"
                    item-value="id"
                    item-title="value"
                    :hide-details="isError(v$.event_type)"
                    :error-messages="
                      getErrorMessages(v$.event_type, {
                        required: 'Required',
                      })
                    "
                  ></v-autocomplete>

                  <v-autocomplete
                    v-if="formInput.event_type"
                    v-model="formInput.rdg_type"
                    :loading="store.getters['eventStore/getLoading']"
                    :items="formList.rdg_types"
                    variant="solo"
                    placeholder="Choose RDG Type"
                    class="mb-3"
                    item-value="id"
                    item-title="value"
                    :hide-details="isError(v$.rdg_type)"
                    :error-messages="
                      getErrorMessages(v$.rdg_type, {
                        required: 'Required',
                      })
                    "
                  ></v-autocomplete>

                  <v-autocomplete
                    v-if="formInput.rdg_type"
                    v-model="formInput.sector"
                    :loading="store.getters['eventStore/getLoading']"
                    :items="formList.sectors"
                    variant="solo"
                    placeholder="Choose Sector"
                    class="mb-3"
                    item-value="idMSector"
                    item-title="sectorName"
                    :hide-details="isError(v$.sector)"
                    :error-messages="
                      getErrorMessages(v$.sector, {
                        required: 'Required',
                      })
                    "
                  ></v-autocomplete>

                  <v-autocomplete
                    v-if="formInput.sector"
                    v-model="formInput.stage"
                    :loading="store.getters['eventStore/getLoading']"
                    :items="formList.stages"
                    variant="solo"
                    placeholder="Choose Stage"
                    class="mb-3"
                    item-value="id"
                    item-title="value"
                    return-object
                    :hide-details="isError(v$.stage)"
                    :error-messages="
                      getErrorMessages(v$.stage, {
                        required: 'Required',
                      })
                    "
                  ></v-autocomplete>
                </v-col>

                <v-col :cols="12" class="mb-2">
                  <p class="pb-3 text-left text-darkBlue font-weight-bold">
                    Content Type<span class="text-redTheme">*</span>
                  </p>
                  <v-autocomplete
                    v-model="formInput.content_type"
                    :items="formList.content_types"
                    variant="solo"
                    placeholder="Choose Event Type"
                    class="mb-3"
                    item-value="id"
                    item-title="descriptions"
                    return-object
                    :hide-details="isError(v$.content_type)"
                    :error-messages="
                      getErrorMessages(v$.content_type, {
                        required: 'Required',
                      })
                    "
                  ></v-autocomplete>
                </v-col>

                <v-col :cols="12" class="mb-2" v-if="formInput.stage">
                  <p class="pb-3 text-left text-darkBlue font-weight-bold">
                    Content Title<span class="text-redTheme">*</span>
                  </p>
                  <v-text-field
                    v-if="isCase1"
                    v-model="formInput.content_title"
                    autocomplete="off"
                    variant="solo"
                    placeholder="Content Name"
                    class="my-input"
                    single-line
                    :hide-details="isError(v$.content_title)"
                    :error-messages="
                      getErrorMessages(v$.content_title, {
                        required: 'Required',
                      })
                    "
                  ></v-text-field>
                  <v-row v-else-if="isCase3">
                    <v-col :cols="4">
                      <v-text-field
                        v-model="formInput.content_title_satker"
                        autocomplete="off"
                        variant="solo"
                        placeholder="Satker"
                        class="my-input"
                        single-line
                        :hide-details="isError(v$.content_title_satker)"
                        :error-messages="
                          getErrorMessages(v$.content_title_satker, {
                            required: 'Required',
                          })
                        "
                      ></v-text-field>
                    </v-col>
                    <v-col :cols="8">
                      <v-text-field
                        v-model="formInput.content_title_document"
                        autocomplete="off"
                        variant="solo"
                        placeholder="Document Name"
                        class="my-input"
                        single-line
                        :hide-details="isError(v$.content_title_document)"
                        :error-messages="
                          getErrorMessages(v$.content_title_document, {
                            required: 'Required',
                          })
                        "
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row v-else>
                    <v-col :cols="4">
                      <v-text-field
                        v-model="formInput.content_title_satker"
                        autocomplete="off"
                        variant="solo"
                        placeholder="Satker"
                        class="my-input"
                        single-line
                        :hide-details="isError(v$.content_title_satker)"
                        :error-messages="
                          getErrorMessages(v$.content_title_satker, {
                            required: 'Required',
                          })
                        "
                      ></v-text-field>
                    </v-col>
                    <v-col :cols="4">
                      <v-text-field
                        v-model="formInput.content_title_number"
                        autocomplete="off"
                        variant="solo"
                        placeholder="Document Number (Optional)"
                        class="my-input"
                        single-line
                        :hide-details="isError(v$.content_title_number)"
                        :error-messages="
                          getErrorMessages(v$.content_title_number, {
                            required: 'Required',
                          })
                        "
                      ></v-text-field>
                    </v-col>
                    <v-col :cols="4">
                      <v-text-field
                        v-model="formInput.content_title_document"
                        autocomplete="off"
                        variant="solo"
                        placeholder="Document Name"
                        class="my-input"
                        single-line
                        :hide-details="isError(v$.content_title_document)"
                        :error-messages="
                          getErrorMessages(v$.content_title_document, {
                            required: 'Required',
                          })
                        "
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <p
                    class="pa-3 mt-2 mb-5 text-left"
                    style="background-color: #e9f5ff; border-radius: 15px"
                  >
                    Content Title : {{ contentTitleValue }}
                  </p>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is this content calculated in the executive summary?<span
                      class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.executive_summary"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Can this content be submitted to STP without approval?<span
                      class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.stp_with_out_approval"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="!canSubmit"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="0"
                      color="#267DC2"
                      :disabled="!canSubmit"
                    ></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Will this content be golden copy?<span class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.golden_copy"
                  >
                    <v-radio
                      label="Yes"
                      :value="goldenCopy ? 0 : 1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="!goldenCopy"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="goldenCopy ? 1 : 0"
                      color="#267DC2"
                      :disabled="!goldenCopy"
                    ></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="" v-if="isCase2">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Will this content be an automatic AIU?<span
                      class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    style="margin-left: -8px"
                    v-model="formInput.automatic_aiu"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is the title visible?<span class="text-redTheme">*</span>
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.title_visible"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col
                  :cols="12"
                  class="mb-2"
                  v-if="formInput.title_visible == 1"
                >
                  <v-textarea
                    v-model="formInput.title_visible_text"
                    autocomplete="off"
                    variant="solo"
                    placeholder="Input title here"
                    class="my-input"
                    single-line
                    :rows="2"
                    :hide-details="isError(v$.title_visible_text)"
                    :error-messages="
                      getErrorMessages(v$.title_visible_text, {
                        required: 'Required',
                      })
                    "
                  ></v-textarea>
                </v-col>

                <v-col :cols="12" class="mt-5">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is it possible to export to Word?
                    <span class="text-redTheme">*</span>
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.export_word"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="mt-5">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is a revision workflow needed for this document?
                    <span class="text-redTheme">*</span>
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.revision_workflow"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                    ></v-radio>
                    <v-radio label="No" :value="0" color="#267DC2"></v-radio>
                  </v-radio-group>
                </v-col>

                <v-col :cols="12" class="mt-5">
                  <p class="text-left text-darkBlue font-weight-bold">
                    Is it possible to Import PPT?<span class="text-redTheme"
                      >*</span
                    >
                  </p>
                  <v-radio-group
                    inline
                    hide-details
                    style="margin-left: -8px"
                    v-model="formInput.import_ppt"
                    :disabled="canImportPPT"
                  >
                    <v-radio
                      label="Yes"
                      :value="1"
                      color="#267DC2"
                      class="me-5"
                      :disabled="canImportPPT"
                    ></v-radio>
                    <v-radio
                      label="No"
                      :value="0"
                      color="#267DC2"
                      :disabled="canImportPPT"
                    ></v-radio>
                  </v-radio-group>
                </v-col>
              </v-row>
            </template>
            <template #2>
              <v-row no-gutters>
                <v-col :cols="12" class="mb-2">
                  <p class="pb-3 text-left text-darkBlue font-weight-bold">
                    Penyusun<span class="text-redTheme">*</span>
                  </p>
                  <v-autocomplete
                    v-model="formInput.penyusuns"
                    v-model:search="searchPenyusun"
                    :items="formList.penyusuns"
                    variant="solo"
                    placeholder="Input penyusun here"
                    item-value="id"
                    item-title="value"
                    clear-on-select
                    return-object
                    chips
                    multiple
                    closable-chips
                    hide-selected
                    searchable
                    :hide-details="isError(v$.penyusuns)"
                    :error-messages="
                      getErrorMessages(v$.penyusuns, {
                        required: 'Penyusun must be filled at least one',
                      })
                    "
                    @update:modelValue="() => (searchPenyusun = '')"
                  ></v-autocomplete>
                </v-col>
              </v-row>
            </template>
            <template #3>
              <v-row class="mb-3">
                <v-col class="px-4">
                  <div
                    class="rounded-lg pa-4"
                    style="border: 2px #babcca solid"
                  >
                    <p class="text-darkBlue font-weight-bold form-title mb-2">
                      {{ contentTitleValue }}
                    </p>
                    <v-row v-for="(item, i) in formInput.sections" :key="i">
                      <v-col class="d-flex flex-justify-between">
                        <div style="width: 90%">
                          <div
                            class="rounded-lg px-2 py-4 mt-2 mx-2"
                            style="border: 2px #babcca solid"
                          >
                            <v-row class="mx-1">
                              <v-col :cols="12">
                                <p class="text-darkBlue font-weight-bold mb-2">
                                  Section Title<span class="text-redTheme"
                                    >*</span
                                  >
                                </p>
                                <v-text-field
                                  v-model="formInput.sections[i].title"
                                  autocomplete="off"
                                  variant="solo"
                                  placeholder="Insert section title"
                                  class="my-input"
                                  single-line
                                  :hide-details="
                                    !hasNestedError(
                                      v$.sections,
                                      v$.sections.$each.$response.$errors[i]
                                        .title
                                    )
                                  "
                                  :error-messages="
                                    getNestedErrorMessage(
                                      v$.sections,
                                      v$.sections.$each.$response.$errors[i]
                                        .title,
                                      {
                                        required: 'Required',
                                        sectionRegex:
                                          'Section title cannot contain semicolon (;)',
                                      }
                                    )
                                  "
                                ></v-text-field>
                              </v-col>
                              <v-col
                                :cols="12"
                                class=""
                                v-if="formInput.content_type.id == 8"
                              >
                                <p
                                  class="text-left text-darkBlue font-weight-bold"
                                >
                                  Sector<span class="text-redTheme">*</span>
                                </p>
                                <v-radio-group
                                  inline
                                  style="margin-left: -8px"
                                  v-model="formInput.sections[i].sector"
                                  :hide-details="
                                    !hasNestedError(
                                      v$.sections,
                                      v$.sections.$each.$response.$errors[i]
                                        .sector
                                    )
                                  "
                                  :error-messages="
                                    getNestedErrorMessage(
                                      v$.sections,
                                      v$.sections.$each.$response.$errors[i]
                                        .sector,
                                      {
                                        required: 'Required',
                                      }
                                    )
                                  "
                                >
                                  <v-radio
                                    v-for="(
                                      item, i
                                    ) in formList.sector_predifined"
                                    :key="i"
                                    :value="item.id"
                                    :label="item.value"
                                    color="#267DC2"
                                    class="me-5"
                                  ></v-radio>
                                </v-radio-group>
                              </v-col>
                              <v-col :cols="12" class="">
                                <p
                                  class="text-left text-darkBlue font-weight-bold"
                                >
                                  Do you want to make it as a header?<span
                                    class="text-redTheme"
                                    >*</span
                                  >
                                </p>
                                <v-radio-group
                                  inline
                                  style="margin-left: -8px"
                                  v-model="formInput.sections[i].isHeader"
                                  :hide-details="
                                    !hasNestedError(
                                      v$.sections,
                                      v$.sections.$each.$response.$errors[i]
                                        .isHeader
                                    )
                                  "
                                  :error-messages="
                                    getNestedErrorMessage(
                                      v$.sections,
                                      v$.sections.$each.$response.$errors[i]
                                        .isHeader,
                                      {
                                        required: 'Required',
                                      }
                                    )
                                  "
                                >
                                  <v-radio
                                    label="Yes"
                                    :value="1"
                                    color="#267DC2"
                                    class="me-5"
                                  ></v-radio>
                                  <v-radio
                                    label="No"
                                    :value="0"
                                    color="#267DC2"
                                  ></v-radio>
                                </v-radio-group>
                              </v-col>
                            </v-row>
                          </div>
                        </div>
                        <div class="align-self-center">
                          <div
                            v-if="i != formInput.sections.length - 1"
                            :style="{ display: 'flex', gap: '10px' }"
                          >
                            <v-btn
                              class="rounded-lg px-2"
                              min-width="0"
                              @click="deleteSection(i)"
                            >
                              <v-icon icon="mdi-delete" color="#CB3A31"></v-icon
                            ></v-btn>
                          </div>
                          <div v-else :style="{ display: 'flex', gap: '10px' }">
                            <v-btn
                              v-if="formInput.sections.length != 1"
                              class="rounded-lg px-2"
                              min-width="0"
                              @click="deleteSection(i)"
                            >
                              <v-icon icon="mdi-delete" color="#CB3A31"></v-icon
                            ></v-btn>
                            <v-btn
                              class="primary-gradient rounded-lg px-2"
                              min-width="0"
                              @click="addSection"
                            >
                              <v-icon icon="mdi-plus"></v-icon
                            ></v-btn>
                          </div>
                        </div>
                      </v-col>
                    </v-row>
                  </div>
                </v-col>
              </v-row>
            </template>
          </Steppy>
          <div class="text-right pb-5 pr-12 mt-n10">
            <v-btn
              class="btn-prev mr-3"
              @click="negativeClick"
              elevation="4"
              width="100"
              height="45"
            >
              {{ step == 1 ? "Cancel" : "Back" }}
            </v-btn>
            <v-btn
              class="btn-next"
              @click="positiveClick"
              elevation="4"
              width="100"
              height="45"
            >
              {{ isLastStep ? "Create" : "Next" }}
            </v-btn>
          </div>
        </v-form>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import { Steppy } from "vue3-steppy";
import {
  computed,
  getCurrentInstance,
  onMounted,
  reactive,
  ref,
  watch,
} from "vue";
import { useVuelidate } from "@vuelidate/core";
import { helpers, required, requiredIf } from "@vuelidate/validators";
import {
  getErrorMessages,
  isError,
  getNestedErrorMessage,
  hasNestedError,
} from "@v2/helpers/validation";
import { useStore } from "vuex";
import { TSelect } from "@/v2/Type";
import { sharePointRegex } from "../../../helpers/validation";
import { Stage } from "@/v2/enum/Enum";
import clientv2 from "@v2/library/ApiClient";
const store = useStore();
const emit = defineEmits(["onSuccess"]);
const instance: any = getCurrentInstance()?.root.refs;

const dialog = ref(false);
const step = ref(1);
const searchPenyusun = ref<string | null>(null);
const sectionRegex = helpers.regex(/^[^;]*$/);
const goldenCopy = ref(false);
const canSubmit = ref<boolean>(true);
const canImportPPT = ref<boolean>(false);
const tabs = reactive([
  {
    title: "Step 1",
    iconSuccess: null,
    isValid: true,
  },
  {
    title: "Step 2",
    iconSuccess: null,
    isValid: true,
  },
  {
    title: "Step 3",
    iconSuccess: null,
    isValid: true,
  },
]);
const formList = ref({
  event_types: [],
  rdg_types: [],
  sectors: [],
  stages: [],
  content_types: [],

  penyusuns: [],

  sector_predifined: [] as TSelect[],
});
const formInput = ref<any>({
  event_type: null,
  rdg_type: null,
  sector: null,
  stage: null,
  content_type: null,
  content_title: null,
  content_title_satker: null,
  content_title_number: null,
  content_title_document: null,

  executive_summary: 0,
  stp_with_out_approval: 0,
  golden_copy: 0,
  automatic_aiu: 0,
  title_visible: 0,
  export_word: 0,
  revision_workflow: 0,
  import_ppt: 0,
  title_visible_text: "",

  penyusuns: [],
  sections: [
    {
      title: null,
      sector: null,
      isHeader: null,
    },
  ],
});

// stage is kbku dan rdgb
const isCase1 = computed((): boolean => {
  const input = formInput.value.stage ?? { id: 0 };
  return [
    0, 8, 9, 20, 21, 32, 33, 56, 57, 64, 70, 71, 72, 73, 83, 84, 93, 74,
  ].includes(input.id);
});

// stage is aiu
const isCase2 = computed((): boolean => {
  const input = formInput.value.stage ?? { id: 0 };
  return [10, 22, 34].includes(input.id);
});

const isCase3 = computed((): boolean => {
  const input = formInput.value.stage ?? { id: 0 };
  return [
    Stage.RakorRispatBulanan,
    Stage.RakorRispatMingguan,
    Stage.RakorRispatTriwulanan,
  ].includes(input.id);
});

const isLastStep = computed((): boolean => step.value == tabs.length);

const rules = computed(() => {
  return {
    event_type: { required },
    rdg_type: { required },
    sector: { required },
    stage: { required },
    content_type: { required },
    content_title: {
      required: requiredIf(isCase1.value),
      sharePointRegex: sharePointRegex,
    },

    content_title_satker: {
      required: requiredIf(!isCase1.value),
      sharePointRegex: sharePointRegex,
    },
    content_title_number: {
      sharePointRegex: sharePointRegex,
    },
    content_title_document: {
      required: requiredIf(!isCase1.value),
      sharePointRegex: sharePointRegex,
    },

    title_visible_text: {
      required: requiredIf(() => formInput.value.title_visible == 1),
    },

    penyusuns: {
      required: requiredIf(() => step.value == 2),
    },
    sections: {
      $each: helpers.forEach({
        title: {
          required: requiredIf(() => step.value == 3),
          sectionRegex: sectionRegex,
        },
        isHeader: {
          required: requiredIf(() => step.value == 3),
        },
        sector: {
          required: requiredIf(
            () => step.value == 3 && formInput.value.content_type.id == 8
          ),
        },
      }),
    },
  };
});
const v$ = useVuelidate(rules, formInput);

const contentTitleValue = computed((): string => {
  const stageValue = formInput.value.stage?.value ?? "";
  const rdgTypeId = formInput.value.rdg_type;
  const rdgMorB = rdgTypeId == 6 ? "M Laporan" : "B";

  const resolvedStage = (() => {
    if (stageValue === "RDG") {
      return rdgTypeId === 4 ? "RDGTK" : `${stageValue}${rdgMorB}`;
    }

    if (stageValue === "Publikasi") {
      return rdgTypeId === 4 ? "Buku LKBI" : "RDGB";
    }

    if (stageValue === "Joint Committee") {
      return "Komite Gabungan KBKK-KMSO-KMSK-KIBD-KMAF-KKPR";
    }

    return stageValue;
  })();

  const title = formInput.value.content_title ?? "";
  const satker = formInput.value.content_title_satker ?? "";
  const doc = formInput.value.content_title_document ?? "";

  if (isCase1.value)
    return resolvedStage === "Buku LKBI"
      ? title
      : `${resolvedStage}_*date*_` + title;
  const no = formInput.value.content_title_number
    ? `_${formInput.value.content_title_number}`
    : "";
  if (isCase3.value)
    return `
    ${satker}_*date*${no}_${doc}
  `;
  return `
    ${satker} ${resolvedStage}_*date*${no}_${doc}
  `;
});

function onOpen() {
  formInput.value = {
    event_type: null,
    rdg_type: null,
    sector: null,
    stage: null,
    content_type: null,
    content_title: null,
    content_title_satker: "",
    content_title_number: "",
    content_title_document: "",

    executive_summary: 0,
    stp_with_out_approval: 0,
    golden_copy: 0,
    automatic_aiu: 0,
    title_visible: 0,
    title_visible_text: "",
    export_word: 0,
    revision_workflow: 0,
    import_ppt: 0,

    penyusuns: [],
    sections: [
      {
        title: null,
        sector: null,
        isHeader: null,
      },
    ],
  };
  step.value = 1;
  v$.value.$reset();
  dialog.value = true;
}

watch(
  [() => formInput.value.stage, () => formInput.value.content_type],
  ([stageVal, contentTypeVal]) => {
    let stage = stageVal?.isGoldenCopy ?? false;
    let contentType = contentTypeVal?.isGoldenCopy ?? false;
    if (stage) {
      if (contentType) {
        goldenCopy.value = true;
      } else {
        goldenCopy.value = false;
      }
    } else {
      goldenCopy.value = false;
    }
    //submit to stp without approval
    canSubmit.value = contentTypeVal?.enabledSubmit ?? true;
    formInput.value.stp_with_out_approval = contentTypeVal?.isSubmit ? 1 : 0;
    //import ppt
    canImportPPT.value =
      contentTypeVal?.isDisableChangeImportPPTStatus ?? false;
    formInput.value.import_ppt = canImportPPT.value ? 1 : 0;
  }
);

function onClose() {
  dialog.value = false;
}

function negativeClick() {
  if (step.value > 1) {
    step.value--;
  } else {
    onClose();
  }
}

function positiveClick() {
  v$.value.$validate().then((res) => {
    if (res) {
      if (step.value < tabs.length) {
        step.value++;
        v$.value.$reset();
      } else {
        const req = {
          documentName: contentTitleValue.value.trim(),
          idMEventSubType: formInput.value.event_type,
          idMEventSubTypeList: formInput.value.rdg_type,
          idSector: formInput.value.sector,
          idMBPTemplate: formInput.value.stage?.id,
          isExecutiveSummary: formInput.value.executive_summary == 1,
          isSubmit: formInput.value.stp_with_out_approval == 1,
          isGoldenCopy: goldenCopy.value
            ? formInput.value.golden_copy == 0
            : formInput.value.golden_copy == 1,
          isAIUotomatis: formInput.value.automatic_aiu == 1,
          isVisibleTitle: formInput.value.title_visible == 1,
          isExportToWord: formInput.value.export_word == 1,
          isRevision: formInput.value.revision_workflow == 1,
          isImportPPT: formInput.value.import_ppt == 1,
          contentType: formInput.value.content_type?.id,
          title: formInput.value.title_visible
            ? formInput.value.title_visible_text.replaceAll(/\n/g, "<br />")
            : null,
          section: formInput.value.sections.map((r: any, i: number) => {
            return {
              order: i,
              sectionName: r.title,
              idMSector: r.sector,
              isHeader: r.isHeader == 1,
            };
          }),
          penyusun: formInput.value.penyusuns.map((r: any, i: number) => {
            return {
              order: i,
              userId: r.id,
              isEditor: true,
              isViewer: true,
              isGroup: r.isGroup,
            };
          }),
        };
        store
          .dispatch("adminStore/storeContentPreDefine", req)
          .then(({ responseMessage }) => {
            instance.toast.show({
              message: responseMessage,
              color: "success",
              timeout: 3000,
            });
            onClose();
            emit("onSuccess", true);
          })
          .catch((error) => {
            instance.toast.show({
              message:
                error.response.data.responseMessage ?? "internal server error",
              color: "warning",
              timeout: 3000,
            });
          });
      }
    }
  });
}

function fetchEventType() {
  store.dispatch("eventStore/fetchListSubEventType", 1).then((data) => {
    formList.value.event_types = data;
  });
}

function fetchSubEventType(id: number) {
  store.dispatch("eventStore/fetchListSubSubEventType", id).then((data) => {
    formList.value.rdg_types = data;
  });
}

function fetchSectors(id: number) {
  const formData = {
    idMEventSubTypeList: id,
  };
  store
    .dispatch("adminStore/getListSector", formData)
    .then(({ responseData }) => {
      formList.value.sectors = responseData;
    });
}

function fetchPenyusun(query: string) {
  if (query.length > 2) {
    const trimmedSearch = query
      .replace(/"/g, "")
      .split(";")
      .map((part) => {
        if (part.trim() === "") return; // Skip empty parts
        const regex = /<[^>]*@[^>]*>/;
        const matchingMail = part.match(regex);
        if (matchingMail !== null) {
          return matchingMail[0].slice(1, -1);
        } else {
          return part.trim();
        }
      })
      .filter((v): v is string => !!v);

    const reqData = {
      name: trimmedSearch.length > 0 ? trimmedSearch : query,
      type: "Page",
    };

    clientv2
      .SearchUserAndGrupIdByNameAndSector({ data: reqData })
      .then((res) => {
        formList.value.penyusuns = [...(res as Array<never>)];
        searchPenyusun.value?.includes(";") &&
          res.length &&
          (formInput.value.penyusuns = [...(res as Array<never>)]);
        searchPenyusun.value?.includes(";") &&
          res.length &&
          (searchPenyusun.value = ""); // Clear the search input after getting results
      });
  }
}

function fetchContentType(id: number) {
  store
    .dispatch("documentStore/getDocumentTypeListByUsername", {
      idMEventSubTypeList: formInput.value.rdg_type,
      idMSector: formInput.value.sector,
      idMBPTemplate: id,
    })
    .then(({ responseData }) => {
      formList.value.content_types = responseData;
    });
}

function fetchStage(id: number) {
  store
    .dispatch("eFormStore/getMBPTemplate", {
      idMEventSubTypeList: formInput.value.rdg_type,
      idMSector: id,
    })
    .then(({ responseData }) => {
      formList.value.stages = responseData;
    });
}

function fetchSectorPredifine() {
  store
    .dispatch("eFormStore/getListSectorPredefine")
    .then(({ responseData }) => {
      formList.value.sector_predifined = responseData;
    });
}

function addSection() {
  formInput.value.sections.push({
    title: null,
    sector: null,
    isHeader: null,
  });
}

function deleteSection(index: number) {
  formInput.value.sections.splice(index, 1);
}

defineExpose({
  onOpen,
});

onMounted(() => {
  fetchEventType();
});

watch(
  () => step.value,
  (val) => {
    if (val === 2) {
      fetchPenyusun("a");
    }
    if (val === 3) {
      fetchSectorPredifine();
    }
  },
  { immediate: false }
);
watch(
  () => formInput.value.event_type,
  (val: any) => {
    formInput.value.rdg_type = null;
    formInput.value.sector = null;
    formInput.value.stage = null;

    formList.value.rdg_types = [];
    formList.value.stages = [];

    if (val) fetchSubEventType(val);
  }
);

watch(
  () => formInput.value.rdg_type,
  (val: any) => {
    formInput.value.sector = null;
    formInput.value.stage = null;

    formList.value.stages = [];

    if (val) fetchSectors(val);
  }
);

watch(
  () => formInput.value.sector,
  (val) => {
    formInput.value.stage = null;
    if (val) fetchStage(val);
  }
);

watch(
  () => formInput.value.stage,
  (val) => {
    formInput.value.content_type = null;
    if (val?.id) fetchContentType(val.id);
  }
);

watch(
  () => searchPenyusun.value,
  (val) => {
    fetchPenyusun(val as string);
  }
);
</script>

<style lang="scss" scoped>
.error-border {
  border: 1px solid #b13737 !important;
}

.btn-section {
  padding: 10px;
  border-radius: 10px;
}

.bg-blue-gradient {
  background: linear-gradient(#065695 -46.47%, #267dc2 157.9%);
}

:deep(.dp__overlay) {
  border-radius: 10px;
}
:deep(.dp__instance_calendar) {
  box-shadow: 1px 1px 7px 3px #7393b3;
  border-radius: 5px;
  padding: 10px;
}

:deep(.dp__overlay_cell_disabled) {
  display: none;
}

:deep(.dp__arrow_top) {
  display: none;
}
:deep(.dp__input_icon_pad) {
  background: white;
  border-radius: 12px;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 5.5vh;
}

.chip-shadow {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 94%;
  color: grey;
  font-size: 16px;
}

.red-color {
  color: red;
}

:deep(.v-chip__append) {
  position: absolute;
  right: 0;
  margin-right: 0.5vw;
}
.gradient-box {
  display: flex;
  align-items: center;
  margin: auto;

  position: relative;
  box-sizing: border-box;

  $border: 2px;
  background: #fff;
  background-clip: padding-box; /* !important */
  border: solid $border transparent; /* !important */
  border-radius: 15px;

  &:before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -1;
    margin: -$border; /* !important */
    border-radius: inherit; /* !important */
    background: linear-gradient(to right, #267dc2, #ff000d);
  }
}

.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  border: none; /* Remove the default border */
  min-height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

:deep(.v-field.v-field--appended) {
  border-radius: 12px !important;
}

:deep(.steppy) {
  margin-left: 35%;
  margin-right: 35%;
}
:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding-left: 20px !important;
  padding-bottom: 0px !important;
  padding-right: 20px !important;
  padding-top: 25px;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  text-align: left;
}
:deep(.steppy-item.success .steppy-item-counter) {
  border: 8px solid #267dc2 !important;
}

:deep(.steppy-item-counter) {
  height: 20px !important;
  width: 20px !important;
  border: 5px solid grey !important;
  background-color: white !important;
}

:deep(.steppy-item.success .steppy-item-counter .icon-success) {
  width: 15px !important;
  height: 15px !important;
  fill: white !important;
  background-color: #267dc2 !important;
  border-radius: 50% !important;
}

:deep(.steppy-item-title) {
  font-size: 14px !important;
  font-weight: 900 !important;
  color: #3a416f !important;
  white-space: nowrap !important;
}

:deep(.steppy-progress) {
  background: #d9d9d9 !important;
  height: 3px !important;
}

:deep(.steppy-progress-bar) {
  background: #267dc2 !important;
  height: 3px !important;
}
:deep(.controls) {
  display: none !important;
}

:deep(.v-field--error) {
  border: 1px solid #b13737 !important;
}
:deep(.v-messages__message) {
  line-height: 12px;
  word-break: break-word;
  overflow-wrap: break-word;
  word-wrap: break-word;
  -webkit-hyphens: auto;
  hyphens: auto;
  transition-duration: 154ms;
  font-size: 13px;
  font-style: normal;
  font-weight: 600;
  font-family: Poppins;
}
.btn-next {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px !important;
  border-color: #267dc2 !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: white;
  font-weight: 900;
}

.btn-prev {
  background: white;
  border-radius: 10px !important;
  /* border-color: #267dc2 !important; */
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;

  color: #267dc2;
  font-weight: 900;
}
.hide {
  display: none;
}

.show {
  display: show;
}

.form-title {
  margin-top: -28px;
  margin-left: 8px;
  background-color: white;
  width: fit-content;
}

:deep(.v-chip.v-chip--density-default.chip-shadow) {
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
  height: 56px;
  width: 98%;
  color: grey !important;
  border: none;
  background: #dfdfdf;
  font-size: 16px;
  margin: 10px;
}

:deep(.v-chip.v-chip--density-default) {
  height: calc(var(--v-chip-height) + 0px);
  border-radius: 5px;
  background: #e9f5ff;
  border: 1px solid #6eb3ea;
  color: #065391;
  padding: 10px;
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>
