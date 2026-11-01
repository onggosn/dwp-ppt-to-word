<template>
  <v-form
    class="inputFieldLogin"
    type="submit"
    @submit.prevent="doLogin"
    lazy-validation
  >
    <v-text-field
      autocomplete="off"
      variant="solo"
      label="Enter username"
      append-inner-icon="mdi-account"
      placeholder="Enter username"
      single-line
      v-model="form.username"
      @blur="v$.form.username.$touch"
      :error-messages="e(v$.form.username)"
      :disabled="isDisabledUsername"
      class="my-input"
      ref="usernameInput"
    ></v-text-field>
    <!-- <div
      class="mb-4 font-weight-bold text-whiteTheme"
      @click="reloadPage"
      v-if="isDisabledUsername"
    >
      Not {{ form.username }}? <span class="badge">Switch accounts.</span>
    </div> -->

    <transition name="password-field" mode="out-in">
      <v-text-field
        v-if="showPassword"
        autocomplete="off"
        variant="solo"
        label="Enter password"
        :type="showPass ? 'text' : 'password'"
        :append-inner-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="showPass = !showPass"
        @blur="v$.form.password.$touch"
        :error-messages="e(v$.form.password)"
        placeholder="Enter password"
        single-line
        v-model="form.password"
        class="custom-input"
        ref="passwordInput"
      ></v-text-field>
    </transition>
    <v-row>
      <v-col cols="12">
        <v-btn
          block
          type="submit"
          :loading="isLoading"
          :disabled="isLoading"
          color="White"
          class="px-2"
          style="
            height: 50px;
            font-size: 20px;
            font-weight: bold;
            color: #1069ad;
          "
        >
          Login
        </v-btn>
      </v-col>
      <!-- <v-btn block @click="logout">logout</v-btn> -->
    </v-row>
  </v-form>

  <modal-error-workspace-create
    :background="false"
    :message="apiError"
    :show="apiError.length > 0"
    @close-modal="closeModalErrorShow"
    :key="'modal-error'"
    :type="type ?? undefined"
  ></modal-error-workspace-create>

  <!-- <loading-spinner v-if="isLoading"></loading-spinner> -->

  <v-overlay :model-value="isLoading" class="align-center justify-center">
    <v-progress-circular
      color="#065695"
      indeterminate
      size="68"
      width="6"
    ></v-progress-circular>
  </v-overlay>

  <ModalConfirm ref="modalConfirm" :form-config="formPopup">
    <template v-slot:icon-img>
      <v-avatar
        size="80"
        style="margin-top: -38px; filter: drop-shadow(#9b9b9b 2px 2px 3px)"
      >
        <img src="/images/icon/iconWarning.png" style="width: 85px" />
      </v-avatar>
    </template>
    <template v-slot:btn-action>
      <div class="d-flex justify-content-between">
        <v-btn
          variant="outlined"
          class="rounded-lg btn-default"
          @click="continueWithPassword(false)"
          >Use Another Account</v-btn
        >
        <v-btn
          class="ml-2 primary-gradient rounded-lg"
          @click="continueWithPassword(true)"
          >Continue with Password</v-btn
        >
      </div>
    </template>
  </ModalConfirm>
</template>

<script setup lang="ts">
import Cookies from "js-cookie";
import { ref, reactive, onMounted, computed, nextTick } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { getMessaging, getToken } from "firebase/messaging";
// import { useMsal } from "@/v2/composables/useMsal";
// import { state } from "@/v2/library/MsalAuthConfig";

import client from "@/library/ApiClient";
import { encrypt } from "@/library/CryptoHelper";
import browser from "browser-detect";
import { getErrorMessages } from "@/library/ValidationHelper";
import { appFirebase } from "@/library/FirebaseHelper";

import ModalErrorWorkspaceCreate from "@/components/utils/ModalErrorWorkspaceCreate.vue";
// import LoadingSpinner from "@/components/loading/LoadingSpinner.vue";
import { handleInitialDatadog } from "@/library/DatadogHelper";
import ModalConfirm from "@v2/components/utils/modal/ModalConfirm.vue";
import { TModalConfirm } from "@v2/Type.d";

interface LoginForm {
  username: string;
  password: string | null;
  deviceType: string;
  firebaseToken: string;
  azureToken?: string;
}
// getAccessToken, isTokenValid
// const { login, handleRedirect } = useMsal();
const store = useStore();
const router = useRouter();
const route = useRoute();

const isLoading = ref(false);
const showPass = ref(false);
const apiError = ref("");
const type = ref<string | undefined>(undefined);
const isAllowNotification = ref(false);
const showPassword = ref<boolean>(false);
const requiredMFA = ref<string>("");
const isUsernameValid = ref<string>("");
const modalConfirm = ref();
const passwordInput = ref();
const usernameInput = ref();

// ✅ Add state for MSAL token checking
// const isCheckingMsalToken = ref(false);
// const hasValidMsalToken = ref(false);
// const msalTokenError = ref("");

// const initializeMsal = async () => {
//   try {
//     await msalInstance.initialize();
//   } catch (error) {
//     void error;
//   }
// };
const form = reactive<LoginForm>({
  username: "",
  password: null,
  deviceType: "web",
  firebaseToken: "not allowing permission",
  azureToken: "",
});

const isDisabledUsername = ref(false);

// const isDisabledUsername = computed(() => {
//   return (
//     requiredMFA.value !== process.env.VUE_APP_SUKHOI &&
//     requiredMFA.value != "" &&
//     isUsernameValid.value === process.env.VUE_APP_APOLLO
//   );
// });

const logout = () => {
  // msalInstance.logout();
  localStorage.clear();
  sessionStorage.clear();
  requiredMFA.value = "";
  showPassword.value = false;
  form.username = "";
};

// const checkExistingMsalToken = async () => {
//   console.log("Checking for existing MSAL token...");

//   isCheckingMsalToken.value = true;
//   try {
//     if (await isTokenValid()) {
//       hasValidMsalToken.value = true;
//     } else {
//       await getAccessToken();
//       hasValidMsalToken.value = true;
//     }
//   } catch (error) {
//     msalTokenError.value = "Failed to acquire MSAL token";
//   } finally {
//     isCheckingMsalToken.value = false;
//   }
// };

const formPopup = ref<TModalConfirm>({
  title: "MFA Not Active",
  btnSubmitLabel: "Yes",
  width: 450,
  btnSubmitColor: "primary-gradient",
  message:
    "<center>Your account has not enabled MFA<br>Enter your password to continue or<br>use another account</center>",
  messageClass: "text-left",
});

const isPublicMode = computed(
  () => process.env.VUE_APP_CURRENT_MODE === "public"
);

const rules = computed(() => ({
  form: {
    username: { required },
    password: showPassword.value ? { required } : {},
  },
}));

const v$ = useVuelidate(rules, { form });
const e = getErrorMessages;

const closeModalErrorShow = () => {
  apiError.value = "";
  type.value = undefined;

  if (!showPassword.value) form.username = "";
  form.password = null;
  form.deviceType = "web";
  form.firebaseToken = isAllowNotification.value
    ? form.firebaseToken
    : "not allowing permission";

  v$.value.$reset();
};

const reloadPage = () => {
  localStorage.clear();
  sessionStorage.clear();
  requiredMFA.value = "";
  showPassword.value = false;
  form.username = "";
};

const requestPermission = async () => {
  try {
    const permission = await Notification.requestPermission();
    const messaging = getMessaging(appFirebase);

    if (permission === "granted") {
      const token = await getToken(messaging, {
        vapidKey: process.env.VUE_APP_VAPID,
      });

      if (token) {
        form.firebaseToken = token;
        isAllowNotification.value = true;
      } else {
        isAllowNotification.value = false;
      }
    } else {
      type.value = "notification";
      apiError.value =
        "Don’t miss a things! Go to Setting to setup push <br>notification to know any update in <br>digital workplace platform ";
      isAllowNotification.value = false;
    }
  } catch (error) {
    isAllowNotification.value = false;
  }
};

const fetchEncryptionKeys = async (isPublic: boolean): Promise<boolean> => {
  isLoading.value = true;
  const clientCall = isPublic ? client.getKeySHA256 : client.getKeySHA256new;

  try {
    const response = await clientCall({ store }, form.username);
    const {
      undertaker,
      johnCena,
      randyOrton,
      reymysterio,
      teriyaki,
      yakiniku,
    } = response.data;

    requiredMFA.value = response.data?.sukhoi;
    isUsernameValid.value = response.data?.apollo;

    await store.dispatch("updateKeys", {
      undertaker,
      johnCena,
      randyOrton,
      reymysterio,
      teriyaki,
      yakiniku,
    });

    return true;
  } catch (error: any) {
    apiError.value =
      error.response?.data?.message ?? "Failed to get encryption keys";
    return false;
  } finally {
    isLoading.value = false;
  }
};

const doRequestLogin = async (isPublic: boolean) => {
  isLoading.value = true;
  // if (requiredMFA.value === process.env.VUE_APP_SUKHOI) {
  //   form.username = state.user?.username.split("@")[0] || form.username;
  //   form.azureToken = state.user?.idToken || "";
  // }

  const clientCall = isPublic ? client.login : client.loginnew;
  try {
    const response = await clientCall({ store, data: form });
    const loginResponseData = isPublic ? response.data : response.plainData;

    const accessToken = loginResponseData?.access_token;
    if (!isPublic && !accessToken) {
      apiError.value = "Login response missing access token";
      return;
    }
    if (!isPublic) {
      await store.dispatch("updateAccessToken", accessToken);
    }

    if (!loginResponseData.mUserView) {
      apiError.value = "Internal server error";
      return;
    }

    const loginData = {
      username: loginResponseData.mUserView.username,
      token: loginResponseData.token,
      browserName: browser().name,
      deviceType: process.env.VUE_APP_DEVICE_TYPE,
      version: process.env.VUE_APP_VERSION,
    };

    store.state.isNotifNew = true;
    localStorage.setItem("isLoggedIn", "true");

    const encryptedLoginData = await encrypt(loginData, store);

    await store.dispatch("updateLoginResponse", {
      username: loginResponseData.mUserView.username,
      token: loginResponseData.token,
      kane: encryptedLoginData.json,
      fullname: loginResponseData.mUserView.name,
      divisi: loginResponseData.mUserView.organizationName,
      sukhoi: requiredMFA.value,
    });

    const nextPath = route.query.next;
    if (nextPath && typeof nextPath === "string") {
      router.replace(nextPath);
    } else {
      router.push({ name: "home" });
    }

    store.dispatch("userStore/fetchCKEditorToken");
    store.dispatch("userStore/fetchCKBoxToken");
    store.dispatch("userStore/fetchDocumentToken");
    store.dispatch("userStore/startIdleTimer");
  } catch (error: any) {
    const message = error.response?.data?.message;
    if (message?.includes("maximum number of login attempts"))
      type.value = "mfa";
    apiError.value = message ?? "internal server error";
    localStorage.clear();
    sessionStorage.clear();
  } finally {
    handleInitialDatadog(store.state);
    isLoading.value = false;
  }
};

const loginFlow = async (isPublic: boolean) => {
  const isValid = await v$.value.$validate();
  if (!isValid) return;

  const keysFetched = await fetchEncryptionKeys(isPublic);
  if (!keysFetched) return;

  let shouldProceed = true;

  if (isUsernameValid.value !== process.env.VUE_APP_APOLLO) {
    apiError.value = "Internal server error";
    showPassword.value = false;
    return;
  }

  if (requiredMFA.value === process.env.VUE_APP_SUKHOI) {
    // await login("popup", form.username + "@bi.go.id");
    // if (!state.isAuthenticated) {
    //   apiError.value = "Login failed, please try again!";
    //   shouldProceed = false;
    //   requiredMFA.value = "";
    // }
  } else {
    // showPassword.value = true;
    if (!form.password) {
      shouldProceed = false;
      modalConfirm.value.show();
    }
  }

  if (shouldProceed) await doRequestLogin(isPublic);
};

const doLogin = () => {
  usernameInput.value.blur();
  if (isPublicMode.value) {
    loginFlow(true);
  } else {
    loginFlow(false);
  }
};

const checkSSO = async () => {
  console.log("cek sso");
  const token_apim = JSON.parse(Cookies.get("ApimInfo-dev")).TokenAPIM;
  const shKey = JSON.parse(Cookies.get("SHAKey256-dev"));

  const { undertaker, johnCena, randyOrton, reymysterio, teriyaki, yakiniku } =
    shKey;
  await store.dispatch("updateAccessToken", token_apim);
  await store.dispatch("updateKeys", {
    undertaker,
    johnCena,
    randyOrton,
    reymysterio,
    teriyaki,
    yakiniku,
  });

  const loginData = {
    username: "gilang_r.i",
    browserName: browser().name,
    deviceType: process.env.VUE_APP_DEVICE_TYPE,
    version: process.env.VUE_APP_VERSION,
  };
  localStorage.setItem("isLoggedIn", "false");
  console.log("loginData", loginData);

  const encryptedLoginData = await encrypt(loginData, store);
  console.log("encryptedLoginData", encryptedLoginData);

  await store.dispatch("updateLoginResponse", {
    username: loginData.username,
    kane: encryptedLoginData.json,
    fullname: "Gilang Ramadhan",
    divisi: "DPID",
  });

  client
    .cekSSO({ store })
    .then((response) => {
      console.log("cek sso response", response);
    })
    .catch((err) => {
      console.log("cek sso error", err);
      void 0; // Silent error handling
    });
};

onMounted(async () => {
  usernameInput.value.focus();
  await requestPermission();
  // await initializeMsal();
  // await handleRedirect();
  // await checkExistingMsalToken();
  checkSSO();
});

const continueWithPassword = async (notMfa: boolean) => {
  if (notMfa) {
    showPassword.value = true;
    isDisabledUsername.value = true;
  } else {
    isDisabledUsername.value = false;
    reloadPage();
  }
  modalConfirm.value.hide();
  await nextTick();
  if (notMfa) passwordInput.value.focus();
  else usernameInput.value.focus();
};
</script>
<style scoped>
.custom-input.v-messages__message::after {
  border-color: #d6212a !important;
  color: #d6212a !important;
}
.my-input.v-input .v-input__slot {
  border-radius: 100px;
}
.v-input--error:not(.v-input--disabled) .v-input__details > .v-icon,
.v-input--error:not(.v-input--disabled) .v-input__details .v-messages,
.v-input--error:not(.v-input--disabled) .v-input__prepend > .v-icon,
.v-input--error:not(.v-input--disabled) .v-input__prepend .v-messages,
.v-input--error:not(.v-input--disabled) .v-input__append > .v-icon,
.v-input--error:not(.v-input--disabled) .v-input__append .v-messages {
  color: #d6212a !important;
}
.buttonUpload-blue {
  background: linear-gradient(180deg, #065695, #267dc2);
  font-size: 16px;
  font-weight: 900;
  text-align: center;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: white !important;
}

/* Transisi untuk password field */
.password-field-enter-active,
.password-field-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.password-field-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
  max-height: 0;
}

.password-field-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
  max-height: 100px;
}

.password-field-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
  max-height: 100px;
}

.password-field-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
  max-height: 0;
}

.badge {
  background: lightseagreen;
  border-radius: 10px;
  padding-left: 5px;
  padding-right: 5px;
}

.btn-default {
  color: #065695;
  border-color: rgb(159, 159, 159);
  font-weight: 700;
}
</style>
