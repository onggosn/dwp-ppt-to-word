// src/composables/useSSO.ts
import { ref } from "vue";
import { useStore } from "vuex";
import Cookies from "js-cookie";
import browser from "browser-detect";
import { encrypt } from "@/library/CryptoHelper";
import { handleInitialDatadog } from "@/library/DatadogHelper";
import { initializeFirebaseApp } from "@/library/FirebaseHelper";
import { useFirebaseMessaging } from "./useFirebaseMessaging";
import { useMsal } from "./useMsal";

export function useSSO() {
  const store = useStore();
  const { requestNotificationPermission, registerServiceWorkerWithConfig } =
    useFirebaseMessaging();
  const { handleRedirect } = useMsal();

  const isLoading = ref(false);
  const apiError = ref("");
  const errorType = ref<string | undefined>(undefined);

  const env = process.env.VUE_APP_ENV;
  const isMfa = process.env.VUE_APP_MFA_STATUS === "true";

  interface SSOValidation {
    apimInfo?: any;
    shKey?: any;
    isValid: boolean;
  }

  const validateSSOCookies = async (apimData?: any): Promise<SSOValidation> => {
    try {
      let apimInfo: any | undefined;
      let shaKey: any | undefined;

      if (isMfa && apimData) {
        // Direct access jika sudah berupa object
        apimInfo = apimData.apim;
        shaKey = apimData.shaKey;
      } else {
        // Ambil dari Cookies dan parse hanya jika data ada
        const rawApim = Cookies.get(`ApimInfo.${env}`);
        const rawSha = Cookies.get(`SHAKey256.${env}`);

        if (rawApim) apimInfo = JSON.parse(rawApim);
        if (rawSha) shaKey = JSON.parse(rawSha);
      }

      // Validasi akhir: pastikan kedua key utama tersedia
      if (!apimInfo || !shaKey) {
        const apimBisa = await store.dispatch("userStore/getTokenApimBisa");
        if (!apimBisa?.access_token) return { isValid: false };

        store.commit("userStore/setApimBisa", apimBisa.access_token);

        const apimDDM = await store.dispatch("userStore/getTokenApimDDM");
        const tokenDDM = apimDDM?.data?.responseData?.apim;
        const shaKeyDDM = apimDDM?.data?.responseData?.shaKey;

        if (!tokenDDM || !shaKeyDDM) return { isValid: false };

        apimInfo = tokenDDM;
        shaKey = shaKeyDDM;

        store.dispatch("updateAccessToken", tokenDDM);
      }

      return {
        apimInfo: apimInfo,
        shKey: shaKey,
        isValid: true,
      };
    } catch (e) {
      console.error("SSO Validation Error:", e);
      return { isValid: false };
    }
  };

  /**
   * Inti dari SSO Auth:
   * Hanya mengelola permission, encryption, dan commit ke store.
   * Mengembalikan boolean atau profile agar pemanggil (Guard/Component)
   * bisa menentukan arah routing selanjutnya.
   */
  const executeSSO = async () => {
    isLoading.value = true;
    try {
      let apimDDM: any = null;

      // 1. MFA Check & Initial Token Fetch
      if (isMfa) {
        await handleRedirect();

        // Ambil token sekaligus (Parallel agar lebih cepat)
        const apimBisa = await store.dispatch("userStore/getTokenApimBisa");
        if (apimBisa) {
          store.commit("userStore/setApimBisa", apimBisa.access_token);
        }

        // 3. Validation
        apimDDM = await store.dispatch("userStore/getTokenApimDDM");
        await store.dispatch("userStore/getProfileBisa");
      }

      const { apimInfo, shKey, isValid } = await validateSSOCookies(
        apimDDM?.data?.responseData
      );

      if (!isValid || !apimInfo) {
        throw new Error("INVALID_COOKIES");
      }

      // 4. Update Store Keys
      await Promise.all([
        store.dispatch("updateAccessToken", apimInfo),
        store.dispatch("updateKeys", shKey),
      ]);

      // 5. Encryption & Profile Initialization
      const commonPayload = {
        browserName: browser().name,
        deviceType: process.env.VUE_APP_DEVICE_TYPE,
      };

      const loginData = {
        ...commonPayload,
        username: "",
        version: process.env.VUE_APP_VERSION,
      };

      const { json: kane } = await encrypt(loginData, store);
      await store.dispatch("updateLoginResponse", { kane });
      // 0. Ambil config dinamis (firebase, dataDog, ckEditor) dari API lebih dulu,
      // lalu init Firebase App supaya bisa dipakai oleh langkah FCM di bawah
      await store.dispatch("userStore/initializeKey");
      const firebaseConfig =
        store.getters["userStore/getInitializeConfig"]?.firebase;
      initializeFirebaseApp(firebaseConfig);
      await registerServiceWorkerWithConfig();

      // 1. Firebase Permission (Non-blocking)
      const tokenFirebase = await requestNotificationPermission().catch(
        (err) => {
          console.warn("FCM blocked, continuing...", err);
          return null;
        }
      );

      // Panggil Datadog tanpa await (fire and forget)
      handleInitialDatadog().catch((err) => console.warn("Datadog fail:", err));

      const profile = await store.dispatch("userStore/initialize", {
        ...commonPayload,
        firebaseToken: tokenFirebase || "",
      });

      if (!profile) {
        throw new Error("INVALID_GET_PROFILE");
      }

      // 6. Finalize Store
      await store.dispatch("updateLoginResponse", {
        username: profile.mUserView.username,
        fullname: profile.mUserView.name,
        divisi: profile.mUserView.organizationName,
        kane,
      });

      return { success: true, profile };
    } catch (error: any) {
      console.error("SSO Process Error:", error);
      apiError.value =
        error.message === "INVALID_COOKIES"
          ? "Sesi login portal telah berakhir."
          : "Gagal memproses autentikasi SSO.";

      return {
        success: false,
        error: error.message,
        status: error?.response?.status,
      };
    } finally {
      isLoading.value = false;
    }
  };

  const refreshTokenCKE = () => {
    let refreshTimer: ReturnType<typeof setInterval> | null = null;

    const executeRefresh = async () => {
      try {
        // Menggunakan Promise.allSettled agar jika salah satu API gagal/error,
        // API yang satunya tidak ikut terhenti.
        await Promise.allSettled([
          store.dispatch("userStore/fetchCKEditorToken"),
          store.dispatch("userStore/fetchCKBoxToken"),
        ]);
      } catch (e) {
        void e;
      }
    };

    const start = (intervalMs: number = 50 * 60 * 1000) => {
      // Default refresh token per 50 menit sekali
      if (refreshTimer) stop();
      executeRefresh();

      // Set interval untuk eksekusi berkala setiap 10 menit (default)
      refreshTimer = setInterval(executeRefresh, intervalMs);
    };

    const stop = () => {
      if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
      }
    };

    return { start, stop };
  };

  return {
    isLoading,
    apiError,
    errorType,
    executeSSO,
    closeError: () => {
      apiError.value = "";
      errorType.value = undefined;
    },
    refreshTokenCKE,
  };
}
