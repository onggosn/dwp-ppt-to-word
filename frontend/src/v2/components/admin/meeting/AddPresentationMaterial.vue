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
      <div v-if="!isEditForm">
        <p class="ml-2 text-left text-darkBlue font-weight-bold">
          Event Type<span class="text-gradient-red">*</span>
        </p>
        <v-autocomplete
          :loading="store.getters['eventStore/getLoading']"
          v-model="state.eventType"
          :items="listEventType"
          variant="solo"
          placeholder="Choose Event Type"
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

      <v-autocomplete
        v-if="state.stage"
        v-model="state.event"
        :loading="store.getters['eventStore/getLoading']"
        :items="listEvent"
        variant="solo"
        placeholder="Choose Event"
        class="px-2 mt-1"
        item-title="value"
        return-object
        :hide-details="isError(v$.event)"
        :error-messages="getErrorMessages(v$.event)"
      ></v-autocomplete>

      <!--CONTENT TITLE -->
      <p class="ml-2 text-left text-darkBlue font-weight-bold pt-4">
        Content Title<span class="text-gradient-red">*</span>
      </p>
      <v-text-field
        variant="solo"
        placeholder="Input Content Title"
        class="px-2 mt-1"
        v-model="state.title"
        :error-messages="getErrorMessages(v$.title)"
        :hide-details="isError(v$.title)"
      ></v-text-field>
    </v-form>
    <div class="text-right pb-5 pr-2 mt-4">
      <v-btn
        class="mr-2 rounded-lg text-light-blue-darken-4"
        :loading="store.getters['eventStore/getLoading']"
        @click="handleShowDialog"
        >Cancel</v-btn
      >

      <v-btn
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
import { TAddPresentationMaterial } from "@/v2/Type";
import { required } from "@vuelidate/validators";
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
const listRdgType = ref([]);
const listSector = ref([]);
const listStage = ref([]);
const listEvent = ref([]);
const state = ref<TAddPresentationMaterial>({
  eventType: null,
  rdgType: null,
  sector: null,
  stage: null,
  event: null,
  title: null,
  username: null,
});
const idEvent = ref();
const rules = computed(() => {
  const localRule = {
    eventType: { required },
    title: { required },
    rdgType: { required },
    sector: { required },
    stage: { required },
    event: { required },
  };

  return localRule;
});

const modalTitle = computed(() => {
  if (!props.isEditForm) return "Add Presentation Material";
  return "Edit Presentation Material";
});

const prependIcon = computed(() => {
  if (!props.isEditForm) {
    return "mdi-plus";
  } else {
    return "mdi-pencil";
  }
});

const v$ = useVuelidate(rules, state);

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
  state.value.event = null;
};

const handleCreate = async () => {
  const valid = await v$.value.$validate();
  if (valid) {
    const req = {
      idMEventTemplate: state.value.event?.id,
      documentName: state.value.title,
      username: store.state.username,
    };

    store
      .dispatch("adminStore/storePresentationMaterial", req)
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
};

/* Event Type */
store.dispatch("eventStore/fetchListSubEventType", 1).then((data) => {
  listEventType.value = data;
});

const fetchSubEventType = (id: number) => {
  store.dispatch("eventStore/fetchListSubSubEventType", id).then((data) => {
    listRdgType.value = data;
  });
};

function fetchSectors(id: number) {
  const formData = {
    idMEventSubTypeList: id,
    isPresentationMaterial: true,
  };
  store
    .dispatch("adminStore/getListSector", formData)
    .then(({ responseData }) => {
      listSector.value = responseData;
    });
}
/* Event */
const fetchEvent = (id: number) => {
  store
    .dispatch("eFormStore/getMEventTemplate", {
      idMBPTemplate: state.value.stage?.id,
      username: store.state.username,
    })
    .then(({ responseData }) => {
      listEvent.value = responseData;
    });
};

/* Stage */
const fetchStage = (id: number) => {
  store
    .dispatch("eFormStore/getMBPTemplateNewMeeting", {
      idMEventSubTypeList: state.value.rdgType?.id,
      idMSector: id,
      isPresentationMaterial: true,
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

watch(
  () => state.value.stage,
  (val: any) => {
    state.value.event = null;

    listEvent.value = [];

    if (val) fetchEvent(val.id);
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
