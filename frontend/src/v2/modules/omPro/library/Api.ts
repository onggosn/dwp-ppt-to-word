declare module "axios" {
  interface AxiosRequestConfig {
    cancelPreviousRequests?: boolean;
  }
}

import axios, { AxiosInstance } from "axios";
import store from "@/store";
import { encrypt, decrypt } from "@/library/CryptoHelper";
import { useToast } from "vue-toastification";
import router from "@/router";
import { redirectToBisa } from "@/v2/helpers/utils";
import { useMsal } from "@v2/composables/useMsal";
import { addApiVersion } from "@v2/helpers/utils";

const toast = useToast();
const pendingRequests: Record<string, AbortController> = {};

function removePendingRequest(url?: string, abort = false): void {
  const controller = url && pendingRequests[url];
  if (controller) {
    if (abort) controller.abort();
    delete pendingRequests[url];
  }
}

function handleResponse(response: any, decryptResponse: boolean) {
  if (!response || !response.data || !decryptResponse) {
    return Promise.resolve(response);
  }
  const decryptedData = decrypt(response.data, store);
  return Promise.resolve(decryptedData);
}

async function handleError(error: any, currentMode: string, isRetry: boolean) {
  const { response } = error;
  const status = response?.status ?? 400;

  if (status === 406) {
    return logoutAndRedirect();
  }

  if (status === 401 && currentMode === "private") {
    if (isRetry) {
      redirectToBisa();
      return Promise.reject(error);
    }
    try {
      const apimBisa = await store.dispatch("userStore/getTokenApimBisa");

      if (!apimBisa?.access_token) {
        throw new Error("Token APIM Bisa tidak ditemukan");
      }

      store.commit("userStore/setApimBisa", apimBisa.access_token);

      const apimDDM = await store.dispatch("userStore/getTokenApimDDM");
      const tokenDDM = apimDDM?.data?.responseData?.apim;

      if (!tokenDDM) {
        throw new Error("Token APIM DDM tidak ditemukan");
      }

      store.dispatch("updateAccessToken", tokenDDM);
    } catch (error) {
      redirectToBisa();
    }
  }

  if (status === 403) {
    toast.warning("Anda tidak memiliki akses");
    router.push({ name: "v2.home" });
  }

  if (response?.data?.response === "FAIL") {
    response.data = JSON.parse(response.data.message);
  }

  return Promise.reject(error);
}

function logoutAndRedirect() {
  return store.dispatch("logout").then(() => {
    redirectToBisa();
  });
}

const client = ({
  encryptRequest = true,
  decryptResponse = true,
  isRetry = false,
} = {}): AxiosInstance => {
  const baseURL = store.state.urlApim;
  const currentMode = process.env.VUE_APP_CURRENT_MODE ?? "public";

  const { accessToken, pkc, undertaker, kane, teriyaki, yakiniku } =
    store.state;

  const instance = axios.create({
    baseURL,
    withCredentials: true,
    headers: {
      Authorization: `Bearer ${accessToken}`,
      ultimatewarrior: teriyaki,
      bubbareydudley: yakiniku,
      dr: kane,
      callafriend:
        "D9E13A0B160B4B7DA6205B3BAEGE9A4A09E21C27E95D753C278F3A62B64EE07F",
      "Referrer-Policy": "no-referrer",
      "Content-Security-Policy": "default-src 'self'; script-src 'self'",
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

  instance.interceptors.request.use(
    async (config: any) => {
      const isMfa = process.env.VUE_APP_MFA_STATUS === "true";
      const { url, cancelPreviousRequests } = config;

      if (cancelPreviousRequests && url && !config.signal) {
        removePendingRequest(url, true);
        const controller = new AbortController();
        config.signal = controller.signal;
        pendingRequests[url] = controller;
      }

      if (isMfa) {
        const { getToken } = useMsal();
        const tokenAzure = await getToken();
        config.headers["authorization-app"] = `${tokenAzure}`;
      }
      config.headers["dr"] = await addApiVersion(kane, "v2");
      if (encryptRequest && config.data) {
        config.data = await encrypt(config.data, store);
      }

      return config;
    },
    (error) => Promise.reject(error)
  );

  instance.interceptors.response.use(
    (res) => handleResponse(res, decryptResponse),
    (err) => handleError(err, currentMode, isRetry)
  );

  return instance;
};

export default client;
