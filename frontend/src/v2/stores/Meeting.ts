import client from "@v2/library/Api";
import {
  THasilPembahasan,
  TListDocument,
  TListOrganizer,
  TMaterialList,
  TMaterialMetadata,
  TSelect,
} from "@v2/Type.d";

export default {
  namespaced: true,
  state: {
    meetingItem: {} as any,
    meetingSummary: {} as any,
    organizerList: [] as TListOrganizer[],
    materialList: [] as TMaterialList[],
    methodList: [] as TSelect[],
    typeDocList: [] as TSelect[],
    satkerPembuatList: [] as TSelect[],
    materialPSList: [] as TSelect[],
    materialEventList: [] as TSelect[],
    eventMemberList: [] as TSelect[],
    materialMetadata: {} as TMaterialMetadata,
    materialFlowButton: [] as any[],
    listDocument: [] as TListDocument[],
    modeDisableBtn: false,
    listAdg: [] as any[],
    meetingFilter: {
      pageSize: 10,
      page: 1,
      calendarType: "range",
      eventTypeFilter: [],
      eventSubTypeListFilter: [],
      eventAdgFilter: [],
      eventSearching: "",
      komite: [],
      dateFilter: null,
    } as any,
  },
  getters: {
    getModeDisableBtn: (state: any) => {
      return state.modeDisableBtn;
    },
    getListAdg: (state: any) => {
      return state.listAdg;
    },
    getMeetingFilter: (state: any) => {
      return state.meetingFilter;
    },
  },
  mutations: {
    setMeetingItem(state: any, payload: any) {
      state.meetingItem = payload;
    },
    setModeDisableBtn(state: any, payload: any) {
      state.modeDisableBtn = payload;
    },
    setOrganizerList(state: any, payload: TListOrganizer[]) {
      state.organizerList = payload;
    },
    setMaterialList(state: any, payload: TMaterialList[]) {
      state.materialList = payload;
    },
    setMeetingSummary(state: any, payload: any) {
      state.meetingSummary = payload;
    },
    setMethodList(state: any, payload: TSelect[]) {
      state.methodList = payload;
    },
    setTypeDocList(state: any, payload: TSelect[]) {
      state.typeDocList = payload;
    },
    setSatkerPembuatList(state: any, payload: TSelect[]) {
      state.satkerPembuatList = payload;
    },
    setMaterialPSList(state: any, payload: TSelect[]) {
      state.materialPSList = payload;
    },
    setMaterialEventList(state: any, payload: TSelect[]) {
      state.materialEventList = payload;
    },
    setEventMemberList(state: any, payload: any) {
      state.eventMemberList = payload.map((elm: any) => {
        if (elm.idGroup == null) {
          return {
            id: elm.idUser,
            value: elm.username,
          };
        }
        return {
          id: elm.idGroup,
          value: elm.groupName,
        };
      }) as TSelect[];
    },
    setMaterialMetadata(state: any, payload: TMaterialMetadata) {
      state.materialMetadata = payload;
    },
    setDocumentList(state, data) {
      state.listDocument = data;
    },
    setMaterialFlowButton(state: any, payload: any) {
      state.materialFlowButton = payload;
    },
    setListAdg(state: any, payload: any) {
      state.listAdg = payload;
    },
    setMeetingFilter(state: any, payload: any) {
      state.meetingFilter = {
        ...state.meetingFilter,
        ...payload,
      };
    },
  },
  actions: {
    /* eslint-disable */
    // meeting
    async getTaskMeetingByIdMeetingByUsername({ commit }, data: string) {
      return client({})
        .post("/MEvent/getEventDetailByIdEventByUsername", {
          idEvent: data,
        })
        .then((res: any) => {
          commit("setMeetingItem", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    //material
    async getMaterialByMeetingId({ commit }, request: any) {
      return client({})
        .post("/Event/getPresentationMaterial", request)
        .then((response: any) => {
          commit("setMaterialList", response.responseData);
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    async uploadMaterial(
      { dispatch },
      payload: {
        request: THasilPembahasan;
        onUploadProgress: any;
      }
    ) {
      const response = await dispatch("userStore/getRefreshToken", null, {
        root: true,
      });
      const token = response.responseData;
      return client({ encryptRequest: false }).post(
        "/Event/UploadMaterial",
        payload.request,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-XSRF-TOKEN": token,
          },
          onUploadProgress: payload.onUploadProgress,
        }
      );
    },
    async deleteMaterial({ commit }, request: any) {
      return client({}).post("/Event/DeleteMaterialById", request);
    },
    //material approval
    async getMaterialMethod({ commit }) {
      return client({})
        .post("/Event/getPresentationMaterialMethod", {})
        .then((res: any) => {
          commit("setMethodList", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getTypeDocument({ commit }) {
      return client({})
        .post("/Event/getPresentationMaterialDocumentType", {})
        .then((res: any) => {
          commit(
            "setTypeDocList",
            res.responseData.map((elm) => {
              return {
                id: elm.id,
                value: elm.documentType,
              };
            })
          );
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getDocumentList({ commit }, idEvent) {
      return client({})
        .post("/Event/getListDocumentPresentationMaterial", { idEvent })
        .then((res: any) => {
          const data = res.responseData.map((doc) => {
            return {
              id: doc.id,
              value: doc.value,
            };
          });

          commit("setDocumentList", data);

          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getSatkerPembuat({ commit }) {
      return client({})
        .post("/Event/getPresentationMaterialSatkerPembuat", {})
        .then((res: any) => {
          commit("setSatkerPembuatList", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getMaterialPS({ commit }) {
      return client({})
        .post("/Event/getPresentationMaterialProgramStrategis", {})
        .then((res: any) => {
          commit("setMaterialPSList", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getMaterialEvent({ commit }) {
      return client({})
        .post("/Event/getPresentationMaterialMEventSubTypeList", {})
        .then((res: any) => {
          commit("setMaterialEventList", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getEventMember({ commit }, idEvent: string) {
      return client({})
        .post("/Event/getListEventMemberByIdEvent", { idEvent: idEvent })
        .then((res: any) => {
          commit("setEventMemberList", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async getMaterialMetadata({ commit }, request: any) {
      return client({})
        .post("/Event/getViewMetadataMaterial", request)
        .then((res: any) => {
          const metadata = res.responseData;
          metadata.listPenyusun = res.responseData.listPenyusun.map(
            (elm: any) => {
              return elm.idGroup ? elm.groupName : elm.username;
            }
          );
          commit("setMaterialMetadata", metadata);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async uploadMaterialApproval(
      { dispatch },
      payload: {
        request: any;
        onUploadProgress: any;
      }
    ) {
      const { responseData } = await dispatch(
        "userStore/getRefreshToken",
        null,
        {
          root: true,
        }
      );
      return client({ encryptRequest: false }).post(
        "/Event/insertMetadataPresentationMaterial",
        payload.request,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-XSRF-TOKEN": responseData,
          },
          onUploadProgress: payload.onUploadProgress,
        }
      );
    },
    async getMaterialFlowButton({ commit }, idMaterial: string) {
      return client({})
        .post("/MEventPresentationMaterialApproval/GetListFlowDetail", {
          idPresentationMaterial: idMaterial,
        })
        .then((res: any) => {
          commit("setMaterialFlowButton", res.responseData);
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    async sendPenyetuju({ commit }, request: any) {
      return client({})
        .post("/Event/Approval", request)
        .then((res: any) => {
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },

    async getOrganizerByMeetingId({ commit }, data) {
      return client({})
        .post("/MEvent/getEventOrganizerByIdEvent", {
          idEvent: data,
        })
        .then((response: any) => {
          commit("setOrganizerList", response.responseData);
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    async fetchAgendaById({ commit }, id: string) {
      return client({}).post("/MEvent/GetEventAgendaByIdEventByUsername", {
        id: id,
      });
    },
    async publishMeetingAgenda({ commit }, id: string) {
      return client({}).post("/EventAgenda/PublishAgenda", {
        id: id,
      });
    },
    async getListEventByCalendarType({ commit }, request: any) {
      return client({}).post("/Calendar/getListEventByCalendarType", request);
    },
    async getMeetingFilter({ commit }) {
      return client({}).post("/Calendar/getMeetingFilter");
    },
    async submitOrderAgenda({ commit }, request: any) {
      return client({}).post("EventAgenda/updateAgendaOrder", request);
    },
    async submitSetAgenda({ commit }, request: any) {
      return client({}).post("MEvent/StartAndStopAgenda", request);
    },
    async getDetailEventAgenda({ commit }, request: any) {
      return client({}).post("MEvent/getEventAgendaById", request);
    },
    async getMemberADG({ commit }) {
      return client({}).post("EventAgenda/MemberADG");
    },
    async getAllStatusAgenda({ commit }) {
      return client({}).post("MEvent/getAgendaStatus");
    },
    async getAllSatker({ commit }) {
      return client({}).post("MSatkerPembuat");
    },
    async addAgenda({ commit }, request) {
      return client({}).post("EventAgenda/InsertAgenda", request);
    },
    async updateDetailAgenda({ commit }, request) {
      return client({}).post("MEvent/UpdateAgenda", request);
    },
    async deleteAgenda({ commit }, request) {
      return client({}).post("EventAgenda/DeleteEventAgenda", request);
    },
    async fetchDashboardSummary({ commit }, request: any) {
      return client({})
        .post("DashboardExec/GetDataByEventId", {
          idEvent: request.idEvent,
        })
        .then((res: any) => {
          commit("setMeetingSummary", res.responseData);
          commit(
            "collaborationStore/setEventName",
            res.responseData.eventName,
            {
              root: true,
            }
          );
          return new Promise((resolve) => {
            resolve(res);
          });
        });
    },
    //meeting result
    async uploadMeetingResult(
      { dispatch },
      payload: {
        request: THasilPembahasan;
        onUploadProgress: any;
      }
    ) {
      const response = await dispatch("userStore/getRefreshToken", null, {
        root: true,
      });
      const token = response.responseData;
      return client({ encryptRequest: false }).post(
        "/Event/UploadHasil",
        payload.request,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-XSRF-TOKEN": token,
          },
          onUploadProgress: payload.onUploadProgress,
        }
      );
    },
    async getMeetingResult({ commit }, request) {
      return client({}).post("/Event/getHasilPembahasan", request);
    },
    async deleteMeetingResult({ commit }, request: any) {
      return client({}).post("/Event/DeleteHasilPembahasanById", request);
    },
  },
};