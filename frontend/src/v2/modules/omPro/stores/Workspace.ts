import client from "@omPro/library/Api";

export default {
  namespaced: true,
  state: {
    isLoading: false,
    searchKeyword: "",
  },
  getters: {
    getIsLoading: (state: any) => {
      return state.isLoading;
    },
    getSearchRDGM: (state: any) => {
      return state.searchKeyword;
    },
  },
  mutations: {
    setIsLoading(state: any, newData: any) {
      state.isLoading = newData;
    },
    setSearchRDGM(state: any, newData: any) {
      state.searchKeyword = newData;
    },
  },
  actions: {
    async fetchListSuperEventByRDGByUsername({ commit }, request) {
      commit("setIsLoading", true);
      return client({})
        .post("/Content/getListSuperEventByRDGByUsername", request)
        .then((res: any) => {
          return res.responseData;
        })
        .finally(() => {
          commit("setIsLoading", false);
        });
    },
  },
};
