import { encrypt, decrypt } from "@/library/CryptoHelper";
import client from "../library/Api";
import store from "@/store";

export default {
  namespaced: true,
  state: {
    countRDGB: 0,
    countRDGTK: 0,
    countRDGM: 0,
    searchWorkpspaceRes: [] as Array<any>,
    workspaceRDG: [] as Array<any>,
    contentFilter: [] as Array<any>,
    contentFilterCommit: {} as any,
    isLoading: false,
  },
  mutations: {
    setWorkspaceRDG(state: any, newData: any) {
      state.workspaceRDG = newData;
    },
    setCountWorkspaceRDG(state: any, newData: any) {
      state.countRDGB = newData.data[0].total;
      state.countRDGM = newData.data[1].total;
      state.countRDGTK = newData.data[2].total;
    },
    setContentFilter(state: any, newData: any) {
      state.contentFilter = newData;
    },
    setSearchResultWorkspace(state: any, newData: any) {
      state.searchWorkpspaceRes = newData;
    },
    setContentFilterCommit(state: any, payload: any) {
      const encData = encrypt(payload, store).json;
      localStorage.setItem("wpcfil", encData);
      state.contentFilterCommit = payload;
    },
    setIsLoading(state: any, newData: any) {
      state.isLoading = newData;
    },
  },
  actions: {
    async fetchListSuperEventByRDGByUsername({ commit }, request) {
      return client({})
        .post("/Content/getListSuperEventByRDGByUsername", request)
        .then((res: any) => {
          commit("setWorkspaceRDG", res.responseData);
          return res.responseData;
        });
    },
    async fetchSearchResultWorkspace({ commit }, request) {
      return client({})
        .post("/DashboardNew/GetListWorkspace", request)
        .then((res: any) => {
          commit("setSearchResultWorkspace", res.responseData);
          return res.responseData;
        });
    },
    async fetchCounterByRDGType({ commit }, request) {
      commit("setIsLoading", true);
      return client({})
        .post("/Content/getCounterByRDGType", request)
        .then((res: any) => {
          commit("setCountWorkspaceRDG", res.responseData);
          return res.responseData;
        })
        .finally(() => {
          commit("setIsLoading", false);
        });
    },
    async fetchContentFilter({ commit }, request) {
      return client({})
        .post("/Content/getContentFilter", request)
        .then((res: any) => {
          commit("setContentFilter", res.responseData);
          return res.responseData;
        });
    },
  },
  getters: {
    getContentFilterCommit(
      state: any,
      getters: any,
      rootState: any,
      rootGetters: any
    ) {
      let data = state.contentFilterCommit;
      if (localStorage.getItem("wpcfil")) {
        const key = {
          getters: {
            encryptionKey: rootGetters.encryptionKey,
            iv: rootGetters.iv,
          },
        };
        data = decrypt(localStorage.getItem("wpcfil"), key);
      }
      return data;
    },
  },
  getIsLoading: (state: any) => {
    return state.isLoading;
  },
};
