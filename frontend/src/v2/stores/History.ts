/* eslint-disable */
import client from "@v2/library/Api";
import { TSelect } from "../Type";
import { formatBytes } from "@/v2/helpers/utils";

export default {
  namespaced: true,
  state: {
    items: [],
    itemsFilter: [],
    subTab: 1,
    refreshList: "",
    loadingProgress: 0,
    labelProgress: "waiting for server response",
    loading: false,
    searchTotalData: {},
  },
  getters: {
    getRefreshList: (state: any) => {
      return state.refreshList;
    },
    getTotalData: (state: any) => {
      return state.searchTotalData;
    },
    getItemsFilter: (state: any) => {
      return state.itemsFilter;
    },
    getSubTab: (state: any) => {
      return state.subTab;
    },
    getLoadingProgress: (state: any) => {
      return state.loadingProgress;
    },
    getLabelProgress: (state: any) => {
      return state.labelProgress;
    },
    getLoading: (state: any) => {
      return state.loading;
    },
  },
  mutations: {
    setRefreshList(state, newValue) {
      state.refreshList = newValue;
    },
    setToastSet(state, newValue) {
      state.toastSet = newValue;
    },
    setItemsFilter(state: any, value: any) {
      state.itemsFilter = value;
    },
    setSubTab(state: any, value: any) {
      state.subTab = value;
    },
    setLoadingProgress(state, newValue) {
      state.loadingProgress = newValue;
    },
    setLoading(state, newValue) {
      state.loading = newValue;
    },
    setLabelProgress(state, newValue) {
      state.labelProgress = newValue;
    },
    setTotalData(state, newValue) {
      state.searchTotalData = newValue;
    },
  },
  actions: {
    async getHistoryList({ commit }, request: any) {
      return client({}).post("/History/GetListWorkSpace", request);
    },
    async GetFilterWorkspaceHistory({ commit }) {
      return client({}).post("/History/GetFilterWorkspaceHistory");
    },
    async downloadHistoryList({ commit }, request: any) {
      return client({ decryptResponse: false }).post(
        "/History/ExportToExcel",
        request,
        { responseType: "blob" }
      );
    },
    async getHistoryActivityTaskList({ commit }, request: any) {
      return client({}).post("/History/GetActivityTaskDetail", request);
    },
    async getHistoryDocumentList({ commit }, request: any) {
      return client({}).post("/History/GetListDocumentHistory", request);
    },
    async getHistoryMeetingList({ commit }, request: any) {
      return client({}).post("/History/GetListMeeting", request);
    },
    async getListAssignment({ commit }, request: any) {
      return client({}).post("/History/GetListAssignment", request);
    },
     async getDetailAssignmentById({ commit }, request: any) {
      return client({}).post("/Assignment/GetDetailAssignmentById", request);
    },
  },
};
