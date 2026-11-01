import clientv2 from "@/v2/library/ApiClient";
import client from "@v2/library/Api";
import { formatBytes, secureRandomFloat } from "@/v2/helpers/utils";
import { mimeTypes } from "../mock/Contants";
/* eslint-disable */
async function fetchData(commit, apiCall, requestData, keyToStore) {
  commit("setLoading", true);
  try {
    const res = await apiCall(requestData);
    const toIgnore = [""];
    if (toIgnore.includes(keyToStore)) {
      commit("setLoading", false);
      return res;
    }
    const dataToUpdate = {};
    dataToUpdate[keyToStore] = res.responseData;
    switch (res.responseCode) {
      case "011000": //code for success
        commit("setData", dataToUpdate);
        commit("setLoading", false);
        if (res.responseData) {
          return res.responseData;
        } else {
          return true;
        }
      case "011016": //code for success
        commit("setData", dataToUpdate);
        commit("setLoading", false);
        if (res.responseData) {
          return res.responseData;
        } else {
          return true;
        }
      default: // code for empty data
        commit("setData", {});
        commit("setLoading", false);
        return {};
    }
  } catch (err) {
    commit("setError", err);
    commit("setLoading", false);
    return {};
  }
}

export default {
  namespaced: true,
  state: {
    count: 0,
    data: new Map(),
    loading: false,
    loadingProgress: 0,
    error: null,
    validasiRevision: {} as any,
    idBpDocNext: "",
    loadingAsync: false,
    asyncType: "",
    onLoadingButtonState: false,
    documentStatus: "",
    labelProgress: "waiting for server response",
    idSector: "",
    loadingCheckRevision: false,
    userLimitError: false,
    connectionFailed: false,
  },
  getters: {
    getData: (state: any) => {
      return state.data;
    },
    getSectorId: (state: any) => {
      return state.idSector;
    },
    getLoading: (state: any) => {
      return state.loading;
    },
    getIdBpDocNext: (state: any) => {
      return state.idBpDocNext;
    },
    getOnloadingButtonState: (state: any) => {
      return state.onLoadingButtonState;
    },
    getDocumentStatus: (state: any) => {
      return state.documentStatus;
    },
    getLoadingProgress: (state: any) => {
      return state.loadingProgress;
    },
    getLabelProgress: (state: any) => {
      return state.labelProgress;
    },
    getCheckRevisionLoadingStatus: (state: any) => {
      return state.loadingCheckRevision;
    },
    getAsyncType: (state: any) => {
      return state.asyncType;
    },
    getUserLimitError: (state: any) => {
      return state.userLimitError;
    },
    getConnectionFailed: (state: any) => {
      return state.connectionFailed;
    },
  },
  mutations: {
    setData(state: any, newData: any) {
      state.data = newData;
    },
    setSectorId(state: any, idSector: string) {
      state.idSector = idSector;
    },
    setLoading(state: any, isLoading: boolean) {
      state.loading = isLoading;
    },
    setError(state: any, error: any) {
      state.error = error;
    },
    setRevision: (state: any, payload: any) => {
      state.validasiRevision = payload;
    },
    setIdBpDocNext: (state: any, payload: any) => {
      state.idBpDocNext = payload;
    },
    setLoadingAsync(state: any, payload: boolean) {
      state.loadingAsync = payload;
    },
    setAsyncType(state: any, payload: boolean) {
      state.asyncType = payload;
    },
    setOnLoadingButtonState(state: any, value: any) {
      state.onLoadingButtonState = value;
    },
    setDocumentStatus(state: any, value: any) {
      state.documentStatus = value;
    },
    setLoadingProgress(state: any, value: any) {
      state.loadingProgress = value;
    },
    setLabelProgress(state: any, value: any) {
      state.labelProgress = value;
    },
    setCheckRevisionLoadingStatus(state: any, value: boolean) {
      state.loadingCheckRevision = value;
    },
    setCheckUserLimit(state: any, value: boolean) {
      state.userLimitError = value;
    },
    setConnectionFailed(state: any, value: boolean) {
      state.connectionFailed = value;
    },
  },
  actions: {
    async fetchDocumentStatus({ commit, dispatch }, id: string) {
      commit("setCheckRevisionLoadingStatus", true);

      const checkRevisionResponse = await client({}).post<unknown, any>(
        "/BPDoc/CheckRevision",
        {
          idBPDocument: id,
        }
      );

      const checkRevision = checkRevisionResponse.responseData;
      commit(
        "collaborationStore/setDocumentStatus",
        checkRevision.statusName ?? "",
        { root: true }
      );
      dispatch("fetchFormDocument", id);
      commit(
        "collaborationStore/setDocumentStatusId",
        checkRevision.idStatus ?? "",
        { root: true }
      );

      commit("setCheckRevisionLoadingStatus", false);
    },
    async fetchDocumentMetadata({ commit }, data: any) {
      const response = await client({}).post<unknown, any>(
        "/BPDoc/getViewMetadataEForm",
        {
          ...data,
        }
      );
      const responseData = response.responseData;
      return responseData;
    },
    async fetchDocumentMetadata2D({ commit }, data: any) {
      const response = await client({}).post<unknown, any>(
        "/BPDoc/GetViewMetadataEFormbySection",
        {
          ...data,
        }
      );
      const responseData = response.responseData;
      return responseData;
    },
    async fetchFormDocument({ commit }, id: string) {
      // setStartDoc default false => temuan security 05/07/2025 case intercept ketika approve
      commit("collaborationStore/setStartDoc", false, { root: true });
      commit("collaborationStore/setLoading", true, { root: true });
      try {
        const checkRevisionResponse = await client({}).post<unknown, any>(
          "/BPDoc/CheckRevision",
          {
            idBPDocument: id,
          }
        );
        const checkRevision = checkRevisionResponse.responseData;
        commit(
          "collaborationStore/setDocumentStatus",
          checkRevision.statusName ?? "",
          { root: true }
        );
        commit(
          "collaborationStore/setDocumentStatusId",
          checkRevision.idStatus ?? 0,
          { root: true }
        );
        commit("setRevision", checkRevision);
        const response = await client({}).post<unknown, any>(
          "/EForm/GetEFormByBPDocAndUsername",
          {
            idBPDocument: id,
            isRevision: checkRevision.isRevision ?? false, // revisi document
            bundleVersion: process.env.VUE_APP_CKEDITOR_BUNDLE_VERSION,
          },
          {
            cancelPreviousRequests: true,
          }
        );
        const responseData = response.responseData;
        commit("setSectorId", responseData?.idSector ?? "");
        commit("setOnLoadingButtonState", true);
        commit(
          "collaborationStore/setFlagAlertCencel",
          responseData?.isCancelReasonView,
          {
            root: true,
          }
        );
        commit("collaborationStore/setUpdateAiu", responseData?.isUpdateAIU, {
          root: true,
        });
        commit("collaborationStore/setEventName", responseData?.eventName, {
          root: true,
        });
        commit(
          "collaborationStore/setDownloadCondition",
          responseData?.isDownloadFinal,
          {
            root: true,
          }
        );
        commit("collaborationStore/setReasonCencel", responseData?.reason, {
          root: true,
        });
        commit("collaborationStore/setAlartLabelCancel", responseData?.bpName, {
          root: true,
        });
        commit(
          "collaborationStore/setreasonReject",
          responseData?.rejectionComment,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setAccessStatus",
          responseData.isEditAccess,
          {
            root: true,
          }
        );
        commit("collaborationStore/setPreviewDoc", responseData.isPreview, {
          root: true,
        });

        commit("collaborationStore/setPreviewPDF", responseData.isPreviewPDF, {
          root: true,
        });
        commit("collaborationStore/setExportWord", responseData.isExportWord, {
          root: true,
        });
        commit("collaborationStore/setImportPPT", responseData.isImportPPT, {
          root: true,
        });
        commit(
          "collaborationStore/setDisableImportPPT",
          responseData.isDisableImportPPT,
          {
            root: true,
          }
        );
        commit("collaborationStore/setNoBkbs", responseData.noBKBS, {
          root: true,
        });
        commit(
          "collaborationStore/setNoRisalahRapat",
          responseData.noRisalahRapat,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setNoRisalahRdg",
          responseData.noRisalahRDG,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setDateRisalahRdg",
          responseData.dateRisalahRDG,
          {
            root: true,
          }
        );

        commit(
          "collaborationStore/setaccessStatusFinal",
          responseData.isEditAccessFinal,
          {
            root: true,
          }
        );
        commit("collaborationStore/setStartDoc", responseData.isStartDoc, {
          root: true,
        });
        commit(
          "collaborationStore/setDocumentName",
          responseData.documentName,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setDocumentTypeId",
          responseData.idDocumentType ?? "",
          { root: true }
        );
        commit("collaborationStore/setRdgType", responseData.rdgType ?? "", {
          root: true,
        });
        commit(
          "collaborationStore/setDocSectoral",
          responseData.isDocSectoral ?? "",
          { root: true }
        );
        commit(
          "collaborationStore/setListTabMetadata",
          responseData?.listTabMetadata ?? "",
          { root: true }
        );
        commit(
          "collaborationStore/setStartEditEForm",
          [29].includes(responseData.idBpDocumentStatus ?? ""),
          { root: true }
        );
        commit("collaborationStore/setDocumentFlowCheck", secureRandomFloat(), {
          root: true,
        });
        commit("collaborationStore/setListForm", responseData.children, {
          root: true,
        });
        commit(
          "collaborationStore/setDisableAllForm",
          responseData.disabledForm,
          {
            root: true,
          }
        );
        commit("collaborationStore/setFormEditor", responseData, {
          root: true,
        });
        commit(
          "collaborationStore/setButtonVersion",
          responseData.isViewVersion,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setDocumentVersion",
          responseData.currentVersion,
          {
            root: true,
          }
        );
        commit("collaborationStore/setViewTitle", responseData.isVisibleTitle, {
          root: true,
        });
        commit("collaborationStore/setTitle", responseData.title, {
          root: true,
        });
        const versionList = await client({}).post<unknown, any>(
          "/EForm/GetListBPDocVersion",
          {
            idBPDocument: id,
          }
        );
        const responseVersion = versionList.responseData ?? [];
        commit("collaborationStore/setListVersion", responseVersion.data, {
          root: true,
        });
        commit(
          "collaborationStore/setFlagAccessDoc",
          !responseData.children?.length,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setFlagAlertAiu",
          responseData.isDeleteReasonView,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setIdBpDocVersion",
          responseData.idBpDocVersioncurrent,
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setEventKop",
          {
            start: responseData.eventStartKop,
            end: responseData.eventDate,
          },
          {
            root: true,
          }
        );
        commit(
          "collaborationStore/setIsEditTitlePNIN",
          responseData.isEditTitlePNIN,
          { root: true }
        );
        commit(
          "collaborationStore/setNoRisalahKomiteGabungan",
          responseData.noRisalahKomiteGabungan,
          { root: true }
        );
        commit(
          "collaborationStore/setIsContentMaterial",
          responseData.isContentMaterial,
          { root: true }
        );
        commit(
          "collaborationStore/setIsContentFinalisasi",
          responseData.isContentFinalisasi,
          { root: true }
        );
        commit(
          "collaborationStore/setDataMaterial",
          responseData.dataMaterial,
          { root: true }
        );
        commit("collaborationStore/setDocConfig", responseData.docConfig, {
          root: true,
        });
        commit("collaborationStore/setLoading", false, { root: true });
        return { checkRevision, responseData, responseVersion };
      } catch (error) {
        commit("collaborationStore/setAccessStatus", false, { root: true });
        commit("collaborationStore/setDocumentName", "", { root: true });
        commit("collaborationStore/setDocumentTypeId", "", { root: true });
        commit("collaborationStore/setRdgType", "", { root: true });
        commit("collaborationStore/setDocSectoral", "", { root: true });
        commit("collaborationStore/setStartEditEForm", false, { root: true });
        commit("collaborationStore/setDocumentFlowCheck", 0, { root: true });
        commit("collaborationStore/setListForm", [], { root: true });
        commit("collaborationStore/setDisableAllForm", false, { root: true });
        commit("collaborationStore/setFormEditor", {}, { root: true });
        commit("collaborationStore/setButtonVersion", false, { root: true });
        commit("collaborationStore/setListVersion", [], { root: true });
        commit("collaborationStore/setFlagAlertAiu", false, { root: true });
        commit("collaborationStore/setFlagAlertCencel", false, { root: true });
        commit("collaborationStore/setDownloadCondition", false, {
          root: true,
        });
        commit("collaborationStore/setReasonCencel", "", { root: true });
        commit("collaborationStore/setAlartLabelCancel", "", { root: true });
        commit("collaborationStore/setIdBpDocVersion", "", { root: true });
        commit("collaborationStore/setTitle", "", { root: true });
        commit("collaborationStore/setViewTitle", false, { root: true });
        commit("collaborationStore/setListTabMetadata", [], { root: true });
        commit("collaborationStore/setNoRisalahKomiteGabungan", null, {
          root: true,
        });
        commit("collaborationStore/setLoading", false, { root: true });
      }
    },

    async fetchPreviewDocument({ commit }, id) {
      const reqParams = {
        data: {
          idBPDocument: id,
        },
      };
      const result = await fetchData(
        commit,
        clientv2.previewDocument,
        reqParams,
        "previewDocument"
      );
      return result;
    },
    async previewDocumentMobile({ commit }, id) {
      const reqParams = {
        data: {
          idBPDocument: id,
        },
      };
      const result = await fetchData(
        commit,
        clientv2.GetViewEFormByBPDocAndUsername,
        reqParams,
        ""
      );
      return result;
    },
    async fetchContentFromStorage({ commit }, id) {
      const reqParams = {
        data: {
          document_id: id,
        },
      };
      const result = await fetchData(
        commit,
        clientv2.getContentFromStorage,
        reqParams,
        ""
      );
      return result;
    },
    async downloadDocument({ commit }, payload) {
      const reqParams = {
        data: {
          id: payload.id,
          exportType: payload.exportType,
        },
        onDownloadProgress: (progressEvent) => {
          commit("setLoadingProgress", formatBytes(progressEvent.loaded));
          commit(
            "setLabelProgress",
            "download " + formatBytes(progressEvent.loaded)
          );
        },
      };
      const result = await fetchData(
        commit,
        clientv2.downloadDocumentApprove,
        reqParams,
        ""
      );
      return result;
    },
    async getContentPlaceholder({ dispatch }, payload) {
      const tName = "CPTemplate.docx";
      const template = await fetch("/" + tName);
      const tType = template.headers.get("Content-Type") ?? mimeTypes["docx"]; // docx
      const newToken = await dispatch("userStore/getRefreshToken", null, {
        root: true,
      });
      const token = newToken.responseData;

      const body = {
        contentControlTag: "lorem", // tag dari content control yang dibuat di template file word (tName var)
        documentId: payload.DocumentId,
        documentType: payload.DocumentType,
        templateFile: new File([await template.blob()], tName, { type: tType }),
      };

      return client({ encryptRequest: false, decryptResponse: false }).post(
        "/Exploration/ContentPlaceholder",
        body,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-XSRF-TOKEN": token,
          },
          responseType: "blob",
          onUploadProgress: () => {},
        }
      );
    },
    async getPDFPreview({ commit }, id) {
      const formatBytes = (bytes, decimals = 2) => {
        if (!+bytes) return "0.00 Bytes";
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${
          sizes[i]
        }`;
      };
      commit("setLoadingProgress", formatBytes(0));
      const reqParams = {
        onDownloadProgress: (progressEvent) => {
          commit("setLoadingProgress", formatBytes(progressEvent.loaded));
        },
        data: {
          idBPDoc: id,
        },
      };
      const result = await fetchData(
        commit,
        clientv2.getDocConvertionPDFBeforeSend,
        reqParams,
        ""
      );
      return result;
    },
    async checkStatusAsyncDocument({ commit, dispatch }, data: any) {
      commit("setLoadingAsync", true);
      commit("setAsyncType", data?.type);
      const { responseData } = await client({}).post<unknown, any>(
        "/BPDoc/CheckStatusInProgress",
        {
          idBPDocument: data.id,
        }
      );

      commit(
        "collaborationStore/setDocumentStatus",
        responseData.status ?? "",
        { root: true }
      );
      commit("collaborationStore/setDocumentStatusId", responseData.id ?? 0, {
        root: true,
      });

      setTimeout(() => {
        // dispatch("fetchFormDocument", id);
        commit("setLoadingAsync", false);
        commit("setAsyncType", "");
        /**
         * jika status dokumen sudah final (approved, canceled, atau published),
         * maka aksi ini akan memicu reload data dokumen.
         * melakukan refetch pembaruan state pada dokumen, button, cek revisi
         */
        if (
          ["approved", "approve", "canceled", "published"].includes(
            responseData.status.toLowerCase()
          )
        )
          dispatch("fetchFormDocument", data.id);
      }, 2000);

      return responseData;
    },
    async getDocumentTypeListByUsername({}, request: any) {
      return client({}).post(
        "/MDocumentType/GetListMdocumentTypeByUsername",
        request
      );
    },
    async updateUserApproval({ commit }, request: any) {
      commit("setLoading", true);
      return client({})
        .post(`/BPDoc/UpdateUserApproval`, request)
        .finally(() => {
          commit("setLoading", false);
        });
    },
    async importPpt(
      { dispatch },
      payload: {
        request: any;
        onUploadProgress: any;
      }
    ) {
      const response = await dispatch("userStore/getRefreshToken", null, {
        root: true,
      });
      const token = response.responseData;
      return client({ encryptRequest: false }).post(
        "/PowerPoint/extractAndMappingEform",
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
    async checkUserLimit({ commit }, isUserLimitError: boolean) {
      commit("setCheckUserLimit", isUserLimitError);
      return isUserLimitError;
    },
    async checkConnectionFailed({ commit }, isConnectionFailed: boolean) {
      commit("setConnectionFailed", isConnectionFailed);
      return isConnectionFailed;
    },
    async getDataViewFinalisasi({}, request: any) {
      return client({}).post("/BPDoc/ViewContentFinalisasi", request);
    }
  },
};
