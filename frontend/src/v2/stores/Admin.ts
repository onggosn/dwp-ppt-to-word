/* eslint-disable */
import client from "@v2/library/Api";
import {
  TSelect,
  ListADG,
  PaginationADG,
  ParamsListADG,
  DetailListADG,
  FormADG,
} from "../Type";
import { formatBytes } from "@/v2/helpers/utils";

export default {
  namespaced: true,
  state: {
    items: [],
    itemsFilter: [],
    subTab: 1,
    refreshList: "",
    searchAdmin: "",
    loadingProgress: 0,
    loadingADG: true,
    labelProgress: "waiting for server response",
    loading: false,
    searchMode: false,
    isMeetingPredefineMaterial: false,
    isAddMeetingPredefineMaterial: false,
    isTypeOngoing: false,
    AdgAccess: false,
    searchTotalData: {},
    listADG: [] as ListADG[],
    paginationADG: {} as PaginationADG,
    currentPageADG: 1 as number,
    paramsListADG: {
      page: 1,
      pageSize: 10,
    } as ParamsListADG,
  },
  getters: {
    getListADG: (state: any) => {
      return state.listADG;
    },
    getLoadingADG: (state: any) => {
      return state.loadingADG;
    },
    getPaginationADG: (state: any) => {
      return state.paginationADG;
    },
    getParamsListADG: (state: any) => {
      return state.paramsListADG;
    },
    getRefreshList: (state: any) => {
      return state.refreshList;
    },
    getTypeOngoing: (state: any) => {
      return state.isTypeOngoing;
    },
    getAdgAccess: (state: any) => {
      return state.AdgAccess;
    },
    getIsMeetingPredefineMaterial: (state: any) => {
      return state.isMeetingPredefineMaterial;
    },
    getIsAddMeetingPredefineMaterial: (state: any) => {
      return state.isAddMeetingPredefineMaterial;
    },
    getTotalData: (state: any) => {
      return state.searchTotalData;
    },
    getItemsFilter: (state: any) => {
      return state.itemsFilter;
    },
    getSearchAdmin: (state: any) => {
      return state.searchAdmin;
    },
    getSubTab: (state: any) => {
      return state.subTab;
    },
    getLoadingProgress: (state: any) => {
      return state.loadingProgress;
    },
    getStatusSearchMode: (state: any) => {
      return state.searchMode;
    },
    getLabelProgress: (state: any) => {
      return state.labelProgress;
    },
    getLoading: (state: any) => {
      return state.loading;
    },
  },
  mutations: {
    setADGPage(state: any, newValue: number) {
      state.currentPageADG = newValue;
    },
    setListADG(state: any, newValue?: ListADG[]) {
      state.listADG = newValue;
    },
    setDetailADG(state: any, { id, detail }) {
      const index = state.listADG.findIndex(
        (item: ListADG) => id === item.idFormasi
      );
      state.listADG[index].detailADG = detail;
    },
    setLoadingADG(state: any, newValue: boolean) {
      state.loadingADG = newValue;
    },
    setPaginationADG(state: any, newValue?: PaginationADG) {
      state.paginationADG = newValue;
    },
    setRefreshList(state, newValue) {
      state.refreshList = newValue;
    },
    setToastSet(state, newValue) {
      state.toastSet = newValue;
    },
    setTypeOngoing(state, newValue) {
      state.isTypeOngoing = newValue;
    },
    setAdgAccess(state, newValue) {
      state.AdgAccess = newValue;
    },
    setIsAddMeetingPredefineMaterial(state, newValue) {
      state.isAddMeetingPredefineMaterial = newValue;
    },
    setIsMeetingPredefineMaterial(state, newValue) {
      state.isMeetingPredefineMaterial = newValue;
    },
    setItemsFilter(state: any, value: any) {
      state.itemsFilter = value;
    },
    setSearchAdmin(state: any, value: any) {
      state.searchAdmin = value;
    },
    setSubTab(state: any, value: any) {
      state.subTab = value;
    },
    setLoadingProgress(state, newValue) {
      state.loadingProgress = newValue;
    },
    setStatusSearchMode(state, newValue) {
      state.searchMode = newValue;
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
    async getContentListResult({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListMBPDocByUsername",
        request
      );
    },
    async getListADGDetail({ commit }, idFormasi: string) {
      try {
        const response: DetailListADG = await client({}).post(
          "/DashboardAdmin/getListFormasiADGDetail",
          { idFormasi }
        );
        commit("setDetailADG", { id: idFormasi, detail: response });

        return response;
      } catch (error) {
        return error;
      }
    },
    async getListADG({ commit }, request: ParamsListADG) {
      commit("setLoadingADG", true);
      try {
        const response: any = await client({}).post(
          "/DashboardAdmin/getListFormasiADG",
          request
        );

        const data = response?.responseData?.list?.map((item: any) => ({
          idFormasi: item.idFormasi,
          name: item.formasiName,
          effectiveDate: item.effectiveDate,
          lastUpdatedDate: item.lastModifiedDate,
          lastUpdatedBy: item.lastModifiedBy,
          isActive: item.isActive,
        }));

        const pagination = response?.responseData?.info;
        commit("setListADG", data);
        commit("setPaginationADG", pagination);
        return response;
      } finally {
        commit("setLoadingADG", false);
      }
    },
    async createADG({}, request: FormADG) {
      return await client({
        encryptRequest: false,
        decryptResponse: false,
      }).post("/DashboardAdmin/insertFormasiADG", request);
    },
    async deleteADG({}, idFormasi?: string) {
      return await client({}).post("/DashboardAdmin/deleteFormasiADG", {
        idFormasi,
      });
    },
    async getMeetingOGResult({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListSuperEventByRDGByUsernameOnGoing",
        request
      );
    },
    async getMeetingList({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListBPEventByIdMUser",
        request
      );
    },
    async getUserList({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetListUserOperasional", request);
    },
    async getListPresentationMaterial({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListMEventDocPresentationMaterial",
        request
      );
    },
    async getPresentationMaterialDetail({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListMEventDocPresentationMaterialDetail",
        request
      );
    },
    async deletePresentationMaterial({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/deletePresentationMaterial",
        request
      );
    },

    async updateSectionOrder({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/UpdateSectionOrder", request);
    },
    async updateSubSectionOrder({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/updateSubSectionOrder", request);
    },

    async getGeneralMeeting({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/getDetailGeneralMeeting",
        request
      );
    },
    async getDeskripsiMeeting({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/getDetailDescriptionMeeting",
        request
      );
    },
    async getListEventMeeting(_, request: any) {
      return client({}).post(
        "DashboardAdmin/GetListMEventByIdMBPTemplate",
        request
      );
    },
    async addSectionMapping(_, request: any) {
      return client({}).post("DashboardAdmin/addMappingSectionPpt", request);
    },
    async getDetailMappingPpt(_, request: any) {
      return client({}).post(`DashboardAdmin/GetDetailMappingPpt`, request);
    },
    async getListSectionNamePpt(_, request: any) {
      return client({}).post(`DashboardAdmin/GetListSectionNamePpt`, request);
    },
    async addMappingSectionPpt(_, request: any) {
      return client({}).post("DashboardAdmin/addMappingSectionPPT", request);
    },
    async mappingSectionPptDownload(_, request: any) {
      return client({ decryptResponse: false }).post(
        "DashboardAdmin/DownloadMappingSectionPPT",
        request,
        {
          responseType: "blob",
        }
      );
    },
    async getListMEventDocPresentationMaterial(_, request: any) {
      return client({}).post(
        "DashboardAdmin/GetListMEventDocPresentationMaterial",
        request
      );
    },
    async updateContentChildList({ commit }, request: any) {
      return client({}).post("/MEformTemplate/updateMEformTemplate", request);
    },
    async getRoleList({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetListMRole", request);
    },
    async getUserRoleDetail({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetListMUserRoleNewDWP", request);
    },
    async getDetailBPDocOnGoing({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetDetailBPDocOnGoing", request);
    },
    async GetSubSectionBPDocOnGoing({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetSubSectionBPDocOnGoing",
        request
      );
    },
    async resetApproval({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/ResetApproval", request);
    },
    async DeleteEFormByIdEForm({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/DeleteEFormByIdEForm", request);
    },
    async AddBPSectionOnGoingByIdBPDocument({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/AddBPSectionOnGoingByIdBPDocument",
        request
      );
    },
    async AddEFormOnGoingByIdBPSection({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/AddEFormOnGoingByIdBPSection",
        request
      );
    },
    async updateEForm({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/UpdateEform", request);
    },
    async ChangeOrderSectionOnGoing({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/ChangeOrderSectionOnGoing",
        request
      );
    },
    async ChangeOrderSubSectionOnGoing({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/ChangeOrderSubSectionOnGoing",
        request
      );
    },
    async getListSection({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetListSection", request);
    },
    async getListSubSectionOg({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListTahapanBPOnGoing",
        request
      );
    },
    async getListSubDetailSectionOg({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListDokumenTahapanBPOnGoing",
        request
      );
    },
    async getListRDGType() {
      return client({}).post("/DashboardAdmin/getListRDGType");
    },
    async getListEventSubType() {
      return client({}).post("/DashboardAdmin/getListEventSubType");
    },
    async getListSector({ commit }, data) {
      return client({}).post("/DashboardAdmin/getListSector", data);
    },
    async getSearchNameMember({ commit }, name: string) {
      return client({}).post("/DashboardAdmin/getSearchNameMemberByBP", {
        name: name,
      });
    },
    async getFlowDoc2d({ commit }, request: any) {
      return client({}).post("/BPDoc/GetViewStatusDocumentbySection", request);
    },
    // add predefine
    async storeContentPreDefine({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/insertContentPreDefine", request);
    },
    // edit predefine
    async getEditContentPreDefine({ commit }, id: number) {
      return client({}).post("/DashboardAdmin/getMBPDocName", {
        idMBPDocumentTemplate: id,
      });
    },
    async updateContentPreDefine({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/updateDocNameByIdMBPDocTemplate`,
        request
      );
    },
    // stp mapping
    async getStpMapping({ commit }, id: number) {
      return await client({})
        .post("/DashboardAdmin/GetMEFormMappingTemplate", {
          idMEFormTemplateSource: id,
        })
        .then((response: any) => {
          // groupping dilakukan karna BE (jensen) tidak mau lakukan grouping
          const data = response.responseData;
          let outputs = (data.content ?? []).reduce(function (rv, x) {
            (rv[x["idBP"]] = rv[x["idBP"]] || []).push(x);
            return rv;
          }, {});

          outputs = Object.entries(outputs).map((entry: any) => {
            const key = entry[0];
            const value = entry[1];
            return {
              content_id: parseInt(key),
              forms: value.map((form: any) => {
                const section = form?.form?.section ?? {};
                const res = {
                  form_id: form.form.idMBPDocumentTemplate as string,
                  section_id: section.idMBPSectionTemplate,
                  sub_section_id: section?.subSection?.idMEFormTemplate,
                  nested_list: {
                    section: [],
                    sub_section: [],
                  },
                };
                return res;
              }),
              nested_list: {
                contents: [],
              },
            };
          });

          if (outputs.length == 0) {
            outputs.push({
              content_id: null,
              forms: [
                {
                  form_id: null,
                  section_id: null,
                  subSection_id: null,
                  nested_list: {
                    section: [] as TSelect[],
                    sub_section: [] as TSelect[],
                  },
                },
              ],
              nested_list: {
                contents: [] as TSelect[],
              },
            });
          }

          const result = {
            content: data.formInput,
            section: data.formSection,
            sub_section: data.formSubSection,
            template_id: data.idMBPTemplate,
            section_id: data.idMEventSubTypeList,
            sector_id: data.idSector,
            outputs: outputs,
          };
          return new Promise((resolve) => {
            resolve(result);
          });
        });
    },
    async getTahapanList({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetMBPList`, request);
    },
    async getContentList({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/GetMBPDocTemplateListMapping`,
        request
      );
    },
    async getSectionList({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/GetMBPSectionTemplateList`,
        request
      );
    },
    async getSubSectionList({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/GetMBPSubSectionTemplateList`,
        request
      );
    },
    async storeStpMapping({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/InsertMEFormMappingTemplate`,
        request
      );
    },
    async getListSortingType({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/getAdminSort", request);
    },
    async getAdminFilter({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/getAdminFilter", request);
    },
    async getOnGoingFilter({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetOnGoingFilter", request);
    },
    async GetMeetingFilter({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetMeetingFilter", request);
    },
    async GetPresentationMaterialFilter({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetPresentationMaterialFilter",
        request
      );
    },
    async GetFilterFAQ({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetFilterFAQ", request);
    },
    // add meeting
    async getUserMeeting() {
      return client({}).post("/DashboardAdmin/getAdminSort");
    },
    async storeAgendaMeeting({ commit }, request: any) {
      return client({}).post(`DashboardAdmin/addMeetingAgenda`, request);
    },
    async getEditAgendaMeeting({ commit }, id: number) {
      return client({}).post("DashboardAdmin/getFormMeetingAgenda", {
        idMEventAgendaTemplate: id,
      });
    },
    async updateAgendaMeeting({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/UpdatePredefineAgenda`, request);
    },
    async updateFormasiADG({ commit }, request: any) {
      return client({
        encryptRequest: false,
        decryptResponse: false,
      }).post("/DashboardAdmin/updateFormasiADG", request);
    },
    async getAdminTabMenu({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/GetListTabMenuAdmin", request);
    },
    async deletePDMeeting({ commit }, request: any) {
      return client({}).post("/Event/deletePredefinedMeeting", request);
    },
    async getListDownload({ commit }) {
      return client({}).post("DashboardAdmin/DownloadList");
    },
    async download({ commit }, request: any) {
      commit("setLabelProgress", "waiting for server response");
      return client({ decryptResponse: false }).post(
        "/DashboardAdmin/DownloadAdmin",
        request,
        {
          responseType: "blob",
          onDownloadProgress: (progressEvent) => {
            commit("setLoadingProgress", formatBytes(progressEvent.loaded));
            commit(
              "setLabelProgress",
              "download " + formatBytes(progressEvent.loaded)
            );
          },
        }
      );
    },
    async downloadRole({ commit }, request: any) {
      commit("setLabelProgress", "waiting for server response");
      return client({ decryptResponse: false }).post(
        "/UserRole/ExportToExcelCSV",
        request,
        {
          responseType: "blob",
          onDownloadProgress: (progressEvent) => {
            commit("setLoadingProgress", formatBytes(progressEvent.loaded));
            commit(
              "setLabelProgress",
              "download " + formatBytes(progressEvent.loaded)
            );
          },
        }
      );
    },
    async storeMeeting({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/addMEventTemplateByIdMUser`,
        request
      );
    },
    async updateDeskripsiMeeting({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/updateEventDescription`, request);
    },
    async updateGeneralMeeting({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/updateEvent`, request);
    },
    async storeSection({ commit }, request: any) {
      commit("setLoading", true);
      return client({})
        .post(
          `/DashboardAdmin/addMBPSectionTemplateByIdMBPDocTemplate`,
          request
        )
        .finally(() => {
          commit("setLoading", false);
        });
    },
    async storeSubSection({ commit }, request: any) {
      commit("setLoading", true);
      return client({})
        .post(
          `/DashboardAdmin/addMEFormTemplateByIdMBPSectionTemplate`,
          request
        )
        .finally(() => {
          commit("setLoading", false);
        });
    },
    async deleteSectionContent({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/deleteListMBPSectionTemplateByIdMBPSectionTemplate`,
        request
      );
    },
    async deleteContent({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/deleteListMBPDocumentTemplateByIdMBPDocumentTemplate`,
        request
      );
    },
    async getListMemberMeeting({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListMEventMemberByIdMEventTemplate",
        request
      );
    },
    async deleteMemberMeeting({ commit }, request: any) {
      return client({}).post("/Event/deletePredefinedMemberMeeting", request);
    },
    async deleteRole({ commit }, request: any) {
      return client({}).post(
        "/BPDoc/deleteMRoleMemberByIdMRoleMember",
        request
      );
    },
    async getListAllMemberbyMRoleId({ commit }, request: any) {
      return client({}).post(
        "/DashboardAdmin/GetListAllMemberbyMRoleId",
        request
      );
    },
    async getListAllListAgenda({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/getDetailMeetingAgenda", request);
    },
    async deletePredefinedAgenda({ commit }, request: any) {
      return client({}).post("/Event/deletePredefinedAgenda", request);
    },
    async getListAccessMemberPresentationMaterial({ commit }, request) {
      return client({}).post(
        "/DashboardAdmin/getListAccessMemberPresentationMaterial",
        request
      );
    },
    async addMemberPresentationMaterial({ commit }, request) {
      return client({}).post(
        "/DashboardAdmin/addMemberPresentationMaterial",
        request
      );
    },
    async updateMemberPresentationMaterial({ commit }, request) {
      return client({}).post(
        "/DashboardAdmin/updateMemberPresentationMaterial",
        request
      );
    },
    async deleteMemberPresentationMaterial({ commit }, request) {
      return client({}).post(
        "/DashboardAdmin/deleteMemberPresentationMaterial",
        request
      );
    },
    async storePresentationMaterial({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/addPresentationMaterial`,
        request
      );
    },
    async getListUsername({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetListUsername`, request);
    },
    async updateMFA({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/updateMFA`, request);
    },
    async updateUserLock({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/UnlockUser`, request);
    },
    async updateToggleMFA({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/UpdateToggleMFA`, request);
    },
    async addFAQTopic({ commit }, request: any) {
      return client({}).post("/DashboardAdmin/AddFAQTopic", request);
    },
    async getListTopics({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetListFAQTopics`, request);
    },
    async getFAQTopicDetail({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetFAQTopicDetail`, request);
    },
    async deleteFAQTopic({ commit }, request: any) {
      return await client({}).post(`/DashboardAdmin/DeleteFAQTopic`, request);
    },
    async deleteFAQQuestion({ commit }, request: any) {
      return await client({}).post(
        `/DashboardAdmin/DeleteFAQQuestion`,
        request
      );
    },
    async getListAnswer({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/getListAnswer`, request);
    },
    async getListNotification({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetListNotification`, request);
    },
    async getListNotificationDetail({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/GetListNotificationDetail`,
        request
      );
    },
    async addFAQTopicQuestion({ commit }, request: any) {
      return client({ encryptRequest: false }).post(
        `/DashboardAdmin/AddFAQTopicQuestion`,
        request,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
    },
    async updateFAQTopicQuestion({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/EditFAQTopicQuestion`, request);
    },
    async getFAQAnswer({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetFAQAnswer`, request);
    },

    async editFAQAnswer({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/EditFAQAnswer`, request);
    },
    async downloadFAQAnswer({ commit }, request: any) {
      return client({ decryptResponse: false }).post(
        `/DashboardAdmin/DownloadFAQ`,
        request,
        {
          responseType: "blob",
        }
      );
    },
    async getNotificationDataEdit({ commit }, request: any) {
      return client({}).post(
        `/DashboardAdmin/GetNotificationDataEdit`,
        request
      );
    },
    async updateNotification({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/UpdateNotification`, request);
    },
    async getListMUserAndRole({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetListMUserAndRole`, request);
    },
    async getDropdownMRole({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/GetDropdownMRole`, request);
    },
    async UpdateUserAndRole({ commit }, request: any) {
      return client({}).post(`/DashboardAdmin/UpdateUserAndRole`, request);
    },
    async mappingPasswordManualLoginAdd({ commit }, request: any) {
      return client({}).post(`/MappingPasswordManualLogin/Add`, request);
    },
    async mappingPasswordManualGetList({ commit }) {
      return client({}).post(`/MappingPasswordManualLogin/GetList`);
    },
  },
};
