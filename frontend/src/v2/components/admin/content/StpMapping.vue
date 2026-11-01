<template>
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
            <p class="text-darkBlue font-weight-bold form-title">Input</p>
            <v-col :cols="12">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">
                Content Title
              </p>
              <div
                class="border-radius-dwp py-3 px-4"
                style="background-color: #eaeaea"
              >
                <p class="text-ellipsis">
                  {{ formRequest.content }}
                </p>
              </div>
            </v-col>
            <v-col :cols="12">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">
                Section Title
              </p>
              <div
                class="border-radius-dwp py-3 px-4"
                style="background-color: #eaeaea"
              >
                <p class="text-ellipsis">
                  {{ formRequest.section }}
                </p>
              </div>
            </v-col>
            <v-col :cols="12" v-if="hasSubSection > 0">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">
                Sub Section Title
              </p>
              <v-chip class="border-radius-dwp py-7 px-4" style="width: 100%">
                <span style="width: 100%">{{ formRequest.sub_section }}</span>
              </v-chip>
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
                    clearable
                    variant="solo"
                    placeholder="Choose Tahapan"
                    item-title="Value"
                    item-value="Id"
                    v-model="formRequest.outputs[x].content_id"
                    @update:model-value="(val: any) => onChangeTahapan(x, val)"
                    :items="listTahapan"
                    :hide-details="
                      !hasNestedError(
                        v$.outputs.$each.$response.$errors[x].content_id
                      )
                    "
                    :error-messages="
                      checkNestedError(
                        v$.outputs.$each.$response.$errors[x].content_id
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
                      clearable
                      variant="solo"
                      placeholder="Choose Content"
                      item-title="Value"
                      item-value="Id"
                      v-model="formRequest.outputs[x].forms[y].form_id"
                      @update:model-value="(val: any) => onChangeContent(x, y, val)"
                      :items="formRequest.outputs[x].nested_list.contents"
                      :disabled="formRequest.outputs[x].content_id == null"
                      :hide-details="
                        !hasNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].form_id ?? []
                        )
                      "
                      :error-messages="
                        checkNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].form_id ?? []
                        )
                      "
                    ></v-autocomplete>
                  </v-col>
                  <v-col :cols="6" class="py-0 pt-3">
                    <v-autocomplete
                      clearable
                      variant="solo"
                      placeholder="Choose Section"
                      item-title="Value"
                      item-value="Id"
                      @blur="
                        v$.formRequest?.outputs[x].forms[y].section_id.$touch()
                      "
                      v-model="formRequest.outputs[x].forms[y].section_id"
                      @update:model-value="(val: any) => onChangeSection(x, y, val)"
                      :items="
                        formRequest.outputs[x].forms[y].nested_list.sections
                      "
                      :disabled="
                        formRequest.outputs[x].forms[y].form_id == null
                      "
                      :hide-details="
                        !hasNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].section_id ?? []
                        )
                      "
                      :error-messages="
                        checkNestedError(
                          v$.outputs.$each.$response.$errors[x].forms[0]
                            ?.$response?.$errors[y].section_id ?? [],
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
                        clearable
                        variant="solo"
                        placeholder="Choose sub section (Optional)"
                        item-title="Value"
                        item-value="Id"
                        v-model="formRequest.outputs[x].forms[y].sub_section_id"
                        :items="
                          formRequest.outputs[x].forms[y].nested_list
                            .sub_sections
                        "
                        :disabled="
                          formRequest.outputs[x].forms[y].section_id == null
                        "
                        :hide-details="
                          !hasNestedError(
                            v$.outputs.$each.$response.$errors[x].forms[0]
                              ?.$response?.$errors[y].sub_sectionsId ?? []
                          )
                        "
                        :error-messages="
                          checkNestedError(
                            v$.outputs.$each.$response.$errors[x].forms[0]
                              ?.$response?.$errors[y].sub_sectionsId ?? [],
                            { unique: 'sub section tidak boleh ada yang sama' }
                          )
                        "
                      ></v-autocomplete>
                      <button
                        type="button"
                        @click="deleteForm(x, y)"
                        class="btn btn-delete-section"
                        :loading="is_loading"
                        v-if="output.forms.length > 1"
                      >
                        <v-icon
                          icon="mdi-delete"
                          color="#D6212A"
                          size="large"
                        ></v-icon>
                      </button>
                      <!-- <button
                        type="button"
                        class="btn btn-delete-section bg-blue-gradient"
                        @click="addForm(x)"
                        :disabled="
                          formRequest.outputs[x].forms[y].section_id == null
                        "
                        :loading="is_loading"
                        v-else
                      >
                        <v-icon
                          icon="mdi-plus"
                          color="#fff"
                          size="large"
                        ></v-icon>
                      </button> -->
                    </div>
                    <div v-if="y == output.forms.length - 1" class="mt-2">
                      <v-btn
                        prepend-icon="mdi-plus"
                        variant="text"
                        @click="addForm(x)"
                        :loading="is_loading"
                        color="#065695"
                        :disabled="
                          formRequest.outputs[x].forms[y].section_id == null
                        "
                        style="letter-spacing: -0.2px"
                        class="font-weight-bold"
                      >
                        Add Content
                      </v-btn>
                      <!-- <button
                        type="button"
                        class="btn btn-delete-section bg-blue-gradient"
                        @click="addForm(x)"
                        :disabled="
                          formRequest.outputs[x].forms[y].section_id == null
                        "
                        :loading="is_loading"
                      >
                        <v-icon
                          icon="mdi-plus"
                          color="#fff"
                          size="small"
                        ></v-icon>
                        <span class="ml-1">Add Content</span>
                      </button> -->
                    </div>
                  </v-col>
                </template>
              </v-row>
            </v-col>
            <v-col :cols="12">
              <v-btn
                elevation="3"
                class="btn-create"
                :loading="is_loading"
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
            :loading="is_loading"
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
import { useVuelidate } from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import { TSelect } from "@/v2/Type";
import { computed, getCurrentInstance, ref } from "vue";
import { useStore } from "vuex";

const instance: any = getCurrentInstance()?.root.refs;
const dialog = ref<boolean>(false);
const id = ref<number>(0);
const store = useStore();
const is_loading = ref<boolean>(false);
const listTahapan = ref([]);
const hasSubSection = ref();
const formRequest = ref({
  content: null,
  section: null,
  sub_section: null,
  template_id: null,
  section_id: null,
  sector_id: null,
  outputs: [
    {
      content_id: null,
      nested_list: {
        contents: [] as TSelect[],
      },
      forms: [
        {
          form_id: null,
          section_id: null,
          sub_section_id: null,
          nested_list: {
            sections: [] as any[],
            sub_sections: [] as TSelect[],
          },
        },
      ],
    },
  ],
});
const rules = computed(() => {
  const localRule = {
    content: {},
    section: {},
    sub_section: {},
    outputs: {
      $each: helpers.forEach({
        content_id: {
          required,
          unique: (value: any, obj: any, idx: any, parent: any) => {
            const validate =
              parent.outputs.filter((output: any) => output.content_id == value)
                .length <= 1 || value == null;
            return validate;
          },
        },
        forms: {
          $each: helpers.forEach({
            form_id: { required },
            section_id: {
              required,
              requiredIf: (value: any, obj: any) => {
                const totalSection = obj.nested_list.section?.length ?? 0;
                return !(value === null && totalSection > 0);
              },
              unique: (value: any, obj: any, idx: any, parent: any) => {
                const idSection = value;
                const totalForm = parent.forms.filter(
                  (form: any) => form.section_id == idSection
                ).length;
                const totalFormMemilikiAnak = parent.forms.filter(
                  (form: any) =>
                    form.section_id == idSection && form.sub_section_id != null
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
                  (form: any) => form.section_id?.IdSection == idSection
                ).length;
                const hasChild = obj.sub_section_id != null;
                const result =
                  idSection == null ||
                  totalForm == 1 ||
                  (totalForm > 1 && hasChild);
                return result;
              },
            },
            sub_section_id: {
              unique: (value: any, obj: any, idx: any, parent: any) => {
                const notHasAnotherForm =
                  parent.forms.filter(
                    (form: any) => form.sub_section_id == value
                  ).length <= 1;
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
const v$ = useVuelidate(rules, formRequest);

function onChangeTahapan(idx: number, val: string | any, reset = true) {
  if (val) {
    if (reset) {
      formRequest.value.outputs[idx].forms = [
        {
          form_id: null,
          section_id: null,
          sub_section_id: null,
          nested_list: {
            sections: [] as TSelect[],
            sub_sections: [] as TSelect[],
          },
        },
      ];
    }
    const form = formRequest.value.outputs[idx];
    form.nested_list.contents = [];
    store
      .dispatch("adminStore/getContentList", {
        idMBPTemplate: val,
        idMEFormTemplateSource: id.value,
      })
      .then(({ responseData }) => {
        form.nested_list.contents = responseData;
      });
  }
}

function onChangeContent(
  idxOutput: number,
  idxForm: number,
  val: string | any,
  reset = true
) {
  if (reset) {
    formRequest.value.outputs[idxOutput].forms[idxForm].section_id = null;
  }
  if (val) {
    const output = formRequest.value.outputs[idxOutput];
    output.forms[idxForm].nested_list.sections = [];
    store
      .dispatch("adminStore/getSectionList", {
        idMBPDocTemplate: val,
      })
      .then(({ responseData }) => {
        output.forms[idxForm].nested_list.sections = responseData.map((r) => {
          return {
            Id: r.idMBPSectionTemplate,
            IdReq: r.idMEFormTemplate,
            Value: r.Value,
          };
        });
      });
  }
}

function onChangeSection(
  idxOutput: number,
  idxForm: number,
  val: any,
  reset = true
) {
  if (val) {
    if (reset) {
      formRequest.value.outputs[idxOutput].forms[idxForm].sub_section_id = null;
    }
    const output = formRequest.value.outputs[idxOutput];
    output.forms[idxForm].nested_list.sub_sections = [];
    store
      .dispatch("adminStore/getSubSectionList", {
        idMBPSectionTemplate: val,
      })
      .then(({ responseData }) => {
        output.forms[idxForm].nested_list.sub_sections = responseData ?? [];
      });
  }
}

function getTahapanList() {
  store
    .dispatch("adminStore/getTahapanList", {
      idMEventSubTypeList: formRequest.value.section_id,
      idSector: formRequest.value.sector_id,
    })
    .then(({ responseData }) => {
      listTahapan.value = responseData;
    });
}

function openDialog(_id: number, _hasSubSection: number) {
  hasSubSection.value = _hasSubSection;
  id.value = _id;
  store.dispatch("adminStore/getStpMapping", _id).then((res: any) => {
    formRequest.value = Object.assign({}, res);

    getTahapanList();
    res.outputs.forEach((output: any, x: number) => {
      onChangeTahapan(x, output.content_id, false);
      output.forms.forEach((form: any, y: number) => {
        onChangeContent(x, y, form.form_id, false);
        if (form.section_id) {
          onChangeSection(x, y, form.section_id, false);
        }
      });
    });
    dialog.value = true;
  });
}

function closeDialog() {
  dialog.value = false;
}

function addOutput() {
  formRequest.value.outputs.push({
    content_id: null,
    nested_list: {
      contents: [] as TSelect[],
    },
    forms: [
      {
        form_id: null,
        section_id: null,
        sub_section_id: null,
        nested_list: {
          sections: [] as TSelect[],
          sub_sections: [] as TSelect[],
        },
      },
    ],
  });
}

function deleteOutput(idx: number) {
  formRequest.value.outputs.splice(idx, 1);
}

function addForm(idxOutput: number) {
  const output = formRequest.value.outputs[idxOutput];
  if (output) {
    output.forms.push({
      form_id: null,
      section_id: null,
      sub_section_id: null,
      nested_list: {
        sections: [] as TSelect[],
        sub_sections: [] as TSelect[],
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

function save() {
  v$.value.$validate().then((res) => {
    if (res) {
      is_loading.value = true;
      const req = {
        idMEFormTemplateSource: id.value,
        idMEFormTemplateDestination: [] as any[],
      };
      formRequest.value.outputs.forEach((output) => {
        output.forms.forEach((form) => {
          const section = form.section_id;
          if (form.sub_section_id) {
            req.idMEFormTemplateDestination.push(form.sub_section_id);
          } else if (section) {
            const secObj = form.nested_list.sections.find(
              (r) => r.Id == section
            );
            if (secObj) {
              req.idMEFormTemplateDestination.push(secObj.IdReq);
            }
          }
        });
      });

      store
        .dispatch("adminStore/storeStpMapping", req)
        .then(({ responseMessage }) => {
          instance.toast.show({
            message: responseMessage,
            color: "success",
            timeout: 3000,
          });
        })
        .catch((error) => {
          instance.toast.show({
            message:
              error.response.data.responseMessage ?? "internal server error",
            color: "warning",
            timeout: 3000,
          });
        })
        .finally(() => {
          is_loading.value = false;
        });
    }
  });
}

defineExpose({ openDialog });
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

.icon-share-empty {
  float: right;
  right: 0px;
  top: -15px;
}

:deep(.v-field--disabled) {
  background-color: rgb(196, 186, 186) !important;
}

.text-ellipsis {
  color: #4b4b4b;
  height: 25px;
  overflow: hidden;
  padding-right: 32px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
