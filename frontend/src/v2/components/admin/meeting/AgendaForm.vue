<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" width="1000" persistent>
      <v-card class="border-radius-dwp">
        <v-card-title class="text-center mt-3">
          <p class="text-18 fw-600 text-blueTheme">
            {{ edit_id == 0 ? "Add" : "Edit" }} Agenda
          </p>
          <v-btn
            density="default"
            icon="mdi-close"
            variant="text"
            class="btn-close"
            @click="onClose"
          />
        </v-card-title>
        <hr class="line mt-3" />
        <v-card-text class="ma-2">
          <v-form ref="form">
            <v-row>
              <v-col :cols="12" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Agenda<span class="text-redTheme">*</span>
                </p>
                <v-text-field
                  v-model="formInput.agendaName"
                  autocomplete="off"
                  variant="solo"
                  placeholder="Insert Agenda"
                  class="my-input"
                  single-line
                  :hide-details="isError(v$.agendaName)"
                  :error-messages="getErrorMessages(v$.agendaName)"
                ></v-text-field>
              </v-col>

              <v-col :cols="12" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Satker Penyaji<!--  <span class="text-redTheme">*</span> -->
                </p>
                <v-autocomplete
                  v-model="formInput.satkerPenyaji"
                  :items="satkers"
                  variant="solo"
                  placeholder="Add Satker Penyaji"
                  class=""
                  item-value="id"
                  item-title="value"
                  chips
                  multiple
                  closable-chips
                  hide-selected
                  searchable
                  :hide-details="isError(v$.satkerPenyaji)"
                  :error-messages="getErrorMessages(v$.satkerPenyaji)"
                ></v-autocomplete>
              </v-col>

              <v-col :cols="12" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Satker Diundang<!--  <span class="text-redTheme">*</span> -->
                </p>
                <v-autocomplete
                  v-model="formInput.satkerDiundang"
                  :items="satkers"
                  variant="solo"
                  placeholder="Add Satker Diundang"
                  class=""
                  item-value="id"
                  item-title="value"
                  chips
                  multiple
                  closable-chips
                  hide-selected
                  searchable
                  :hide-details="isError(v$.satkerDiundang)"
                  :error-messages="getErrorMessages(v$.satkerDiundang)"
                ></v-autocomplete>
              </v-col>

              <v-col :cols="12" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Room<!--  <span class="text-redTheme">*</span> -->
                </p>
                <v-text-field
                  v-model="formInput.room"
                  autocomplete="off"
                  variant="solo"
                  placeholder="Insert Room Name"
                  class="my-input"
                  single-line
                  :hide-details="isError(v$.room)"
                  :error-messages="getErrorMessages(v$.room)"
                ></v-text-field>
              </v-col>

              <v-col :cols="12" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Day Order<span class="text-redTheme">*</span>
                </p>
                <v-text-field
                  v-model="formInput.dayOrder"
                  autocomplete="off"
                  variant="solo"
                  placeholder="Insert The Order of Days"
                  class="my-input"
                  single-line
                  type="number"
                  min="0"
                  :hide-details="isError(v$.dayOrder)"
                  :error-messages="getErrorMessages(v$.dayOrder)"
                ></v-text-field>
              </v-col>

              <v-col :cols="4" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Start Time<span class="text-redTheme">*</span>
                </p>
                <v-text-field
                  v-model="formInput.startTime"
                  autocomplete="off"
                  variant="solo"
                  placeholder="Insert Start Time"
                  class="my-input"
                  single-line
                  :hide-details="
                    isError(v$.startTime) && !timeOverlapMessage.start
                  "
                  :error-messages="[
                    ...getErrorMessages(v$.startTime),
                    timeOverlapMessage.start,
                  ]"
                ></v-text-field>
              </v-col>

              <v-col :cols="4" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Finish Time<span class="text-redTheme">*</span>
                </p>
                <v-text-field
                  v-model="formInput.endTime"
                  autocomplete="off"
                  variant="solo"
                  placeholder="Insert Finish Time"
                  class="my-input"
                  single-line
                  :hide-details="isError(v$.endTime) && !timeOverlapMessage.end"
                  :error-messages="[
                    ...getErrorMessages(v$.endTime),
                    timeOverlapMessage.end,
                  ]"
                ></v-text-field>
              </v-col>

              <v-col :cols="4" class="mb-0">
                <p class="pb-3 text-left text-darkBlue font-weight-bold">
                  Minute
                </p>
                <v-text-field disabled variant="solo">{{
                  rangeTime == 0 ? "Total Minute" : rangeTime
                }}</v-text-field>
              </v-col>
            </v-row>
          </v-form>
          <div class="text-right pb-5 mt-4">
            <v-btn
              class="btn-prev mr-3"
              elevation="4"
              width="100"
              height="45"
              @click="onClose"
            >
              Cancel
            </v-btn>
            <v-btn
              class="btn-next"
              elevation="4"
              width="100"
              height="45"
              @click="() => onSave()"
            >
              Save
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <ModalLoading ref="modalLoading" text="Checking schedule availability..." />

    <ModalConfirm
      ref="modalWarning"
      :form-config="modalWarningConfig"
      :is-loading="isLoading"
      @action-cancel="closeOverlapModal"
      @action-confirm="() => onSave(true)"
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
          <b>({{ formInput.startTime }} - {{ formInput.endTime }})</b> overlaps
          with an existing agenda. Do you want to continue ?
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
  </Teleport>
</template>
<script lang="ts" setup>
import { computed, getCurrentInstance, onMounted, ref } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import { getErrorMessages, isError, timeRegex } from "@v2/helpers/validation";
import { useStore } from "vuex";
import { reformatTimes } from "@/v2/helpers/DateHelper";
import ModalConfirm from "../../utils/modal/ModalConfirm.vue";
import ModalLoading from "../../utils/modal/ModalLoading.vue";
import { TModalConfirm } from "@/v2/Type.js";

const store = useStore();
const dialog = ref<boolean>(false);
const edit_id = ref<number>(0);
const instance: any = getCurrentInstance()?.root.refs;
const emit = defineEmits(["onSuccess"]);

const dateDefault = ref<string>(new Date().toISOString().substring(0, 10));
const satkers = ref([]);

const formInput = ref<any>({
  idMEventTemplate: 0,
  agendaName: null,
  satkerPenyaji: [],
  satkerDiundang: [],
  room: null,
  dayOrder: null,
  startTime: null,
  endTime: null,
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

const isLoading = ref(false);
const overlappedItems = ref<any[] | null>(null);

const activeOverlappedItem = computed(() => {
  if (!overlappedItems.value?.length) return null;
  return overlappedItems.value.find((item) => item.idStatus === 24);
});

const timeOverlapMessage = computed(() => {
  if (!overlappedItems.value?.length) return { start: "", end: "" };

  const target = activeOverlappedItem.value || {
    startTime: overlappedItems.value[0].startTime,
    endTime: overlappedItems.value[overlappedItems.value.length - 1].endTime,
  };
  const { startTime, endTime } = target;

  const intStartTime = +formInput.value.startTime.replace(":", "");
  const intEndTime = +formInput.value.endTime.replace(":", "");

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

const rules = computed(() => {
  return {
    agendaName: { required },
    satkerPenyaji: {},
    satkerDiundang: {},
    room: {},
    dayOrder: { required },
    startTime: {
      required,
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
      moreThanStartTime: (val: string, obj: any) => {
        if (!obj.startTime) return true;
        const end = new Date("05/02/2023 " + val).getTime();
        const start = new Date("05/02/2023 " + obj.startTime).getTime();
        return start < end;
      },
    },
  };
});
const v$ = useVuelidate(rules, formInput);
const rangeTime = computed((): number => {
  if (!formInput.value.startTime || !formInput.value.endTime) return 0;
  const start = new Date("05/02/2023 " + formInput.value.startTime).getTime();
  const end = new Date("05/02/2023 " + formInput.value.endTime).getTime();
  const result = isNaN(end - start) ? 0 : end - start;
  return result / 1000 / 60;
});

function onOpen(
  param: { event_id: number; bp_id: number; dateDefault: string },
  _id = 0
) {
  dialog.value = true;
  dateDefault.value = param.dateDefault;
  formInput.value = {
    idMEventTemplate: param.event_id,
    agendaName: null,
    satkerPenyaji: [],
    satkerDiundang: [],
    room: null,
    dayOrder: null,
    startTime: null,
    endTime: null,
    startDate: null,
    startEnd: null,
  };
  if (_id) fetchEditData(_id);
  v$.value.$reset();
}

function onClose() {
  edit_id.value = 0;
  formInput.value.idMEventTemplate = 0;
  dialog.value = false;
  overlappedItems.value = null;
  modalWarning.value.hide(false);
}

function fetchSatker() {
  store.dispatch("meetingStore/getAllSatker").then(({ responseData }) => {
    satkers.value = responseData;
  });
}

function fetchEditData(_id: number) {
  edit_id.value = _id;
  store
    .dispatch("adminStore/getEditAgendaMeeting", _id)
    .then(({ responseData }) => {
      responseData.satkerPenyaji = responseData.satkerPenyaji.map(
        (r: any) => r.idSatkerPenyaji
      );
      responseData.satkerDiundang = responseData.satkerDiundang.map(
        (r: any) => r.idSatkerDiundang
      );
      responseData.startDate = responseData.startTime?.substring(0, 10);
      responseData.endDate = responseData.endTime?.substring(0, 10);
      responseData.startTime = responseData.startTime?.substring(16, 11);
      responseData.endTime = responseData.endTime?.substring(16, 11);
      formInput.value = responseData;
    });
}

const handleSaveResponse = (req: any) => {
  if (edit_id.value != 0) {
    req.id = edit_id.value;
    delete req.idMEventAgendaTemplate, req.idMEventTemplate, req.minutes;
  }

  const dispatchType = `${edit_id.value != 0 ? "update" : "store"}`;
  store
    .dispatch(`adminStore/${dispatchType}AgendaMeeting`, req)
    .then(({ responseMessage }) => {
      instance.toast.show({
        message: responseMessage,
        color: "success",
        timeout: 3000,
      });
      emit("onSuccess", true);
      onClose();
    })
    .catch((error) => {
      const err = JSON.parse(error.response.data);
      if (Array.isArray(err.responseData)) {
        overlappedItems.value = err.responseData;
        if (activeOverlappedItem.value) return;
        dialog.value = false;
        return modalWarning.value.show();
      }
      instance.toast.show({
        message: err.responseMessage ?? "internal server error",
        color: "warning",
        timeout: 3000,
      });
    })
    .finally(() => {
      isLoading.value = false;
      modalLoading.value.hide();
    });
};

function onSave(skipOverlapping = false) {
  v$.value.$validate().then((res) => {
    if (!res) return;

    if (!skipOverlapping) modalLoading.value.show();
    isLoading.value = true;

    const req = { ...formInput.value, skipOverlapping };
    req.satkerPenyaji = req.satkerPenyaji.map((r) => {
      return { idSatkerPenyaji: r };
    });
    req.satkerDiundang = req.satkerDiundang.map((r) => {
      return { idSatkerDiundang: r };
    });

    req.startTime =
      (edit_id.value != 0 ? `${req.startDate} ` : `${dateDefault.value} `) +
      req.startTime;
    req.endTime =
      (edit_id.value != 0 ? `${req.endDate} ` : `${dateDefault.value} `) +
      req.endTime;

    console.log("on save:", req);

    handleSaveResponse(req);
  });
}

const closeOverlapModal = () => {
  dialog.value = true;
};

defineExpose({
  onOpen,
});

onMounted(() => {
  fetchSatker();
  // onOpen({ event_id: 1, bp_id: 1 }, 2);
});
</script>

<style lang="scss" scoped>
:deep(.v-text-field .v-field) {
  border-radius: 12px !important;
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

:deep(.v-chip__append) {
  position: absolute;
  right: 0;
  margin-right: 0.5vw;
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

:deep(.v-field--disabled) {
  color: #000000;
  background-color: rgb(196, 186, 186) !important;
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
</style>
