/**
 * POC mode (npm run serve-poc): runs the real DWP shell without SSO or the DWP middleware.
 *
 * - The user is seeded into the store, so SSO is skipped (see App.vue).
 * - Every axios request to the DWP middleware gets a canned "success" answer from mockAdapter.
 *   Request/response encryption is off in this mode (see CryptoHelper.js).
 * - The PPT to Word page talks to the real conversion backend (backend/app.py) through
 *   the dev-server proxy /poc-api, with its own axios instance, so it is not mocked.
 */
import axios, { AxiosResponse, InternalAxiosRequestConfig } from "axios";

export const isPocMock = process.env.VUE_APP_POC_MOCK === "true";

export const POC_USER = {
  username: "deflin.anggita",
  fullname: "Deflin Anggita",
  divisi: "DKEM",
};

const MENU = [
  { label: "Home", route: "home", iconName: "home", tooltip: "Home" },
  {
    label: "PPT to Word",
    route: "ppt-to-word",
    iconName: "workspacemanagement",
    tooltip: "PPT to Word Convert (POC)",
  },
];

function answer(url: string): any {
  const base = {
    responseCode: "011000",
    responseMessage: "OK (POC mock)",
    ResponseCode: "011000",
    ResponseData: { value: "" },
    responseData: {} as any,
  };
  if (url.includes("/RoleMenu/")) {
    base.responseData = { roleMenuList: MENU };
  } else if (url.includes("/Notification/")) {
    return { ...base, notifications: [], responseData: [] };
  } else if (url.includes("checkRoleMrdg") || url.includes("CheckRoleMrdg")) {
    base.responseData = { isCreate: false };
  }
  return base;
}

async function mockAdapter(
  config: InternalAxiosRequestConfig
): Promise<AxiosResponse> {
  const url = `${config.baseURL || ""}${config.url || ""}`;
  // eslint-disable-next-line no-console
  console.debug("[POC mock]", config.method?.toUpperCase(), url);
  return {
    data: answer(url),
    status: 200,
    statusText: "OK",
    headers: {},
    config,
  };
}

export function installPocMock(store: any) {
  if (!isPocMock) return;
  axios.defaults.adapter = mockAdapter;
  store.commit("updateLoginResponse", {
    token: "poc",
    username: POC_USER.username,
    fullname: POC_USER.fullname,
    kane: "poc",
    divisi: POC_USER.divisi,
    sukhoi: "poc",
  });
  store.state.accessToken = "poc";
  store.state.urlApim = "/mock-dwp-api";
}
