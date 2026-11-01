<template>
  <v-btn v-if="type" class="pa-2 mr-2 shadow" min-width="0" @click="openDialog">
    <v-icon>mdi-delete</v-icon>
  </v-btn>
  <v-btn
    v-else-if="!type && isIconButton"
    @click="openDialog"
    :class="['rounded-lg px-2 py-2', btnClass]"
    min-width="0"
    :color="btnColor"
    :variant="btnVariant"
    :disabled="disabled"
  >
    <v-icon :color="btnColor" small style="cursor: pointer">mdi-delete</v-icon>
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
    :disabled="disabled"
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
  <v-dialog v-model="dialog" width="450" persistent>
    <v-card
      style="
        border-radius: 10px;
        background: transparent;
        box-shadow: 0px 0px;
        position: relative;
      "
    >
      <v-card-title class="text-center pa-0">
        <v-sheet style="background: transparent; height: 6vh"> </v-sheet>
      </v-card-title>
      <v-card-text
        style="
          padding-top: 0px;
          background: white;
          border-radius: 10px 10px 0px 0px;
          box-shadow: none;
          position: relative;
        "
      >
        <v-btn
          icon
          variant="text"
          style="position: absolute; top: 8px; right: 8px; z-index: 10"
          @click="dialog = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-sheet style="background: transparent" class="text-center">
          <img
            class="mt-n8"
            src="/images/sampahModalNew.svg"
            style="margin-top: -60px; height: 100px"
          />
        </v-sheet>
        <p
          class="text-h6 pt-2 text-center"
          style="justify-content: center; color: #3a416f"
        >
          {{ title }}
        </p>
        <p class="text-center" style="color: rgb(121, 121, 121)">
          {{ subtitle }}
        </p>
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
          box-shadow: 10px 10px;
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
          "
          :style="type ? 'color: #065695' : 'color: red'"
          @click="dialog = false"
        >
          {{ negativeTextButton }}
        </v-btn>
        <v-btn
          v-if="!showCounter"
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
          {{ positiveTextButton }}
        </v-btn>
        <v-btn
          v-if="showCounter"
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
            background: linear-gradient(grey, darkgrey);
            pointer-events: none;
            width: 6.5vw;
          "
        >
          <p style="position: absolute">
            {{ positiveTextButton }} ({{ countDownState }})
          </p>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <ModalConfirm ref="modalWarning" :form-config="modalConfig">
    <template v-slot:icon-img>
      <v-avatar color="white" size="80" style="margin-top: -60px">
        <img :src="'/images/warningAlert.png'" style="width: 75px" />
      </v-avatar>
    </template>
    <template v-slot:btn-action>
      <div style="text-align: center">
        <v-btn
          @click="handleCloseWarning"
          class="mr-2 rounded-lg btn primary-gradient"
        >
          Close
        </v-btn>
      </div>
    </template>
  </ModalConfirm>
</template>
<script lang="ts" setup>
import { ref, onUpdated, watch, onUnmounted } from "vue";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { TModalConfirm } from "@v2/Type";
const dialog = ref(false);

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
  appendIcon: { type: Boolean, default: false },
  prependIcon: { type: Boolean, default: false },
  countDown: { type: Number, default: 10 },
  negativeTextButton: { type: String, default: "Cancel" },
  positiveTextButton: { type: String, default: "Yes" },
  btnDensity: { type: String, default: "default" },
  isIconButton: { type: Boolean, default: false },
  btnClass: { type: String, required: false },
  disabledDeleteLastItem: { type: Boolean, default: false },
  itemCount: { type: Number, default: 0 },
  warningMessage: {
    type: String,
    default:
      "You cannot delete the last section. At least one section must remain to ensure the continuity of this content",
  },
  type: { type: String, default: "" },
  disabled: { type: Boolean, default: false },
});

const countDownState = ref(props.countDown);
const loading = ref(false);
const showCounter = ref(true);
const interval = ref();
const emit = defineEmits(["update"]);
const modalWarning = ref();
const modalConfig = ref<TModalConfirm>({
  title: "Warning",
  message: props.warningMessage,
});

const positiveButton = () => {
  emit("update");
};

const handleCloseWarning = () => {
  modalWarning.value.hide();
};

const openDialog = () => {
  if (props.disabledDeleteLastItem) {
    modalWarning.value.show({});
  } else {
    dialog.value = true;
  }
};

defineExpose({ openDialog });

watch(dialog, (isOpen) => {
  // clear interval first
  if (interval.value) {
    clearInterval(interval.value);
    interval.value = null;
  }

  if (isOpen) {
    if (props.type) {
      countDownState.value = 0;
      showCounter.value = false;
    } else {
      // then start countdown
      showCounter.value = true;
      countDownState.value = props.countDown;

      interval.value = setInterval(() => {
        countDownState.value--;

        if (countDownState.value <= 0) {
          clearInterval(interval.value);
          interval.value = null;
          showCounter.value = false;
        }
      }, 1000);
    }
  } else {
    showCounter.value = true;
  }
});

//always clear interval on unmount
onUnmounted(() => {
  if (interval.value) {
    clearInterval(interval.value);
  }
});
</script>
