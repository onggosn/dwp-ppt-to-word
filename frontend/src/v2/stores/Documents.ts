/* eslint-disable */
import client from "@v2/library/Api";
import { formatBytes } from "@/v2/helpers/utils";
export default {
  namespaced: true,
  state: {
    itemsFilter: [],
    itemsSort: [],
    searchMode: {},
    searchTotalDataMateri: {},
    searchTotalDataHasil: {},
    searchTotalDataWorkspace: null,
    totalWorkspacePerPage: 0,
  },
  getters: {
    getItemsFilter: (state: any) => {
      return state.itemsFilter;
    },
    getItemsSort: (state: any) => {
      return state.itemsSort;
    },
    getStatusSearch: (state: any) => {
      return state.searchMode;
    },
    getTotalDataMateri: (state: any) => {
      return state.searchTotalDataMateri;
    },
    getTotalDataHasil: (state: any) => {
      return state.searchTotalDataHasil;
    },
    getTotalDataWorkspace: (state: any) => {
      return state.searchTotalDataWorkspace;
    },
    getTotalWorkspacePerPage: (state: any) => {
      return state.totalWorkspacePerPage;
    },
  },
  mutations: {
    setItemsFilter(state: any, value: any) {
      state.itemsFilter = value;
    },
    setItemsSort(state: any, value: any) {
      state.itemsSort = value;
    },
    setStatusSearch(state: any, value: any) {
      state.searchMode = value;
    },
    setTotalDataMateri(state: any, value: any) {
      state.searchTotalDataMateri = value;
    },
    setTotalDataHasil(state: any, value: any) {
      state.searchTotalDataHasil = value;
    },
    setTotalDataWorkspace(state: any, value: any) {
      if (typeof value === "object" && value) {
        state.searchTotalDataWorkspace = value;
      } else {
        state.searchTotalDataWorkspace = null;
      }
    },
    setTotalWorkspacePerPage(state: any, value: any) {
      state.totalWorkspacePerPage = value;
    },
    setResetTotalData(state: any, _) {
      state.totalWorkspacePerPage = 0;
      state.searchTotalDataWorkspace = {};   
    },
  },
  actions: {
    async getMateriList({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListDocument", request);
    },
    async getHasilList({ commit }, request: any) {
      return client({}).post(
        "/DashboardNew/GetListDocumentHasilPembahasan",
        request
      );
    },
    async getCounterMateri({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListCounterDocument", request);
    },
    async getCounterHasil({ commit }, request: any) {
      return client({}).post(
        "/DashboardNew/GetListCounterDocumentHasilPembahasan",
        request
      );
    },
    async getDocumentFilter({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListFilterDocument", request);
    },
    async SearchDocumentType({ commit }, request: any) {
      return client({}).post("/DashboardNew/SearchDocumentType", request);
    },
    async GetListWorkspace({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListWorkspace", request);
    },
    async GetListBpWorkspace({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListBpWorkspace", request);
    },
    async GetListContent({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListContent", request);
    },
    async GetListWorkspaceDetail({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListWorkspaceDetail", request);
    },
  },
};
