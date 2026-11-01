import clientv2 from "@/v2/library/ApiClient";
import client from "@v2/library/Api";
import { encrypt, decrypt } from "@/library/CryptoHelper";
import { encryptStorage } from "@/library/storage";

async function fetchData(commit, apiCall, requestData, keyToStore) {
  commit("setLoading", true);
  try {
    const res = await apiCall(requestData);
    const toIgnore = [
      "userSearchResult",
      "createEventRole",
      // "ckeditorToken",
      // "ckBoxToken",
    ];
    if (toIgnore.includes(keyToStore)) {
      commit("setLoading", false);
      return res;
    }
    const dataToUpdate = {};
    dataToUpdate[keyToStore] = res.responseData;
    switch (res.responseCode) {
      case "011000": //code for success
        commit("setData", dataToUpdate);
        commit("setLoading", false);
        if (res.responseData) {
          return res.responseData;
        } else {
          return true;
        }
      default: // code for empty data
        commit("setData", {});
        commit("setLoading", false);
        return {};
    }
  } catch (err) {
    commit("setError", err);
    commit("setLoading", false);
    return {};
  }
}

export default {
  namespaced: true,
  state: {
    count: 0,
    data: new Map(),
    loading: false,
    loadingProgress: 0,
    error: null,
    loadingTokenCke: false,
    tokenCKEditor: {} as any,
    tokenCKBox: "" as string,
    tokenDocument: "" as string,
    dataNotification: [] as any,
    isIdle: false,
    activeAccount: {} as any,
    apimBisa: "" as string,
    initializeConfig: {} as any,
  },
  getters: {
    getData: (state: any) => {
      return state.data;
    },
    getLoading: (state: any) => {
      return state.loading;
    },
    getLoadingTokenCke: (state: any) => {
      return state.loadingTokenCke;
    },
    getTokenCKEditor: (
      state: any,
      getters: any,
      rootState: any,
      rootGetters: any
    ) => {
      const data = state.tokenCKEditor;
      if (localStorage.getItem("coteka")) {
        try {
          const key = {
            getters: {
              encryptionKey: rootGetters.encryptionKey,
              iv: rootGetters.iv,
            },
          };
          return decrypt(localStorage.getItem("coteka"), key);
        } catch (error) {
          console.error("Error in getTokenCKEditor getter:", error);
          return data;
        }
      }
      return data;
    },
    getTokenCKBox: (state: any) => {
      return state.tokenCKBox;
    },
    getTokenDocument(state: any) {
      return state.tokenDocument;
    },
    getListNotification: (state: any) => {
      return state.dataNotification;
    },
    getActiveAccount: (state: any) => {
      return state.activeAccount;
    },
    getApimBisa: (state: any) => {
      return state.apimBisa;
    },
    getInitializeConfig: (state: any) => {
      if (Object.keys(state.initializeConfig || {}).length) {
        return state.initializeConfig;
      }

      const savedEncrypted = localStorage.getItem("dic");
      if (!savedEncrypted) return {};

      try {
        const decrypted = encryptStorage.decryptString(savedEncrypted);
        return JSON.parse(decrypted);
      } catch (error) {
        console.error("Error parsing initialize config:", error);
        return {};
      }
    },
  },
  mutations: {
    setIdle(state, value) {
      state.isIdle = value;
    },
    setData(state: any, newData: any) {
      state.data = newData;
    },
    setLoading(state: any, isLoading: boolean) {
      state.loading = isLoading;
    },
    setLoadingTokenCke(state: any, newData: boolean) {
      state.loadingTokenCke = newData;
    },
    setError(state: any, error: any) {
      state.error = error;
    },
    setActiveAccount(state: any, payload: any) {
      state.activeAccount = payload;
    },
    setApimBisa(state: any, newData: any) {
      state.apimBisa = newData;
    },
    setInitializeConfig(state: any, payload: any) {
      state.initializeConfig = payload || {};
      encryptStorage.setItem("dic", JSON.stringify(state.initializeConfig));
      const encrypted = encryptStorage.getItem("dic", true);
      localStorage.setItem("dic", encrypted);
    },
    async setTokenCKEditor(state: any, payload: any) {
      const encResult = await encrypt(payload.data, payload.encryptCode);
      const encData = encResult.json;
      localStorage.setItem("coteka", encData);
      state.tokenCKEditor = payload.data;
    },
    async setTokenCKBox(state: any, payload: any) {
      const encResult = await encrypt(payload.data, payload.encryptCode);
      const encData = encResult.json;
      localStorage.setItem("coteki", encData);
      state.tokenCKBox = payload.data;
    },
    async setTokenDocument(state: any, payload: any) {
      const encResult = await encrypt(payload.data, payload.encryptCode);
      const encData = encResult.json;
      localStorage.setItem("coteku", encData);
      state.tokenDocument = payload.data;
    },
    setListNotification(state: any, newData: any) {
      state.dataNotification = newData;
    },
    setIsRead(state, payload) {
      const notification = state.dataNotification.find(
        (item) => item.id === payload.id
      );
      if (notification) {
        notification.data.isRead = payload.isRead;
      }
    },
  },
  /* eslint-disable */
  actions: {
    async startIdleTimer({ commit }) {
      let timer;
      const resetTimer = () => {
        commit("setIdle", false);
        clearTimeout(timer);
        timer = setTimeout(() => {
          commit("setIdle", true);
        }, 86400000); // 24 hour idle time - 86400000 milliseconds
      };

      window.addEventListener("mousemove", resetTimer);
      window.addEventListener("keydown", resetTimer);
      window.addEventListener("scroll", resetTimer);
      resetTimer();
    },
    async fetchSearchUserNew(
      { commit },
      payload: { query: string; isEvent?: boolean }
    ) {
      const reqParams = {
        data: {
          name: payload.query,
          isEvent: payload.isEvent ?? false,
        },
      };
      return await fetchData(
        commit,
        clientv2.SearchUserBynameNew,
        reqParams,
        "userSearchResult"
      );
    },
    async SearchUserAndGroupNew(
      { commit },
      payload: { query: string; isEvent?: boolean }
    ) {
      const reqParams = {
        data: {
          name: payload.query,
          isEvent: payload.isEvent ?? false,
        },
      };
      return await fetchData(
        commit,
        clientv2.SearchUserAndGroupNew,
        reqParams,
        "userSearchResult"
      );
    },
    async fetchSearchUser({ commit }, query: string) {
      const reqParams = {
        data: {
          name: query,
        },
      };
      return await fetchData(
        commit,
        clientv2.SearchUserByname,
        reqParams,
        "userSearchResult"
      );
    },
    async fetchSearchUserSectorTemplate({ commit }, query: string) {
      const reqParams = {
        data: {
          name: query,
          type: "Page",
        },
      };
      const response = await fetchData(
        commit,
        clientv2.SearchUserAndGrupIdByNameAndSectorTemplate,
        reqParams,
        "userSearchResult"
      );

      return response;
    },
    async fetchMenuList({ commit, rootState }) {
      const reqParams = {
        data: {},
      };
      return await fetchData(
        commit,
        clientv2.getListMenu,
        reqParams,
        "userMenuList"
      );
    },
    async fetchListADG({ commit }) {
      const reqParams = {};
      return await fetchData(commit, clientv2.getListADG, reqParams, "listADG");
    },
    async fetchListADGDetail({ commit }) {
      const reqParams = {};

      return await fetchData(
        commit,
        clientv2.getListADGDetail,
        reqParams,
        "listADGDetail"
      );
    },
    async detachUser({ commit, rootState }) {
      const reqParams = {
        data: {
          username: rootState.username,
          deviceType: "web",
        },
      };
      return await fetchData(commit, clientv2.Logout, reqParams, "detach");
    },
    async getKeyAPIM({ commit }, request: any) {
      return client({}).post("Login/getKeyAPIM", request);
    },
    async getRefreshToken({ rootState }) {
      return client({}).post("/AntiForgery/getCacheToken", {
        username: rootState.username,
      });
    },
    async getNotificationLimitViewAndTotalNotifByUsername({ rootState }) {
      return client({})
        .post(
          "/Notification/getNotificationLimitViewAndTotalNotifByUsername",
          {}
        )
        .then((res: any) => {
          return new Promise((resolve) => {
            resolve(res.notificationViewList);
          });
        });
    },
    async createEventRole({ commit, rootState }) {
      const reqParams = {
        data: {
          username: rootState.username,
        },
      };
      const result = await fetchData(
        commit,
        clientv2.checkRoleMrdgByUsername,
        reqParams,
        "createEventRole"
      );
      return result;
    },
    async fetchCKEditorToken({ commit, rootGetters, getters }) {
      // if (typeof getters.getTokenCKEditor.ResponseCode !== "undefined")
      //   return true;
      const timeout = setTimeout(() => {
        // ketika proses lebih dari 2 detik muncul loading
        //bypass temuan security 11/02/2025 mustakim default value true
        commit("setLoadingTokenCke", false);
      }, 2000);
      const result = (await client({})
        .post("/CKEditor/GetTokenCkEditor")
        .catch((e) => {
          return e;
        })) as any;
      const key = {
        getters: {
          encryptionKey: rootGetters.encryptionKey,
          iv: rootGetters.iv,
        },
      };

      clearTimeout(timeout);
      commit("setLoadingTokenCke", false);
      commit("setTokenCKEditor", { data: result, encryptCode: key });

      return result;
    },
    async getDecryptedCKEditorToken({ state, rootGetters }) {
      // Action to properly handle async decryption
      let data = state.tokenCKEditor;
      if (localStorage.getItem("coteka")) {
        try {
          const key = {
            getters: {
              encryptionKey: rootGetters.encryptionKey,
              iv: rootGetters.iv,
            },
          };
          data = await decrypt(localStorage.getItem("coteka"), key);
        } catch (error) {
          console.error("Error decrypting CKEditor token:", error);
        }
      }
      return data;
    },
    async getDecryptedCKBoxToken({ state, rootGetters }) {
      let data = state.tokenCKBox;
      if (localStorage.getItem("coteki")) {
        try {
          const key = {
            getters: {
              encryptionKey: rootGetters.encryptionKey,
              iv: rootGetters.iv,
            },
          };
          data = await decrypt(localStorage.getItem("coteki"), key);
        } catch (error) {
          console.error("Error decrypting CKBox token:", error);
        }
      }
      return data;
    },
    async getDecryptedDocumentToken({ state, rootGetters }) {
      let data = state.tokenDocument;
      if (localStorage.getItem("coteku")) {
        try {
          const key = {
            getters: {
              encryptionKey: rootGetters.encryptionKey,
              iv: rootGetters.iv,
            },
          };
          data = await decrypt(localStorage.getItem("coteku"), key);
        } catch (error) {
          console.error("Error decrypting CKEditor token:", error);
        }
      }
      return data;
    },
    async fetchCKBoxToken({ commit, rootGetters, getters }) {
      const key = {
        getters: {
          encryptionKey: rootGetters.encryptionKey,
          iv: rootGetters.iv,
        },
      };
      const result = (await client({}).post("/CKEditor/GetTokenCkBox")) as any;
      commit("setTokenCKBox", {
        data: result.ResponseData?.value,
        encryptCode: key,
      });
      return result;
    },
    async fetchDocumentToken({ commit, rootGetters, getters }) {
      if (getters.getTokenDocument) return true;
      const result = (await client({}).post(
        "/CKEditor/GetTokenDocumentCKEditor"
      )) as any;
      const key = {
        getters: {
          encryptionKey: rootGetters.encryptionKey,
          iv: rootGetters.iv,
        },
      };
      commit("setTokenDocument", {
        data: result.ResponseData.value,
        encryptCode: key,
      });
      return result;
    },
    async getNotificationViewByUsernameNew(
      { commit, rootState },
      payload: any
    ) {
      return await client({})
        .post(
          "/Notification/new/getNotificationViewByUsername",
          payload.payload
        )
        .then((res: any) => {
          return new Promise((resolve) => {
            const notifications = res.notifications;
            resolve(notifications);
          });
        });
    },
    async updateNotificationViewById({ commit }, request) {
      return client({}).post("/Notification/new/markAsRead", request);
    },
    async getListTopics({ commit }, request) {
      return client({}).post("/FAQ/GetListTopics", request);
    },
    async getListQuestions({ commit }, request) {
      return client({}).post("/FAQ/GetListQuestion", request);
    },
    async getAnswer({ commit }, request) {
      return client({}).post("/FAQ/GetListAnswer", request);
    },
    handleRead({ commit }, payload) {
      commit("setIsRead", payload);
    },
    async getUserProfile({ commit }, request) {
      const response = await client({}).post("/MUser/GetProfile", request);
      return response;
    },
    async initialize({ commit }, request) {
      const response = await client({}).post("/Initialize", request);
      return response;
    },
    async getTokenApimBisa({}) {
      const response = await client({
        baseURL: process.env.VUE_APP_MW_AUTH_BISA,
        encryptRequest: false,
        decryptResponse: false,
        isRetry: true
      }).get("/Auth/GetTokenApim?device=web");
      return response.data;
    },
    async getTokenApimDDM({}) {
      const request = {
        appId: 3,
        deviceType: "web",
      };
      const response = await client({
        baseURL: process.env.VUE_APP_API_BISA,
        encryptRequest: false,
        decryptResponse: false,
        isRetry:true
      }).post("/App/RedirectApplication", request);
      return response;
    },
    async getProfileBisa({}) {
      const response = await client({
        baseURL: process.env.VUE_APP_API_BISA,
        encryptRequest: false,
        decryptResponse: false,
        isRetry: true
      }).post("/Profile");
      return response.data;
    },
    async initializeKey({ commit }, request) {
      const response = await client({}).post("Config/initializeConfig", request);
      const responseData =
        (response as any)?.responseData ??
        (response as any)?.data?.responseData ??
        {};
      commit("setInitializeConfig", responseData);
      return response;
    },
  },
};
