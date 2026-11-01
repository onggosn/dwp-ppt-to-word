<template>
  <v-app>
    <SsoAuthLoading v-if="isLoading"></SsoAuthLoading>
    <template v-else>
      <v-main>
        <vue3-progress />
        <router-view></router-view>
      </v-main>
      <Toast ref="toast" />
      <ModalAlert ref="modalAlertRef" @confirm="logout" />
      <notification-alert ref="notificationAlertRef"></notification-alert>
    </template>
  </v-app>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  watchEffect,
  getCurrentInstance,
  onUnmounted,
} from "vue";
import { useStore } from "vuex";
import { useToast } from "vue-toastification";

// Components
import Toast from "./components/utils/ToastComponent.vue";
import ModalAlert from "./components/utils/ModalAlertComponent.vue";
import NotificationAlert from "./components/utils/NotificationComponent.vue";
import SsoAuthLoading from "./v2/components/loading/SsoAuthLoading.vue";

// Helpers & Composables
import client from "./library/ApiClient";
import { handleInitialDatadog } from "@/library/DatadogHelper";
import { useFirebaseMessaging } from "@/v2/composables/useFirebaseMessaging";
import { useSSO } from "@/v2/composables/useSSO";
import { redirectToBisa } from "@/v2/helpers/utils";
import { isPocMock } from "@/v2/poc/pocMock";

// Refs for DOM/Components
const toast = ref<InstanceType<typeof Toast> | null>(null);
const modalAlertRef = ref<InstanceType<typeof ModalAlert> | null>(null);
const notificationAlertRef = ref<InstanceType<typeof NotificationAlert> | null>(
  null
);

// Hooks & Store
const store = useStore();
const toastAlert = useToast();
const { proxy } = getCurrentInstance() as any;

// Initialize Composable
const { initListener } = useFirebaseMessaging();
const { isLoading, executeSSO, refreshTokenCKE } = useSSO();
const { start: startCkeditorRefresh, stop: stopCkeditorRefresh } =
  refreshTokenCKE();

// --- Watchers ---
watchEffect(() => {
  if (store.getters.isLoggedIn && store.state.userStore.isIdle) {
    localStorage.setItem("isLoggedIn", "false");
    const currentPath = window.location.pathname.replace(/^\/+/, "");
    store.dispatch("logout").then(() => {
      toastAlert.warning(
        "Oops, your session has been expired. Please log in again!",
        { timeout: 2000 }
      );
      setTimeout(() => {
        redirectToBisa(true, currentPath);
      }, 2000);
    });
    handleInitialDatadog(store.state);
  }
});

// --- Logic Functions ---
const getTokenFromAPIM = () => {
  client
    .getAccessToken({})
    .then((response: any) => {
      const accessToken = response.data.access_token;
      store.dispatch("updateAccessToken", accessToken);
    })
    .finally(() => {
      proxy.$progress.finish();
    });
};

const logout = () => {
  localStorage.setItem("isLoggedIn", "false");
  store.dispatch("logout").then(() => {
    window.location.reload();
    modalAlertRef.value?.hide();
  });
};

// --- Lifecycle Hooks ---

onMounted(async () => {
  if (isPocMock) {
    // POC mode: user is seeded in main.ts, no SSO / Firebase / CKEditor tokens
    proxy.$root.toast = toast.value;
    proxy.$root.m_alert = modalAlertRef.value;
    proxy.$root.alert = notificationAlertRef.value;
    proxy.$root.toastAlert = toastAlert;
    return;
  }
  const result = await executeSSO();
  if (!result.success) {
    // Jika gagal (misal cookie habis), arahkan ke login portal
    if (result.error) {
      toast.value?.show({
        message: result?.error,
        color: "error",
        timeout: 5000,
      });
    }
    const currentPath = window.location.pathname.replace(/^\/+/, "");
    setTimeout(() => {
      if (result.status === 401) {
        redirectToBisa(true, currentPath);
      } else {
        redirectToBisa();
      }
    }, 2000);
    return;
  }
  // Mapping to root for legacy support
  proxy.$root.toast = toast.value;
  proxy.$root.m_alert = modalAlertRef.value;
  proxy.$root.alert = notificationAlertRef.value;
  proxy.$root.toastAlert = toastAlert;

  store.dispatch("userStore/startIdleTimer");

  // Firebase app baru siap setelah initializeKey di executeSSO, jadi listener foreground dipasang di sini
  initListener();

  if (process.env.VUE_APP_CURRENT_MODE === "public") {
    proxy.$progress.start();
    getTokenFromAPIM();
  }

  startCkeditorRefresh();
  window.addEventListener("beforeunload", stopCkeditorRefresh);
  handleInitialDatadog(store.state);
});

onUnmounted(() => {
  stopCkeditorRefresh();
  window.removeEventListener("beforeunload", stopCkeditorRefresh);
});
</script>

<style>
@import "./assets/styles/index.css";
@import "@/assets/styles/main.css";
@import "@/assets/styles/scrollbar.css";
@import "@/v2/components/side-project/ckeditor/build/ckeditor.css";

.Vue-Toastification__toast--default.my-custom-toast-class {
  background-color: #fff8f8e3;
  width: 70%;
  margin-left: -10px;
  cursor: pointer;
}
.Vue-Toastification__close-button.my-button-class {
  color: #283487 !important;
  margin-top: -10px;
  position: absolute;
  right: 20px;
}
.Vue-Toastification__progress-bar {
  background-color: rgb(119 113 113 / 70%) !important;
}

.bg-gradient-darkred {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%) !important;
}

.bg-gradient-darkblue {
  background: linear-gradient(
    92.09deg,
    #065695 -46.47%,
    #267dc2 157.9%
  ) !important;
}

.text-newBlack {
  color: #4b4b4b !important;
}

.text-darkBlue {
  color: #3a416f !important;
}

.border-radius-dwp {
  border-radius: 12px !important;
}

.text-cammelCase {
  text-transform: capitalize !important;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(180deg, #065695 0%, #267dc2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.text-gradient-red {
  background: -webkit-linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.text-gradient-grey {
  background: linear-gradient(
    92.72deg,
    rgba(121, 121, 121, 0.9) 0%,
    rgba(187, 187, 187, 0.9) 152.21%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-orange {
  color: #ff9900 !important;
}

.text-36 {
  font-size: 36px !important;
}

.text-28 {
  font-size: 28px !important;
}

.text-24 {
  font-size: 24px !important;
}

.text-20 {
  font-size: 20px !important;
}

.text-12 {
  font-size: 12px !important;
}
</style>
