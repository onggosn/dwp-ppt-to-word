declare module "axios" {
  interface AxiosRequestConfig {
    cancelPreviousRequests?: boolean;
  }
}

import axios, { AxiosInstance } from "axios";
import store from "@/store";
// import { randomRequestId } from "@/library/util";
import { encrypt, decrypt } from "@/library/CryptoHelper";
import { useToast } from "vue-toastification";
import router from "@/router";
import { useMsal } from "@v2/composables/useMsal";
import { addApiVersion, redirectToBisa } from "@v2/helpers/utils";

const toast = useToast();
const pendingRequests: { [key: string]: AbortController } = {};
const removePendingRequest = (url: string | undefined, abort = false): void => {
  // check if pendingRequests contains our request URL
  if (url && pendingRequests[url]) {
    // if we want to abort ongoing call, abort it
    if (abort) {
      pendingRequests[url].abort();
    }
    // remove the request URL from pending requests
    delete pendingRequests[url];
  }
};

const client = ({
  encryptRequest = true,
  decryptResponse = true,
  baseURL = store.state.urlApim,
  isRetry = false,
}): AxiosInstance => {
  // manage http dan https
  const current_mode = process.env.VUE_APP_CURRENT_MODE;
  // const requestId = randomRequestId();

  const instance = axios.create({
    baseURL: baseURL,
    withCredentials: true,
    headers: {
      Authorization: `Bearer ${store.state.accessToken}`,
      ultimatewarrior: store.state.teriyaki,
      bubbareydudley: store.state.yakiniku,
      dr: store.state.kane,
      callafriend:
        "D9E13A0B160B4B7DA6205B3BAEGE9A4A09E21C27E95D753C278F3A62B64EE07F",
      "Referrer-Policy": "no-referrer",
      "Content-Security-Policy": "default-src 'self'; script-src 'self'",
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });

  // handle response data
  instance.interceptors.response.use(
    async function (response) {
      if (!response || !response.data || !decryptResponse) {
        return Promise.resolve(response);
      }
      const plainData = await decrypt(response.data, store);
      return Promise.resolve(plainData);
    },
    async function (error) {
      if (error.response) {
        const status = error.response?.status ?? 400;
        if ([406].includes(status)) {
          store.dispatch("logout").then(() => {
            redirectToBisa();
          });
        } else if ([401].includes(status) && current_mode == "private") {
          if (isRetry) {
            redirectToBisa(true);

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
        } else if ([403].includes(status)) {
          toast.warning("Anda tidak memiliki akses");
          router.push({ name: "v2.home" });
        } else if (error.response.data.response == "FAIL") {
          error.response.data = JSON.parse(error.response.data.message);
        }
      }
      return Promise.reject(error);
    }
  );
  instance.interceptors.request.use(
    async function (config: any) {
      if (config.cancelPreviousRequests && config.url && !config.signal) {
        removePendingRequest(config.url, true);
        const abortController = new AbortController();
        config.signal = abortController.signal;
        pendingRequests[config.url] = abortController;
      }
      config.headers["dr"] = await addApiVersion(store.state.kane, "v2");

      const isMfa = process.env.VUE_APP_MFA_STATUS === "true";
      const apimBisa = store.getters["userStore/getApimBisa"];
      let tokenAzure: string | null = null;
      if (isMfa) {
        const { getToken } = useMsal();
        tokenAzure = await getToken();
      }

      const isGetTokenApim = config.url?.includes("GetTokenApim");
      const isRedirectApp = config.url?.includes("RedirectApplication");

      if (isRedirectApp) {
        config.headers["Authorization"] = `bearer ${apimBisa}`;
        if (isMfa) {
          config.headers["authorization-app"] = tokenAzure;
        }
      } else if (isGetTokenApim) {
        if (isMfa) {
          config.headers["Authorization"] = `bearer ${tokenAzure}`;
        } else {
          // Hapus default header jika bukan MFA di endpoint GetTokenApim
          delete config.headers?.["Authorization"];
        }
      } else if (isMfa) {
        // Default MFA untuk request lainnya
        config.headers["authorization-app"] = tokenAzure;
      }

      if (encryptRequest) {
        const data = config.data;
        const finalPayload = encryptRequest ? await encrypt(data, store) : data;
        config.data = finalPayload;
      }
      return config;
    },
    function (error) {
      return Promise.reject(error);
    }
  );

  return instance;
};

export default client;
