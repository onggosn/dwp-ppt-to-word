/* eslint-disable */
import client from "@v2/library/Api";
import { formatBytes } from "@/v2/helpers/utils";
export default {
  namespaced: true,
  state: {
    itemsFilter: [],
    itemsSort: [],
    dashboardItemsSort: [],
    searchMode: {},
  },
  getters: {
    getItemsFilter: (state: any) => {
      return state.itemsFilter;
    },
    getItemsSort: (state: any) => {
      return state.itemsSort;
    },
    getDashboardItemsSort: (state: any) => {
      return state.dashboardItemsSort;
    },
    getStatusSearch: (state: any) => {
      return state.searchMode;
    },
  },
  mutations: {
    setItemsFilter(state: any, value: any) {
      state.itemsFilter = value;
    },
    setItemsSort(state: any, value: any) {
      state.itemsSort = value;
    },
    setDashboardItemsSort(state: any, value: any) {
      state.dashboardItemsSort = value;
    },
    setStatusSearch(state: any, value: any) {
      state.searchMode = value;
    },
  },
  actions: {
    async getPenugasanList({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListAssignmentbyTipePenugasan",
        request
      );
    },
    async getArahanList({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListAssignmentbyTipeArahan",
        request
      );
    },
    async getCounterPenugasan({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListCounterAssignmentbyTipePenugasanbyAssignmentMember",
        request
      );
    },
    async getCounterArahan({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListCounterAssignmentbyTipeArahanbyAssignmentMember",
        request
      );
    },
    async getCounterPenugasanInAssignment({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetCounterAssignmentPenugasan",
        request
      );
    },
    getCounterArahanInAssignment({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetCounterAssignmentArahan",
        request
      );
    },
    async getMemberAssignment({ commit }, request: any) {
      return client({}).post(
        "/AssignmentMemberNew/GetListAssignmentMemberByIdAssignment",
        request
      );
    },
    async InsertListAssignmentMember({ commit }, request: any) {
      return client({}).post(
        "/AssignmentMemberNew/InsertListAssignmentMember",
        request
      );
    },
    async EditAssignmentMemberByUserName({ commit }, request: any) {
      return client({}).post(
        "/AssignmentMemberNew/EditAssignmentMemberByUserName",
        request
      );
    },
    async DeleteAssignmentMemberByUserName({ commit }, request: any) {
      return client({}).post(
        "/AssignmentMemberNew/DeleteAssignmentMemberByUserName",
        request
      );
    },
    async getAssignmentFilter({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetFilterDashboard", request);
    },
    async getWorkspaceFilter({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListFilterWorkspace");
    },
    async getDashboardSort({ commit }, req: any) {
      const { responseData } = await client({}).post<unknown, any>("/DashboardNew/GetListSortWorkspace");

      commit("setDashboardItemsSort", responseData.data ?? []);

      return responseData.data;
    },
    async deleteAssignment({ commit }, request: any) {
      return client({}).post("/AssignmentNew/DeleteAssignment", request);
    },
    async GetListFlowApprovalByIdAssignment({ commit }, request: any) {
      return client({}).post(
        "/MAssignmentApprovalFlowNew/GetListFlowApprovalByIdAssignment",
        request
      );
    },
    async AssignmentApproval({ commit }, request: any) {
      return client({}).post("/AssignmentNew/AssignmentApproval", request);
    },
    async getDetailAssignmentById({ commit }, request: any) {
      return client({}).post("/AssignmentNew/GetDetailAssignmentById", request);
    },
    async GetListCounterWorkspace({ commit }, request: any) {
      return client({}).post("/DashboardNew/GetListCounterWorkspace");
    },
    async getCounterAssignmentPenugasan({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListCounterAssignmentbyTipePenugasanbyAssignmentMember"
      );
    },
    async getCounterAssignmentArahan({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListCounterAssignmentbyTipeArahanbyAssignmentMember"
      );
    },
    async getListAssignmentPenugasan({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListAssignmentbyTipePenugasanAndAssignmentMember",
        request
      );
    },
    async getListAssignmentArahan({ commit }, request: any) {
      return client({}).post(
        "/AssignmentNew/GetListAssignmentbyTipeArahanAndAssignmentMember",
        request
      );
    },
  },
};
