<template>
  <div>
    <Transition name="modal">
      <div
        v-if="show"
        class="modal-mask"
        id="approveNotifModal"
        :style="
          background
            ? 'z-index: 20011;background-color:transparent'
            : 'z-index: 20011;'
        "
      >
        <div class="modal-wrapper">
          <div
            class="modal-container d-flex flex-column"
            style="min-width: 550px; position: relative"
          >
            <div style="position: relative" class="align-self-center">
              <v-sheet style="background: transparent" class="text-center">
                <v-avatar
                  v-if="getTypeBoolean('notification')"
                  image="/images/icon/badge-notification.png"
                  size="80"
                  class="mt-n16 icon-popup"
                ></v-avatar>
                <v-avatar
                  v-else-if="getTypeBoolean('mfa')"
                  image="/images/icon/iconWarning.png"
                  size="80"
                  class="mt-n10"
                ></v-avatar>
                <v-icon
                  v-else
                  class="mt-n16 icon-popup"
                  icon="mdi-close-circle-outline"
                  size="100"
                  color="red"
                ></v-icon>
              </v-sheet>
            </div>
            <span
              @click="closeModal()"
              class="closeModal pointer-click"
              style="
                text-align: end;
                position: absolute;
                right: 1px;
                top: 1vh;
                cursor: pointer;
              "
            >
              <v-icon class="mr-4">mdi-close</v-icon>
              <!-- <img
                class="pointer-click"
                style="height: 25px; position: relative; left: -11px"
                src="/images/closeIcon.png"
              /> -->
            </span>
            <div class="mt-6">
              <div class="row text-center">
                <p
                  v-if="getTypeBoolean('notification')"
                  style="color: #3a416f; margin-top: -10px"
                  class="text-17 fw-800 mb-2"
                >
                  Enable Notification
                </p>
                <p
                  v-else-if="getTypeBoolean('mfa')"
                  style="color: #3a416f; margin-top: -10px"
                  class="text-17 fw-800 mb-2"
                >
                  Oops
                </p>
                <h4 v-else style="color: black">Error</h4>
                <div
                  style="color: rgb(121, 121, 121)"
                  v-html="message"
                  class="mb-2"
                ></div>
                <v-btn
                  v-if="getTypeBoolean('notification')"
                  class="btn-primary"
                  @click="closeModal"
                  >Ok</v-btn
                >
                <v-btn
                  v-if="getTypeBoolean('mfa')"
                  class="btn-primary mt-6"
                  @click="closeModal"
                  >Close</v-btn
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
export default {
  props: {
    background: Boolean,
    message: String,
    show: Boolean,
    task: String,
    type: String,
  },
  data: function () {
    return {
      modalWidth:
        window.innerWidth < 960
          ? window.innerWidth < 820
            ? "75%"
            : "50%"
          : "580px",
    };
  },
  methods: {
    closeModal() {
      this.$emit("close-modal");
    },
    getTypeBoolean(type) {
      return this.type == type;
    },
  },
};
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 19999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 580px;
  border-radius: 20px;
  margin: 0px auto;
  padding: 20px 30px;
  transition: all 0.3s ease;
  background: #ffffff;
  box-shadow: 0px -4px 4px rgb(0 0 0 / 25%), 0px 4px 4px rgb(0 0 0 / 25%);
  backdrop-filter: blur(6px);
}
.icon-popup {
  background: white;
  border-radius: 100px;
  border: 3px solid white;
  box-shadow: 0px 1px 6px 1px darkgray;
}
.btn-primary {
  color: white !important;
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  border-radius: 10px;
}
</style>
