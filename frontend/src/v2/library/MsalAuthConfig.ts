import {
  PublicClientApplication,
  type AccountInfo,
  type RedirectRequest,
} from "@azure/msal-browser";
import { reactive } from "vue";

export const msalConfig = {
  auth: {
    clientId: process.env.VUE_APP_MFA_CLIENT_ID || "",
    authority: process.env.VUE_APP_MFA_AUTH_URL || "",
    redirectUri: window.location.origin,
  },
  cache: {
    cacheLocation: "localStorage",
    storeAuthStateInCookie: true,
  },
};

export const graphScopes: RedirectRequest = {
  scopes: [
    "openid",
    "profile",
    "email",
    `api://${process.env.VUE_APP_MFA_CLIENT_ID}/access_as_user`,
  ],
};
export const state = reactive({
  isAuthenticated: false,
  user: null as AccountInfo | null,
});

export const msalInstance = new PublicClientApplication(msalConfig);
