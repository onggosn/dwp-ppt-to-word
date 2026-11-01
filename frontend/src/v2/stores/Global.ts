export default {
  namespaced: true,
  state: {
    statusSearch: false,
    search: "",
    totalData: 0,
    totalDataPerPage: 0,
    needRefreshTOC: false,
  },
  getters: {
    getStatusSearch: (state: any) => {
      return state.statusSearch;
    },
    getSearch: (state: any) => {
      return state.search;
    },
    getTotalData: (state: any) => {
      return state.totalData;
    },
    getTotalDataPerPage: (state: any) => {
      return state.totalDataPerPage;
    },
    getNeedRefreshTOC: (state: any) => {
      return state.needRefreshTOC;
    },
  },
  mutations: {
    setStatusSearch: (state: any, value: any) => {
      state.statusSearch = value;
    },
    setSearch(state: any, value: any) {
      state.search = value;
    },
    setTotalData: (state: any, value: any) => {
      state.totalData = value;
    },
    setTotalDataPerPage: (state: any, value: any) => {
      state.totalDataPerPage = value;
    },
    setNeedRefreshTOC: (state: any, value: any) => {
      state.needRefreshTOC = value;
    },
  },
};
