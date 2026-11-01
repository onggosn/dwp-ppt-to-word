<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showModal" class="modal-response" style="z-index: 20011">
        <div class="modal-wrapper">
          <div
            class="modal-container d-flex flex-column"
            :style="{
              height: '250px',
              width: modalWidth,
              position: 'relative',
            }"
          >
            <div style="position: relative" class="align-self-center">
              <img
                v-if="isError"
                src="/images/cancelNotif.png"
                style="margin-top: -45px"
              />
              <img
                v-else
                src="/images/checkNotif.png"
                style="margin-top: -45px"
              />
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
              <img
                class="pointer-click"
                style="height: 25px; position: relative; left: -11px"
                src="/images/closeIcon.png"
              />
            </span>
            <div class="mt-6">
              <div class="row text-center">
                <h2 style="font-weight: 700; color: #3a416f">
                  {{ isError ? "Error" : "Success" }}
                </h2>
                <div class="mt-1 text-16">
                  {{ message }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  name: "modalResponse",
  emits: ["close-modal"],
  data: function () {
    return {
      showModal: false,
      message: null,
      isError: false,
    };
  },
  methods: {
    openModal(msg, isError = false) {
      this.showModal = true;
      this.message = msg;
      this.isError = isError;
    },
    closeModal() {
      this.showModal = false;
      this.msg = null;
      this.isError = false;
      this.$emit("close-modal");
    },
  },
  computed: {
    modalWidth() {
      return window.innerWidth < 960
        ? window.innerWidth < 820
          ? "75%"
          : "50%"
        : "580px";
    },
  },
};
</script>

<style scoped>
.modal-response {
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
</style>
