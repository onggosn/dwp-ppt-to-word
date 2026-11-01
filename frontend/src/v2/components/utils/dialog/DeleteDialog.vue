<template>
  <v-btn v-if="type" class="pa-2 mr-2 shadow" min-width="0" @click="openDialog">
    <v-icon>mdi-delete</v-icon>
  </v-btn>
  <v-btn
    v-else-if="!type && isIconButton"
    @click="openDialog"
    :class="['rounded pa-1 mt-1', btnClass]"
    min-width="0"
    :color="btnColor"
    :variant="btnVariant"
    :size="btnSize"
  >
    <v-icon
      v-if="hideIcon == false"
      :color="btnColor"
      size="medium"
      style="cursor: pointer"
    >
      mdi-delete
    </v-icon>
    <slot />
  </v-btn>

  <v-btn
    v-else
    @click="openDialog"
    :variant="btnVariant"
    :color="btnColor"
    :class="['rounded-lg', btnClass]"
    :density="btnDensity"
    style="letter-spacing: 0px"
  >
    <v-icon
      :icon="btnIcon"
      start
      :color="btnIconColor"
      v-if="appendIcon"
    ></v-icon>
    {{ btnTitle }}
    <v-icon
      :icon="btnIcon"
      end
      :color="btnIconColor"
      v-if="prependIcon"
    ></v-icon>
  </v-btn>
  <v-dialog v-model="dialog" :width="dialogWidth" persistent>
    <v-card
      style="
        border-radius: 10px;
        background: transparent;
        box-shadow: 0px 0px;
        overflow: visible;
      "
    >
      <v-card-text
        style="
          padding-top: 0px;
          background: white;
          border-radius: 10px 10px 0px 0px;
        "
      >
        <v-sheet style="background: transparent" class="text-center">
          <img
            class="mt-n8"
            src="/images/sampahModalNew.svg"
            style="margin-top: -60px; height: 100px"
          />
        </v-sheet>
        <p
          class="text-h5 pt-2 text-center"
          style="
            color: #404040;
            font-weight: 700;
            margin-bottom: 20px;
            font-family: Poppins;
            justify-content: center;
          "
        >
          {{ title }}
        </p>
        <div class="px-10">
          <p
            class="text-center"
            style="color: rgb(121, 121, 121); margin-bottom: 24px"
          >
            {{ subtitle }}
          </p>
        </div>
        <p class="text-center" style="color: rgb(121, 121, 121)">
          {{ description }}
        </p>
      </v-card-text>
      <v-card-actions
        class="justify-end pb-5"
        :class="type ? 'pt-5' : ''"
        style="
          padding-top: 0px;
          background: white;
          border-radius: 0px 0px 10px 10px;
        "
      >
        <v-spacer></v-spacer>
        <v-btn
          :disabled="loading"
          elevation="3"
          style="
            background: linear-gradient(#fff -46.47%, #fff 157.9%);
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            font-weight: 800;
            width: 5.5vw;
            color: #065695;
          "
          @click="dialog = false"
        >
          {{ negativeTextButton }}
        </v-btn>
        <v-btn
          :disabled="timer > 0"
          :loading="loading"
          elevation="3"
          class="btn-color-process mr-4"
          style="
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
            margin-left: 10px;
            font-weight: 800;
            color: white;
            font-weight: 600;
            background: linear-gradient(#d6212a, #ff000d);
            width: 5.5vw;
          "
          @click="positiveButton"
        >
          {{ positiveTextButton }} <span v-if="timer > 0">({{ timer }})</span>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <ModalConfirm ref="modalWarning" :form-config="warningConfig">
    <template v-slot:icon-img>
      <v-avatar color="white" size="80" style="margin-top: -60px">
        <img :src="'/images/warningAlert.png'" style="width: 75px" />
      </v-avatar>
    </template>
    <template v-slot:btn-action>
      <div>
        <v-btn
          @click="handleCloseWarning"
          variant="outlined"
          color="#065695"
          class="mr-2 rounded-lg btn"
        >
          Close
        </v-btn>
        <v-btn
          @click="handleConfirmWarning"
          class="mr-2 rounded-lg btn primary-gradient"
        >
          Yes
        </v-btn>
      </div>
    </template>
  </ModalConfirm>
</template>
<script lang="ts" setup>
import { ref, onUpdated, watch } from "vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { TModalConfirm } from "@v2/Type";
const dialog = ref(false);
const timer = ref(0);
watch(dialog, (newVal) => {
  if (!newVal) return;
  timer.value = Math.abs(props.positiveButtonTimer);
  if (timer.value > 0) {
    setTimeout(() => {
      const rundown = setInterval(() => {
        timer.value--;
        if (timer.value == 0) clearInterval(rundown); // STOP RUNDOWN
      }, 1000);
    }, 500); // Timer Delay times
  }
});

const props = defineProps({
  idToDelete: { type: Number, default: -99 },
  title: { type: String, default: "Delete" },
  subtitle: { type: String, default: "Delete" },
  description: { type: String, default: "Delete" },
  btnTitle: { type: String, default: "Delete" },
  btnColor: { type: String, default: "red" },
  btnIcon: { type: String, default: "mdi-delete" },
  btnIconColor: { type: String, default: "red" },
  btnVariant: { type: String, default: "outlined" },
  btnSize: { type: String, default: "small" },
  appendIcon: { type: Boolean, default: false },
  prependIcon: { type: Boolean, default: false },
  countDown: { type: Number, default: 10 },
  negativeTextButton: { type: String, default: "Cancel" },
  positiveTextButton: { type: String, default: "Yes" },
  positiveButtonTimer: { type: Number, default: 0 },
  btnDensity: { type: String, default: "default" },
  isIconButton: { type: Boolean, default: false },
  hideIcon: { type: Boolean, default: false },
  btnClass: { type: String, required: false },
  disabledDeleteLastItem: { type: Boolean, default: false },
  itemCount: { type: Number, default: 0 },
  warningTitle: { type: String, default: "Warning" },
  warningMessage: {
    type: String,
    default:
      "You cannot delete the last section. At least one section must remain to ensure the continuity of this content",
  },
  type: { type: String, default: "" },
  dialogWidth: { type: Number, default: 450 },
});

const countDownState = ref(props.countDown);
const loading = ref(false);
const showCounter = ref(true);
const interval = ref();
const emit = defineEmits(["update", "onConfirmed"]);
const modalWarning = ref();
const warningConfig = ref<TModalConfirm>({
  title: props.warningTitle,
  message: props.warningMessage,
});

const positiveButton = () => {
  emit("update", { dialog, modalWarning, warningConfig });
};

const handleCloseWarning = () => {
  modalWarning.value.hide();
};

const handleConfirmWarning = () => {
  emit("onConfirmed");
  handleCloseWarning();
};

const openDialog = () => {
  if (props.disabledDeleteLastItem) {
    modalWarning.value.show({});
  } else {
    dialog.value = true;
  }
};

defineExpose({ openDialog });

onUpdated(() => {
  if (dialog.value) {
    if (props.type) {
      countDownState.value = 0;
      showCounter.value = false;
    } else {
      countDownState.value = props.countDown;
      interval.value = setInterval(() => {
        countDownState.value--;

        if (countDownState.value <= 0) {
          clearInterval(interval.value);
          showCounter.value = false;
        }
      }, 1000);
    }
  } else {
    clearInterval(interval.value);
    showCounter.value = true;
  }
});
</script>
