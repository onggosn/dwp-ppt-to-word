import axios from "axios";
import qs from "query-string";
import { encrypt, decrypt } from "../library/CryptoHelper";
import { dd, randomRequestId } from "@/library/util";
import vuex from "@/store";
import router from "../router";
import { useToast } from "vue-toastification";
import { useMsal } from "@v2/composables/useMsal";
import { addApiVersion } from "@v2/helpers/utils";

const toast = useToast();
const newmiddlewareEndpoint = process.env.VUE_APP_MIDDLEWARE_NEW_PATH;
const client_id = process.env.VUE_APP_CLIENT_ID;
const client_secret = process.env.VUE_APP_CLIENT_SECRET;
const token_url = process.env.VUE_APP_TOKEN_URL;
const current_mode = process.env.VUE_APP_CURRENT_MODE;

async function apiCall({
  method = "post",
  url,
  data,
  store,
  decryptResponse = true,
  encryptRequest = true,
  addDefaultHeaders = true,
  customHeaders = {},
  responseType,
  onUploadProgress = () => undefined,
  onDownloadProgress = () => undefined,
  withCredentials = true,
  isRetry = false,
  baseURL = vuex.state.urlApim,
}) {
  const requestId = randomRequestId();
  const finalPayload = encryptRequest ? await encrypt(data, store) : data;
  const isMfa = process.env.VUE_APP_MFA_STATUS === "true";
  let authHeaders = {};
  dd(
    `[API][${requestId}][Req]`,
    method,
    url,
    "encrypted",
    finalPayload,
    "plain:",
    JSON.stringify(data)
  );
  if (addDefaultHeaders) {
    if (isMfa) {
      // Ambil token Azure secara otomatis & silent
      const { getToken } = useMsal();
      const tokenAzure = await getToken();

      authHeaders = {
        "authorization-app": `${tokenAzure}`,
      };
    }
  }

  const drHeader = await addApiVersion(store.state.kane, "v1");
  const defaultHeaders = addDefaultHeaders
    ? {
        ...authHeaders,
        Authorization: `Bearer ${store.state.accessToken}`,
        ultimatewarrior: store.state.teriyaki,
        bubbareydudley: store.state.yakiniku,
        dr: drHeader,
        callafriend:
          "D9E13A0B160B4B7DA6205B3BAEGE9A4A09E21C27E95D753C278F3A62B64EE07F",
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    : {};

  return axios({
    baseURL,
    method,
    url,
    data: finalPayload,
    headers: { ...defaultHeaders, ...customHeaders },
    responseType: responseType,
    onUploadProgress: onUploadProgress,
    onDownloadProgress: onDownloadProgress,
    withCredentials: withCredentials,
  })
    .then(async (response) => {
      if (!response || !response.data || !decryptResponse) {
        dd(`[API][${requestId}][Res]`, "data:", response.data);
        return response;
      }

      try {
        const plainData = await decrypt(response.data, store);
        dd(
          `[API][${requestId}][Res]`,
          "encrypted:",
          response.data,
          "plain",
          plainData
        );

        return { ...response, plainData };
      } catch (decryptError) {
        throw new Error(`Decryption failed: ${decryptError.message}`);
      }
    })
    .catch(async (err) => {
      if (err.response) {
        let status = err.response?.status ?? 400;
        if ([406].includes(status)) {
          vuex.dispatch("logout").then(() => {
            window.location.href = `${process.env.VUE_APP_URI_BISA}`;
          });
        } else if ([401].includes(status) && current_mode == "private") {
          if (isRetry) {
            window.location.href = `${process.env.VUE_APP_URI_BISA}`;
            return Promise.reject(err);
          }
          try {
            const apimBisa = await store.dispatch("userStore/getTokenApimBisa");

            if (!apimBisa?.access_token) {
              throw new Error("Token APIM Bisa tidak ditemukan");
            }

            store.commit("userStore/setApimBisa", apimBisa.access_token);

            const apimDDM = await store.dispatch("userStore/getTokenApimDDM");
            const tokenDDM = apimDDM?.data?.responseData?.apim;

            if (!tokenDDM) {
              throw new Error("Token APIM DDM tidak ditemukan");
            }

            store.dispatch("updateAccessToken", tokenDDM);
          } catch (error) {
            window.location.href = `${process.env.VUE_APP_URI_BISA}`;
          }
        } else if ([403].includes(status)) {
          toast.warning("Anda tidak memiliki akses");
          router.push({ name: "home" });
        }
      }
      return Promise.reject(err);
    });
}

const client = {
  getKeySHA256({ store }, username) {
    return apiCall({
      method: "get",
      url: "/Login/getKeySHA256?username=" + username,
      addDefaultHeaders: true,
      decryptResponse: false,
      encryptRequest: false,
      store,
    });
  },
  getKeySHA256new({ store }, username) {
    return apiCall({
      method: "get",
      baseURL: newmiddlewareEndpoint,
      url: "/Login/getKeySHA256?username=" + username,
      addDefaultHeaders: true,
      decryptResponse: false,
      encryptRequest: false,
      store,
    });
  },

  //=====================PUBLIC MODE ONLY!!=============================\\
  getAccessToken() {
    const payload = {
      client_id: client_id,
      client_secret: client_secret,
      scope: "dmp",
      grant_type: "client_credentials",
    };

    const queryString = qs.stringify(payload);

    return apiCall({
      url: token_url,
      data: queryString,
      customHeaders: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      encryptRequest: false,
      decryptResponse: false,
      addDefaultHeaders: false,
    });
  },
  //=====================PUBLIC MODE ONLY!!=============================\\

  login({ data, store }) {
    return apiCall({
      data,
      url: "/Login/Login",
      decryptResponse: false,
      encryptRequest: true,
      store,
    });
  },
  async loginnew({ data, store }) {
    return await apiCall({
      data,
      baseURL: newmiddlewareEndpoint,
      url: "/Login/Login",
      decryptResponse: true,
      encryptRequest: true,
      store,
    });
  },

  getKeyAPIM({ data, store }) {
    return apiCall({
      data,
      baseURL: newmiddlewareEndpoint,
      url: "/Login/getKeyAPIM",
      decryptResponse: true,
      encryptRequest: true,
      store,
    })
      .then((response) => {
        store.dispatch("updateAccessToken", response.access_token);
      })
      .catch(() => {
        vuex
          .dispatch("logout")
          .then(() => {
            router.push({ name: "login" });
          })
          .then(() => {
            window.location.reload();
          });
      });
  },

  getNotificationLimitViewAndTotalNotifByUsername({ data, store }) {
    return apiCall({
      url: "/Notification/getNotificationLimitViewAndTotalNotifByUsername",
      data,
      store,
    });
  },

  getWorspaceInProgressByTaskMember(params) {
    return apiCall({
      url: "/Workspace/getWorspaceInProgressByTaskMember",
      ...params,
    });
  },
  Logout(params) {
    return apiCall({
      url: "/Login/Logout",
      ...params,
    });
  },

  getWorspaceDoneByTaskMember(params) {
    return apiCall({
      url: "/Workspace/getWorspaceDoneByTaskMember",
      ...params,
    });
  },

  getTaskMeetingByUsername(params) {
    return apiCall({
      url: "/TaskMeeting/getTaskMeetingByUsername",
      ...params,
    });
  },
  GetRecentlyAssignedTaskByUsername(params) {
    return apiCall({
      url: "/Tasks/GetRecentlyAssignedTaskByUsername",
      ...params,
    });
  },
  GetListDocumentAsApprovalByUsername(params) {
    return apiCall({
      url: "/TaskDocument/GetListDocumentAsApprovalByUsername",
      ...params,
    });
  },

  getWorspaceNotStartedByTaskMember(params) {
    return apiCall({
      url: "/Workspace/getWorspaceNotStartedByTaskMember",
      ...params,
    });
  },

  GetUserByUsername(params) {
    return apiCall({
      url: "/MUser/GetUserByUsername",
      ...params,
    });
  },

  getWorkspaceTypes({ data, store }) {
    return apiCall({
      method: "get",
      data,
      url: "/Workspace/WorkspaceType",
      decryptResponse: false,
      encryptRequest: false,
      store,
    });
  },

  getWorkspaceTypesNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetWorkspaceAndTaskbyWorkspaceTypeStartDate",
      ...params,
    });
  },

  getWorkspaceNameNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetEventbyEventSubtypeList",
      ...params,
    });
  },

  getWorkspaceTypeByUsername(params) {
    return apiCall({
      url: "/Workspace/WorkspaceTypeByUsername",
      ...params,
    });
  },

  getPreviewDocumentDate(params) {
    return apiCall({
      url: "/Event/previewTglEvent",
      ...params,
    });
  },

  createPredefinedWorkspaceActivityAndTask(params) {
    return apiCall({
      url: "/Workspace/createPredefinedWorkspaceActivityAndTask",
      ...params,
    });
  },

  createWorkspaceCustom(params) {
    return apiCall({
      url: "/Workspace/InsertWorkspace",
      ...params,
    });
  },

  getListWorkspaceInProgressByTaskMember(params) {
    return apiCall({
      url: "/Workspace/getListWorkspaceInProgressByTaskMember",
      ...params,
    });
  },
  getListWorspaceDoneByTaskMember(params) {
    return apiCall({
      url: "/Workspace/getListWorspaceDoneByTaskMember",
      ...params,
    });
  },
  getListWorkspaceNotStartedByTaskMember(params) {
    return apiCall({
      url: "/Workspace/getListWorkspaceNotStartedByTaskMember",
      ...params,
    });
  },
  deleteWorkspace(params) {
    return apiCall({
      url: "/Workspace/deleteWorkspace",
      ...params,
    });
  },
  updateWorkspace(params) {
    return apiCall({
      url: "/Workspace/updateWorkspace",
      ...params,
    });
  },
  getListActivityAndTaskByTaskMemberandIdWorkspace(params) {
    return apiCall({
      url: "/Workspace/getListActivityAndTaskByTaskMemberandIdWorkspace",
      ...params,
    });
  },
  getListWorkspaceByUserName(params) {
    return apiCall({
      url: "/Workspace/getListWorkspaceByUsername",
      ...params,
    });
  },
  getListTaskMemberDataByIdTask(params) {
    return apiCall({
      url: "/TaskMember/getListTaskMemberDataByIdTask",
      ...params,
    });
  },
  GetListDocumentDetailViewByUsernameAndIdTask(params) {
    return apiCall({
      url: "/TaskDocument/GetListDocumentDetailViewByUsernameAndIdTask",
      ...params,
    });
  },
  getListDocumentUtama(params) {
    return apiCall({
      url: "/TaskDocument/GetListDocumentDetailViewByUsernameAndIdTaskWithPagination",
      ...params,
    });
  },
  getListDocumentPendukung(params) {
    return apiCall({
      url: "/TaskDocumentSupport/getTaskDocumentSupportViewByTaskIdAndUsernameWithPagination",
      ...params,
    });
  },
  GetListFlowDetailbyTaskDocumentId(params) {
    return apiCall({
      url: "/MdocumentApprovalFlow/GetListFlowDetailbyTaskDocumentId",
      ...params,
    });
  },
  GetListAcessMemberDocumentSupportByIdDocument(params) {
    return apiCall({
      url: "/TaskDocumentSupportAccess/GetListAcessMemberDocumentSupportByIdDocument",
      ...params,
    });
  },
  GetListAcessMemberByIdDocument(params) {
    return apiCall({
      url: "/TaskDocumentAccess/GetListAcessMemberByIdDocument",
      ...params,
    });
  },
  ApproveDocument(params) {
    return apiCall({
      url: "/TaskDocument/ApproveDocument",
      ...params,
    });
  },
  ApproveDocumentSupport(params) {
    return apiCall({
      url: "/TaskDocumentSupport/ApproveDocumentSupport",
      ...params,
    });
  },
  getTasksByIdTask(params) {
    return apiCall({
      url: "/Tasks/getTasksByIdTask",
      ...params,
    });
  },
  getTaskMemberByIdTasks(params) {
    return apiCall({
      url: "/TaskMember/getListTaskMemberDataByIdTask",
      ...params,
    });
  },
  async checkOwner(params) {
    let res = await this.getTasksByIdTask({
      ...params,
    });
    return res.plainData[0].isOwner;
    // let searchIndex = res.plainData.findIndex(
    //   (listMember) => listMember.user.username == username
    // );
    // return res.plainData[searchIndex];
    // if (res.plainData[searchIndex].memberType == 1) {
    //   return true;
    // } else {
    //   return false;
    // }
  },
  checkNotif(params) {
    this.getNotificationLimitViewAndTotalNotifByUsername({
      ...params,
    }).then((response) => {
      params.store.dispatch("checkNotif", {
        totalNotification: response.plainData.totalNotification,
        notificationViewList: response.plainData.notificationViewList,
      });
    });
  },
  getTaskDocumentSupportViewByTaskId(params) {
    return apiCall({
      url: "/TaskDocumentSupport/getTaskDocumentSupportViewByTaskId",
      ...params,
    });
  },
  insertTaskMeeting(params) {
    return apiCall({
      url: "/TaskMeeting/insertTaskMeeting",
      ...params,
      encryptRequest: false,
      decryptResponse: false,
    });
  },
  updateTaskMeeting(params) {
    return apiCall({
      url: "/TaskMeeting/updateTaskMeeting",
      ...params,
      encryptRequest: false,
      decryptResponse: false,
    });
  },
  getTaskMeetingByIdTasks(params) {
    return apiCall({
      url: "/TaskMeeting/getTaskMeetingByIdTasks",
      ...params,
    });
  },
  getTaskDiscussionViewByIdTask(params) {
    return apiCall({
      url: "/TaskDiscussion/getTaskDiscussionViewByIdTask",
      ...params,
    });
  },
  insertTaskDiscussion(params) {
    return apiCall({
      url: "/TaskDiscussion/insertTaskDiscussion",
      ...params,
    });
  },
  startTasks(params) {
    return apiCall({
      url: "/Tasks/startTasks",
      ...params,
    });
  },
  closingTasks(params) {
    return apiCall({
      url: "/Tasks/closingTasks",
      ...params,
    });
  },
  UpdateActivity(params) {
    return apiCall({
      url: "/Activity/UpdateActivity",
      ...params,
    });
  },
  deleteActivity(params) {
    return apiCall({
      url: "/Activity/deleteActivity",
      ...params,
    });
  },
  updateTasks(params) {
    return apiCall({
      url: "/Tasks/updateTasks",
      ...params,
    });
  },
  deleteTasks(params) {
    return apiCall({
      url: "/Tasks/deleteTasks",
      ...params,
    });
  },
  SearchUserByname(params) {
    return apiCall({
      url: "/MUser/SearchUserAndGrupByName",
      ...params,
    });
  },
  deleteTaskMember(params) {
    return apiCall({
      url: "/TaskMember/deleteTaskMember",
      ...params,
    });
  },
  updateTaskMember(params) {
    return apiCall({
      url: "/TaskMember/updateTaskMember",
      ...params,
    });
  },
  insertTaskMember(params) {
    return apiCall({
      url: "/TaskMember/insertTaskMember",
      ...params,
    });
  },
  MSatkerPembuat(params) {
    return apiCall({
      url: "/MSatkerPembuat",
      ...params,
    });
  },
  getMTaskTypeByActivityType(params) {
    return apiCall({
      url: "/MTaskType/GetMTaskTypeByActivityType",
      ...params,
    });
  },
  MProgramStrategis(params) {
    return apiCall({
      url: "/MProgramStrategis",
      ...params,
    });
  },
  cekSSO(params) {
    return apiCall({
      withCredentials: true,
      url: "/MProgramStrategis",
      ...params,
    });
  },
  getMKomiteList(params) {
    return apiCall({
      url: "/MKomite/getListKomite",
      ...params,
    });
  },
  getMAdgList(params) {
    return apiCall({
      url: "/MAdg/getListAdg",
      ...params,
    });
  },
  getListWeekMonthYear(params) {
    return apiCall({
      url: "/Periode/getListWeekMonthYear",
      ...params,
    });
  },
  getMDestinationStatement(params) {
    return apiCall({
      url: "/MDestinationStatement/getListDestinationStatement",
      ...params,
    });
  },
  getListPegawaiByIdRole(params) {
    return apiCall({
      url: "/UserRole/getListPegawaiByIdRole",
      ...params,
    });
  },
  getListPegawaiByKomite(params) {
    return apiCall({
      url: "/MappingKomitePegawai/getListPegawaiByKomite",
      ...params,
    });
  },
  MUserListPimpinanSatkerbySatker(params) {
    return apiCall({
      url: "/MUser/ListPimpinanSatkerbySatker",
      ...params,
    });
  },
  GetOrganizationNameByUsername(params) {
    return apiCall({
      url: `/MUser/GetOrganizationNameByUsername`,
      ...params,
    });
  },
  MEvent(params) {
    return apiCall({
      url: "/MEvent",
      ...params,
    });
  },
  insertTaskDocumentSupport(params) {
    return apiCall({
      url: "/TaskDocumentSupport/insertTaskDocumentSupport",
      ...params,
      encryptRequest: false,
      decryptResponse: false,
      progressBar: true,
      customHeaders: {
        "Content-Type": "multipart/form-data",
        "X-XSRF-TOKEN": params.additional.tokenCookie,
      },
    });
  },
  insertTaskDocumentSupportApprove(params) {
    return apiCall({
      url: "/TaskDocumentSupport/insertTaskDocumentSupport",
      ...params,
      encryptRequest: false,
      decryptResponse: false,
      customHeaders: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  insertTaskDocumentByUpload(params) {
    return apiCall({
      url: "/TaskDocument/insertTaskDocumentByUpload",
      ...params,
      customHeaders: {
        "X-XSRF-TOKEN": params.additional.tokenCookie,
      },
    });
  },
  deleteTaskMeeting(params) {
    return apiCall({
      url: "/TaskMeeting/deleteTaskMeeting",
      ...params,
    });
  },
  GetListApprovalDocumentDetailViewsByDocumentId(params) {
    return apiCall({
      url: "/TaskDocument/GetListApprovalDocumentDetailViewsByDocumentId",
      ...params,
    });
  },
  GetListTaskDocumentFinalInWorkspace(params) {
    return apiCall({
      url: "/TaskDocument/GetListTaskDocumentFinalInWorkspace",
      ...params,
    });
  },
  getTaskMeetingByIdMeeting(params) {
    return apiCall({
      url: "/TaskMeeting/getTaskMeetingByIdMeeting",
      ...params,
    });
  },
  GetTaskDocumentByIdDocument(params) {
    return apiCall({
      url: "/TaskDocument/GetTaskDocumentByIdDocument",
      ...params,
    });
  },
  getTaskDocumentSupportViewByDocumentId(params) {
    return apiCall({
      url: "/TaskDocumentSupport/getTaskDocumentSupportViewByDocumentId",
      ...params,
    });
  },
  MDocumentType(params) {
    return apiCall({
      url: "/MDocumentType",
      ...params,
    });
  },
  GetDocumentTypeForApproval(params) {
    return apiCall({
      url: "/DocumentType/GetDocumentTypeForApproval",
      ...params,
    });
  },
  GetAllDocumentType(params) {
    return apiCall({
      url: "/DocumentType/GetAllDocumentType",
      ...params,
    });
  },
  uploadFinalTaskDocument(params) {
    return apiCall({
      url: "/TaskDocument/uploadFinalTaskDocument",
      ...params,
      decryptResponse: false,
      encryptRequest: false,
      progressBar: true,
      customHeaders: {
        "Content-Type": "multipart/form-data",
        "X-XSRF-TOKEN": params.additional.tokenCookie,
      },
    });
  },
  insertTaskDocumentSupportByUpload(params) {
    return apiCall({
      url: "/TaskDocumentSupport/insertTaskDocumentSupportByUpload",
      ...params,
      decryptResponse: false,
      encryptRequest: false,
      customHeaders: {
        "Content-Type": "multipart/form-data",
        "X-XSRF-TOKEN": params.additional.tokenCookie,
      },
    });
  },
  DownloadDocument(params) {
    return apiCall({
      url: "/TaskDocumentSupport/DownloadDocument",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  DownloadDocumentUtama(params) {
    return apiCall({
      method: "get",
      url: "/TaskDocument/DownloadDocument/" + params.data.id,
      decryptResponse: false,
      encryptRequest: false,
      responseType: "blob",
      ...params,
    });
  },
  DownloadDocumentById(params) {
    return apiCall({
      url: "/TaskDocument/DownloadDocumentById",
      decryptResponse: false,
      // encryptRequest: false,
      responseType: "blob",
      ...params,
    });
  },

  PreviewDocument(params) {
    return apiCall({
      url: "/TaskDocument/PreviewDocument",
      decryptResponse: false,
      // encryptRequest: false,
      ...params,
    });
  },
  PreviewDocumentPendukung(params) {
    return apiCall({
      url: "/TaskDocumentSupport/previewDocument",
      decryptResponse: false,
      //encryptRequest: false,
      ...params,
    });
  },
  GetMdocumentApprovalByIdMdocumentType(params) {
    return apiCall({
      method: "get",
      url:
        "/MdocumentApproval/GetMdocumentApprovalByIdMdocumentType/" +
        params.data.id,
      decryptResponse: false,
      encryptRequest: false,
      ...params,
    });
  },
  getMemberMeetingByIdTaskMeeting(params) {
    return apiCall({
      url: "/MemberMeeting/getMemberMeetingByIdTaskMeeting",
      ...params,
    });
  },
  insertTaskDocumentSupportGoldenCopy(params) {
    return apiCall({
      url: "/TaskDocumentSupportGoldenCopy/insertTaskDocumentSupportGoldenCopy",
      ...params,
      decryptResponse: false,
      encryptRequest: false,
    });
  },
  MeetingPlatform(params) {
    return apiCall({
      url: "/MeetingPlatform",
      ...params,
    });
  },
  GetListFlowDetailSupportbyTaskDocumentId(params) {
    return apiCall({
      url: "/MDocumentSupportApprovalFlow/GetListFlowDetailSupportByTaskDocumentId",
      ...params,
    });
  },
  GetDocumentSupportTypeForApproval(params) {
    return apiCall({
      url: "/DocumentSupportType/GetDocumentSupportTypeForApproval",
      ...params,
    });
  },
  DeleteDocument(params) {
    return apiCall({
      url: "/TaskDocument/DeleteDocument",
      ...params,
    });
  },
  deleteTaskDocumentSupportById(params) {
    return apiCall({
      url: "/TaskDocumentSupport/deleteTaskDocumentSupportById",
      ...params,
    });
  },
  deleteTaskDocumentSupportGoldenCopyById(params) {
    return apiCall({
      url: "/TaskDocumentSupportGoldenCopy/deleteTaskDocumentSupportGoldenCopyById",
      ...params,
    });
  },
  updateListTaskDocumentSupportAccess(params) {
    return apiCall({
      url: "/TaskDocumentSupportAccess/updateListTaskDocumentSupportAccess",
      ...params,
      decryptResponse: false,
      encryptRequest: false,
    });
  },
  updateListTaskDocumentAccess(params) {
    return apiCall({
      url: "/TaskDocumentAccess/updateListTaskDocumentAccess",
      ...params,
      decryptResponse: false,
      encryptRequest: false,
    });
  },
  getTaskDocumentSupportViewByTaskIdAndUsername(params) {
    return apiCall({
      url: "/TaskDocumentSupport/getTaskDocumentSupportViewByTaskIdAndUsername",
      ...params,
    });
  },
  sektor(params) {
    return apiCall({
      url: "/Sektor",
      ...params,
    });
  },
  periode(params) {
    return apiCall({
      url: "/Periode",
      ...params,
    });
  },
  GetChartpack(params) {
    return apiCall({
      url: "/Chartpack/GetChartpack",
      ...params,
    });
  },
  SearchChartpack(params) {
    return apiCall({
      url: "/Chartpack/SearchChartpack",
      ...params,
    });
  },
  PreviewDocumentChartPack(params) {
    return apiCall({
      url: "/Chartpack/PreviewDocumentChartPack",
      decryptResponse: false,
      ...params,
    });
  },
  DownloadChartpack(params) {
    return apiCall({
      url: "/Chartpack/DownloadChartpack",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  GetChartpackDetailByid(params) {
    return apiCall({
      url: "/Chartpack/GetChartpackDetailByid",
      ...params,
    });
  },
  getDashboardTaskList(params) {
    return apiCall({
      url: "/Tasks/GetTasksDashboardList",
      ...params,
    });
  },
  // untuk counter task
  getTaskStatusByUsername(params) {
    return apiCall({
      url: "/Tasks/GetTasksDashboardSts",
      ...params,
    });
  },
  // untuk counter workspace
  getWorkspaceStatusByUsername(params) {
    return apiCall({
      url: "/Workspace/GetWorkspaceStatusByUsername",
      ...params,
    });
  },
  // untuk filter dashboard
  getFilterDashboard(params) {
    return apiCall({
      url: "/Dashboard/GetFilterDashboard",
      ...params,
    });
  },
  // untuk filter dokument
  getFilterDocument(params) {
    return apiCall({
      url: "/Dashboard/GetFilterAndSortTaskDocument",
      ...params,
    });
  },
  // untuk list wpc persetujuan
  getListDashboardWorkspaceApproval(params) {
    return apiCall({
      url: "/Workspace/getListDashboardWorkspaceApproval",
      ...params,
    });
  },
  // untuk counter wpc persetujuan
  getWorkspaceStatusByUsernameApproval(params) {
    return apiCall({
      url: "/Workspace/getWorkspaceStatusByUsernameApproval",
      ...params,
    });
  },
  // untuk list task persetujuan
  getListDashboardTaskApproval(params) {
    return apiCall({
      url: "/Tasks/GetTasksDashboardListApproval",
      ...params,
    });
  },
  // untuk counter task persetujuan
  getTaskStatusByUsernameApproval(params) {
    return apiCall({
      url: "/Tasks/getTaskStatusByUsernameApproval",
      ...params,
    });
  },
  // untuk list wpc pengajuan
  getListDashboardWorkspaceSubmission(params) {
    return apiCall({
      url: "/Workspace/getListDashboardWorkspaceSubmission",
      ...params,
    });
  },
  // untuk counter wpc pengajuan
  getWorkspaceStatusByUsernameSubmission(params) {
    return apiCall({
      url: "/Workspace/getWorkspaceStatusByUsernameSubmission",
      ...params,
    });
  },
  // untuk update
  getWorkspaceById(params) {
    return apiCall({
      url: "/Workspace/getWorkspaceById",
      ...params,
    });
  },
  getTaskAsesmentById(params) {
    return apiCall({
      url: "/Tasks/getTasksAsesmentById",
      ...params,
    });
  },
  getTaskKomiteById(params) {
    return apiCall({
      url: "/Tasks/getTasksKomiteById",
      ...params,
    });
  },
  getTaskRDGById(params) {
    return apiCall({
      url: "/Tasks/getTasksRDGById",
      ...params,
    });
  },
  updateTaskAsesmen(params) {
    return apiCall({
      url: "/Tasks/updateTasksAsesmen",
      ...params,
    });
  },
  updateTaskKomite(params) {
    return apiCall({
      url: "/Tasks/updateTasksKomite",
      ...params,
    });
  },
  updateTaskRDG(params) {
    return apiCall({
      url: "/Tasks/updateTasksRDG",
      ...params,
    });
  },
  postTaskAsesmen(params) {
    return apiCall({
      url: "/Tasks/insertTasksAsesmen",
      ...params,
    });
  },
  postTaskKomite(params) {
    return apiCall({
      url: "/Tasks/insertTasksKomite",
      ...params,
    });
  },
  postTaskRDG(params) {
    return apiCall({
      url: "/Tasks/insertTasksRDG",
      ...params,
    });
  },
  getFilterMeeting(params) {
    return apiCall({
      url: "/MTaskType/GetTaskTypeByWorkspaceLevel",
      ...params,
    });
  },
  searchMeeting(params) {
    //sprint 3 2023
    return apiCall({
      url: "/TaskMeeting/GetTaskMeetingUsingMemberMeetingByUsernameAndWorkspaceLevel",
      ...params,
    });
  },
  getListAssignmentByTipePenugasanAndAssignmentMemberNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetListAssignmentbyTipePenugasanAndAssignmentMember",
      ...params,
    });
  },
  getListAssignmentByTipePenugasanAndAssignmentMember(params) {
    return apiCall({
      url: "/Assignment/GetListAssignmentbyTipePenugasanAndAssignmentMember",
      ...params,
    });
  },
  getListAssignmentbyTipeArahanAndAssignmentMemberNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetListAssignmentbyTipeArahanAndAssignmentMember",
      ...params,
    });
  },
  getListAssignmentbyTipeArahanAndAssignmentMember(params) {
    return apiCall({
      url: "/Assignment/GetListAssignmentbyTipeArahanAndAssignmentMember",
      ...params,
    });
  },
  // untuk list task pengajuan
  getListDashboardTaskSubmission(params) {
    return apiCall({
      url: "/Tasks/GetListDashboardTaskSubmission",
      ...params,
    });
  },
  // untuk counter task pengajuan
  getTaskStatusByUsernameSubmission(params) {
    return apiCall({
      url: "/Tasks/getTaskStatusByUsernameSubmission",
      ...params,
    });
  },
  // untuk approval wpc
  workspaceApproval(params) {
    return apiCall({
      url: "/Workspace/workspaceApproval",
      ...params,
    });
  },
  // untuk approval task
  tasksApproval(params) {
    return apiCall({
      url: "/Tasks/taskApproval",
      ...params,
    });
  },
  // untuk approval task 2
  taskSubmission(params) {
    return apiCall({
      url: "/Tasks/taskSubmission",
      ...params,
    });
  },
  // untuk counter dokument materi
  getTaskDocumentCounterByUsername(params) {
    return apiCall({
      url: "/TaskDocument/GetTaskDocumentCounterByUsername",
      ...params,
    });
  },
  // untuk counter dokument hasil
  getTaskDocumentSupportCounterByUsername(params) {
    return apiCall({
      url: "/TaskDocumentSupport/GetTaskDocumentSupportCounterByUsername",
      ...params,
    });
  },
  getRefreshToken(params) {
    return apiCall({
      url: "/AntiForgery/getCacheToken",
      ...params,
    });
  },
  getListWorkspaceByStatusAndLevel(params) {
    return apiCall({
      url: "/Workspace/GetListWorkspaceByStatusAndWorkspaceLevelAndUsername",
      ...params,
    });
  },
  // untuk list dokument materi
  getListDocumentByUsername(params) {
    return apiCall({
      url: "/TaskDocument/GetListDocumentDetailViewByUsername",
      ...params,
    });
  },
  // untuk list dokument hasil
  getListDocumentSupportByUsername(params) {
    return apiCall({
      url: "/TaskDocumentSupport/GetTaskDocumentSupportDetailViewByUsername",
      ...params,
    });
  },
  // untuk counter assignment penugasan
  getListCounterAssignmentbyTipePenugasan(params) {
    return apiCall({
      url: "/Assignment/GetListCounterAssignmentbyTipePenugasanbyAssignmentMember",
      ...params,
    });
  },
  getListCounterAssignmentbyTipePenugasanNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetListCounterAssignmentbyTipePenugasanbyAssignmentMember",
      ...params,
    });
  },
  // untuk counter assignment arahan
  getListCounterAssignmentbyTipeArahan(params) {
    return apiCall({
      url: "/Assignment/GetListCounterAssignmentbyTipeArahanbyAssignmentMember",
      ...params,
    });
  },
  getListCounterAssignmentbyTipeArahanNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetListCounterAssignmentbyTipeArahanbyAssignmentMember",
      ...params,
    });
  },
  getListActivityType(params) {
    return apiCall({
      url: "/MActivityType/GetActivityTypeByWorkspaceType",
      ...params,
    });
  },
  insertActivity(params) {
    return apiCall({
      url: "/Activity/insertActivity",
      ...params,
    });
  },
  GetVisualSignByUsername(params) {
    return apiCall({
      url: "/MUser/GetVisualSignByUsername",
      ...params,
    });
  },
  updateVisualSignByUsername(params) {
    return apiCall({
      url: "/MUser/updateVisualSignByUsername",
      ...params,
      decryptResponse: true,
      encryptRequest: false,
      customHeaders: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  writeLog(params) {
    return apiCall({
      url: "/Log/LogApps",
      ...params,
    });
  },
  getListWorkspaceInProgressByUsername(params) {
    //sprint 3 2023
    return apiCall({
      url: "/Workspace/getListWorkspaceInProgressByUsername",
      ...params,
    });
  },
  getTaskByWorkspaceAndUsername(params) {
    //sprint 3 2023
    return apiCall({
      url: "/Tasks/GetTaskByWorkspaceAndUsername",
      ...params,
    });
  },
  insertSendToOtherWorkspace(params) {
    //sprint 3 2023
    return apiCall({
      url: "/TaskDocumentSupportGoldenCopy/insertSendTaskDocumentSupportGoldenCopy",
      ...params,
    });
  },
  getAssignmentType(params) {
    return apiCall({
      url: "/Assignment/GetAssignmentType",
      ...params,
    });
  },
  getAssignmentReminderPeriode(params) {
    return apiCall({
      url: "/Assignment/GetMAssignmentReminderPeriod",
      ...params,
    });
  },
  getWorkspaceAndTaskbyWorkspaceTypeAndTaskStartDate(params) {
    return apiCall({
      url: "/Workspace/GetWorkspaceAndTaskbyWorkspaceTypeAndTaskStartDate",
      ...params,
    });
  },
  getTipePenugasanByAssignmentType(params) {
    return apiCall({
      url: "/Assignment/GetTipePenugasanByAssignmentType",
      ...params,
    });
  },
  getUserMGroupbySatkerId(params) {
    return apiCall({
      url: "/MUser/GetUserMGroupbySatkerId",
      ...params,
    });
  },
  insertAssignment(params) {
    return apiCall({
      url: "/Assignment/InsertAssignment",
      ...params,
    });
  },
  insertAssignmentNew(params) {
    return apiCall({
      url: "/AssignmentNew/InsertAssignment",
      ...params,
    });
  },
  getListTaskMemberTypeByIdTask(params) {
    //sprint 3 2023
    return apiCall({
      url: "/TaskMember/getListTaskMemberTypeByIdTask",
      ...params,
    });
  },
  CheckRoleMenuByUserId(params) {
    return apiCall({
      url: "/RoleMenu/CheckRoleMenuByUserId",
      ...params,
    });
  },
  getListFlowApprovalAssignment(params) {
    return apiCall({
      url: "/MAssignmentApprovalFlow/GetListFlowApprovalByIdAssignment",
      ...params,
    });
  },
  getListDiscussionAssignmentNew(params) {
    return apiCall({
      url: "/AssignmentDiscussionNew/GetAssignmentDiscussionByIdAssignment",
      ...params,
    });
  },
  getListDiscussionAssignment(params) {
    return apiCall({
      url: "/AssignmentDiscussion/GetAssignmentDiscussionByIdAssignment",
      ...params,
    });
  },
  getAssignmentDetailNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetDetailAssignmentById",
      ...params,
    });
  },
  getAssignmentDetail(params) {
    return apiCall({
      url: "/Assignment/GetDetailAssignmentById",
      ...params,
    });
  },
  insertDiscussionAssignmentNew(params) {
    return apiCall({
      url: "/AssignmentDiscussionNew/InsertDiscussion",
      ...params,
    });
  },
  insertDiscussionAssignment(params) {
    return apiCall({
      url: "/AssignmentDiscussion/InsertDiscussion",
      ...params,
    });
  },
  approveDiscussionAssignment(params) {
    return apiCall({
      url: "/Assignment/AssignmentApproval",
      ...params,
    });
  },
  getListAssignmentbyTipePenugasanNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetListAssignmentbyTipePenugasan",
      ...params,
    });
  },
  getListAssignmentbyTipePenugasan(params) {
    return apiCall({
      url: "/Assignment/GetListAssignmentbyTipePenugasan",
      ...params,
    });
  },
  getListAssignmentbyTipeArahanNew(params) {
    return apiCall({
      url: "/AssignmentNew/GetListAssignmentbyTipeArahan",
      ...params,
    });
  },
  getListAssignmentbyTipeArahan(params) {
    return apiCall({
      url: "/Assignment/GetListAssignmentbyTipeArahan",
      ...params,
    });
  },
  getCounterAssignmentPenugasan(params) {
    return apiCall({
      url: "/Assignment/GetCounterAssignmentPenugasan",
      ...params,
    });
  },
  getCounterAssignmentArahan(params) {
    return apiCall({
      url: "/Assignment/GetCounterAssignmentArahan",
      ...params,
    });
  },
  downloadFileAssignment(params) {
    return apiCall({
      url: "/AssignmentDiscussion/DownloadDocumentbyId",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  downloadFileAssignmentNew(params) {
    return apiCall({
      url: "/AssignmentDiscussionNew/DownloadDocumentbyId",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  uploadFileAssignment(params) {
    return apiCall({
      url: "/AssignmentDiscussion/insertAssignmentDiscussionByUpload",
      encryptRequest: false,
      // decryptResponse: false,
      progressBar: true,
      customHeaders: {
        "Content-Type": "multipart/form-data",
        "X-XSRF-TOKEN": params.additional.tokenCookie,
      },
      ...params,
    });
  },
  uploadFileAssignmentNew(params) {
    return apiCall({
      url: "/AssignmentDiscussionNew/insertAssignmentDiscussionByUpload",
      encryptRequest: false,
      // decryptResponse: false,
      progressBar: true,
      customHeaders: {
        "Content-Type": "multipart/form-data",
        "X-XSRF-TOKEN": params.additional.tokenCookie,
      },
      ...params,
    });
  },
  getListAssignmentMemberByIdAssignment(params) {
    return apiCall({
      url: "/AssignmentMember/GetListAssignmentMemberByIdAssignment",
      ...params,
    });
  },
  editAssignmentMemberByUserName(params) {
    return apiCall({
      url: "/AssignmentMember/EditAssignmentMemberByUserName",
      ...params,
    });
  },
  deleteAssignmentMemberByUserName(params) {
    return apiCall({
      url: "/AssignmentMember/DeleteAssignmentMemberByUserName",
      ...params,
    });
  },
  insertListAssignmentMember(params) {
    return apiCall({
      url: "/AssignmentMember/InsertListAssignmentMember",
      ...params,
    });
  },
  editAssignmentByIdAssignment(params) {
    return apiCall({
      url: "/Assignment/EditAssignmentByIdAssignment",
      ...params,
    });
  },
  editAssignmentByIdAssignmentNew(params) {
    return apiCall({
      url: "/AssignmentNew/EditAssignmentByIdAssignment",
      ...params,
    });
  },
  deleteAssignment(params) {
    return apiCall({
      url: "/Assignment/DeleteAssignment",
      ...params,
    });
  },
  newlogin(params) {
    return apiCall({
      baseURL: newmiddlewareEndpoint,
      url: "/Login/Login",
      ...params,
    });
  },
  MBusinessProcess(params) {
    return apiCall({
      url: "/MBusinessProcess",
      ...params,
    });
  },
  MClassification(params) {
    return apiCall({
      url: "/MClassification",
      ...params,
    });
  },
  CreateDocumentSupport(params) {
    return apiCall({
      url: "/TaskDocumentSupport/insertTaskDocumentSupportByTemplate",
      ...params,
      decryptResponse: true,
      encryptRequest: true,
    });
  },
  GetMdocumentSupportApprovalByIdMdocumentType(params) {
    return apiCall({
      url: "/MdocumentSupportApproval/GetMdocumentSupportApprovalByIdMdocumentType",
      ...params,
      decryptResponse: true,
      encryptRequest: true,
    });
  },
  getListUsernameAndRole(params) {
    return apiCall({
      url: "/UserRole/getListUsernameAndRole",
      ...params,
    });
  },
  getListAllRole(params) {
    return apiCall({
      url: "/UserRole/getListAllRole",
      ...params,
    });
  },
  updateUserRoleByUsername(params) {
    return apiCall({
      url: "/UserRole/updateUserRoleByUsername",
      ...params,
    });
  },
  getListWorkspaceCustom(params) {
    return apiCall({
      url: "/Workspace/getListWorkspaceCustom",
      ...params,
    });
  },
  GetTaskDocumentSupportDetail(params) {
    return apiCall({
      url: "/TaskDocumentSupport/GetTaskDocumentSupportDetail",
      ...params,
    });
  },
  GetTaskDocumentDetail(params) {
    return apiCall({
      url: "/TaskDocument/GetTaskDocumentDetail",
      ...params,
    });
  },
  getDataSuptechExecutiveSummary(params) {
    return apiCall({
      url: "/Suptech/getDataSuptechExecutiveSummary",
      decryptResponse: true,
      encryptRequest: true,
      ...params,
    });
  },
  getDataSuptechLiquidity(params) {
    return apiCall({
      url: "/Suptech/getDataSuptechLiquidity",
      decryptResponse: true,
      encryptRequest: true,
      ...params,
    });
  },
  getDataCredit(params) {
    return apiCall({
      url: "/Suptech/getDataCredit",
      decryptResponse: true,
      encryptRequest: true,
      ...params,
    });
  },
  getListPimpinanSatkerAndProjectLeader(params) {
    return apiCall({
      url: "/MUser/getListPimpinanSatkerByIdWorkspaceCustom",
      ...params,
    });
  },
  updatePimpinanSatkerByIdWorkspaceCustomandUsername(params) {
    return apiCall({
      url: "/Workspace/updatePimpinanSatkerByIdWorkspaceCustomandUsername",
      ...params,
    });
  },
  getListWorkspacePredefine(params) {
    return apiCall({
      url: "/Workspace/getListWorkspacePredefined",
      ...params,
    });
  },
  getTaskDocumentSupportEditByIdDocument(params) {
    return apiCall({
      url: "/TaskDocumentSupport/GetTaskDocumentSupportEditByIdDocument",
      ...params,
    });
  },
  updateMetadataDokumen(params) {
    return apiCall({
      url: "/TaskDocumentSupport/updateMetadataDokumen",
      ...params,
      decryptResponse: true,
      encryptRequest: true,
    });
  },
  GetDocumentSupportTypeByIdMethod(params) {
    return apiCall({
      url: "/DocumentSupportType/GetDocumentSupportTypeByIdMethod",
      ...params,
    });
  },
  UpdateTaskDocumentSupportProgress(params) {
    return apiCall({
      url: "/TaskDocumentSupport/UpdateTaskDocumentSupportProgress",
      ...params,
      decryptResponse: true,
      encryptRequest: true,
    });
  },
  getDocumentSupportMethod(params) {
    return apiCall({
      url: "/MDocumentSupportMethod",
      ...params,
      decryptResponse: true,
      encryptRequest: true,
    });
  },
  downloadDocumentMateriExcel(params) {
    return apiCall({
      url: "/TaskDocumentSupport/downloadDokumenByFormat",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  downloadDocumentHasilExcel(params) {
    return apiCall({
      url: "/TaskDocument/DownloadDokumenExcel",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  getDetailListWorkspacePredefined(params) {
    return apiCall({
      url: "/Workspace/getDetailListWorkspacePredefined",
      ...params,
    });
  },
  updateTaskTemplate(params) {
    return apiCall({
      url: "/TaskTemplate/updateTaskTemplate",
      ...params,
    });
  },
  previewDocumentSupport(params) {
    return apiCall({
      url: "/TaskDocumentSupport/previewDocumentweb",
      ...params,
      decryptResponse: false,
    });
  },
  previewDocumentUtama(params) {
    return apiCall({
      url: "/TaskDocument/previewDocumentweb",
      ...params,
      decryptResponse: false,
    });
  },
  getDataReportPoltech(params) {
    return apiCall({
      url: "/Poltech/getDataReportPoltech",
      ...params,
    });
  },
  getDataReportSuptech(params) {
    return apiCall({
      url: "/Suptech/getDataReportSuptech",
      ...params,
    });
  },
  getDataSectorSuptech(params) {
    return apiCall({
      url: "/Suptech/getDataSectorSuptech",
      ...params,
    });
  },
  getDataSectorPoltech(params) {
    return apiCall({
      url: "/Poltech/getDataSectorPoltech",
      ...params,
    });
  },
  getListTemplate(params) {
    return apiCall({
      url: "/Template/GetListTaskDocumentSupportTemplate",
      ...params,
    });
  },
  downloadTemplate(params) {
    return apiCall({
      url: "/TaskDocumentSupport/downloadDocumentSupportByTemplate",
      ...params,
      decryptResponse: false,
      responseType: "blob",
    });
  },
  GetDetailDocumentIkuIck(params) {
    return apiCall({
      url: "/Template/getTemplateDocumentIKUICKByIdTemplate",
      ...params,
    });
  },
  getPenyusunSection(params) {
    return apiCall({
      url: "/MGroup/GetMGroup",
      ...params,
    });
  },
  updateTemplateMetadata(params) {
    return apiCall({
      url: "/Template/updateTemplateDocumentIKUICK",
      ...params,
    });
  },
};

export default client;
