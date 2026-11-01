<template>
  <v-dialog v-model="show" persistent :width="500" class="dialog-visible">
    <div
      class="modal-container d-flex flex-column"
      :style="{ 'min-width': '500px' }"
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
        <v-avatar color="white" size="90" style="margin-top: -60px">
          <v-icon size="90" :color="color">
            {{ icon }}
          </v-icon>
        </v-avatar>
      </div>
      <div class="text-center my-1">
        <p class="mb-0 text-17" style="font-weight: 700; color: #3a416f">
          {{ title }}
        </p>
        <div class="mt-2 text-15 text-center">
          <div class="mx-4" v-html="message"></div>
        </div>
      </div>
      <div class="text-center mt-4">
        <slot name="btn-action-confirm" :confirmText="confirmText">
          <v-btn
            @click="hide()"
            class="mr-2 rounded-lg btn"
            color="info"
            style="background: #fff"
          >
            {{ confirmText }}
          </v-btn>
        </slot>
      </div>
    </div>
  </v-dialog>
</template>

<script>
export default {
  name: "modalAlertComponent",
  data: function () {
    return {
      show: false,
      isDelay: false,
      icon: "mdi-help-circle-outline",
      color: "grey",
      title: "no title set",
      message: "no message set",
      confirmText: "Ok",
    };
  },
  methods: {
    start(data = {}) {
      this.icon = this.getIcon(data.icon);
      this.color = this.getColor(data.icon);
      this.title = data.title || "no title set";
      this.message = data.message || "no message set";
      this.confirmText = data.confirmText || "Ok";
      this.show = true;
    },
    getIcon(icon) {
      const MapIcon = {
        info: "mdi-information-outline",
        success: "mdi-check-circle-outline",
        warning: "mdi-information-outline mdi-rotate-225",
        error: "mdi-close-circle-outline",
      };

      return MapIcon[icon] || "mdi-help-circle-outline";
    },
    getColor(icon) {
      const MapColor = {
        info: "info",
        success: "success",
        warning: "warning",
        error: "error",
      };

      return MapColor[icon] || "grey";
    },
    hide() {
      this.show = false;
      this.$emit("confirm");
    },
  },
  watch: {
    "$store.state.modelAlertData": function (val) {
      this.start(val);
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
