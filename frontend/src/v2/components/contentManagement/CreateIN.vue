<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="800" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            Add Issue Note
          </div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="hide"
          ></v-btn>
        </v-card-title>
        <div class="separatorHorizontalGradient"></div>
        <v-card-text>
          <v-row>
            <v-col :cols="12" v-if="isRDGB">
              <p class="pb-1 text-left text-darkBlue font-weight-bold">
                Sector
              </p>
              <v-autocomplete
                variant="solo"
                placeholder="Choose Sector"
                item-title="value"
                item-value="id"
                v-model="formRequest.sector"
                :hide-details="isError(v$.sector)"
                :items="store.state.contentStore.sectorList"
                :error-messages="getErrorMessages(v$.sector)"
              ></v-autocomplete>
            </v-col>
            <v-col
              :cols="12"
              :key="x"
              v-for="(form, x) in formRequest.forms"
              class="px-4 mt-2"
            >
              <div
                class="rounded-lg px-5 py-4"
                style="border: 2px #babcca solid"
              >
                <button
                  class="btn btn-delete-form"
                  type="button"
                  @click="deleteForm(x)"
                  v-if="x != formRequest.forms.length - 1"
                >
                  <v-icon
                    icon="mdi-delete"
                    color="#D6212A"
                    size="x-small"
                  ></v-icon>
                </button>
                <p class="text-darkBlue font-weight-bold form-title">
                  Form {{ x + 1 }}
                </p>
                <v-row class="mb-3">
                  <v-col :cols="12" class="pb-0">
                    <p class="text-darkBlue font-weight-bold my-3">Title</p>
                    <v-text-field
                      variant="solo"
                      placeholder="Insert Title"
                      v-model="formRequest.forms[x].title"
                      :hide-details="
                        !hasNestedError(
                          v$.forms.$each.$response.$errors[x].title
                        )
                      "
                      :error-messages="
                        checkNestedError(
                          v$.forms.$each.$response.$errors[x].title
                        )
                      "
                    ></v-text-field>
                  </v-col>
                  <v-col :cols="12" class="pb-0">
                    <p class="text-darkBlue font-weight-bold my-3">Section</p>
                    <template v-for="(section, y) in form.sections" :key="y">
                      <div class="d-flex mt-2">
                        <v-autocomplete
                          variant="solo"
                          placeholder="Choose Section"
                          item-title="value"
                          item-value="id"
                          class="mr-3"
                          v-model="formRequest.forms[x].sections[y].id"
                          :items="listSection"
                          :hide-details="true"
                        ></v-autocomplete>
                        <button
                          type="button"
                          @click="addSection(x)"
                          class="btn btn-delete-section bg-blue-gradient"
                          :loading="isLoading"
                          v-if="
                            y == form.sections.length - 1 && y < limitSection
                          "
                        >
                          <v-icon
                            icon="mdi-plus"
                            color="#fff"
                            size="large"
                          ></v-icon>
                        </button>
                        <button
                          type="button"
                          @click="deleteSection(x, y)"
                          class="btn btn-delete-section"
                          :loading="isLoading"
                          v-else
                        >
                          <v-icon
                            icon="mdi-delete"
                            color="#D6212A"
                            size="large"
                          ></v-icon>
                        </button>
                      </div>
                      <span
                        class="text-danger ml-5 text-12"
                        v-if="
                          hasNestedError(
                            v$.forms.$each.$response.$errors[x].sections[0]
                              ?.$response?.$errors[y].id ?? []
                          )
                        "
                      >
                        {{
                          checkNestedError(
                            v$.forms.$each.$response.$errors[x].sections[0]
                              ?.$response?.$errors[y].id ?? []
                          ).join(", ")
                        }}
                      </span>
                    </template>
                  </v-col>
                </v-row>
              </div>
            </v-col>
            <v-col :cols="12" class="py-0">
              <v-btn
                elevation="3"
                class="btn-create"
                @click="addForm"
                :loading="isLoading"
              >
                <v-icon icon="mdi-plus" color="#fff"></v-icon> Add Form
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="d-flex justify-end px-6 py-4">
          <v-btn elevation="3" class="btn-cancel" @click="hide"> Cancel </v-btn>
          <v-btn
            elevation="3"
            class="btn-create"
            @click="save"
            :loading="isLoading"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@v2/helpers/validation";
import { TRequestCreatePN, TSelect } from "@/v2/Type";
import { ref, watch, computed, getCurrentInstance } from "vue";
import { responsePromise } from "@v2/helpers/utils";

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();
const route = useRoute();
const dialog = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const idDoc = computed((): string => route.params.idDoc as string);
const isRDGB = computed((): boolean => {
  return (route.params.typeRDG as string) == "rdgb";
});
const idBp = computed(() => {
  const detail = store.state.meetingStore.meetingSummary;
  return { ...detail.issueNote }.idBp;
});
const listSection = computed((): TSelect[] => {
  return store.state.contentStore.formList;
});
const limitSection = computed((): number => listSection.value.length - 1);

const formRequest = ref<TRequestCreatePN>({
  sector: null,
  forms: [
    {
      title: null,
      sections: [
        {
          id: null,
        },
      ],
    },
  ],
});

const rules = computed(() => {
  const localRule = {
    sector: {},
    forms: {
      $each: helpers.forEach({
        title: {
          required,
          unique: (value: any, obj: any, idx: any, parent: any) => {
            const validate =
              parent.forms.filter(
                (form) => form.title?.toLowerCase() == value?.toLowerCase()
              ).length <= 1 || value == null;
            return validate;
          },
        },
        sections: {
          $each: helpers.forEach({
            id: {
              required,
              unique: (value: any, obj: any, idx: any, parent: any) => {
                const validate =
                  parent.sections.filter((sec: any) => sec.id == value)
                    .length <= 1 || value == null;
                return validate;
              },
            },
          }),
        },
      }),
    },
  };
  if (isRDGB.value) localRule.sector = { required };
  return localRule;
});

const v$ = useVuelidate(rules, formRequest);

function checkNestedError(item: any[]) {
  const customMessage = {
    required: "Wajib diisi",
    unique: "Data sudah ada",
  };
  return item.map((d) => {
    return customMessage[d.$validator] ?? d.$message;
  });
}

function hasNestedError(item: any[]): boolean {
  return v$.value.$dirty && item.length != 0;
}

function clear() {
  formRequest.value = {
    sector: null,
    forms: [
      {
        title: null,
        sections: [
          {
            id: null,
          },
        ],
      },
    ],
  };
  store.commit("contentStore/setFormList", []);
  v$.value.$reset();
}

function hide() {
  clear();
  dialog.value = false;
}

function show() {
  clear();
  dialog.value = true;
}

function save() {
  v$.value.$validate().then((res) => {
    if (res) {
      const req = {
        idSector: formRequest.value.sector,
        listOutput: formRequest.value.forms.map((item) => {
          return {
            idBp: idBp.value,
            title: item.title,
            idBPSection: item.sections.map((sec) => sec.id),
          };
        }),
      };
      store
        .dispatch("contentStore/createAIUCustom", req)
        .then((res) => {
          response.success(res, function () {
            hide();
          });
        })
        .catch(response.error)
        .finally(() => {
          isLoading.value = false;
        });
    }
  });
}

function addForm() {
  formRequest.value.forms.push({
    title: null,
    sections: [
      {
        id: null,
      },
    ],
  });
}

function deleteForm(idx: number) {
  formRequest.value.forms.splice(idx, 1);
}

function addSection(idxForm: number) {
  const form = formRequest.value.forms[idxForm];
  if (form) {
    form.sections.push({
      id: null,
    });
  }
}

function deleteSection(idxForm: number, idxSection: number) {
  const form = formRequest.value.forms[idxForm];
  if (form) {
    form.sections.splice(idxSection, 1);
  }
}

defineExpose({
  hide,
  show,
});

watch(
  () => formRequest.value.sector,
  (val) => {
    store.commit("contentStore/setFormList", []);
    formRequest.value.forms = [
      {
        title: null,
        sections: [
          {
            id: null,
          },
        ],
      },
    ];
    if (val != null) {
      const req = {
        idSector: val,
        idBP: idBp.value,
      };

      store.dispatch("contentStore/getFormList", req);
    }
  }
);
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
  margin-top: -28px;
  margin-left: 10px;
  background-color: white;
  width: fit-content;
}

.btn-delete-form {
  position: absolute;
  right: 0;
  margin-top: -16px;
  margin-right: 29px;
  padding: 1px 6px 2px 6px;
  border-radius: 0px 7px 0px 7px;
}

.btn-delete-section {
  padding: 10px;
  margin: 5px 0px 5px 5px;
  border-radius: 10px;
}
</style>
