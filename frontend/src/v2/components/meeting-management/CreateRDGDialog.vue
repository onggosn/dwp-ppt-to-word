<template>
  <Teleport to="body">
    <v-dialog v-model="dialog" :max-width="800" persistent>
      <v-card class="mb-5 border-radius-dwp">
        <v-card-title class="d-flex justify-center align-center">
          <div class="text-18 text-blueTheme fw-500 mt-2 mb-2">Add Meeting</div>
          <v-btn
            class="mr-2"
            style="position: absolute; right: 0"
            variant="text"
            icon="mdi-close"
            @click="onClose()"
          ></v-btn>
        </v-card-title>
        <v-card-text>
          <div class="separatorHorizontalGradient"></div>
        </v-card-text>
        <Steppy
          v-model:step="step"
          nextText="Next"
          backText="Back"
          doneText="Create"
          :tabs="tabs"
        >
          <template #1>
            <v-form ref="form">
              <!-- EVENT TYPE -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                Event Type<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="store.getters['eventStore/getLoading']"
                v-model="state._eventType"
                :items="listEventType"
                variant="solo"
                placeholder="Choose event type"
                class="px-2 mt-1"
                item-title="value"
                item-value="id"
                return-object
              ></v-autocomplete>
              <!-- #endregion -->

              <!-- RDG TYPE -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                RDG Type<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="store.getters['eventStore/getLoading']"
                v-model="state._rdgType"
                :items="listRDGType"
                variant="solo"
                placeholder="Choose RDG type"
                class="px-2 mt-1"
                item-title="value"
                item-value="id"
                @update:modelValue="
                  () => {
                    state._month = null;
                    state._year = null;
                    state._rdg = null;
                    state._event = null;
                  }
                "
                return-object
              ></v-autocomplete>
              <!-- #endregion -->

              <!-- MONTH, YEAR -->
              <!-- #region -->
              <v-sheet class="d-flex flex-row">
                <div style="width: 50%">
                  <p class="ml-2 text-left text-darkBlue font-weight-bold">
                    Month<span class="text-gradient-red">*</span>
                  </p>
                  <v-autocomplete
                    :loading="store.getters['eventStore/getLoading']"
                    v-model="state._month"
                    :items="listMonths"
                    variant="solo"
                    placeholder="Choose month"
                    class="px-2 mt-1"
                    item-title="name"
                    item-value="id"
                    return-object
                    ><template v-slot:append-inner>
                      <img
                        :src="require('@/v2/assets/icon/date.svg')"
                      /> </template
                  ></v-autocomplete>
                </div>
                <div style="width: 50%">
                  <p class="ml-2 text-left text-darkBlue font-weight-bold">
                    Year<span class="text-gradient-red">*</span>
                  </p>
                  <v-autocomplete
                    :loading="store.getters['eventStore/getLoading']"
                    v-model="state._year"
                    :items="getYearPicker()"
                    variant="solo"
                    placeholder="Choose year"
                    class="px-2 mt-1"
                    return-object
                    ><template v-slot:append-inner>
                      <img
                        :src="require('@/v2/assets/icon/date.svg')"
                      /> </template
                  ></v-autocomplete>
                </div>
              </v-sheet>
              <!-- #endregion -->

              <!-- RDG -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                RDG<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="store.getters['eventStore/getLoading']"
                v-model="state._rdg"
                :items="listRDG"
                variant="solo"
                placeholder="Choose RDG"
                class="px-2 mt-1"
                item-title="eventName"
                item-value="idEvent"
                return-object
                :disabled="state._month === null || state._year === null"
                :bg-color="
                  state._month === null || state._year === null
                    ? '#DFDFDF'
                    : '#fff'
                "
              ></v-autocomplete>
              <!-- #endregion -->

              <!-- Event -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                Event<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="store.getters['eventStore/getLoading']"
                v-model="state._event"
                :items="listEvent"
                variant="solo"
                placeholder="Choose event"
                class="px-2 mt-1"
                item-title="bPName"
                item-value="idEvent"
                return-object
              ></v-autocomplete>
              <!-- #endregion -->
            </v-form>
          </template>
          <template #2>
            <v-form ref="form">
              <!-- TITLE -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                Title<span class="text-gradient-red">*</span>
              </p>
              <v-text-field
                variant="solo"
                placeholder="Please input event title"
                :hide-details="true"
                class="px-2 mt-1"
                v-model="state._title"
              ></v-text-field>
              <!-- #endregion -->

              <!-- DESCRIPTION -->
              <!-- #region -->
              <p class="ml-2 mt-4 text-left text-darkBlue font-weight-bold">
                Description<span class="text-gradient-red">*</span>
              </p>
              <v-text-field
                variant="solo"
                placeholder="Please input description"
                :hide-details="true"
                class="px-2 mt-1"
                v-model="state._description"
              ></v-text-field>
              <!-- #endregion -->

              <!-- Method -->
              <!-- #region -->
              <p class="ml-2 mt-4 text-left text-darkBlue font-weight-bold">
                Method<span class="text-gradient-red">*</span>
              </p>
              <v-autocomplete
                :loading="store.getters['eventStore/getLoading']"
                v-model="state._method"
                :items="listMethod"
                variant="solo"
                placeholder="Choose method"
                class="px-2 mt-1"
                item-title="value"
                item-value="id"
                return-object
              ></v-autocomplete>
              <!-- #endregion -->

              <!-- Media -->
              <!-- #region -->
              <template v-if="isNotOffline()">
                <p class="ml-2 text-left text-darkBlue font-weight-bold">
                  Main Media<span class="text-gradient-red">*</span>
                </p>
                <v-autocomplete
                  :loading="store.getters['eventStore/getLoading']"
                  v-model="state._media"
                  :items="listMedia"
                  variant="solo"
                  placeholder="Choose media"
                  class="px-2 mt-1"
                  item-title="platform"
                  item-value="id"
                  return-object
                ></v-autocomplete>
              </template>
              <!-- #endregion -->

              <!-- Link meeting -->
              <!-- #region -->
              <template v-if="showLinkMeeting">
                <p class="ml-2 text-left text-darkBlue font-weight-bold">
                  Main Link<span class="text-gradient-red">*</span>
                </p>
                <v-text-field
                  variant="solo"
                  placeholder="Please input link meeting"
                  class="px-2 mt-1 mb-4"
                  v-model="state._linkMeeting"
                  :error-messages="getErrorMessages(v$._linkMeeting)"
                ></v-text-field>
              </template>

              <!-- #endregion -->

              <!-- Media Bakcup -->
              <!-- #region -->
              <template v-if="isNotOffline()">
                <p class="ml-2 text-left text-darkBlue font-weight-bold">
                  Backup Media
                </p>
                <v-autocomplete
                  :loading="store.getters['eventStore/getLoading']"
                  v-model="state._mediaBackup"
                  :items="listMedia"
                  variant="solo"
                  placeholder="Choose media"
                  class="px-2 mt-1"
                  item-title="platform"
                  item-value="id"
                  return-object
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :disabled="state._media && item.raw.id == state._media.id"
                    ></v-list-item>
                  </template>
                </v-autocomplete>
              </template>
              <!-- #endregion -->

              <!-- Link meeting backup -->
              <!-- #region -->
              <template v-if="showLinkMeetingBackup">
                <p class="ml-2 text-left text-darkBlue font-weight-bold">
                  Backup Link
                </p>
                <v-text-field
                  variant="solo"
                  placeholder="Please input link meeting"
                  class="px-2 mt-1 mb-4"
                  v-model="state._linkMeetingBackup"
                ></v-text-field>
              </template>

              <!-- #endregion -->

              <!-- Place -->
              <!-- region -->
              <template v-if="isOffline()">
                <p class="ml-2 text-left text-darkBlue font-weight-bold">
                  Place<span class="text-gradient-red">*</span>
                </p>
                <v-text-field
                  variant="solo"
                  placeholder="Please input meeting place"
                  :hide-details="true"
                  class="px-2 mt-1 mb-4"
                  v-model="state._place"
                ></v-text-field>
              </template>
              <!-- endregion -->

              <!-- START DATETIME -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                Start time<span class="text-gradient-red">*</span>
              </p>
              <v-sheet class="d-flex flex-row">
                <div style="width: 50%">
                  <VueDatePicker
                    v-model="state._startDate"
                    :year-range="[minYear, maxYear]"
                    :enable-time-picker="false"
                    :month-change-on-scroll="false"
                    auto-apply
                    model-type="dd/MM/yyyy"
                    :alt-position="() => ({ top: -300, left: 0 })"
                  >
                    <template #trigger>
                      <v-text-field
                        :value="state._startDate"
                        variant="solo"
                        placeholder="dd/mm/yyyy"
                        class="pl-2 pr-2"
                      >
                        <template v-slot:append-inner>
                          <img :src="require('@/v2/assets/icon/date.svg')" />
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
                </div>
                <div style="width: 50%">
                  <v-text-field
                    v-model="state._startTime"
                    variant="solo"
                    mask="time"
                    placeholder="Choose time"
                    class="pl-2 pr-2"
                    disabled
                    :error-messages="getErrorMessages(v$._startTime)"
                  ></v-text-field>
                </div>
              </v-sheet>
              <!-- #endregion -->

              <!-- END DATETIME -->
              <!-- #region -->
              <p class="ml-2 text-left text-darkBlue font-weight-bold">
                End time<span class="text-gradient-red">*</span>
              </p>
              <v-sheet class="d-flex flex-row">
                <div style="width: 50%">
                  <VueDatePicker
                    v-model="state._endDate"
                    :year-range="[minYear, maxYear]"
                    :enable-time-picker="false"
                    :month-change-on-scroll="false"
                    auto-apply
                    model-type="dd/MM/yyyy"
                    disabled
                    :alt-position="() => ({ top: -300, left: 0 })"
                  >
                    <template #trigger>
                      <v-text-field
                        :value="state._endDate"
                        variant="solo"
                        placeholder="dd/mm/yyyy"
                        class="pl-2 pr-2"
                        disabled
                        :error-messages="
                          getErrorMessages(v$._endDate, {
                            moreThanStartDate:
                              'Event tidak boleh berakhir sebelum dimulai',
                          })
                        "
                      >
                        <template v-slot:append-inner>
                          <img :src="require('@/v2/assets/icon/date.svg')" />
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
                </div>
                <div style="width: 50%">
                  <v-text-field
                    v-model="state._endTime"
                    variant="solo"
                    placeholder="Choose time"
                    class="pl-2 pr-2"
                    mask="time"
                    disabled
                    :error-messages="
                      getErrorMessages(v$._endTime, {
                        moreThanStartDate:
                          'Event tidak boleh berakhir sebelum dimulai',
                        notSameAs:
                          'Event tidak boleh mulai dan berakhir di waktu yang sama ',
                      })
                    "
                  ></v-text-field>
                </div>
              </v-sheet>
              <!-- #endregion -->
            </v-form>
          </template>
        </Steppy>
        <div class="text-right pb-5 pr-15">
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
            >{{ step != 2 ? "Next" : "Save" }}</v-btn
          >
        </div>
      </v-card>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
/* eslint-disable */
import { computed, reactive, ref, watch, getCurrentInstance } from "vue";
import { Steppy } from "vue3-steppy";
import { useStore } from "vuex";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import { getErrorMessages } from "@v2/helpers/validation";
import { responsePromise } from "@v2/helpers/utils";
import { monthNames } from "@/v2/mock/Contants";
import { getYearPicker } from "@/v2/helpers/datetime";
import type { TRequestCreateRDGLainnya } from "@/v2/Type";

const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const emit = defineEmits(["created"]);

const store = useStore();
const dialog = ref(false);
const form = ref();
const step = ref(1);
const buttonNext = ref(false);
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

const initialState = ref<TRequestCreateRDGLainnya>({
  _eventType: null,
  _rdgType: null,
  _month: null,
  _year: null,
  _rdg: null,
  _event: null,
  _title: "",
  _description: "",
  _method: null,
  _media: null,
  _mediaBackup: null,
  _linkMeeting: "",
  _linkMeetingBackup: "",
  _place: "",
  _startDate: null,
  _endDate: null,
  _startTime: null,
  _endTime: null,
});
const state = reactive({ ...initialState.value });
const rules = computed(() => {
  const localRule = {
    _eventType: { required },
    _rdgType: { required },
    _month: { required },
    _year: { required },
    _rdg: { required },
    _event: { required },
    _title: { required },
    _description: { required },
    _method: { required },
    _media: {},
    _linkMeeting: {},
    _place: {},
    _startDate: { required },
  };
  if (state._method && [1, 3].includes(state._method)) {
    localRule._media = { required };
  }
  if (state._media && ![1].includes(state._media.id)) {
    localRule._linkMeeting = { required };
  }
  return localRule;
});
const v$ = useVuelidate(rules, state);

/* FORM 1 */
const listEventType = ref([]);
const listRDGType = ref([]);
const listMonths = ref(monthNames);
const listRDG = ref([]);
const listEvent = ref([]);
/* FORM 2 */
const listMethod = ref([]);
const listMedia = ref([]);
const currentYear = new Date().getFullYear();
const minYear = computed(() => currentYear - 5);
const maxYear = computed(() => currentYear + 10);

function show() {
  dialog.value = true;
  /* Event Type */
  store.dispatch("eventStore/fetchListEventType").then((data) => {
    listEventType.value = data;
  });

  const req = {
    sectorName: "",
  };

  /* RDG Type */
  store.dispatch("eventStore/fetchMEventSubTypeList", req).then((data) => {
    listRDGType.value = data;
  });
}

function onClose() {
  step.value = 1;
  dialog.value = false;

  resetForm();
}

function resetForm() {
  state._eventType = null;
  state._rdgType = null;
  state._month = null;
  state._year = null;
  state._rdg = null;
  state._event = null;
  state._title = "";
  state._description = "";
  state._method = null;
  state._media = null;
  state._linkMeeting = "";
  state._place = "";
  state._startDate = null;
  state._endDate = null;
  state._startTime = null;
  state._endTime = null;
}

function negativeClick() {
  if (step.value > 1) {
    step.value--;
  } else {
    onClose();
  }
}

/* CREATE RDG */
function create(state) {
  let startformatdate = state._startDate && state._startDate.split("/");
  if (startformatdate) {
    startformatdate =
      startformatdate[2] + "-" + startformatdate[1] + "-" + startformatdate[0];
  }

  let endformatdate = state._endDate && state._endDate.split("/");
  if (endformatdate) {
    endformatdate =
      endformatdate[2] + "-" + endformatdate[1] + "-" + endformatdate[0];
  }
  const req = {
    title: state._title,
    eventDescription: `<p>${state._description}</p>`,
    idMEventSubTypeList: 1,
    idMEventMethod: state._method.id,
    idMeetingPlatform: state._media == null ? 1 : state._media.id,
    idMeetingBackupPlatform:
      state._mediaBackup == null ? null : state._mediaBackup.id,
    idEvent: state._event.idEvent,
    eventLink: state._linkMeeting,
    eventLinkBackup: state._linkMeetingBackup,
    eventPlace: state._place,
    eventStart: `${startformatdate}T00:00Z`,
  };

  store
    .dispatch("eventStore/insertEventOthers", req)
    .then(() => {
      dialog.value = false;
      root.refs.toast.show({
        message: "Successfully Created",
        color: "success",
        timeout: 3000,
      });
      emit("created", true);

      resetForm();
      step.value--;
    })
    .catch(response.error);
}
function positiveClick() {
  if (step.value == 2) {
    v$.value.$validate().then((valid) => {
      if (valid) {
        create(state);
      }
    });
  } else {
    step.value++;
  }
}
/* HYBRID & ONLINE */
function isNotOffline() {
  if (state._method) {
    // online (1) atau Hybrid(3)
    return [1, 3].includes(state._method.id);
  }
  return false;
}
const showLinkMeeting = computed((): boolean => {
  return state._media && state._media.id != 1;
});

const showLinkMeetingBackup = computed((): boolean => {
  return state._mediaBackup && state._mediaBackup.id != 1;
});
function isNotTeams() {
  if (state._method) {
    //offline(2)
    return (
      [1].includes(state._method.id) ||
      ([3].includes(state._method.id) && ![1].includes(state._media.id))
    );
  }
  return false;
}
function isOffline() {
  if (state._method) {
    return [2, 3].includes(state._method.id);
  }
  return false;
}

watch([state], () => {
  if (
    step.value == 1 &&
    state._eventType !== null &&
    state._rdgType !== null &&
    state._month !== null &&
    state._year !== null &&
    state._rdg !== null &&
    state._event !== null
  ) {
    buttonNext.value = true;
  }
});

// Watch _month and _year, dispatch only when both are not null and change
watch(
  [() => state._month, () => state._year],
  ([newMonth, newYear], [oldMonth, oldYear]) => {
    // Only dispatch if both are not null and changed
    if (
      newMonth !== null &&
      newYear !== null &&
      (newMonth !== oldMonth || newYear !== oldYear)
    ) {
      state._rdg = null;
      store
        .dispatch("eventStore/fetchEventSubTypeListByEventId", {
          rdgType: state._rdgType.id,
          month: newMonth.id,
          year: typeof newYear === "string" ? parseInt(newYear) : newYear,
        })
        .then((data) => {
          listRDG.value = data;
        });
    }
  }
);

watch(
  () => state._rdg,
  (val) => {
    if (val) {
      store
        .dispatch("eventStore/fetchEventbySubTypeListId", {
          idEvent: val.idEvent,
        })
        .then((data) => {
          listEvent.value = data;
        });
      state._event = null;
    }
  }
);

watch(
  () => state._method,
  (val) => {
    if (val) {
      if ([1, 3].includes(val.id)) {
        /* Media */
        store.dispatch("eventStore/fetchListMeetingPlatform").then((data) => {
          listMedia.value = data;
        });
      }
      state._media = null;
      state._mediaBackup = null;
      state._linkMeeting = "";
    }
  }
);

watch(
  () => state._media,
  (val) => {
    if (val == state._mediaBackup) {
      state._mediaBackup = null;
      state._linkMeetingBackup = "";
    }
  }
);

watch(
  () => step.value,
  (val) => {
    if (val === 2) {
      /* Method */
      store.dispatch("eventStore/fetchListMeetingMethod").then((data) => {
        listMethod.value = data;
      });
    }
  }
);
defineExpose({
  show,
});
</script>

<style scoped>
:deep(.steppy) {
  margin-left: auto;
  margin-right: auto;
  max-width: 600px;
  width: 100%;
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
  margin: 60px 0 0 0 !important;
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

.red-color {
  color: red;
}

div.v-field__append-inner > i {
  display: none !important;
}

:deep(.v-input__details) {
  text-align: start;
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

:deep(.v-messages__message) {
  font-family: "Poppins", sans-serif;
}

:deep(.v-field--disabled) {
  background-color: #dfdfdf;
}
</style>
