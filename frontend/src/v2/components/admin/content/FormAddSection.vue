<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="1000" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">
            {{ labelDialog }}
          </div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="closeDialog"
          ></v-btn>
        </v-card-title>
        <v-card-text>
          <hr class="line mt-3" />
          <v-row
            class="rounded-lg px-2 mt-2 pb-5 mx-2"
            style="border: 2px #babcca solid"
          >
            <span class="text-darkBlue font-weight-bold form-title">{{
              prop.item.bPDocumentName
            }}</span>

            <!-- SUB SECTION FORM -->
            <template v-if="isSubSection">
              <!-- SECTION TITLE -->
              <!-- #region -->
              <v-col cols="12" class="pb-0">
                <p class="pb-2 text-left text-darkBlue font-weight-bold">
                  Section Title
                </p>
                <v-text-field
                  v-model="itemSubSection.bPEFormLabel"
                  variant="solo"
                  placeholder="Insert Section Title"
                  disabled
                ></v-text-field>
              </v-col>
              <!-- #endregion -->

              <v-col
                class="pt-0 pr-0"
                :cols="12"
                v-for="(section, i) in state.sections"
                :key="i"
              >
                <div class="d-flex flex-justify-between">
                  <div style="width: 100%">
                    <v-row
                      class="rounded-lg px-1 mt-2 mx-2"
                      style="border: 2px #babcca solid"
                    >
                      <!-- SUB SECTION TITLE -->
                      <!-- #region -->
                      <v-col cols="12">
                        <p
                          class="pb-2 text-left text-darkBlue font-weight-bold"
                        >
                          Sub Section Title<span class="text-gradient-red"
                            >*</span
                          >
                        </p>
                        <v-text-field
                          v-model="state.sections[i].title"
                          variant="solo"
                          placeholder="Insert Section Title"
                          :error-messages="
                            getNestedErrorMessage(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].title,
                              {
                                required: 'Required',
                                sectionRegex:
                                  'Invalid input. Avoid using semicolon (;)',
                              }
                            )
                          "
                          :hide-details="
                            !hasNestedError(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].title
                            )
                          "
                        ></v-text-field>
                      </v-col>
                      <!-- #endregion -->

                      <!-- SECTOR -->
                      <!-- #region -->
                      <v-col
                        cols="12"
                        v-if="
                          item.isDocBuku2d ||
                          item.isDocBuku1d ||
                          item.isDocBuku4
                        "
                      >
                        <p
                          class="pb-1 text-left text-darkBlue font-weight-bold"
                        >
                          Sector<span class="text-gradient-red">*</span>
                        </p>
                        <v-radio-group
                          inline
                          style="margin-left: -8px"
                          v-model="state.sections[i].sector"
                          :error-messages="
                            getNestedErrorMessage(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].sector,
                              {
                                required: 'Required',
                              }
                            )
                          "
                          :hide-details="
                            !hasNestedError(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].sector
                            )
                          "
                        >
                          <v-radio
                            v-for="(item, index) in listSector"
                            :key="index"
                            :value="item.id"
                            :label="item.value"
                            color="#065695"
                            class="me-5"
                          ></v-radio>
                        </v-radio-group>
                      </v-col>
                      <!-- #endregion -->
                    </v-row>
                  </div>
                  <div class="align-self-center mx-2">
                    <div
                      v-if="i != state.sections.length - 1"
                      :style="{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '10px',
                      }"
                    >
                      <v-btn
                        color="#CB3A31"
                        variant="outlined"
                        icon="mdi-delete"
                        size="medium"
                        class="btn-icon"
                        @click="handleDelete(i)"
                      ></v-btn>
                    </div>
                    <div
                      v-else
                      :style="{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '10px',
                      }"
                    >
                      <v-btn
                        v-if="state.sections.length != 1"
                        color="#CB3A31"
                        variant="outlined"
                        icon="mdi-delete"
                        size="medium"
                        class="btn-icon"
                        @click="handleDelete(i)"
                      ></v-btn>
                      <v-btn
                        variant="elevated"
                        icon="mdi-plus"
                        size="x-large"
                        class="primary-gradient btn-icon"
                        @click="handleAdd"
                      ></v-btn>
                    </div>
                  </div>
                </div>
              </v-col>
            </template>
            <template v-else>
              <!-- SECTION FORM -->
              <v-col
                :cols="12"
                v-for="(section, i) in state.sections"
                :key="i"
                class="pr-0"
              >
                <div class="d-flex flex-justify-between">
                  <div style="width: 100%">
                    <v-row
                      class="rounded-lg px-1 mt-2 mx-2"
                      style="border: 2px #babcca solid"
                    >
                      <!--Section Title  -->
                      <!-- #region -->
                      <v-col cols="12">
                        <p
                          class="pb-1 text-left text-darkBlue font-weight-bold"
                        >
                          Section Title<span class="text-gradient-red">*</span>
                        </p>
                        <v-text-field
                          v-model="state.sections[i].title"
                          variant="solo"
                          placeholder="Insert Section Title"
                          :error-messages="
                            getNestedErrorMessage(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].title,
                              {
                                required: 'Required',
                                sectionRegex:
                                  'Invalid input. Avoid using semicolon (;)',
                              }
                            )
                          "
                          :hide-details="
                            !hasNestedError(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].title
                            )
                          "
                        ></v-text-field>
                      </v-col>
                      <!-- #endregion -->

                      <!-- SECTOR -->
                      <!-- #region -->
                      <v-col
                        cols="12"
                        v-if="
                          item.isDocBuku2d ||
                          item.isDocBuku1d ||
                          item.isDocBuku4
                        "
                      >
                        <p
                          class="pb-1 text-left text-darkBlue font-weight-bold"
                        >
                          Sector<span class="text-gradient-red">*</span>
                        </p>
                        <v-radio-group
                          inline
                          style="margin-left: -8px"
                          v-model="state.sections[i].sector"
                          :error-messages="
                            getNestedErrorMessage(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].sector,
                              {
                                required: 'Required',
                              }
                            )
                          "
                          :hide-details="
                            !hasNestedError(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].sector
                            )
                          "
                        >
                          <v-radio
                            v-for="(item, index) in listSector"
                            :key="index"
                            :value="item.id"
                            :label="item.value"
                            color="#065695"
                            class="me-5"
                          ></v-radio>
                        </v-radio-group>
                      </v-col>
                      <!-- #endregion -->

                      <!-- HEADER -->
                      <!-- #region -->
                      <v-col cols="12">
                        <p
                          class="pb-1 text-left text-darkBlue font-weight-bold"
                        >
                          Do you want to make it as a header?<span
                            class="text-gradient-red"
                            >*</span
                          >
                        </p>
                        <v-radio-group
                          inline
                          style="margin-left: -8px"
                          v-model="state.sections[i].isHeader"
                          :error-messages="
                            getNestedErrorMessage(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].isHeader,
                              {
                                required: 'Required',
                              }
                            )
                          "
                          :hide-details="
                            !hasNestedError(
                              v$.sections,
                              v$.sections.$each.$response.$errors[i].isHeader
                            )
                          "
                        >
                          <v-radio
                            label="Yes"
                            :value="true"
                            color="#065695"
                            class="me-5"
                          ></v-radio>
                          <v-radio
                            label="No"
                            :value="false"
                            color="#065695"
                          ></v-radio>
                        </v-radio-group>
                      </v-col>
                      <!-- #endregion -->
                    </v-row>
                  </div>
                  <div class="align-self-center mx-2">
                    <div
                      v-if="i != state.sections.length - 1"
                      :style="{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '10px',
                      }"
                    >
                      <v-btn
                        color="#CB3A31"
                        variant="outlined"
                        icon="mdi-delete"
                        class="btn-icon"
                        @click="handleDelete(i)"
                      ></v-btn>
                    </div>
                    <div
                      v-else
                      :style="{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '10px',
                      }"
                    >
                      <v-btn
                        v-if="state.sections.length != 1"
                        color="#CB3A31"
                        variant="outlined"
                        icon="mdi-delete"
                        class="btn-icon"
                        @click="handleDelete(i)"
                      ></v-btn>
                      <v-btn
                        variant="elevated"
                        icon="mdi-plus"
                        size="x-large"
                        class="primary-gradient btn-icon"
                        @click="handleAdd"
                      ></v-btn>
                    </div>
                  </div>
                </div>
              </v-col>
            </template>
          </v-row>
        </v-card-text>
        <v-card-actions class="d-flex p-2 justify-end px-6 py-4 form-action">
          <v-btn
            elevation="3"
            style="color: #065695"
            class="item-btn font-weight-medium"
            @click="closeDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            elevation="3"
            color="#065695"
            size="large"
            class="item-btn item-add"
            style="color: white"
            @click="handleCreate"
            :loading="store.getters['adminStore/getLoading']"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </Teleport>
</template>
<script lang="ts" setup>
import {
  ref,
  defineExpose,
  computed,
  getCurrentInstance,
  defineProps,
} from "vue";
import { helpers, required, requiredIf } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import { useStore } from "vuex";
import {
  semicolonRegex,
  getNestedErrorMessage,
  hasNestedError,
} from "@/v2/helpers/validation";
import { DocTypeToSectorMap } from "@/v2/enum/Enum";

const emit = defineEmits(["onSuccess"]);
const { root } = getCurrentInstance() as any;
const dialog = ref<boolean>(false);
const listSector = ref<any>([]);
const store = useStore();
const labelDialog = ref("Add Section");
const itemSubSection = ref();
const isSubSection = computed(() => {
  return (
    itemSubSection.value && itemSubSection.value.idMBPSectionTemplate != null
  );
});
const prop = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
});

const state = ref({
  sections: [
    {
      title: null,
      isHeader: null,
      sector: null,
    },
  ],
});

const closeDialog = () => {
  dialog.value = false;
};

defineExpose({ openDialog });

function openDialog(_item: any) {
  if (_item) {
    // value untuk add subsection
    itemSubSection.value = _item;
    labelDialog.value = "Add Sub Section";
  } else {
    labelDialog.value = "Add Section";
    itemSubSection.value = {};
  }
  state.value.sections = [
    {
      title: null,
      isHeader: null,
      sector: null,
    },
  ];
  dialog.value = true;
}

const handleAdd = () => {
  state.value.sections.push({
    title: null,
    isHeader: null,
    sector: null,
  });
};

const handleDelete = (index: number) => {
  state.value.sections.splice(index, 1);
};

const rules = computed(() => {
  const localRule = {
    sections: {
      $each: helpers.forEach({
        title: { required, sectionRegex: semicolonRegex },
        isHeader: { required: requiredIf(() => !isSubSection.value) },
        sector: {
          required: requiredIf(() =>
            Object.keys(DocTypeToSectorMap).some((key) => prop.item[key])
          ),
        },
      }),
    },
  };
  return localRule;
});

const v$ = useVuelidate(rules, state);
store.dispatch("eFormStore/getListSectorPredefine").then(({ responseData }) => {
  const matchedEntry = Object.entries(DocTypeToSectorMap).find(
    ([key]) => prop.item[key]
  );
  if (matchedEntry) {
    listSector.value = responseData.filter(
      (item) => item.type === matchedEntry[1]
    );
  }
});

const handleCreate = () => {
  v$.value.$validate().then((res) => {
    if (res) {
      isSubSection.value ? storeSubSection() : storeSection();
    }
  });
};

function storeSubSection() {
  const req = {
    idMBPDoc: prop.item.idMBPDocumentTemplate,
    idMBPSection: itemSubSection.value.idMBPSectionTemplate,
    arraySubSection: [] as any[],
  };

  state.value.sections.forEach((item) => {
    const section = {
      eFormName: item.title,
      idMSector: item.sector == null ? 0 : item.sector,
    };
    req.arraySubSection.push(section);
  });

  store
    .dispatch("adminStore/storeSubSection", req)
    .then((res) => {
      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
    })
    .catch((err) => {
      const errMessage = err?.response?.data
        ? JSON.parse(err.response.data)?.responseMessage
        : "Failed Added Section";
      root.refs.toast.show({
        message: errMessage,
        color: "error",
        timeout: 3000,
      });
    })
    .finally(() => {
      closeDialog();
      emit("onSuccess", true);
    });
}
function storeSection() {
  const req = {
    idMBPDoc: prop.item.idMBPDocumentTemplate,
    arraySection: [] as any[],
  };

  state.value.sections.forEach((item) => {
    const section = {
      sectionName: item.title,
      isHeader: item.isHeader,
      idMSector: item.sector == null ? 0 : item.sector,
    };
    req.arraySection.push(section);
  });

  store
    .dispatch("adminStore/storeSection", req)
    .then((res) => {
      root.refs.toast.show({
        message: res.responseMessage,
        color: "success",
        timeout: 3000,
      });
    })
    .catch((err) => {
      const errMessage = err?.response?.data
        ? JSON.parse(err.response.data)?.responseMessage
        : "Failed Added Section";
      root.refs.toast.show({
        message: errMessage,
        color: "error",
        timeout: 3000,
      });
    })
    .finally(() => {
      closeDialog();
      emit("onSuccess", true);
    });
}
</script>
<style scoped>
.form-title {
  margin-top: -15px;
  margin-left: 20px;
  background-color: white;
  width: fit-content;
}
:deep(.v-field--variant-solo, .v-field.v-field--appended) {
  border-radius: 12px !important;
}
.btn-icon {
  width: 41px !important;
  height: 41px !important;
}
:deep(.btn-icon.v-btn) {
  border-radius: 12px !important;
  padding: 8px !important;
}
:deep(.v-text-field .v-input__details) {
  padding-inline-start: 0;
}
:deep(.v-field--disabled) {
  background-color: rgb(196, 186, 186) !important;
}
.line {
  margin-top: -10px !important;
  margin-bottom: 40px;
  border: none; /* Remove the default border */
  height: 2px; /* Set the height of the hr */
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}
.form-action {
  gap: 0.5rem;
  display: flex;
  justify-content: end;
  align-items: center;
  button {
    border-radius: 10px !important;
  }
}
.item-btn {
  height: 45px !important;
  font-size: 15px !important;
  padding-left: 1rem;
  padding-right: 1rem;
}
.item-btn.item-add {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}
</style>
