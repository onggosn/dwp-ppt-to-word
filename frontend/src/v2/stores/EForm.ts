import client from "@v2/library/Api";
import { TListVersion } from "@v2/Type.d";
import { useToast } from "vue-toastification";

const toast = useToast();
export default {
  namespaced: true,
  state: {
    statusBpDoc: Object,
    versionBpDoc: [] as TListVersion[],
  },
  getters: {
    getStatusBpDoc: (state: any) => {
      return state.statusBpDoc;
    },
    getVersionBpDoc: (state: any) => {
      return state.versionBpDoc;
    },
  },
  mutations: {
    setStatusBpDoc(state: any, payload: any) {
      state.statusBpDoc = payload;
    },
    setVersionBpDoc(state: any, payload: TListVersion[]) {
      state.versionBpDoc = payload;
    },
  },
  actions: {
    /* eslint-disable */
    async SearchUserAndGrupByName({ commit }, name: string) {
      return client({}).post("/MUser/SearchUserAndGrupByName", {
        name: name
      });
    },
    async GetListFlowDetail({ commit }, request: any) {
      return client({}).post("/MBPApprovalFlow/GetListFlowDetail", request);
    },
    async GetListBpDocApproval({ commit }, request: any) {
      return client({}).post("/MBPApprovalFlow/GetListBPDocApproval", request);
    },
    async doApproval({ commit }, request: any) {
      return client({})
        .post("/BPDoc/Approval", request)
        .catch((err: any) => {
          if (err.response.status === 400) {
            toast.warning(
              err.response.data.responseMessage ?? "internal server error"
            );
          }
          return err;
        });
    },
    async doRevisi({ rootState }, request: any) {
      return client({}).post("/BPDoc/ApprovalRevision", request);
    },
    async saveEachContentEForm({ commit }, request) {
      return client({}).post("/EForm/UpdateEFormByIdFormEditor", request);
    },
    async updateBPDocStatusById({ commit }, request) {
      return client({}).post("/BPDoc/updateBPDocStatusById", request);
    },
    async updateAiuOtomatis({ commit }, request) {
      return client({}).post("/BPDoc/UpdateDataAIU", request);
    },
    async getStatusBpDoc({ commit }, request: any) {
      return client({})
        .post("/BPDoc/updateSendBPDocStatusById ", request)
        .then((response: any) => {
          commit("setStatusBpDoc", response.responseData);
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    async restoreCollabSession({ commit }, request) {
      return client({}).post("/CKEditor/RestoreCollaborativeSession", request);
    },
    /* PREVIEW MERGED DOCUMENT */
    async getPreviewbeforeSendByBPDocAndUsername({}, request) {
      return client({})
        .post("/EForm/GetPreviewbeforeSendByBPDocAndUsername", request, {
          cancelPreviousRequests: true
        })
        .catch((err: any) => {
          if (err.response.status === 400) {
            toast.warning(
              err.response.data.responseMessage ?? "internal server error"
            );
          }
          return err;
        });
    },
    async submitSTPMappingByUsername({}, request) {
      return client({}).post("/EForm/submitSTPMappingByUsername", request);
    },
    async getVersionBpDoc({ commit }, request) {
      return client({})
        .post("/EForm/GetListBPDocVersion", request)
        .then((response: any) => {
          commit("setVersionBpDoc", response.responseData);
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    /* Version MERGED DOCUMENT */
    async getVersionPreviewByBPDocVerAndUsername({}, request) {
      return client({}).post("/EForm/GetPreviewVersioning", request, {
        cancelPreviousRequests: true
      });
    },
    async downloadDocument({}, request) {
      return client({ decryptResponse: false }).post(
        "/BPDoc/DownloadBPDocumentFinal",
        request
      );
    },
    async getNextVersionToLoad({ commit }, request) {
      return client({})
        .post("/BPDoc/GetOtherIdBPDoc", request)
        .then((response: any) => {
          commit("documentStore/setIdBpDocNext", response.responseData);
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    async getAuditLog({}, request) {
      return client({})
        .post("/CKEditor/GetSuggestion", request)
        .then((response: any) => {
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    async getRevision({}, request) {
      return client({})
        .post("/CKEditor/GetRevisions", request)
        .then((response: any) => {
          return new Promise((resolve) => {
            resolve(response);
          });
        });
    },
    async getMBPTemplate({}, request: any) {
      return client({})
      .post("/EForm/GetMBPTemplate", request)
      .then((response: any) => {
        return new Promise((resolve) => {
          resolve(response);
        });
      });
    },
    async getListSectorPredefine() {
      return client({}).post("/EForm/GetSectorListPredifine");
    },
    async getMBPTemplateNewMeeting({}, request: any) {
      return client({})
      .post("/EForm/GetMBPTemplateNewMeeting", request)
      .then((response: any) => {
        return new Promise((resolve) => {
          resolve(response);
        });
      });
    },
    async getSubmitDetail({}, request: any) {
      return client({}).post("EForm/GetSubmitDetail", request);
    },
    async getMEventTemplate({}, request: any) {
      return client({}).post("/DashboardAdmin/GetMEventTemplate", request);
    },
    async updateTitleEForm({}, request: any) {
      return client({}).post("/EForm/UpdateTitlePNIN", request);
    },
    async uploadFinalizedDoc({}, payload: any) {
      return client({ encryptRequest: false }).post("/BPDoc/UploadFinalisasiPDF", payload.request,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: payload.onUploadProgress,
        });
    },
  }
};
