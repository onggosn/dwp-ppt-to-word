<template>
  <v-dialog
    v-model="dialog"
    width="900"
    persistent
    :class="[isShowDialog ? 'show' : 'hide']"
  >
    <v-card class="border-radius-dwp">
      <v-card-title class="text-center mt-3">
        <h3 class="text-h6 font-weight-regular">Create Event</h3>
        <v-btn
          density="default"
          icon="mdi-close"
          variant="text"
          class="btn-close"
          @click="onclose()"
        />
      </v-card-title>
      <hr class="line mt-3" />

      <Steppy
        v-model:step="step"
        nextText="Next"
        backText="Back"
        doneText="Create"
        :tabs="tabs"
      >
        <template #1>
          <v-form ref="form">
            <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
              Event Type
            </p>
            <v-autocomplete
              :loading="store.getters['eventStore/getLoading']"
              v-model="eventType"
              :items="listType"
              variant="solo"
              placeholder="Choose Event Type"
              class="pl-2 pr-2"
              item-title="value"
              return-object
            ></v-autocomplete>
            <v-autocomplete
              :loading="store.getters['eventStore/getLoading']"
              v-model="eventSubType"
              v-if="eventType"
              :items="listSubType"
              variant="solo"
              :placeholder="`Choose ${eventName} Type`"
              class="pl-2 pr-2"
              item-title="value"
              item-value="id"
              return-object
            ></v-autocomplete>
            <v-autocomplete
              :loading="store.getters['eventStore/getLoading']"
              v-model="eventSubSubType"
              v-if="showLast"
              :items="listSubSubType"
              variant="solo"
              :placeholder="`Choose ${eventSubTypeName} Type`"
              item-title="value"
              return-object
              class="pl-2 pr-2"
            ></v-autocomplete>
          </v-form>
        </template>
        <template #2>
          <v-container class="mt-n5">
            <v-row no-gutters>
              <v-col cols="12" :sm="canShowWeek ? '6' : '8'">
                <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                  Event Name
                </p>
                <v-chip :class="chipClass">
                  <p class="ellipsis-text">
                    {{ fullEventName || eventSubSubTypeName }}
                  </p>
                </v-chip>
              </v-col>
              <v-col v-if="canShowWeek" cols="12" sm="2">
                <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                  Week
                </p>
                <v-chip :class="chipClass">
                  <p>{{ weekName || "ex. M1" }}</p>
                </v-chip>
              </v-col>
              <v-col cols="12" sm="2">
                <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                  Month
                </p>
                <v-chip :class="chipClass">
                  <p>{{ monthName || "ex. Januari" }}</p>
                </v-chip>
              </v-col>
              <v-col cols="12" sm="2">
                <p class="ml-2 pb-1 text-left text-darkBlue font-weight-bold">
                  Year
                </p>
                <v-chip :class="chipClass">
                  <p>{{ yearName || "ex. 2025" }}</p>

                  <!-- <template v-slot:append>
                      <img :src="require('@/v2/assets/icon/date.svg')" />
                    </template> -->
                </v-chip>
              </v-col>
            </v-row>

            <p class="ml-2 pb-1 pt-4 text-left text-darkBlue font-weight-bold">
              Date
            </p>
            <VueDatePicker
              v-model="datePicker"
              :year-range="[minYear, maxYear]"
              :enable-time-picker="false"
              :month-change-on-scroll="false"
              auto-apply
              model-type="dd/MM/yyyy"
              :disabled-dates="disabledDates"
              :alt-position="() => ({ top: -280, left: 0 })"
            >
              <template #trigger>
                <v-text-field
                  variant="solo"
                  :placeholder="
                    [1, 2].includes(eventSubSubType?.id)
                      ? 'Choose Date H2 RDGB'
                      : 'Choose Date'
                  "
                  class="pl-2 pr-2"
                  :value="datePicker"
                  :hide-details="!isError"
                  :error-messages="messageError"
                >
                  <template v-slot:append-inner>
                    <img :src="require('@/v2/assets/icon/date.svg')" />
                  </template>
                </v-text-field>
              </template>

              <template #calendar-header="{ index, day }">
                <div :class="index === 5 || index === 6 ? 'red-color' : ''">
                  {{ day }}
                </div>
              </template>
            </VueDatePicker>
            <template v-if="progress > 0">
              <LoadingProgressBar ref="modal" />
            </template>
          </v-container>
        </template>
      </Steppy>
      <div class="text-right pb-5 pr-15 mt-n10">
        <v-btn
          class="btn-prev mr-3"
          @click="negativeClick"
          elevation="4"
          width="100"
          height="45"
          >{{ step == 1 ? "Cancel" : "Back" }}</v-btn
        >
        <v-btn
          class="btn-next"
          @click="positiveClick"
          elevation="4"
          width="100"
          height="45"
          :loading="store.getters['eventStore/getLoading']"
          :disabled="!buttonNext"
          >{{ step != 2 ? "Next" : "Create" }}</v-btn
        >
      </div>
    </v-card>
  </v-dialog>

  <ModalConfirm
    ref="modalFailedSubmit"
    :form-config="failSubmit"
    @action-confirm="cancelSubmitDocument()"
    :is-warning="true"
  >
    <template v-slot:icon-img>
      <img
        :src="require('@/v2/assets/icon/failed-submit-warning.png')"
        style="
          width: 80px;
          margin-top: -60px;
          filter: drop-shadow(#9b9b9b 2px 2px 3px);
        "
      />
    </template>
  </ModalConfirm>
</template>
<script setup lang="ts">
import { ref, reactive, watch, computed, defineExpose } from "vue";
import { Steppy } from "vue3-steppy";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import LoadingProgressBar from "@/v2/components/loading/LoadingProgressBar.vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { TModalConfirm } from "@v2/Type.d";
import { getWeekNumber } from "@/v2/helpers/DateHelper";

const disabledDates = [
  // Disable an array of dates
  // new Date(2024, 1, 16),
  // new Date(2024, 1, 17),
  // new Date(),
  // new Date(2024, 1, 18),
];
const modalFailedSubmit = ref();
const store = useStore();
const router = useRouter();

const dialog = ref(false);
const listType = ref([]);
const eventType = ref(null);
const eventName = ref();

const progress = computed(() => {
  return store.getters["loadingStore/getProgress"];
});

const isShowDialog = computed(() => {
  return progress.value >= 0 && progress.value <= 100;
});

const canShowWeek = computed(() => {
  if (eventSubSubType.value) {
    return eventSubSubType.value.id == 6;
  }
  return false;
});

const modal = ref();
const showDialogEvent = () => {
  dialog.value = true;
  store.dispatch("eventStore/fetchListEventType").then((data) => {
    listType.value = data;
  });
};

defineExpose({
  showDialogEvent,
});

const listSubType = ref([]);
const eventSubType = ref(null);
const eventSubTypeName = ref();

watch(eventType, (val: any) => {
  if (val) {
    eventName.value = val.value;
    buttonNext.value = false;
    showLast.value = false;
    eventSubSubType.value = null;
    eventSubType.value = null;

    store
      .dispatch("eventStore/fetchListSubEventType", val.id)
      .then((data) => (listSubType.value = data));
  }
});

const form = ref();
const listSubSubType = ref([]);
const eventSubSubType = ref<any>();
const eventSubSubTypeName = ref();

watch(eventSubType, (val: any) => {
  if (eventSubType.value == null) return;
  if (val) {
    eventSubTypeName.value = val.value;

    store
      .dispatch("eventStore/fetchListSubSubEventType", val.id)
      .then((data) => {
        showLast.value = true;
        listSubSubType.value = data;
      });
  }
});

const eventDate = ref();
const showLast = ref(false);
const buttonNext = ref(false);
const datePicker = ref<any>();
const monthName = ref<string>("");
const weekName = ref<string | number>("");
const yearName = ref<string>("");
const fullEventName = ref();
const currentYear = new Date().getFullYear();

const failSubmit = ref<TModalConfirm>({
  title: "Oops",
  message: "",
  btnSubmitLabel: "Close",
  width: 500,
  btnSubmitColor: "primary-gradient",
});

// 5 years before the current date
const minYear = computed(() => currentYear - 5);
// 10 years ahead of the current date
const maxYear = computed(() => currentYear + 100);

const step = ref(1);
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
]);

watch(step, () => {
  if (
    eventType.value !== null &&
    eventSubType.value !== null &&
    eventSubSubType.value !== null
  ) {
    buttonNext.value = true;
  }

  if (eventType.value == null) {
    buttonNext.value = false;
  }
});

watch(datePicker, (val) => {
  if (datePicker.value == null) return;
  if (val) {
    weekName.value = getWeekNumber(val);
    var dateString: string = val;
    var parts = dateString.split("/");

    monthName.value = months[parseInt(parts[1])];
    yearName.value = parts[2];
    fullEventName.value = `${eventSubSubTypeName.value} ${monthName.value} ${yearName.value}`;
    buttonNext.value = true;

    var date_parts = datePicker.value.split("/");
    eventDate.value = date_parts[2] + "-" + date_parts[1] + "-" + date_parts[0];
    errorState.value.message = "";
    errorState.value.hasError = false;
  }
});

watch(eventSubSubType, (val: any) => {
  if (eventSubSubType.value == null) return;
  eventSubSubTypeName.value = val.value;
  buttonNext.value = true;
  datePicker.value = null;
  monthName.value = "";
  yearName.value = "";
  weekName.value = "";
  fullEventName.value = "";
});

watch(step, (val) => {
  if (val == 2 && datePicker.value == null) {
    buttonNext.value = false;
  }
});

const oncloseState = () => {
  step.value = 1;
  showLast.value = false;
  eventType.value = null;
  datePicker.value = null;
  dialog.value = false;
  buttonNext.value = false;
  eventSubType.value = null;
  eventSubSubType.value = null;
  errorState.value.message = "";
  errorState.value.hasError = false;
};

const negativeClick = () => {
  if (step.value > 1) {
    step.value--;
  } else {
    oncloseState();
  }
};
const errorState = ref({
  message: "",
  hasError: false,
});

// ID sub-sub-type event yang tidak perlu validasi bulan
const NO_MONTH_VALIDATION_IDS = [4, 6]; // 4: RDGTK, 6: Mingguan

// Kelompok bulan untuk validasi tipe RDGB (1-based)
const RDGB_MONTHS = [2, 3, 5, 6, 8, 9, 11, 12]; // Feb, Mar, Mei, Jun, Agu, Sep, Nov, Des
const RDGTW_MONTHS = [1, 4, 7]; // Jan, Apr, Jul
const RDGBT_MONTHS = [10]; // Okt

const RDGB_ID = 1;
const RDGTW_ID = 2;
const RDGT_ID = 3;

const messageError = computed((): string => {
  if (!eventDate.value) return errorState.value.message;

  const month = new Date(eventDate.value).getMonth() + 1;
  const subTypeId = eventSubSubType.value?.id;

  if (NO_MONTH_VALIDATION_IDS.includes(subTypeId)) {
    return errorState.value.message;
  }

  if (RDGB_MONTHS.includes(month) && subTypeId !== RDGB_ID) {
    return "Tipe RDGB tidak sesuai. Event pada bulan tersebut digunakan pada RDGB Bulanan.";
  }

  if (RDGTW_MONTHS.includes(month) && subTypeId !== RDGTW_ID) {
    return "Tipe RDGB tidak sesuai. Event pada bulan tersebut digunakan pada RDGB Triwulanan.";
  }

  if (RDGBT_MONTHS.includes(month) && subTypeId !== RDGT_ID) {
    return "Tipe RDGB tidak sesuai. Event pada bulan tersebut digunakan pada RDGB Tahunan.";
  }

  return errorState.value.message;
});

const isError = computed((): boolean => {
  return messageError.value !== "" || errorState.value.hasError;
});
const chipClass = computed(() => {
  return isError.value
    ? "error-border chip-shadow border-radius-dwp mr-2"
    : "chip-shadow border-radius-dwp mr-2";
});

import { getCurrentInstance } from "vue";
import { includes } from "lodash";
const instance: any = getCurrentInstance()?.root.refs;
const positiveClick = () => {
  if (step.value == 2) {
    if (isError.value === false) {
      const interval = setInterval(() => {
        let newValue = store.getters["loadingStore/getProgress"] + 1;
        if (store.getters["loadingStore/getProgress"] < 98) {
          store.dispatch("loadingStore/updateProgress", newValue);
        }
      }, 50);

      const payload = {
        eventName: fullEventName.value,
        idEventSubTypeList: eventSubSubType.value.id,
        eventDate: eventDate.value,
        week: weekName.value,
        bundleVersion: process.env.VUE_APP_CKEDITOR_BUNDLE_VERSION,
      };

      store
        .dispatch("eventStore/insertEvent", payload)
        .then((res) => {
          store.dispatch("loadingStore/updateProgress", 100);
          if (res.responseCode === "011024") {
            failSubmit.value.message = res.responseMessage;
            modalFailedSubmit.value.show({});
            errorState.value.message = res.responseMessage.split(".")[0] + ".";
            errorState.value.hasError = true;
          } else if (res.responseCode === "011000") {
            instance.toast.show({
              message: res.responseMessage,
              color: "success",
              timeout: 3000,
            });
            oncloseState();
            router.push({ name: "v2.meeting-management" });
          } else {
            instance.toast.show({
              message: "something went wrong!",
              color: "warning",
              timeout: 3000,
            });
          }
        })
        .finally(() => {
          clearInterval(interval);
          store.dispatch("loadingStore/updateProgress", 0);
        });
    }
  } else {
    step.value++;
  }
};

const onclose = () => {
  step.value = 1;
  showLast.value = false;
  eventType.value = null;
  datePicker.value = null;
  dialog.value = false;
  eventSubType.value = null;
  eventSubSubType.value = null;
  buttonNext.value = false;
  errorState.value.message = "";
  errorState.value.hasError = false;
};

const months = [
  "-",
  "Januari",
  "Februari",
  "Maret",
  "April",
  "Mei",
  "Juni",
  "Juli",
  "Agustus",
  "September",
  "Oktober",
  "November",
  "Desember",
];
function cancelSubmitDocument() {
  modalFailedSubmit.value.hide();
  errorState.value.message = "";
  errorState.value.hasError = false;
}
</script>

<style lang="scss" scoped>
.ellipsis-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 320px;
}

.error-border {
  border: 1px solid #b13737 !important;
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
  height: 56px !important;
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

.text-blueRedTheme-gradien {
  background: -webkit-linear-gradient(left, #267dc2, #ff000d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
  height: 2px; /* Set the height of the hr */
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
  margin-top: 25px;
  margin-left: 25%;
  margin-right: 25%;
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
</style>
