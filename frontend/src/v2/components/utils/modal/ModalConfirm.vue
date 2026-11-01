<template>
  <Teleport to="body">
    <v-dialog
      v-model="isShow"
      persistent
      :width="config.width"
      class="dialog-visible"
    >
      <div
        class="modal-container d-flex flex-column"
        style="border-radius: 10px"
        :style="{ 'min-width': config.width + 'px' }"
      >
        <span
          @click="closeModal"
          class="closeModal pointer-click"
          style="
            text-align: end;
            position: absolute;
            right: 1px;
            top: 1vh;
            cursor: pointer;
          "
        >
          <img
            class="pointer-click"
            style="height: 25px; position: relative; left: -11px"
            :src="require('@v2/assets/icon/close.svg')"
          />
        </span>
        <div
          style="position: relative"
          class="text-center"
          v-if="config.showIcon"
        >
          <slot name="icon-img">
            <v-avatar
              :color="config.icon?.backgrounColor"
              size="90"
              style="
                margin-top: -60px;
                filter: drop-shadow(#9b9b9b 1px 1px 1.5px);
              "
            >
              <v-icon
                :size="config.icon.size"
                :color="config.icon.color"
                v-if="config.icon"
              >
                {{ config.icon.code }}
              </v-icon>
            </v-avatar>
          </slot>
        </div>
        <div class="text-center my-1">
          <p
            class="mb-0"
            :class="config.titleClass || 'text-17'"
            style="padding-top: 20px; font-weight: 700; color: #3a416f"
          >
            {{ config.title }}
          </p>
          <div class="mt-2 text-15" :class="config.messageClass">
            <slot name="desc">
              <div class="txt-message mx-4" v-html="config.message"></div>
            </slot>
          </div>
          <div class="mt-2 text-15 text-center">
            <slot name="text-area" />
          </div>
        </div>
        <div :class="[isWarning ? 'text-center' : 'text-end', 'mt-4']">
          <slot name="btn-action" :modalData="modalData">
            <v-btn
              v-if="!isWarning"
              @click="closeModal()"
              class="mr-2 rounded-lg btn"
              color="#065695"
              style="background: #fff; color: #065695"
            >
              {{ config.btnCancelLabel || "Cancel" }}
            </v-btn>
            <slot name="btn-action-confirm" :modalData="modalData">
              <v-btn
                v-if="isLoading"
                :class="[
                  'ml-2 rounded-lg btn',
                  config.btnSubmitColor ?? 'btn-danger',
                ]"
                :loading="true"
              ></v-btn>
              <v-btn
                v-else
                @click="actionConfirm()"
                :class="[
                  'ml-2 rounded-lg btn',
                  isDelay ? 'btn-disable' : '',
                  config.btnSubmitColor ?? 'btn-danger',
                ]"
                :loading="isDelay"
                :disabled="isDelay"
              >
                {{ config.btnSubmitLabel }}

                <template v-slot:loader v-if="config.usingTimeOut">
                  <span class="text-11 d-flex align-center">
                    {{ config.btnSubmitLabel }} ({{ countDelay }})
                  </span>
                </template>
              </v-btn>
            </slot>
          </slot>
        </div>
      </div>
    </v-dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { PropType } from "vue";
import type { TModalConfirm } from "@v2/Type.d";
import { computed } from "vue";

const isShow = ref(false);
const countDelay = ref<number>(0);
const modalData = ref<any>(null);
// eslint-disable-next-line no-undef
const intervalId = ref<NodeJS.Timeout | undefined>(); // Added to store interval ID
const emit = defineEmits(["actionConfirm", "actionCancel"]);

const prop = defineProps({
  formConfig: {
    type: Object as PropType<TModalConfirm>,
    default: function () {
      return {
        title: null,
        message: "No Message Detected",
      };
    },
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  isWarning: {
    type: Boolean,
    default: false,
  },
});

const config = computed((): TModalConfirm => {
  return {
    width: 500,
    btnSubmitLabel: "Submit",
    btnSubmitColor: "btn-danger",
    showIcon: true,
    icon: {
      code: "mdi-trash-can-outline",
      color: "red",
      backgrounColor: "white",
      size: 70,
    },
    usingTimeOut: false,
    ...prop.formConfig,
  };
});

const isDelay = computed((): boolean => {
  return countDelay.value != 0;
});

function show(data: any, delay = 0) {
  modalData.value = data;

  // Clear any existing interval before starting a new one
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = undefined;
  }

  if (delay > 0) {
    countDelay.value = delay;
    intervalId.value = setInterval(() => {
      countDelay.value--;
      if (countDelay.value <= 0) {
        clearInterval(intervalId.value);
        intervalId.value = undefined;
      }
    }, 1000);
  }
  isShow.value = true;
}

function closeModal(): void {
  if (prop.isLoading === false) {
    // Clear the interval when closing the modal
    if (intervalId.value) {
      clearInterval(intervalId.value);
      intervalId.value = undefined;
    }
    hide();
  }
}

function hide(withCancel = true) {
  isShow.value = false;
  if (withCancel) {
    emit("actionCancel");
  }
}

function actionConfirm() {
  emit("actionConfirm", modalData.value);
}

defineExpose({
  show,
  hide,
  actionConfirm,
});
</script>

<style scoped>
:deep(.v-dialog) {
  overflow: visible !important;
}

.btn {
  font-weight: 600;
  box-shadow: 0px 1px 5px #888888;
}

.btn-disable {
  color: white !important;
  background: #9b9b9b;
}

.modal-container {
  border-radius: 20px;
  margin: 0px auto;
  padding: 20px 30px;
  background: #ffffff;
  box-shadow: 0px -4px 4px rgb(0 0 0 / 25%), 0px 4px 4px rgb(0 0 0 / 25%);
  backdrop-filter: blur(6px);
}
.txt-message {
  color: #797979e5;
}
</style>
