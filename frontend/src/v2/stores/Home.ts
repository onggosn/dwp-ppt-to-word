/* eslint-disable */
import client from "@v2/library/Api";

export default {
  namespaced: true,
  state: {
    isLoading: false,
  },
  getters: {
    getIsLoading: (state: any) => {
      return state.isLoading;
    },
  },
  mutations: {
    setIsLoading(state: any, payload: boolean) {
      state.isLoading = payload;
    },
  },
  actions: {
    async getTop5WorkList({ commit }: any) {
      commit("setIsLoading", true);
      return client({}).post("/Home/GetTop5WorkList").finally(() => {
        commit("setIsLoading", false);
      });
    },
  },
};
