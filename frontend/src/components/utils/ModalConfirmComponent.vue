<template>
  <v-dialog
    v-model="show"
    persistent
    :width="formConfirm.width"
    class="dialog-visible"
  >
    <div
      class="modal-container d-flex flex-column"
      :style="{ 'min-width': formConfirm.width + 'px' }"
    >
      <span
        @click="hide"
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
          src="/images/closeIcon.png"
        />
      </span>
      <div style="position: relative" class="text-center">
        <slot name="icon-img">
          <v-avatar
            v-if="formConfirm.icon && formConfirm.icon.code"
            color="white"
            size="90"
            style="margin-top: -60px"
          >
            <v-icon size="90" :color="formConfirm.icon.color">
              {{ formConfirm.icon.code }}
            </v-icon>
          </v-avatar>
          <img
            v-else
            src="/images/sampahModal.svg"
            style="margin-top: -60px; height: 100px"
          />
        </slot>
      </div>
      <div class="text-center my-1">
        <p class="mb-0 text-17" style="font-weight: 700; color: #3a416f">
          {{ formConfirm.title }}
        </p>
        <div class="mt-2 text-15 text-center">
          <slot>
            <div class="mx-4" v-html="formConfirm.message"></div>
          </slot>
        </div>
      </div>
      <div class="text-end mt-4">
        <slot name="btn-action" :modalData="modalData">
          <v-btn
            @click="hide()"
            class="mr-2 rounded-lg btn"
            color="#065695"
            style="background: #fff; color: #065695"
          >
            Cancel
          </v-btn>
          <slot name="btn-action-confirm" :modalData="modalData">
            <v-btn
              @click="actionConfirm()"
              :class="[
                'ml-2 rounded-lg btn',
                isDelay ? 'btn-disable' : '',
                formConfirm.btnSubmitColor ?? 'btn-danger',
              ]"
              :loading="isDelay"
              :disabled="isDelay"
            >
              {{ formConfirm.btnSubmitLabel }}
            </v-btn>
          </slot>
        </slot>
      </div>
    </div>
  </v-dialog>
</template>

<script>
export default {
  name: "modalConfirm",
  props: {
    formConfirm: {
      type: Object,
      default: function () {
        return {
          title: null,
          width: 500,
          btnSubmitLabel: "Submit",
          btnSubmitColor: "btn-danger",
          message: "No Message Detected",
          icon: {
            code: "mdi-close-circle-outline",
            color: "red",
          },
        };
      },
    },
  },
  data: function () {
    return {
      show: false,
      isDelay: false,
      modalData: null,
    };
  },
  methods: {
    start(modalData, delay = 0) {
      this.modalData = modalData;

      if (delay > 0) {
        this.isDelay = true;
        setTimeout(() => {
          this.isDelay = false;
        }, delay * 1000);
      }
      this.show = true;
    },
    hide() {
      this.show = false;
    },
    open() {
      this.show = true;
    },
    closeModal() {
      this.hide();
    },
    actionConfirm() {
      this.show = false;
      this.$emit("action-confirm", this.modalData);
    },
  },
};
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
</style>
