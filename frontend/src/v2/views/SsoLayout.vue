<template>
  <SsoAuthLoading :show="isLoading" />
  <Modal
    :background="true"
    :message="apiError"
    :show="apiError.length > 0"
    @close-modal="closeModalErrorShow"
    :key="'modal-error'"
    :type="type ?? undefined"
  />
</template>

<script setup lang="ts">
import SsoAuthLoading from "@/v2/components/loading/SsoAuthLoading.vue";
import { onMounted, ref, computed } from "vue";
import Cookies from "js-cookie";
import { useStore } from "vuex";
import { useToast } from "vue-toastification";
import { useRouter, useRoute } from "vue-router";
import browser from "browser-detect";
import { encrypt } from "@/library/CryptoHelper";
import { getMessaging, getToken } from "firebase/messaging";
import { appFirebase } from "@/library/FirebaseHelper";
import Modal from "@/components/utils/ModalErrorWorkspaceCreate.vue";
import { handleInitialDatadog } from "@/library/DatadogHelper";
import { redirectToBisa } from "@/v2/helpers/utils";

const store = useStore();
const toast = useToast();
const router = useRouter();
const route = useRoute();

const apiError = ref("");
const type = ref<string | undefined>(undefined);
const tokenFirebase = ref("");
const isAllowNotification = ref(false);
const isLoading = ref(true);

//Environment config
const env = computed(() => process.env.VUE_APP_ENV);
const deviceType = computed(() => process.env.VUE_APP_DEVICE_TYPE);
const appVersion = computed(() => process.env.VUE_APP_VERSION);

const SSO_TIMEOUT = 3000;
const dr = ref();

// Cookie helpers
const getCookieData = (cookieName: string) => {
  try {
    const cookieValue = Cookies.get(cookieName);
    return cookieValue ? JSON.parse(cookieValue) : null;
  } catch (error) {
    console.error(`Error parsing cookie ${cookieName}:`, error);
    return null;
  }
};

const validateSSOCookies = () => {
  const apimData = getCookieData(`ApimInfo.${env.value}`);
  const shKeyData = getCookieData(`SHAKey256.${env.value}`);

  const token_apim = apimData?.TokenAPIM;
  const shKey = shKeyData;

  return { token_apim, shKey, isValid: !!(token_apim && shKey) };
};

// Error handling
const handleSSOError = (message: string, redirectToLogin = true) => {
  toast.warning(message);
  console.error("SSO Error:", message);

  if (redirectToLogin) {
    setTimeout(() => {
      redirectToBisa();
    }, SSO_TIMEOUT);
  }
};

const handleCriticalError = (error: any, context: string) => {
  console.error(`Critical error in ${context}:`, error);
  isLoading.value = false;
  apiError.value = `Terjadi kesalahan saat ${context}. Silakan refresh halaman.`;
  setTimeout(() => {
    store.dispatch("logout").then(() => {
      redirectToBisa();
    });
  }, SSO_TIMEOUT);
};

// fetch encryption keys
const fetchEncryptionKeys = async () => {
  try {
    const { token_apim, shKey, isValid } = validateSSOCookies();

    if (!isValid) {
      handleSSOError("Sesi Anda telah berakhir, silahkan login kembali!", true);
      return false;
    }

    const {
      undertaker,
      johnCena,
      randyOrton,
      reymysterio,
      teriyaki,
      yakiniku,
    } = shKey;

    await Promise.all([
      store.dispatch("updateAccessToken", token_apim),
      store.dispatch("updateKeys", {
        undertaker,
        johnCena,
        randyOrton,
        reymysterio,
        teriyaki,
        yakiniku,
      }),
    ]);

    return true;
  } catch (error) {
    handleCriticalError(error, "mengambil kunci enkripsi");
    return false;
  }
};

// Optimized set headers
const setHeaders = async () => {
  try {
    // Set token di header untuk setiap request API
    const loginData = {
      username: "",
      browserName: browser().name,
      deviceType: deviceType.value,
      version: appVersion.value,
    };

    const encryptedLoginData = await encrypt(loginData, store);
    dr.value = encryptedLoginData.json;
    await store.dispatch("updateLoginResponse", {
      kane: dr.value,
    });

    return true;
  } catch (error) {
    handleCriticalError(error, "mengatur header");
    return false;
  }
};

// Optimized notification permission
const requestPermission = async () => {
  try {
    const permission = await Notification.requestPermission();

    if (permission !== "granted") {
      type.value = "notification";
      apiError.value =
        "Don't miss a things! Go to Setting to setup push <br>notification to know any update in <br>digital workplace platform";
      isAllowNotification.value = false;
      return;
    }

    const messaging = getMessaging(appFirebase);
    const token = await getToken(messaging, {
      vapidKey: process.env.VUE_APP_VAPID,
    });

    if (token) {
      tokenFirebase.value = token;
      isAllowNotification.value = true;
    } else {
      isAllowNotification.value = false;
    }
  } catch (error) {
    console.warn("Notification permission error:", error);
    isAllowNotification.value = false;
  }
};

// Optimized user profile fetch
const fetchUserProfile = async () => {
  try {
    const profile = await store.dispatch("userStore/getUserProfile", {
      browserName: browser().name,
      deviceType: deviceType.value,
      firebaseToken: tokenFirebase.value,
    });

    await store.dispatch("updateLoginResponse", {
      username: profile.mUserView.username,
      fullname: profile.mUserView.name,
      divisi: profile.mUserView.organizationName,
      kane: dr.value,
    });

    return profile;
  } catch (error) {
    console.error("Error fetching user profile:", error);
    throw error;
  }
};

const ssoAuth = async () => {
  try {
    isLoading.value = true;

    // 1. Get value cookie SSO for Encryption Keys
    const keysSuccess = await fetchEncryptionKeys();
    if (!keysSuccess) return;

    const headersSuccess = await setHeaders();
    if (!headersSuccess) return;

    // 2. Init DataDog
    await handleInitialDatadog().catch((err) => {
      console.warn("DataDog initialization failed:", err);
    });

    // Redirect to main application after successful auth
    setTimeout(() => {
      const path = route.query.next;
      if (path) {
        router.push(path as string);
      } else {
        router.push({ name: "v2.home" });
      }
    }, 1500);
  } catch (error) {
    handleCriticalError(error, "autentikasi SSO");
  } finally {
    // Keep loading for a bit to show completion
    setTimeout(() => {
      isLoading.value = false;
    }, 1000);
  }
};

// Modal handlers
const closeModalErrorShow = () => {
  apiError.value = "";
  type.value = undefined;
};

onMounted(async () => {
  try {
    // Run permission request in parallel with SSO auth
    await Promise.all([requestPermission(), ssoAuth()]);
  } catch (error) {
    console.error("Initialization error:", error);
    isLoading.value = false;
  }
});
</script>

<style scoped></style>
