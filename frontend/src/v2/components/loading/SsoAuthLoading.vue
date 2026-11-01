<template>
  <div class="auth-loading-container d-flex align-center justify-center">
    <div class="bubble bubble-tl"></div>
    <div class="bubble bubble-br"></div>

    <div class="d-flex flex-column align-center position-relative z-10">
      <div class="position-relative d-flex align-center justify-center mb-10">
        <v-progress-circular
          indeterminate
          color="blue-darken-2"
          size="90"
          width="4"
          class="slow-spinner"
        >
          <v-icon
            icon="mdi-shield-lock"
            color="blue-lighten-3"
            size="36"
            class="icon-pulse"
          ></v-icon>
        </v-progress-circular>
      </div>

      <div class="text-center mb-8">
        <h2
          class="text-h6 font-weight-bold text-white mb-2 tracking-widest text-uppercase"
        >
          Memverifikasi Sesi
        </h2>
        <p class="text-body-2 text-grey-darken-1">
          Menghubungkan ke Single Sign-On...
        </p>
      </div>

      <div style="width: 220px">
        <v-progress-linear
          indeterminate
          color="blue-darken-3"
          rounded
          height="2"
          class="opacity-40 slow-bar"
        ></v-progress-linear>
      </div>
    </div>
  </div>
</template>

<style scoped>
:deep(.slow-spinner svg) {
  animation-duration: 2.5s !important;
}

:deep(.slow-spinner .v-progress-circular__overlay) {
  animation-duration: 2s !important;
  transition-timing-function: ease-in-out;
}

:deep(
    .slow-bar
      .v-progress-linear__indeterminate--active
      .v-progress-linear__indeterminate
  ) {
  animation-duration: 3s !important;
}

.auth-loading-container {
  position: fixed;
  inset: 0;
  background-color: #070f23;
  z-index: 9999;
  overflow: hidden;
}

.icon-pulse {
  animation: soft-pulse 3s infinite ease-in-out;
}

@keyframes soft-pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.92);
  }
}

.bubble {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  animation: float 18s infinite ease-in-out;
}

.bubble-tl {
  top: -10%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(
    circle,
    rgba(21, 101, 192, 0.25) 0%,
    transparent 70%
  );
}

.bubble-br {
  bottom: -10%;
  right: -10%;
  width: 450px;
  height: 450px;
  background: radial-gradient(
    circle,
    rgba(21, 101, 192, 0.2) 0%,
    transparent 70%
  );
  animation-delay: -9s;
}

.z-10 {
  z-index: 10;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(40px, 30px);
  }
}

.tracking-widest {
  letter-spacing: 0.3em !important;
}

.text-uppercase {
  text-transform: uppercase;
}
</style>
