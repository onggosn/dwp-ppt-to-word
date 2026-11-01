<template>
  <div>
    <Teleport to="body">
      <v-dialog v-if="!openPopUp" v-model="visibility" persistent width="800">
        <v-card v-if="!isLoading" class="border-radius-dwp px-5 wrapper">
          <v-card-title
            class="text-center mt-4 mb-2 font-weight-medium"
            style="color: #4b4b4b"
          >
            <div class="text-h6">{{ title }}</div>
            <v-btn
              class="mr-5 mt-3"
              style="position: absolute; right: 0; top: 0"
              fab
              small
              elevation="0"
              @click="close()"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <hr class="line mt-5 mb-4" />
          </v-card-title>
          <v-card-text>
            <v-form class="wrapper_form">
              <div>
                <div class="mb-2">Agenda</div>
                <v-text-field
                  v-model="form.agendaName"
                  required
                  variant="solo"
                  class="input-white"
                  placeholder="Insert Agenda"
                  :error-messages="
                    v$.agendaName.$errors.map((e) => 'Wajib diisi')
                  "
                ></v-text-field>
              </div>

              <div class="mb-2">Satker Penyaji</div>
              <v-autocomplete
                v-model="form.listPresentingUnit"
                chips
                :items="penyaji"
                return-object
                item-title="value"
                multiple
                closable-chips
                hide-selected
                searchable
                variant="solo"
                placeholder="Add satker penyaji"
              ></v-autocomplete>
              <div class="mb-2">Satker Diundang</div>
              <v-autocomplete
                v-model="form.listInvitedUnit"
                chips
                :items="diundang"
                return-object
                item-title="value"
                multiple
                closable-chips
                hide-selected
                searchable
                variant="solo"
                placeholder="Add satker Diundang"
              ></v-autocomplete>
              <div class="mb-2">Anggota Dewan Gubernur Bidang</div>
              <v-row class="mb-5">
                <v-col
                  cols="4"
                  style="padding: 5px"
                  v-for="item in members"
                  :key="item.id"
                >
                  <v-checkbox
                    v-model="selectedAdg"
                    :label="item.value"
                    color="success"
                    :value="item.id"
                    hide-details
                    class="checkbox-wrap"
                  ></v-checkbox>
                </v-col>
              </v-row>
              <div>
                <div class="py-3">Kehadiran Anggota Dewan Gubernur</div>
                <v-row class="mb-5">
                  <v-col
                    cols="4"
                    style="padding: 5px"
                    v-for="item in members"
                    :key="item.id"
                  >
                    <v-checkbox
                      v-model="attendanceAdg"
                      :label="item.value"
                      color="success"
                      :value="item.id"
                      hide-details
                      class="checkbox-wrap"
                    ></v-checkbox>
                  </v-col>
                </v-row>
              </div>
              <div>
                <div class="pt-3 mb-2">Room</div>
                <v-text-field
                  v-model="form.agendaPlace"
                  required
                  variant="solo"
                  class="input-white"
                  placeholder="Insert room name"
                ></v-text-field>
              </div>
            </v-form>
            <div>
              <div class="mb-2">Date<span style="color: red">*</span></div>
              <VueDatePicker
                v-model="form.date"
                :year-range="[minYear, maxYear]"
                :enable-time-picker="false"
                :month-change-on-scroll="false"
                auto-apply
                model-type="MM/dd/yyyy"
                :disabled="!inProgressEdit"
              >
                <template #trigger>
                  <v-text-field
                    :value="form.date"
                    variant="solo"
                    :disabled="!inProgressEdit"
                    placeholder="Choose Date"
                    :class="{ 'is-disabled': !inProgressEdit }"
                    :error-messages="
                      getErrorMessages(v$.date, {
                        required: 'Wajib diisi',
                        // endDatePicker:
                        //   'Tanggal berakhir agenda tidak boleh melebihi H + 7 event',
                      })
                    "
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
              <v-row>
                <v-col cols="4">
                  <div class="mb-2">Start Time</div>
                  <v-text-field
                    v-model="form.startTime"
                    variant="solo"
                    placeholder="Input start time"
                    :error-messages="[
                      ...v$.startTime.$errors.map((e) => e.$message.toString()),
                      timeOverlapMessage.start,
                    ]"
                    :disabled="!inProgressEdit"
                    :class="{ 'is-disabled': !inProgressEdit }"
                  >
                    <template v-slot:append-inner>
                      <v-icon color="#065391">mdi-clock-outline</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <div class="mb-2">Finish Time</div>
                  <v-text-field
                    v-model="form.endTime"
                    variant="solo"
                    placeholder="Input end time"
                    :error-messages="[
                      ...getErrorMessages(v$.endTime, {
                        required: 'Wajib diisi',
                        endTimePicker:
                          'Event tidak boleh berakhir sebelum dimulai',
                      }),
                      timeOverlapMessage.end,
                    ]"
                  >
                    <template v-slot:append-inner>
                      <v-icon color="#065391">mdi-clock-outline</v-icon>
                    </template>
                  </v-text-field>
                </v-col>
                <v-col cols="4">
                  <div class="mb-2">Minutes</div>
                  <v-chip class="chip-shadow border-radius-dwp">
                    {{ minutes }}
                  </v-chip>
                </v-col>
              </v-row>
            </div>
            <div>
              <div class="mb-2">Status</div>
              <v-chip
                v-if="title != 'Edit Agenda'"
                class="chip-shadow border-radius-dwp ml-2 mr-2"
              >
                {{
                  form.status == 23
                    ? "Waiting"
                    : form.status == 24
                    ? "In Progress"
                    : "Done"
                }}
              </v-chip>
              <v-chip v-else class="chip-shadow border-radius-dwp ml-2 mr-2">
                {{
                  form.status == 23
                    ? "Waiting"
                    : form.status == 24
                    ? "In Progress"
                    : "Done"
                }}
              </v-chip>
            </div>
          </v-card-text>
          <v-card-actions class="mr-4">
            <v-spacer />
            <v-btn
              class="btn-cancel mr-3"
              @click="close"
              elevation="4"
              width="100"
              height="45"
              :loading="isLoadingBtn"
              >Cancel</v-btn
            >
            <v-btn
              class="btn-save"
              elevation="4"
              width="100"
              height="45"
              :loading="isLoadingBtn"
              @click="submitDetailAgenda()"
              :disabled="isSaveDisabled"
              >Save</v-btn
            >
          </v-card-actions>
        </v-card>

        <v-card v-if="isLoading">
          <v-row class="my-5 mx-5">
            <v-col cols="12" v-for="i in 5" :key="i">
              <free-style-shimmer
                :is-loading="true"
                width="100%"
                height="4rem"
                border-radius="10px"
              />
            </v-col>
          </v-row>
        </v-card>
      </v-dialog>
    </Teleport>
  </div>

  <ModalConfirm
    ref="modalConfirmNotif"
    :form-config="formValidate"
    :is-loading="isLoading"
    @action-cancel="close()"
  >
    <template v-slot:btn-action>
      <div class="text-end mt-4">
        <v-btn
          class="btn-prev"
          elevation="4"
          width="100"
          height="45"
          :loading="isLoadingBtn"
          @click="submitDetailAgenda(true, false)"
          >No, Skip</v-btn
        >
        <v-btn
          class="btn-next ml-2"
          elevation="4"
          width="117"
          height="45"
          :loading="isLoadingBtn"
          @click="submitDetailAgenda(true, true)"
          >Yes, Send</v-btn
        >
      </div>
    </template>
  </ModalConfirm>

  <ModalLoading ref="modalLoading" text="Checking schedule availability..." />

  <ModalConfirm
    ref="modalWarning"
    :form-config="modalWarningConfig"
    :is-loading="isLoadingBtn"
    @action-cancel="closeOverlapModal"
    @action-confirm="submitDetailAgenda(true)"
  >
    <template #icon-img>
      <v-avatar
        size="80"
        style="margin-top: -42px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img src="/images/icon/iconWarning.png" style="width: 80px" />
      </v-avatar>
    </template>
    <template #desc>
      <p style="color: #616161">
        The selected time
        <b>({{ form.startTime }} - {{ form.endTime }})</b> overlaps with an
        existing agenda. Do you want to continue ?
      </p>
    </template>
    <template #text-area>
      <div
        class="px-2 py-3 mb-4 rounded-lg overflow-y-auto"
        style="
          color: #25282b;
          background-color: #f5f5f5;
          border: 1px solid #ededed;
          max-height: 208px;
        "
      >
        <b>Conflicting Agenda :</b>
        <ul class="text-left mt-1 mb-0">
          <li v-for="item in overlappedItems" :key="item.id">
            {{ item.agendaName }} ({{ reformatTimes(item.startTime) }} -
            {{ reformatTimes(item.endTime) }})
          </li>
        </ul>
      </div>
    </template>
  </ModalConfirm>
</template>

<script lang="ts" setup>
import {
  computed,
  ref,
  reactive,
  onMounted,
  getCurrentInstance,
  PropType,
  nextTick,
} from "vue";
import { useRoute } from "vue-router";
import { TAgendaData } from "@v2/Type.d";
import { useStore } from "vuex";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { getErrorMessages } from "@v2/helpers/validation";
import { responsePromise } from "@v2/helpers/utils";
import { TModalConfirm } from "@v2/Type.d";
import { messageEditEvent } from "@v2/enum/Enum";
import { isEqual, some } from "lodash";

import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { uniqueOptions } from "@/helpers/utils";
import ModalLoading from "../utils/modal/ModalLoading.vue";
import {
  reformatTimes,
  formatDate,
  formatDateTime,
} from "@/v2/helpers/DateHelper";

type TModalType = "edit" | "add";
const timeRegex = helpers.regex(/^(?:[01]\d|2[0-3]):(?:[0-5]\d)$/);

const props = defineProps({
  type: {
    type: String as PropType<TModalType>,
    default: "edit",
  },
  title: {
    type: String,
    required: false,
  },
  id: {
    type: String,
    required: false,
  },
  editStatus: {
    type: String,
    required: false,
  },
  visible: {
    type: Boolean,
    default: false,
  },
  date: {
    // belum di provide BE sementara pakai props
    type: String,
    required: true,
  },
  modelValue: {
    type: String,
    default: "",
  },
  dateStart: {
    type: String,
    default: "",
  },
});

const inProgressEdit = ref<boolean>(props.editStatus !== "In Progress");
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();
const currentYear = new Date().getFullYear();
const minYear = computed(() => currentYear - 5);
const maxYear = computed(() => currentYear + 10);
const selectedAdg = ref<string[]>([]);
const attendanceAdg = ref<string[]>([]);
const isLoading = ref<boolean>(false);
const isLoadingBtn = ref<boolean>(false);
const route = useRoute();
const modalConfirmNotif = ref();
const openPopUp = ref<boolean>(false);
const listAdg = computed(() => store.getters["meetingStore/getListAdg"]);

const formValidate = ref<TModalConfirm>({
  title: "Send Outlook Update",
  titleClass: "text-20 mb-4",
  message: "",
  btnSubmitLabel: "Yes",
  width: 554,
  btnSubmitColor: "primary-gradient",
  showIcon: false,
});

const modalLoading = ref();
const modalWarning = ref();
const modalWarningConfig: TModalConfirm = {
  title: "Schedule Conflict",
  titleClass: "text-24 text-black",
  message: "",
  btnSubmitLabel: "Continue Anyway",
  btnSubmitColor: "primary-gradient",
  showIcon: true,
  btnCancelLabel: "Change Time",
};

const form = reactive<TAgendaData>({
  id: "",
  date: "",
  agendaName: "",
  agendaOrder: 0,
  invited: [],
  endTime: "",
  listInvitedUnit: [],
  listPresentingUnit: [],
  startTime: "",
  status: 0,
  adgBidang: [],
  adgBidangAttendance: [],
  agendaPlace: "",
});

const originalAgendaName = ref<string>("");
const originalListPresentingUnit = ref<any[]>([]);
const originalListInvitedUnit = ref<any[]>([]);
const originalSelectedAdg = ref<string[]>([]);
const originalAttendanceAdg = ref<string[]>([]);
const originalAgendaPlace = ref<string>("");
const originalDate = ref<string>("");
const originalStartTime = ref<string>("");
const originalEndTime = ref<string>("");

const overlappedItems = ref<any[] | null>(null);

const activeOverlappedItem = computed(() => {
  if (!overlappedItems.value?.length || !inProgressEdit.value) return null;
  return overlappedItems.value.find((item) => item.idStatus === 24);
});

const timeOverlapMessage = computed(() => {
  if (!overlappedItems.value?.length) return { start: "", end: "" };

  const target = activeOverlappedItem.value || {
    startTime: overlappedItems.value[0].startTime,
    endTime: overlappedItems.value[overlappedItems.value.length - 1].endTime,
  };
  const { startTime, endTime } = target;

  const intStartTime = +form.startTime.replace(":", "");
  const intEndTime = +form.endTime.replace(":", "");

  const intOverlapStartTime = +reformatTimes(startTime).replace(":", "");
  const intOverlapEndTime = +reformatTimes(endTime).replace(":", "");

  const startIsInside =
    intStartTime >= intOverlapStartTime && intStartTime < intOverlapEndTime;
  const endIsInside =
    intEndTime > intOverlapStartTime && intEndTime <= intOverlapEndTime;
  const isSwallowing =
    intStartTime <= intOverlapStartTime && intEndTime >= intOverlapEndTime;

  const startIsError = startIsInside || isSwallowing;
  const endIsError = endIsInside || isSwallowing;

  return {
    start: startIsError ? "selected time overlaps with an existing agenda" : "",
    end: endIsError ? "selected time overlaps with an existing agenda" : "",
  };
});

const isAgendaChanged = computed(() => {
  return form.agendaName !== originalAgendaName.value;
});

const isListPresentingUnitChanged = computed(() => {
  return !isEqual(form.listPresentingUnit, originalListPresentingUnit.value);
});

const isListInvitedUnitChanged = computed(() => {
  return !isEqual(form.listInvitedUnit, originalListInvitedUnit.value);
});

const isSelectedAdgChanged = computed(() => {
  return !isEqual(selectedAdg.value, originalSelectedAdg.value);
});

const isAttendanceAdgChanged = computed(() => {
  return !isEqual(attendanceAdg.value, originalAttendanceAdg.value);
});

const isAgendaPlaceChanged = computed(() => {
  return form.agendaPlace !== originalAgendaPlace.value;
});

const isDateChanged = computed(() => {
  return form.date !== originalDate.value;
});

const isStartTimeChanged = computed(() => {
  return form.startTime !== originalStartTime.value;
});

const isEndTimeChanged = computed(() => {
  return form.endTime !== originalEndTime.value;
});

const isSaveDisabled = computed(() => {
  const changeFlags = [
    isAgendaChanged.value,
    isListPresentingUnitChanged.value,
    isListInvitedUnitChanged.value,
    isSelectedAdgChanged.value,
    isAttendanceAdgChanged.value,
    isAgendaPlaceChanged.value,
    isDateChanged.value,
    isStartTimeChanged.value,
    isEndTimeChanged.value,
  ];

  return !some(changeFlags) || store.getters["eventStore/getLoading"];
});

const rules = {
  agendaName: { required },
  status: { required },
  date: {
    required,
  },
  startTime: {
    required: helpers.withMessage("Wajib diisi", required),
    timeRegex: helpers.withMessage(
      "Format waktu Invalid!. Gunakan format HH:mm (Ex 18:30).",
      timeRegex
    ),
  },
  endTime: {
    required,
    timeRegex: helpers.withMessage(
      "Format waktu Invalid!. Gunakan format HH:mm (Ex 18:30).",
      timeRegex
    ),
    endTimePicker: (value, vm) => {
      const start = getEndTimePickerError(vm.startTime);
      const end = getEndTimePickerError(value);

      return start < end || start === end;
    },
  },
};

const v$ = useVuelidate(rules, form);

const emit = defineEmits<{
  (e: "refetch", value: unknown): void;
  (e: "close", value: boolean): void;
}>();

const members = ref();
const getMemberADG = () => {
  members.value = listAdg.value.map((item: any) => ({
    id: item.id,
    value: item.displayName,
  }));
};

const mappingAdg = (item): string[] => {
  const result = item.map((value) => {
    return value.id;
  });

  return result;
};

const loadDetail = () => {
  isLoading.value = true;

  store
    .dispatch("meetingStore/getDetailEventAgenda", { id: props.id })
    .then((response) => {
      //reformat date
      const date = props.date.split("/");
      form.date = date[1] + "/" + date[0] + "/" + date[2];

      const data = response.responseData;
      form.listInvitedUnit = data?.listInvitedUnit;
      form.listPresentingUnit = data?.listPresentingUnit;
      form.agendaName = data?.agendaName;
      form.agendaPlace = data?.agendaPlace || "";
      form.startTime = formatDateTime(data?.startTime);
      form.endTime = formatDateTime(data?.endTime);
      form.status = data?.status;
      selectedAdg.value = mappingAdg(data?.adgBidang);
      attendanceAdg.value = mappingAdg(data.adgBidangAttendance);
      form.agendaOrder = data?.agendaOrder;

      // get original values for comparison
      originalAgendaName.value = data?.agendaName;
      originalListPresentingUnit.value = data?.listPresentingUnit;
      originalListInvitedUnit.value = data?.listInvitedUnit;
      originalSelectedAdg.value = mappingAdg(data?.adgBidang);
      originalAttendanceAdg.value = mappingAdg(data.adgBidangAttendance);
      originalAgendaPlace.value = data?.agendaPlace || "";
      originalDate.value = date[1] + "/" + date[0] + "/" + date[2];
      originalStartTime.value = formatDateTime(data?.startTime);
      originalEndTime.value = formatDateTime(data?.endTime);
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const listItem = ref<string[]>([]);
store.dispatch("meetingStore/getAllStatusAgenda").then((response) => {
  listItem.value = response.responseData;
});

const allSatker = ref<any[]>([]);
store.dispatch("meetingStore/getAllSatker").then((response) => {
  allSatker.value = response.responseData;
});
const penyaji = computed(() =>
  uniqueOptions(allSatker.value, form.listInvitedUnit)
);
const diundang = computed(() =>
  uniqueOptions(allSatker.value, form.listPresentingUnit)
);

const submitDetailAgenda = async (
  skipOverlapping = false,
  isPopup?: boolean
) => {
  const result = await v$.value.$validate();
  if (!result) return;

  const selected = selectedAdg.value.map((value) => {
    return { id: value };
  });

  const attendance = attendanceAdg.value.map((value) => {
    return { id: value };
  });

  const payload = {
    ...(props.type === "edit"
      ? { id: props.id }
      : { idEvent: route.params.idEvent }),
    agendaName: form.agendaName,
    satkerPenyaji: form.listPresentingUnit,
    satkerDiundang: form.listInvitedUnit,
    startTime: form.startTime
      ? `${form.date} ${form.startTime}`
      : `${form.date} 00:00`,
    endTime: form.endTime
      ? `${form.date} ${form.endTime}`
      : `${form.date} 00:00`,
    status: form.status,
    adgBidang: selected,
    adgBidangAttendance: attendance,
    agendaOrder: form.agendaOrder ?? 0,
    agendaPlace: form.agendaPlace,
    sendInvitationOutlookPopUp: isPopup,
    skipOverlapping,
  };

  if (props.type === "edit") submitEdit(payload, isPopup);
  if (props.type === "add") submitAdd(payload, isPopup);
};

const openModalLoading = (skipOverlapping = false, isPopup?: boolean) => {
  openPopUp.value = true;
  if (!skipOverlapping && typeof isPopup === "undefined") {
    return modalLoading.value.show();
  }
  isLoadingBtn.value = true;
};

const closeOverlapModal = () => {
  openPopUp.value = false;
};

const submitEdit = async (payload, isPopup?: boolean) => {
  openModalLoading(payload.skipOverlapping, isPopup);
  try {
    const res = await store.dispatch(
      "meetingStore/updateDetailAgenda",
      payload
    );
    if (Array.isArray(res.responseData)) {
      overlappedItems.value = res.responseData;
      if (activeOverlappedItem.value) {
        openPopUp.value = false;
        return;
      }
      return modalWarning.value.show();
    }
    if (res.responseCode === "011061") {
      formValidate.value.message =
        messageEditEvent[res.responseData?.popUpNotifType];
      modalWarning.value.hide(false);
      modalConfirmNotif.value.show();

      return nextTick(() => {
        openPopUp.value = true;
      });
    }
    openPopUp.value = false;
    nextTick(() => {
      response.success(res, function () {
        refetch(true);
        modalConfirmNotif.value.hide();
        close();
      });
    });
  } catch (err) {
    openPopUp.value = false;
    response.error(err);
  } finally {
    modalLoading.value.hide();
    isLoadingBtn.value = false;
  }
};

const submitAdd = async (payload, isPopup?: boolean) => {
  openModalLoading(payload.skipOverlapping, isPopup);
  try {
    const res = await store.dispatch("meetingStore/addAgenda", payload);
    if (Array.isArray(res.responseData)) {
      overlappedItems.value = res.responseData;
      if (activeOverlappedItem.value) {
        openPopUp.value = false;
        return;
      }
      return modalWarning.value.show();
    }
    openPopUp.value = false;
    nextTick(() => {
      response.success(res, function () {
        refetch(true);
        close();
      });
    });
  } catch (err) {
    openPopUp.value = false;
    response.error(err);
  } finally {
    modalLoading.value.hide();
    isLoadingBtn.value = false;
  }
};

const close = () => {
  originalAgendaName.value = "";
  originalListPresentingUnit.value = [];
  originalListInvitedUnit.value = [];
  originalSelectedAdg.value = [];
  originalAttendanceAdg.value = [];
  originalAgendaPlace.value = "";
  originalDate.value = "";
  originalStartTime.value = "";
  originalEndTime.value = "";
  emit("close", true);
};

const refetch = (value: unknown) => {
  emit("refetch", value);
};

const load = () => {
  if (props.type === "edit") {
    loadDetail();
  } else {
    form.status = 23; // set status to waiting
    const formattedDate = formatDate(props.dateStart);
    form.date = formattedDate;
    originalDate.value = formattedDate; // Set original date to match initial form date
  }

  getMemberADG();
};

onMounted(() => {
  load();
});

const minutes = computed(() => {
  const total = calculateMinute(form.startTime, form.endTime);
  return total || 0;
});

const visibility = computed({
  get() {
    return props.visible;
  },
  set(value: boolean) {
    emit("close", value);
  },
});

function calculateMinute(timeInHour1: string, timeInHour2: string) {
  const timeParts1 = timeInHour1.split(":");
  const timeParts2 = timeInHour2.split(":");
  return (
    (Number(timeParts2[0]) - Number(timeParts1[0])) * 60 +
    (Number(timeParts2[1]) - Number(timeParts1[1]))
  );
}

const getEndTimePickerError = (value: string) => {
  const start = value.split(":");

  var time = new Date();
  time.setHours(parseInt(start[0]));
  time.setMinutes(parseInt(start[1]));

  return time;
};
</script>
<style lang="scss" scoped>
.wrapper {
  &_form {
    :deep(.v-selection-control .v-label) {
      font-size: 15px;
      color: rgba(var(--v-theme-on-surface), var(--v-high-emphasis-opacity));
      white-space: nowrap;
    }
  }
  :deep(.checkbox-wrap .v-label) {
    white-space: normal !important;
    word-wrap: break-word;
    overflow-wrap: break-word;
    line-height: 1.2;
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

  :deep(.v-field) {
    border-radius: 10px;
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
  }

  :deep(.dp__instance_calendar) {
    box-shadow: 1px 1px 7px 3px #7393b3;
    border-radius: 5px;
    padding: 10px;
  }

  :deep(.dp__overlay) {
    border-radius: 5px;
  }

  :deep(.v-messages__message) {
    padding: 0 0 4px 0;
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

  .btn-save {
    background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
    border-radius: 10px !important;
    border-color: #267dc2 !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    font-size: 14px !important;
    color: white;
    font-weight: 900;
  }

  .btn-cancel {
    background: white;
    border-radius: 10px !important;
    /* border-color: #267dc2 !important; */
    padding-left: 16px !important;
    padding-right: 16px !important;
    font-size: 14px !important;

    color: #267dc2 !important;
    font-weight: 900;
  }
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

.is-disabled:deep(.v-field) {
  opacity: 1;
  background-color: #dfdfdf;
  color: grey;
  box-shadow: 0px 3px 1px -2px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)),
    0px 2px 2px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)),
    0px 1px 5px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.12));
}
</style>
