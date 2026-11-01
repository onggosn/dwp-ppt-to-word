<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="800" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            Add Analisis Indikator Utama
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
            <v-col :cols="12">
              <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                Sector
              </p>
              <v-autocomplete
                variant="solo"
                placeholder="Choose Sector"
                class="px-2"
                item-title="value"
                item-value="id"
                v-model="formRequest.sector"
                :items="store.state.contentStore.sectorList"
                :hide-details="isError(v$.sector)"
                :error-messages="getErrorMessages(v$.sector)"
              ></v-autocomplete>
            </v-col>
            <v-col
              :cols="12"
              v-for="(item, i) in formRequest.forms"
              :key="i"
              class="px-4"
            >
              <div
                class="rounded-lg px-2 py-4"
                style="border: 2px #babcca solid"
              >
                <button
                  v-if="i != 0"
                  class="btn btn-delete-form"
                  type="button"
                  @click="deleteForm(i)"
                >
                  <v-icon
                    icon="mdi-delete"
                    color="#D6212A"
                    size="x-small"
                  ></v-icon>
                </button>
                <p class="text-darkBlue font-weight-bold form-title">
                  Form {{ i + 1 }}
                </p>
                <p class="text-darkBlue font-weight-bold ml-2 my-2">Title</p>
                <v-autocomplete
                  variant="solo"
                  placeholder="Choose section"
                  class="px-2"
                  item-title="value"
                  item-value="id"
                  v-model="formRequest.forms[i].id"
                  :items="itemList"
                  :loading="loadingList"
                  :hide-details="true"
                ></v-autocomplete>
                <span
                  class="text-danger ml-5 text-12"
                  v-if="
                    v$.$dirty &&
                    v$.forms.$each.$response.$errors[i] &&
                    v$.forms.$each.$response.$errors[i].id.length
                  "
                >
                  {{
                    getErrorMessages(
                      v$.forms.$each.$response.$errors[i].id[0],
                      {
                        required: "Form wajib disi",
                        unique: "Form tidak boleh ada yang sama",
                      }
                    ).toString()
                  }}
                </span>
                <v-text-field
                  v-show="isManualAIU(formRequest.forms[i].id)"
                  variant="solo"
                  placeholder="Input Title"
                  class="px-2 mt-3"
                  v-model="formRequest.forms[i].name"
                  :hide-details="true"
                ></v-text-field>
                <span
                  class="text-danger ml-5 text-12"
                  v-if="
                    v$.$dirty &&
                    v$.forms.$each.$response.$errors[i] &&
                    v$.forms.$each.$response.$errors[i].name.length
                  "
                >
                  {{
                    getErrorMessages(
                      v$.forms.$each.$response.$errors[i].name[0],
                      {
                        required: "Title wajib disi",
                        unique: "Title tidak boleh ada yang sama",
                      }
                    ).toString()
                  }}
                </span>
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
/* eslint-disable */
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { ref, watch, getCurrentInstance, computed } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { getErrorMessages, isError } from "@v2/helpers/validation";
import { TRequestCreateAIU } from "@/v2/Type";
import { responsePromise, secureRandomFloat } from "@v2/helpers/utils";

const emits = defineEmits(["refreshToc"]);
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();
const route = useRoute();
const dialog = ref<boolean>(false);
const isLoading = ref<boolean>(false);
const loadingList = ref<boolean>(false);
const router = useRouter();
const idBp = computed(() => {
  const detail = store.state.meetingStore.meetingSummary;
  return { ...detail.aiu }.idBp;
});
const itemList = computed(() => {
  const items = store.state.contentStore.formList;

  return items;
});
const idEvent = computed((): string => route.params.idEvent as string);
const typeRDG = computed((): string => route.params.typeRDG as string);

const formRequest = ref<TRequestCreateAIU>({
  sector: null,
  forms: [
    {
      id: null,
      name: null
    }
  ]
});

const rules = computed(() => {
  return {
    sector: { required },
    forms: {
      $each: helpers.forEach({
        id: {
          required,
          unique: (value: any) => {
            const isManual = isManualAIU.value(value);
            const validate =
              formRequest.value.forms.filter((item: any) => item.id === value)
                .length <= 1 || value == null;
            return isManual || validate;
          }
        },
        name: {
          required: (value: any, meta: any) => {
            const isManual = isManualAIU.value(meta.id);
            if (isManual) return value != null;
            return true;
          },
          unique: (value: any) => {
            const validate =
              formRequest.value.forms.filter((item: any) => item.name === value)
                .length <= 1 || value == null;
            return validate;
          }
        }
      })
    }
  };
});

const v$ = useVuelidate(rules, formRequest);

// gunakan ketika butuh pembatasan add form button
const showAddForm = computed(() => {
  return (
    formRequest.value.forms.length < store.state.contentStore.formList.length
  );
});

//get name form
const isManualAIU = computed(() => {
  const list = store.state.contentStore.formList;
  return (id: any): boolean => {
    const item = list.find((e: any) => e.id == id);
    return item && item.templateType == "free-text";
  };
});

function clear() {
  formRequest.value = {
    sector: null,
    forms: [
      {
        id: null,
        name: null
      }
    ]
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
      isLoading.value = true;
      const req = {
        idBP: idBp.value,
        idEvent: idEvent.value,
        idSector: formRequest.value.sector,
        listForm: [...formRequest.value.forms].map((item: any) => {
          const name = isManualAIU.value(item.id) ? item.name : "manual";
          return {
            idBPDocTemplate: item.id,
            bpDocName: name
          };
        })
      };
      store
        .dispatch("contentStore/createAIUCustom", req)
        .then((res) => {
          response.success(res, function () {
            hide();
            emits("refreshToc");
            store.commit("contentStore/setReloadToc", secureRandomFloat());
            let redirectTo: string;
            switch (typeRDG.value) {
              case "rdgb":
                redirectTo = "v2.rdg-collaboration";
                break;
              case "rdgm":
                redirectTo = "om.rdg-collaboration";
                break;
              default:
                redirectTo = "";
                break;
            }
            router.push({
              name: redirectTo,
              params: {
                typeRDG: typeRDG.value,
                idEvent: idEvent.value,
                idDoc: res.responseData.idBPDocument
              }
            });
          });
        })
        .catch(response.error)
        .finally(() => {
          isLoading.value = false;
        });
    }
  });
  //   dialog.value = false;
}

function addForm() {
  formRequest.value.forms.push({
    id: null,
    name: null
  });
}

function deleteForm(idx: number) {
  formRequest.value.forms.splice(idx, 1);
}

defineExpose({
  hide,
  show
});

watch(
  () => formRequest.value.sector,
  (val) => {
    if (val) {
      loadingList.value = true;
      store.commit("contentStore/setFormList", []);
        formRequest.value.forms = [
          {
            id: null,
            name: null
          }
        ];

        const req = {
          idSector: val,
          idBP: idBp.value
        };
        store.dispatch("contentStore/getFormList", req).finally(() => {
          loadingList.value = false;
        });
    }
  }
);
</script>

<style scoped>
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
  margin-left: 20px;
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
</style>
