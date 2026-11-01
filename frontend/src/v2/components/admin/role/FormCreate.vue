<template>
  <v-btn
    prepend-icon="mdi-plus"
    class="bg-gradient-darkblue font-weight-bold"
    elevation="4"
    style="color: white; border-radius: 10px"
    @click="openDialog"
  >
    Add Formasi ADG
  </v-btn>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="1000" persistent>
      <v-card class="border-radius-dwp red-lighten-1">
        <v-card-title class="text-center mt-2">
          <h3 class="text-h6 my-3 font-weight-regular">Add Formasi ADG</h3>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="closeDialog"
          />
        </v-card-title>
        <hr class="line mt-3" />
        <v-form v-if="loadingForm" style="padding: 40px">
          <v-row no-gutters class="mt-5">
            <v-col cols="12" v-for="index in 5" :key="index" class="mb-2">
              <free-style-shimmer
                :is-loading="true"
                width="100%"
                height="40px"
                border-radius="10px"
              />
            </v-col>
          </v-row>
        </v-form>
        <v-form v-else ref="form">
          <Steppy v-model:step="step" :tabs="tabs">
            <template #1>
              <v-card-text>
                <v-row
                  class="rounded-lg px-2 mt-2 pb-5 mx-2"
                  style="border: 2px #babcca solid"
                >
                  <span class="text-darkBlue font-weight-bold form-title">
                    ADG {{ detailPage }}
                  </span>

                  <v-col cols="12" class="pb-0">
                    <form-label :text="'Nama ADG'" important />
                    <SearchBar
                      v-model="selectedItems[detailPage - 1]"
                      :is-admin="false"
                      :type="'global'"
                      @selected="catchValue"
                      placeHolderSearch="Input Name"
                      hideIcon
                    />
                  </v-col>

                  <v-col cols="12" class="pb-0">
                    <form-label :text="'Pangkat'" important />
                    <v-text-field
                      variant="solo"
                      placeholder="Input Pangkat"
                      disabled
                      v-model="formADG.detailADG[detailPage - 1].pangkat"
                      :error-messages="
                        checkNestedError(
                          v$.detailADG.$each.$response.$errors[detailPage - 1]
                            ?.pangkat
                        )
                      "
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" class="pb-0">
                    <form-label :text="'Jabatan'" important />
                    <v-text-field
                      variant="solo"
                      placeholder="Input Jabatan"
                      disabled
                      v-model="formADG.detailADG[detailPage - 1].jabatan"
                      :error-messages="
                        checkNestedError(
                          v$.detailADG.$each.$response.$errors[detailPage - 1]
                            ?.jabatan
                        )
                      "
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" class="pb-0">
                    <form-label :text="'Email'" important />
                    <v-text-field
                      disabled
                      variant="solo"
                      placeholder="Input Email"
                      v-model="formADG.detailADG[detailPage - 1].email"
                      :error-messages="
                        checkNestedError(
                          v$.detailADG.$each.$response.$errors[detailPage - 1]
                            ?.email
                        )
                      "
                    />
                  </v-col>

                  <v-col cols="12" class="pb-0">
                    <form-label :text="'Bidang'" important />
                    <v-text-field
                      variant="solo"
                      placeholder="Input Bidang"
                      v-model="formADG.detailADG[detailPage - 1].adgBidang"
                      :error-messages="
                        checkNestedError(
                          v$.detailADG.$each.$response.$errors[detailPage - 1]
                            ?.adgBidang
                        )
                      "
                    />
                  </v-col>
                </v-row>
                <div class="list-action">
                  <div class="button-cover">
                    <v-btn
                      class="btn btn-primary"
                      elevation="4"
                      height="45"
                      align-self="center"
                      @click="addListDetail"
                      :disabled="v$.detailADG.$invalid"
                    >
                      <v-icon>mdi-plus</v-icon>
                      Add ADG
                    </v-btn>
                    <v-btn
                      v-if="formADG.detailADG.length > 1"
                      :color="'red'"
                      class="btn btn-danger"
                      elevation="4"
                      width="100"
                      height="45"
                      @click="removeListDetail"
                    >
                      <v-icon>mdi-delete</v-icon>
                      Delete
                    </v-btn>
                  </div>
                  <v-pagination
                    :total-visible="1"
                    v-model="detailPage"
                    show-first-last-page
                    class="adg-pagination"
                    :length="formADG.detailADG.length"
                    first-icon="mdi-chevron-double-left"
                    last-icon="mdi-chevron-double-right"
                  ></v-pagination>
                </div>
              </v-card-text>
            </template>
            <template #2>
              <v-row>
                <v-col cols="12">
                  <form-label text="Detail Event Banner" :important="true" />
                  <InputImageArea
                    v-model="formADG.bannerEventDetail"
                    v-model:fileName="formADG.bannerEventDetailExtention"
                  />
                </v-col>
                <v-col cols="12">
                  <form-label text="Homepage Event Banner" :important="true" />
                  <InputImageArea
                    v-model="formADG.homepageEventBanner"
                    v-model:fileName="formADG.homepageEventBannerExtention"
                  />
                </v-col>
                <v-col cols="12">
                  <form-label text="Effective Date" :important="true" />
                  <VueDatePicker
                    v-model="formADG.effectiveDate"
                    :enable-time-picker="false"
                    :month-change-on-scroll="false"
                    auto-apply
                    model-type="dd/MM/yyyy"
                    :alt-position="() => ({ top: -280, left: 0 })"
                  >
                    <template #trigger>
                      <v-text-field
                        variant="solo"
                        placeholder="Select Effective Date"
                        class="pl-2 pr-2"
                        :model-value="formADG.effectiveDate"
                        readonly
                      >
                        <template v-slot:append-inner>
                          <v-img
                            :width="30"
                            :src="require('@/v2/assets/icon/date.svg')"
                          />
                        </template>
                      </v-text-field>
                    </template>

                    <template #calendar-header="{ index, day }">
                      <div
                        :class="index === 5 || index === 6 ? 'red-color' : ''"
                      >
                        {{ day }}
                      </div>
                    </template>
                  </VueDatePicker>
                </v-col>
                <v-col cols="12">
                  <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                    Status<span style="color: red">*</span>
                  </p>
                  <v-radio-group
                    v-model="formADG.status"
                    inline
                    style="margin-left: -8px"
                    hide-details
                  >
                    <v-radio
                      label="Active"
                      :value="'active'"
                      color="#757575"
                      class="me-2"
                    >
                      <template v-slot:label>
                        <span style="color: #404040">Active</span>
                      </template>
                    </v-radio>
                    <v-radio
                      label="Inactive"
                      :value="'inactive'"
                      color="#757575"
                      class="me-2"
                    >
                      <template v-slot:label>
                        <span style="color: #404040">In Active</span>
                      </template>
                    </v-radio>
                  </v-radio-group>
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
              Cancel
            </v-btn>
            <v-btn
              class="btn-next"
              @click="positiveClick"
              elevation="4"
              width="100"
              height="45"
              :disabled="isLastStep ? v$.$invalid : v$.detailADG.$invalid"
            >
              {{ isLastStep ? "Add" : "Next" }}
            </v-btn>
          </div>
        </v-form>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import {
  computed,
  getCurrentInstance,
  nextTick,
  reactive,
  ref,
  onMounted,
  toRaw,
} from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import { Steppy } from "vue3-steppy";
import { required, email, helpers } from "@vuelidate/validators";
import {
  type DetailFormADG as DetailADG,
  type FormADG,
  type ParamsListADG,
} from "@/v2/Type";
import useVuelidate from "@vuelidate/core";
import SearchBar from "@v2/components/collaboration/SearchBar.vue";
import InputImageArea from "@v2/components/units/input/InputImageArea.vue";
import FormLabel from "@v2/components/units/label/FormLabel.vue";

const emit = defineEmits(["onSuccess"]);

const createDetailADG = (): DetailADG => ({
  username: "",
  namaADG: "",
  jabatan: "",
  pangkat: "",
  email: "",
  adgBidang: "",
});

const createFormADG = (): FormADG => ({
  bannerEventDetail: "",
  bannerEventDetailExtention: "",
  homepageEventBanner: "",
  homepageEventBannerExtention: "",
  effectiveDate: "",
  status: "participant",
  detailADG: [createDetailADG()],
});

const formADG = reactive<FormADG>(createFormADG());

const props = defineProps({
  isDocSectoral: {
    type: Boolean,
    default: false,
  },
  approvalData: {
    type: Object,
    default: () => ({}),
  },
});

const tabs = reactive([
  {
    title: "Step 1",
    iconSuccess: "",
    isValid: true,
  },
  {
    title: "Step 2",
    iconSuccess: "",
    isValid: true,
  },
]);

const dialog = ref(false);
const step = ref(1);
const itemsMemberApproval = ref<any>();
const detailPage = ref<number>(1);
const loadingForm = ref<boolean>(false);
const selectedItems = ref<any[]>([null]);

const route = useRoute();
const store = useStore();

const vm = getCurrentInstance() as any;

const mandatory = helpers.withMessage("Wajib diisi", required);

const rules = computed(() => ({
  bannerEventDetail: { mandatory },
  bannerEventDetailExtention: { mandatory },
  homepageEventBanner: { mandatory },
  homepageEventBannerExtention: { mandatory },
  effectiveDate: { mandatory },
  status: { mandatory },

  detailADG: {
    $each: helpers.forEach({
      username: {},
      namaADG: { mandatory },
      jabatan: {},
      pangkat: {},
      email: {
        mandatory,
        email: helpers.withMessage("Format email tidak valid", email),
      },
      adgBidang: { mandatory },
    }),
  },
}));

const v$ = useVuelidate(rules, formADG, {
  $autoDirty: true,
});

const isLastStep = computed((): boolean => step.value == tabs.length);
const isDocument2d = computed(
  () => store.getters["collaborationStore/getDocumentSectoral"]
);
const params = computed<ParamsListADG>(
  () => store.getters["adminStore/getParamsListADG"]
);

const showToast = async (opts: {
  message: string;
  color: string;
  timeout?: number;
}) => {
  await nextTick();
  vm?.root?.refs?.toast?.show?.({ timeout: 3000, ...opts });
};

const openDialog = () => (dialog.value = true);
const closeDialog = () => {
  dialog.value = false;
  resetModalForm();
};

function resetModalForm() {
  step.value = 1;
  detailPage.value = 1;
  selectedItems.value = [];

  Object.assign(formADG, createFormADG());
  v$.value?.$reset?.();
}

function checkNestedError(item?: Array<{ $message: string }>) {
  return item?.[0]?.$message ?? "";
}

function catchValue(res: any) {
  const idx = detailPage.value - 1;

  formADG.detailADG[idx] = {
    ...formADG.detailADG[idx],
    email: res.inputEmail ?? "",
    username: res.username ?? "",
    namaADG: res.value ?? "",
    jabatan: res.jabatanName ?? "",
    pangkat: res.gradeName ?? "",
  };
}

function negativeClick() {
  if (step.value > 1) {
    step.value--;
  } else {
    closeDialog();
  }
}

function toIsoWithTime(dateStr, timeStr = "00:00:00Z") {
  const [dd, mm, yyyy] = dateStr.split("/");
  return `${yyyy}-${mm.padStart(2, "0")}-${dd.padStart(2, "0")}T${timeStr}`;
}

async function positiveClick() {
  if (step.value < tabs.length) {
    step.value++;
    return;
  }

  const ok = await v$.value.$validate();
  if (!ok) return;

  try {
    loadingForm.value = true;
    const payload = {
      ...toRaw(formADG),
      username: store.state.username,
      effectiveDate: toIsoWithTime(formADG.effectiveDate),
    };

    await store.dispatch("adminStore/createADG", payload);
    await store.dispatch("adminStore/getListADG", params.value);
    await showToast({ message: "Successfully Saved", color: "success" });

    emit("onSuccess", true);
    closeDialog();
  } catch (e) {
    await showToast({ message: "Sorry, failed Saved", color: "error" });
  } finally {
    loadingForm.value = false;
  }
}

function addListDetail() {
  formADG.detailADG.push(createDetailADG());
  selectedItems.value.push(null);
  detailPage.value += 1;
}

function removeListDetail() {
  const idx = detailPage.value - 1;
  formADG.detailADG.splice(idx, 1);
  selectedItems.value.splice(idx, 1);

  if (detailPage.value > formADG.detailADG.length) {
    detailPage.value = formADG.detailADG.length;
  }
  if (detailPage.value < 1) detailPage.value = 1;
}

onMounted(() => {
  getUserApproval();
});

const getUserApproval = () => {
  const reqData = isDocument2d.value
    ? {
        id: route.params.idDoc,
        idSector: props.approvalData.idMSector,
      }
    : {
        id: route.params.idDoc,
      };

  store.dispatch("eFormStore/GetListBpDocApproval", reqData).then((res) => {
    if (res) {
      const { responseData } = res;

      const data = responseData.map((el: any) => {
        const { value: name, id, jabatanSatker: department } = el;

        return {
          name,
          type: "person",
          id,
          inputName: el.value,
          value: el.value,
          department,
        };
      });

      itemsMemberApproval.value = data;
    }
  });
};
</script>

<style lang="scss" scoped>
.btn-close {
  position: absolute;
  right: 0;
  top: 0;
  margin-top: 10px;
  margin-right: 10px;
}

.line {
  margin-top: -10px !important;
  margin-bottom: 40px;
  border: none;
  height: 2px;
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
}

.btn-next,
.btn-primary,
.btn-danger {
  border-radius: 10px !important;
  border-color: #267dc2 !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: white;
  font-weight: 900;
}

.btn-next,
.btn-primary {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
}

.btn-prev {
  background: white;
  border-radius: 10px !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
  font-size: 14px !important;
  color: #267dc2;
  font-weight: 900;
}

.form-title {
  margin-top: -15px;
  margin-left: 20px;
  background-color: white;
  width: fit-content;
}

:deep(.adg-pagination) {
  ul.v-pagination__list li {
    margin: 0;
    color: #267dc2;

    button span.v-btn__overlay {
      background: none !important;
    }
    button.v-btn--icon.v-btn--density-default {
      width: fit-content !important;
    }
    button.v-btn--size-default {
      --v-btn-height: 1rem !important;
      padding: 0 0.2rem;
    }

    & i {
      font-size: 2rem !important;
    }
    &.v-pagination__item--is-active span {
      font-size: 1.2rem !important;
      font-weight: 600 !important;
    }
    &.v-pagination__first i,
    &.v-pagination__last i {
      font-size: 1.5rem !important;
    }
  }
}

/* Vuetify field/text-field tweaks */
:deep(.v-field--variant-solo, .v-field.v-field--appended) {
  border-radius: 12px !important;
}

:deep(.v-text-field .v-input__details) {
  padding-inline-start: 0;
}

:deep(.v-field--disabled) {
  background-color: rgb(196, 186, 186) !important;
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

/* Steppy overrides */
:deep(.steppy) {
  margin-left: 15vw;
  margin-right: 15vw;
}

:deep(.number) {
  display: none !important;
}

:deep(.wrapper-steppy) {
  padding-left: 20px !important;
  padding-right: 20px !important;
  padding-top: 25px;
  padding-bottom: 0px !important;
}

:deep(.steppy-pane) {
  box-shadow: none !important;
  text-align: left !important;
  .v-input__details .v-messages__message {
    text-align: left !important;
  }
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

/* (Optional) v-chip styling — keep kalau SearchBar memang pakai chip */
:deep(.v-chip__append) {
  position: absolute;
  right: 0;
  margin-right: 0.5vw;
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
.list-action {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: 40px;
  align-items: center;
}

.button-cover .btn {
  margin-right: 12px;
}
</style>
