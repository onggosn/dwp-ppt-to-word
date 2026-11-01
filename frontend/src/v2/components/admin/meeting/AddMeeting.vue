<template>
  <CustomDialog
    @handleShowDialog="handleShowDialog"
    :showDialogProps="isShowDialog"
    :buttonClass="btnStyle"
    :variant="variant"
    :title="modalTitle"
    :buttonLabel="modalTitle"
    :prependIcon="prependIcon"
  >
    <hr class="line mt-3" />
    <v-form ref="form" class="pt-4">
      <!-- EVENT TYPE -->
      <!-- #region -->
      <div v-if="!isEditForm">
        <p class="ml-2 text-left text-darkBlue font-weight-bold">
          Event Type<span class="text-gradient-red">*</span>
        </p>
        <v-autocomplete
          :loading="store.getters['eventStore/getLoading']"
          v-model="state.eventType"
          :items="listEventType"
          variant="solo"
          placeholder="Choose event type"
          class="px-2 mt-1"
          item-title="value"
          item-value="id"
          return-object
          :error-messages="getErrorMessages(v$.eventType)"
          :hide-details="isError(v$.eventType)"
        ></v-autocomplete>
      </div>

      <v-autocomplete
        v-if="state.eventType"
        v-model="state.rdgType"
        :loading="store.getters['eventStore/getLoading']"
        :items="listRdgType"
        variant="solo"
        placeholder="Choose RDG Type"
        class="px-2 mt-1"
        item-title="value"
        return-object
        :hide-details="isError(v$.rdgType)"
        :error-messages="getErrorMessages(v$.rdgType)"
      ></v-autocomplete>

      <v-autocomplete
        v-if="state.rdgType"
        v-model="state.sector"
        :loading="store.getters['eventStore/getLoading']"
        :items="listSector"
        variant="solo"
        placeholder="Choose Sector"
        class="px-2 mt-1"
        item-value="idMSector"
        item-title="sectorName"
        return-object
        :hide-details="isError(v$.sector)"
        :error-messages="getErrorMessages(v$.sector)"
      ></v-autocomplete>

      <v-autocomplete
        v-if="state.sector"
        v-model="state.stage"
        :loading="store.getters['eventStore/getLoading']"
        :items="listStage"
        variant="solo"
        placeholder="Choose Stage"
        class="px-2 mt-1"
        item-title="value"
        return-object
        :hide-details="isError(v$.stage)"
        :error-messages="getErrorMessages(v$.stage)"
      ></v-autocomplete>
      <!-- #endregion -->

      <!-- TITLE -->
      <!-- #region -->
      <p class="ml-2 text-left text-darkBlue font-weight-bold pt-4">
        Title<span class="text-gradient-red">*</span>
      </p>
      <v-text-field
        variant="solo"
        placeholder="Insert title"
        class="px-2 mt-1"
        v-model="state.title"
        :error-messages="getErrorMessages(v$.title)"
        :hide-details="isError(v$.title)"
      ></v-text-field>
      <!-- #endregion -->

      <!-- METHOD -->
      <!-- #region -->
      <p class="ml-2 text-left text-darkBlue font-weight-bold pt-4">
        Method<span class="text-gradient-red">*</span>
      </p>
      <v-autocomplete
        :loading="store.getters['eventStore/getLoading']"
        v-model="state.method"
        :items="listMethod"
        variant="solo"
        placeholder="Choose method"
        class="px-2 mt-1"
        item-title="value"
        item-value="id"
        :error-messages="getErrorMessages(v$.method)"
        :hide-details="isError(v$.method)"
      ></v-autocomplete>
      <!-- #endregion -->

      <!-- MEDIA -->
      <!-- #region -->
      <template v-if="!isOffline">
        <p class="ml-2 text-left text-darkBlue font-weight-bold pt-4">
          Media<span class="text-gradient-red">*</span>
        </p>
        <v-autocomplete
          :loading="store.getters['eventStore/getLoading']"
          v-model="state.media"
          :items="listMedia"
          variant="solo"
          placeholder="Choose media"
          class="px-2 mt-1"
          item-title="platform"
          item-value="id"
          :error-messages="getErrorMessages(v$.media)"
          :hide-details="isError(v$.media)"
        ></v-autocomplete>
      </template>

      <!-- #endregion -->

      <!-- START DATE -->
      <!-- #region -->
      <p class="ml-2 text-left text-darkBlue font-weight-bold pt-4">
        Start Date<span class="text-gradient-red">*</span>
      </p>
      <div class="d-flex">
        <div>
          <v-autocomplete
            v-model="state.prependStartDate"
            :items="[
              { id: '1', value: '-' },
              { id: '2', value: '+' },
            ]"
            variant="solo"
            item-title="value"
            item-value="id"
            :hide-details="isError(v$.prependStartDate)"
            :error-messages="getErrorMessages(v$.prependStartDate)"
            class="start-date mt-1"
          ></v-autocomplete>
        </div>
        <div class="flex-1-0">
          <v-text-field
            variant="solo"
            placeholder="Input number"
            class="mt-1 input-number"
            v-model="state.startDate"
            :error-messages="getErrorMessages(v$.startDate)"
            :hide-details="isError(v$.startDate)"
          >
          </v-text-field>
        </div>
      </div>

      <span class="text-grey-darken-3 text-11 ml-2"
        >Number of days before (-) or after (+) {{ rdgStartDateLabel }}</span
      >
      <!-- #endregion -->
    </v-form>
    <div class="text-right pb-5 pr-2 mt-4">
      <v-btn
        class="mr-2 rounded-lg text-light-blue-darken-4"
        :loading="store.getters['eventStore/getLoading']"
        @click="handleShowDialog"
        >Cancel</v-btn
      >
      <v-btn
        v-if="isEditForm"
        class="primary-gradient rounded-lg px-5"
        elevation="4"
        :loading="store.getters['eventStore/getLoading']"
        @click="handleEdit"
        >Save</v-btn
      >
      <v-btn
        v-else
        class="primary-gradient rounded-lg"
        elevation="4"
        :loading="store.getters['eventStore/getLoading']"
        @click="handleCreate"
        >Create</v-btn
      >
    </div>
  </CustomDialog>
</template>
<script lang="ts" setup>
import { ref, computed, watch, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import CustomDialog from "@/v2/components/utils/dialog/CustomDialog.vue";
import { TRequestAddMeeting } from "@/v2/Type";
import { numeric, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { getErrorMessages, isError } from "@/v2/helpers/validation";

const emit = defineEmits(["onSuccess"]);

const props = defineProps({
  isEditForm: {
    type: Boolean,
    default: false,
  },
  formData: {
    type: Object,
    default: () => ({}),
  },
  btnStyle: {
    type: Array,
    default: () => ["primary-gradient", "mr-2 rounded-lg", "font-weight-bold"],
  },
  variant: {
    type: String,
    default: "elevated",
  },
});

const { root } = getCurrentInstance() as any;
const store = useStore();
const isShowDialog = ref<boolean>(false);
const listEventType = ref([]);
const listMethod = ref([]);
const listMedia = ref([]);
const listRdgType = ref([]);
const listSector = ref([]);
const listStage = ref([]);
const state = ref<TRequestAddMeeting>({
  eventType: null,
  rdgType: null,
  sector: null,
  stage: null,
  title: null,
  method: null,
  media: null,
  startDate: null,
  prependStartDate: "-",
});
const idEvent = ref();
const rules = computed(() => {
  const localRule = {
    eventType: {},
    title: { required },
    method: { required },
    media: {},
    startDate: { required, numeric },
    rdgType: {},
    sector: {},
    stage: {},
    prependStartDate: { required },
  };

  if (state.value.method && [1, 3].includes(state.value.method))
    localRule.media = { required };

  if (!props.isEditForm) {
    localRule.eventType = { required };
    localRule.rdgType = { required };
    localRule.sector = { required };
    localRule.stage = { required };
  }

  return localRule;
});

const modalTitle = computed(() => {
  if (!props.isEditForm) return "Add Meeting";
  return "Edit Meeting";
});

const rdgStartDateLabel = computed(() => {
  const rdgType = state.value.rdgType?.value?.toLowerCase();

  if (rdgType?.includes("rdgm")) return "RDGM";
  return "RDGB H2";
});

const prependIcon = computed(() => {
  if (!props.isEditForm) {
    return "mdi-plus";
  } else {
    return "mdi-pencil";
  }
});

const v$ = useVuelidate(rules, state);

const isOffline = computed(() => {
  return state.value.method && [2].includes(state.value.method);
});

const handleShowDialog = () => {
  if (props.isEditForm) {
    isShowDialog.value = !isShowDialog.value;
  } else {
    isShowDialog.value = !isShowDialog.value;
    clearFormInput();
    v$.value.$reset();
  }
};
const clearFormInput = () => {
  state.value.eventType = null;
  state.value.rdgType = null;
  state.value.sector = null;
  state.value.stage = null;
  state.value.title = null;
  state.value.method = null;
  state.value.media = null;
  state.value.startDate = null;
  state.value.prependStartDate = "-";
};
function validateTimeType(temp: any) {
  if (temp === "-" || temp === "1") {
    return false;
  } else {
    return true;
  }
}
const handleEdit = () => {
  v$.value.$validate().then((valid) => {
    if (valid) {
      const req = {
        idMEventTemplate: idEvent.value,
        title: state.value.title,
        idMeventMethod: resolveEventMethod(state.value.method),
        idMeetingPlatfrom:
          resolveMeetingPlatform(state.value.media) == null
            ? 0
            : resolveMeetingPlatform(state.value.media),
        timeDifferentMainEvent: state.value.startDate,
        isTimeType: validateTimeType(state.value.prependStartDate),
      };
      store
        .dispatch("adminStore/updateGeneralMeeting", req)
        .then(() => {
          root.refs.toast.show({
            message: "Successfully Saved",
            color: "success",
            timeout: 3000,
          });
        })
        .catch(() => {
          root.refs.toast.show({
            message: "Sorry, failed Saved",
            color: "error",
            timeout: 3000,
          });
        })
        .finally(() => {
          emit("onSuccess", true);
          handleShowDialog();
        });
    }
  });
};

// Add helper function to resolve idEventMethod when state.value.method is a string
function resolveEventMethod(method: any): number {
  if (typeof method === "string") {
    const found = listMethod.value.find(
      (item: any) => item.value === method
    ) as any;
    return found ? found.id : 0;
  }
  return method;
}

// Add helper function to resolve idMeetingPlatfrom from media value
function resolveMeetingPlatform(media: any): number {
  if (typeof media === "string") {
    const found = listMedia.value.find(
      (item: any) => item.platform === media
    ) as any;
    return found ? found.id : 0;
  }
  return media;
}

// In handleCreate, update idEventMethod using the helper function
const handleCreate = () => {
  v$.value.$validate().then((valid) => {
    if (valid) {
      const req = {
        idMEventSubType: state.value.eventType?.id,
        idMEventSubTypeList: state.value.rdgType?.id,
        MEventTemplateType: state.value.eventType?.value,
        idMSector: state.value.sector?.idMSector,
        idMBPTemplate: state.value.stage?.id,
        MEventName: state.value.title,
        idEventMethod: state.value.method,
        idMeetingPlatform: resolveMeetingPlatform(state.value.media),
        timeDiffFromMainEvent: parseInt(state.value.startDate),
        isTimeType: validateTimeType(state.value.prependStartDate),
      };
      store
        .dispatch("adminStore/storeMeeting", req)
        .then(() => {
          root.refs.toast.show({
            message: "Successfully Created",
            color: "success",
            timeout: 3000,
          });
        })
        .catch(() => {
          root.refs.toast.show({
            message: "Sorry, failed Created",
            color: "error",
            timeout: 3000,
          });
        })
        .finally(() => {
          emit("onSuccess", true);
          handleShowDialog();
        });
    }
  });
};

/* Event Type */
store.dispatch("eventStore/fetchListSubEventType", 1).then((data) => {
  listEventType.value = data;
});
/* Method */
store.dispatch("eventStore/fetchListMeetingMethod").then((data) => {
  listMethod.value = data;
});
/* Media */
store.dispatch("eventStore/fetchListMeetingPlatform").then((data) => {
  listMedia.value = data;
});
/* Rdg Type */
const fetchSubEventType = (id: number) => {
  store.dispatch("eventStore/fetchListSubSubEventType", id).then((data) => {
    listRdgType.value = data;
  });
};

function fetchSectors(id: number) {
  const formData = {
    idMEventSubTypeList: id,
  };
  store
    .dispatch("adminStore/getListSector", formData)
    .then(({ responseData }) => {
      listSector.value = responseData;
    });
}
/* Stage */
const fetchStage = (id: number) => {
  store
    .dispatch("eFormStore/getMBPTemplateNewMeeting", {
      idMEventSubTypeList: state.value.rdgType?.id,
      idMSector: id,
    })
    .then(({ responseData }) => {
      listStage.value = responseData;
    });
};

watch(
  () => state.value.eventType,
  (val: any) => {
    state.value.rdgType = null;
    state.value.sector = null;
    state.value.stage = null;
    listRdgType.value = [];
    listStage.value = [];
    listSector.value = [];
    if (val) fetchSubEventType(val.id);
  }
);

watch(
  () => isShowDialog.value,
  (val: any) => {
    if (val && props.isEditForm) {
      idEvent.value = props.formData.idEvent ?? props.formData.id;
      state.value.title = props.formData.title;
      state.value.method = props.formData.method;
      state.value.media = props.formData.media;
      state.value.prependStartDate =
        props.formData.isTimeType == true ? "+" : "-";
      // convertPrependValue(
      //   props.formData.timeDifferent
      // );
      state.value.startDate = Math.abs(parseInt(props.formData.timeDifferent));
    }
  }
);

watch(
  () => state.value.rdgType,
  (val: any) => {
    state.value.sector = null;
    state.value.stage = null;

    listStage.value = [];
    listSector.value = [];
    if (val) fetchSectors(val.id);
  }
);

watch(
  () => state.value.sector,
  (val: any) => {
    state.value.stage = null;

    listStage.value = [];

    if (val) fetchStage(val.idMSector);
  }
);
</script>
<style scoped>
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
:deep(.v-text-field .v-input__details) {
  padding-inline-start: 0;
}
:deep(.v-field--variant-solo, .v-field.v-field--appended) {
  border-radius: 12px !important;
}
:deep(.input-number .v-field--variant-solo) {
  border-top-left-radius: 0px !important;
  border-bottom-left-radius: 0px !important;
}
:deep(.start-date .v-field.v-field--appended) {
  border-top-right-radius: 0px !important;
  border-bottom-right-radius: 0px !important;
}
</style>
