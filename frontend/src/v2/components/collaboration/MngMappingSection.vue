<template>
  <v-btn
    size="small"
    variant="outlined"
    style="border-radius: 10px"
    prepend-icon="mdi-share-variant"
    class="mr-2"
    color="#065695"
    @click="openDialog"
    :disabled="!buttonState || isApprovalInProgress"
  >
    Mapping
  </v-btn>
  <!-- <v-btn
    size="small"
    style="border-radius: 10px"
    prepend-icon="mdi-share-variant"
    class="mr-2 fw-800"
    color="red"
    icon="mdi-information"
  ></v-btn> -->
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="800" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            Manage Mapping
          </div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="closeDialog"
          ></v-btn>
        </v-card-title>
        <div class="separatorHorizontalGradient"></div>
        <v-card-text>
          <v-row
            class="rounded-lg px-1 py-2 mt-2"
            style="border: 2px #babcca solid"
          >
            <p class="text-darkBlue font-weight-bold form-title">
              {{ formRequest.bpName }}
            </p>
            <v-col :cols="12">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">Input</p>
              <v-text-field
                disabled
                variant="solo"
                v-model="formRequest.input"
                :hide-details="true"
              ></v-text-field>
            </v-col>
            <v-col :cols="12">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">
                Section
              </p>
              <v-text-field
                disabled
                variant="solo"
                v-model="formRequest.section"
                :hide-details="true"
              ></v-text-field>
            </v-col>
            <v-col
              :cols="12"
              v-for="(output, x) in formRequest.outputs"
              :key="x"
            >
              <v-row
                class="rounded-lg px-1 py-2 mt-1 mx-0"
                style="border: 2px #babcca solid"
              >
                <button
                  class="btn btn-delete-form"
                  type="button"
                  @click="deleteOutput(x)"
                >
                  <v-icon
                    icon="mdi-delete"
                    color="#D6212A"
                    size="x-small"
                  ></v-icon>
                </button>
                <p class="text-darkBlue font-weight-bold form-title">
                  Output {{ x + 1 }}
                </p>
                <v-col :cols="12">
                  <v-autocomplete
                    variant="solo"
                    placeholder="Choose Content"
                    item-title="Value"
                    item-value="Id"
                    v-model="formRequest.outputs[x].contentId"
                    @update:model-value="(val: any) => onChangeBpList(x, val)"
                    :items="store.state.contentStore.bpList"
                    :hide-details="
                      !hasNestedError(
                        v$.outputs.$each.$response.$errors[x].contentId
                      )
                    "
                    :error-messages="
                      checkNestedError(
                        v$.outputs.$each.$response.$errors[x].contentId
                      )
                    "
                  ></v-autocomplete>
                </v-col>
                <template
                  v-for="(form, y) in formRequest.outputs[x].forms"
                  :key="y"
                >
                  <v-col :cols="6" class="pb-0 pt-3">
                    <v-autocomplete
                      variant="solo"
                      placeholder="Choose Form"
                      item-title="Value"
                      item-value="Id"
                      v-model="formRequest.outputs[x].forms[y].formId"
                      @update:model-value="(val: any) => onChangeDocList(x, y, val)"
                      :items="formRequest.outputs[x].nestedList.doc"
                      :disabled="formRequest.outputs[x].contentId == null"
                      :hide-details="
                        !hasNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].formId ?? []
                        )
                      "
                      :error-messages="
                        checkNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].formId ?? []
                        )
                      "
                    ></v-autocomplete>
                  </v-col>
                  <v-col :cols="6" class="py-0 pt-3">
                    <v-autocomplete
                      variant="solo"
                      placeholder="Choose Section"
                      item-title="Value"
                      item-value="IdSection"
                      return-object
                      v-model="formRequest.outputs[x].forms[y].sectionId"
                      @update:model-value="(val: any) => onChangeSectionList(x, y, val)"
                      :items="
                        formRequest.outputs[x].forms[y].nestedList.section
                      "
                      :disabled="formRequest.outputs[x].forms[y].formId == null"
                      :hide-details="
                        !hasNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].sectionId ?? []
                        )
                      "
                      :error-messages="
                        checkNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].sectionId ?? [],
                          {
                            requiredIf: 'wajib diisi',
                            shouldChose: 'Silahkan pilih subsection',
                            unique: 'Section tidak boleh ada yang sama',
                          }
                        )
                      "
                    ></v-autocomplete>
                  </v-col>
                  <v-col :cols="12" class="pt-0">
                    <div class="d-flex mt-2">
                      <v-autocomplete
                        variant="solo"
                        placeholder="Choose Subsection (Optional)"
                        item-title="Value"
                        item-value="Id"
                        v-model="formRequest.outputs[x].forms[y].subSectionId"
                        :items="
                          formRequest.outputs[x].forms[y].nestedList.subSection
                        "
                        :disabled="
                          formRequest.outputs[x].forms[y].sectionId == null
                        "
                        :hide-details="
                          !hasNestedError(
                            v$.outputs.$each.$response.$errors[x].forms[0]
                              ?.$response?.$errors[y].subSectionId ?? []
                          )
                        "
                        :error-messages="
                          checkNestedError(
                            v$.outputs.$each.$response.$errors[x].forms[0]
                              ?.$response?.$errors[y].subSectionId ?? [],
                            { unique: 'Subsection tidak boleh ada yang sama' }
                          )
                        "
                      ></v-autocomplete>
                      <button
                        type="button"
                        @click="deleteForm(x, y)"
                        class="btn btn-delete-section"
                        :loading="isLoading"
                        v-if="y != output.forms.length - 1"
                      >
                        <v-icon
                          icon="mdi-delete"
                          color="#D6212A"
                          size="large"
                        ></v-icon>
                      </button>
                      <button
                        type="button"
                        class="btn btn-delete-section bg-blue-gradient"
                        @click="addForm(x)"
                        :disabled="
                          formRequest.outputs[x].forms[y].sectionId == null
                        "
                        :loading="isLoading"
                        v-else
                      >
                        <v-icon
                          icon="mdi-plus"
                          color="#fff"
                          size="large"
                        ></v-icon>
                      </button>
                    </div>
                  </v-col>
                </template>
              </v-row>
            </v-col>
            <v-col :cols="12">
              <v-btn
                elevation="3"
                class="btn-create"
                :loading="isLoading"
                @click="addOutput"
              >
                <v-icon icon="mdi-plus" color="#fff"></v-icon> Add Output
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="d-flex justify-end px-6 py-4">
          <v-btn elevation="3" class="btn-cancel" @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn
            elevation="3"
            class="btn-create"
            :loading="isLoading"
            @click="save"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import { ref, computed, getCurrentInstance, onMounted } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { TSelect, TFormMappingSection } from "@/v2/Type";
import { helpers, required } from "@vuelidate/validators";
import { responsePromise } from "@v2/helpers/utils";

const prop = defineProps({
  formSource: {
    type: String,
    requried: true,
  },
});

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const route = useRoute();
const store = useStore();
const hasMapping = ref<boolean>(false);
const dialog = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const idEvent = computed((): string => route.params.idEvent as string);
const idDoc = computed((): string => route.params.idDoc as string);
const buttonState = computed(
  (): boolean => store.getters["documentStore/getOnloadingButtonState"]
);
const isApprovalInProgress = computed(
  (): boolean => store.getters["collaborationStore/getDocumentStatusId"] == "49"
);
const rules = computed(() => {
  const localRule = {
    input: {},
    section: {},
    outputs: {
      $each: helpers.forEach({
        contentId: {
          required,
          unique: (value: any, obj: any, idx: any, parent: any) => {
            const validate =
              parent.outputs.filter((output: any) => output.contentId == value)
                .length <= 1 || value == null;
            return validate;
          },
        },
        forms: {
          $each: helpers.forEach({
            formId: { required },
            sectionId: {
              requiredIf: (value: any, obj: any) => {
                const totalSection = obj.nestedList.section?.length ?? 0;
                return !(value === null && totalSection > 0);
              },
              unique: (value: any, obj: any, idx: any, parent: any) => {
                const idSection = value?.IdSection;
                const totalForm = parent.forms.filter(
                  (form: any) => form.sectionId?.IdSection == idSection
                ).length;
                const totalFormMemilikiAnak = parent.forms.filter(
                  (form: any) =>
                    form.sectionId?.IdSection == idSection &&
                    form.subSectionId != null
                ).length;
                const result =
                  idSection == null ||
                  totalForm == 1 ||
                  (totalForm > 1 && totalFormMemilikiAnak > 0);
                return result;
              },
              shouldChose: (value: any, obj: any, idx: any, parent: any) => {
                const idSection = value?.IdSection;
                const totalForm = parent.forms.filter(
                  (form: any) => form.sectionId?.IdSection == idSection
                ).length;
                const hasChild = obj.subSectionId != null;
                const result =
                  idSection == null ||
                  totalForm == 1 ||
                  (totalForm > 1 && hasChild);
                return result;
              },
            },
            subSectionId: {
              unique: (value: any, obj: any, idx: any, parent: any) => {
                const notHasAnotherForm =
                  parent.forms.filter((form: any) => form.subSectionId == value)
                    .length <= 1;
                const result = notHasAnotherForm || value == null;
                return result;
              },
            },
          }),
        },
      }),
    },
  };
  return localRule;
});
const formRequest = ref<TFormMappingSection>({
  bpName: null,
  input: null,
  section: null,
  idEFormSource: null,
  idSector: 0,
  outputs: [
    {
      contentId: null,
      forms: [
        {
          formId: null,
          sectionId: null,
          subSectionId: null,
          nestedList: {
            section: [] as TSelect[],
            subSection: [] as TSelect[],
          },
        },
      ],
      nestedList: {
        doc: [] as TSelect[],
      },
    },
  ],
});
const v$ = useVuelidate(rules, formRequest);

function clear() {
  formRequest.value = {
    bpName: null,
    input: null,
    section: null,
    idSector: 0,
    idEFormSource: null,
    outputs: [
      {
        contentId: null,
        forms: [
          {
            formId: null,
            sectionId: null,
            subSectionId: null,
            nestedList: {
              section: [] as TSelect[],
              subSection: [] as TSelect[],
            },
          },
        ],
        nestedList: {
          doc: [] as TSelect[],
        },
      },
    ],
  };
  v$.value.$reset();
}

function openDialog() {
  clear();
  dialog.value = true;
  isLoading.value = false;

  store
    .dispatch("contentStore/getMappingSection", {
      idEFormSource: prop.formSource,
    })
    .then((res: TFormMappingSection) => {
      formRequest.value = Object.assign({}, res);
      getBPList();
      res.outputs.forEach((output, x) => {
        onChangeBpList(x, output.contentId, false);
        output.forms.forEach((form, y) => {
          onChangeDocList(x, y, form.formId, false);
          if (form.sectionId) {
            onChangeSectionList(x, y, form.sectionId, false);
          }
        });
      });
    });
}

function closeDialog() {
  clear();
  dialog.value = false;
}

function save() {
  v$.value.$validate().then((res) => {
    if (res) {
      isLoading.value = true;
      const req = {
        IdEFormSource: prop.formSource,
        IdEformDestination: [] as string[],
      };
      formRequest.value.outputs.forEach((output) => {
        output.forms.forEach((form) => {
          const section = form.sectionId as any;
          if (form.subSectionId) {
            req.IdEformDestination.push(form.subSectionId);
          } else if (section) {
            req.IdEformDestination.push(section?.IdEForm ?? "");
          }
        });
      });

      store
        .dispatch("contentStore/mappingSection", req)
        .then((res) => {
          response.success(res, function () {
            store.dispatch("documentStore/fetchFormDocument", idDoc.value);
            closeDialog();
          });
        })
        .catch(response.error)
        .finally(() => {
          isLoading.value = false;
        });
    }
  });
}

function addOutput() {
  formRequest.value.outputs.push({
    contentId: null,
    forms: [
      {
        formId: null,
        sectionId: null,
        subSectionId: null,
        nestedList: {
          section: [] as TSelect[],
          subSection: [] as TSelect[],
        },
      },
    ],
    nestedList: {
      doc: [] as TSelect[],
    },
  });
}

function deleteOutput(idx: number) {
  formRequest.value.outputs.splice(idx, 1);
}

function addForm(idxOutput: number) {
  const output = formRequest.value.outputs[idxOutput];
  if (output) {
    output.forms.push({
      formId: null,
      sectionId: null,
      subSectionId: null,
      nestedList: {
        section: [] as TSelect[],
        subSection: [] as TSelect[],
      },
    });
  }
}

function deleteForm(idxOutput: number, idForm: number) {
  const output = formRequest.value.outputs[idxOutput];
  if (output) {
    output.forms.splice(idForm, 1);
  }
}

function getBPList() {
  store.commit("contentStore/setBpList", []);
  store.dispatch("contentStore/getBpList", {
    idEvent: idEvent.value,
    idSector: formRequest.value.idSector,
  });
}

function onChangeBpList(idx: number, val: string | any, reset = true) {
  if (val) {
    if (reset) {
      formRequest.value.outputs[idx].forms = [
        {
          formId: null,
          sectionId: null,
          subSectionId: null,
          nestedList: {
            section: [] as TSelect[],
            subSection: [] as TSelect[],
          },
        },
      ];
    }
    const form = formRequest.value.outputs[idx];
    form.nestedList.doc = [];
    store
      .dispatch("contentStore/getBpDocMappingList", {
        idBP: val,
        IdEFormSource: formRequest.value.idEFormSource,
      })
      .then((res: TSelect[]) => {
        form.nestedList.doc = res;
      });
  }
}

function onChangeDocList(
  idxOutput: number,
  idxForm: number,
  val: string | any,
  reset = true
) {
  if (reset) {
    formRequest.value.outputs[idxOutput].forms[idxForm].sectionId = null;
  }
  if (val) {
    const output = formRequest.value.outputs[idxOutput];
    output.forms[idxForm].nestedList.section = [];
    store
      .dispatch("contentStore/getBpDocSectionMappingList", {
        idBPDoc: val,
      })
      .then((res: TSelect[]) => {
        output.forms[idxForm].nestedList.section = res;
      });
  }
}

function onChangeSectionList(
  idxOutput: number,
  idxForm: number,
  val: any,
  reset = true
) {
  if (val) {
    if (reset) {
      formRequest.value.outputs[idxOutput].forms[idxForm].subSectionId = null;
    }
    const output = formRequest.value.outputs[idxOutput];
    output.forms[idxForm].nestedList.subSection = [];
    store
      .dispatch("contentStore/getBpDocSubSectionMappingList", {
        idBPSection: val.IdSection,
      })
      .then((res: TSelect[]) => {
        output.forms[idxForm].nestedList.subSection = res;
      });
  }
}

function checkNestedError(item: any[], customMessage = {}) {
  const message = {
    required: "Wajib diisi",
    unique: "Content tidak boleh ada yang sama",
    ...customMessage,
  };

  return item.map((d) => {
    return message[d.$validator] ?? d.$message;
  });
}

function hasNestedError(item: any[]): boolean {
  return v$.value.$dirty && item.length != 0;
}

defineExpose({
  openDialog,
  closeDialog,
});

onMounted(() => {
  store.commit("collaborationStore/setdocumentSubmitCheck", false);

  store
    .dispatch("contentStore/getMappingSection", {
      idEFormSource: prop.formSource,
    })
    .then((res: TFormMappingSection) => {
      hasMapping.value =
        res.outputs.filter((out) => out.contentId != null).length > 0;

      if (hasMapping.value)
        store.commit("collaborationStore/setdocumentSubmitCheck", true);
    });
});
</script>

<style scoped>
.bg-blue-gradient {
  background: linear-gradient(#065695 -46.47%, #267dc2 157.9%);
}

.btn-cancel {
  background: linear-gradient(#fff -46.47%, #fff 157.9%);
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  font-weight: 800;
  color: #065695 !important;
}

.btn-create {
  background: linear-gradient(#065695 -46.47%, #267dc2 157.9%);
  border-radius: 10px;
  padding-left: 15px;
  padding-right: 15px;
  font-weight: 800;
  width: 120px;
  color: white !important;
}

.form-title {
  margin-top: -21px;
  margin-left: 20px;
  background-color: white;
  width: fit-content;
}

.btn-delete-form {
  position: absolute;
  right: 0;
  background-color: #fff;
  margin-top: -20px;
  margin-right: 22px;
  padding: 1px 6px 2px 6px;
  border-radius: 7px 7px 7px 7px;
}

.btn-delete-section {
  padding: 10px;
  margin: 5px 0px 5px 5px;
  border-radius: 10px;
}

:deep(.v-field--disabled) {
  background-color: rgb(196, 186, 186) !important;
}

:deep(button:disabled, button[disabled]) {
  background: rgb(238, 238, 238) !important;
}

.icon-share-empty {
  float: right;
  right: 0px;
  top: -15px;
}
</style>
