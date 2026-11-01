import axios from "axios";
import { encrypt, decrypt } from "@/library/CryptoHelper";
import vuex from "@/store/index.js";
import store from "@/store";
import { useToast } from "vue-toastification";
import router from "@/router";
import { useMsal } from "../composables/useMsal";
import { addApiVersion, redirectToBisa } from "@v2/helpers/utils";

const toast = useToast();
const current_mode = process.env.VUE_APP_CURRENT_MODE;

async function apiCall({
  method = "post",
  url,
  data,
  decryptResponse = true,
  encryptRequest = true,
  addDefaultHeaders = true,
  customHeaders = {},
  responseType,
  onUploadProgress = () => undefined,
  onDownloadProgress = () => undefined,
  signal,
  isRetry = false,
}: any) {
  const finalPayload = encryptRequest ? await encrypt(data, store) : data;
  const isMfa = process.env.VUE_APP_MFA_STATUS === "true";
  const { getToken } = useMsal();
  let authHeaders = {};

  if (addDefaultHeaders) {
    if (isMfa) {
      // Ambil token Azure secara otomatis & silent
      const tokenAzure = await getToken();

      authHeaders = {
        "authorization-app": `${tokenAzure}`,
      };
    }
  }

  const drHeader = await addApiVersion(store.state.kane, "v2");
  const defaultHeaders = addDefaultHeaders
    ? {
        ...authHeaders,
        Authorization: `Bearer ${store.state.accessToken}`,
        ultimatewarrior: store.state.teriyaki,
        bubbareydudley: store.state.yakiniku,
        dr: drHeader,
        callafriend:
          "D9E13A0B160B4B7DA6205B3BAEGE9A4A09E21C27E95D753C278F3A62B64EE07F",
        "Referrer-Policy": "no-referrer",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'",
        Accept: "application/json",
        "Content-Type": "application/json",
      }
    : {};
  const finalUrl = url.startsWith("/") ? `${store.state.urlApim}${url}` : url;

  return axios({
    method,
    url: finalUrl,
    data: finalPayload,
    headers: { ...defaultHeaders, ...customHeaders },
    responseType: responseType,
    onUploadProgress: onUploadProgress,
    onDownloadProgress: onDownloadProgress,
    signal: signal,
    withCredentials: true,
  })
    .then((response) => {
      if (!response || !response.data || !decryptResponse) {
        return response;
      }

      const plainData = decrypt(response.data, store);
      return plainData;
    })
    .catch(async (err) => {
      if (err.response) {
        const status = err.response?.status ?? 400;
        if ([406].includes(status)) {
          vuex.dispatch("logout").then(() => {
            redirectToBisa();
          });
        } else if ([401].includes(status) && current_mode == "private") {
          if (isRetry) {
            redirectToBisa();
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
            redirectToBisa();
          }
        } else if ([403].includes(status)) {
          toast.warning("Anda tidak memiliki akses");
          router.push({ name: "v2.home" });
        }

        if (typeof err.response?.data === "string") {
          err.response.data = JSON.parse(err.response?.data) || {};
        }
      }
      return Promise.reject(err);
    });
}

const clientv2 = {
  async getListExample(params) {
    return await apiCall({
      url: "/Workspace/getListWorkspaceInProgressByUsername",
      store: store,
      ...params,
    });
  },
  async getListEventType(params) {
    return await apiCall({
      url: "/MEvent/getMEventType",
      store: store,
      ...params,
    });
  },
  async getEventSubTypeByEventTypeId(params) {
    return await apiCall({
      url: "/MEvent/getEventSubTypeByEventTypeId",
      ...params,
    });
  },
  async getEventSubTypeListByEventSubTypeId(params) {
    return await apiCall({
      url: "/MEvent/getEventSubTypeListByEventSubTypeId",
      ...params,
    });
  },
  async insertEvent(params) {
    return await apiCall({
      url: "/MEvent/InsertEvent",
      ...params,
    });
  },
  async getTaskMeetingByUsername(params) {
    return await apiCall({
      url: "/TaskMeeting/getTaskMeetingByUsername",
      store: store,
      ...params,
    });
  },
  async getTop3EventByUser(params) {
    return await apiCall({
      url: "/MEvent/getTop3EventByUser",
      ...params,
    });
  },
  async getEventDetailByIdEventEdit(params) {
    return await apiCall({
      url: "/MEvent/getEventDetailByIdEvent",
      ...params,
    });
  },
  async getEventMethod(params) {
    return await apiCall({
      url: "/MEvent/getMeetingMethod",
      ...params,
    });
  },
  async getMeetingPlatform(params) {
    return await apiCall({
      url: "/MeetingPlatform",
      ...params,
    });
  },
  async getListADG(params) {
    return await apiCall({
      url: "/MAdg/getListAdg",
      ...params,
    });
  },
  async getListADGDetail(params) {
    return await apiCall({
      url: "/MAdg/getListAdgDetail",
      ...params,
    });
  },
  async getListADGFormation(params) {
    return await apiCall({
      url: "/DashboardAdmin/getListFormasiADG",
      ...params,
    });
  },
  async getListMenu(params) {
    return await apiCall({
      url: "/RoleMenu/CheckNewRoleMenuByUserId",
      ...params,
    });
  },
  async SearchUserByname(params) {
    return await apiCall({
      url: "/MUser/SearchUserAndGrupByName",
      ...params,
    });
  },
  async SearchUserAndGroupAndEmailByName(params) {
    return await apiCall({
      url: "/MUser/SearchUserAndGroupAndEmailByName",
      ...params,
    });
  },
  async SearchSatker(params) {
    return await apiCall({
      url: "/DashboardAdmin/SearchSatker",
      ...params,
    });
  },
  async SearchGrade(params) {
    return await apiCall({
      url: "/DashboardAdmin/SearchGrade",
      ...params,
    });
  },
  async SearchJabatan(params) {
    return await apiCall({
      url: "/DashboardAdmin/SearchJabatan",
      ...params,
    });
  },
  async SearchRole(params) {
    return await apiCall({
      url: "/DashboardAdmin/SearchRole",
      ...params,
    });
  },
  async GetUserByUsername(params) {
    return await apiCall({
      url: "/MUser/GetUserByUsername",
      ...params,
    });
  },
  async checkRoleMrdgByUsername(params) {
    return await apiCall({
      url: "/RoleMenu/CheckRoleMRDG",
      ...params,
    });
  },
  async downloadLogFile(params) {
    return await apiCall({
      url: "/Calendar/downloadLogEvent",
      ...params,
    });
  },
  async SearchUserBynameNew(params) {
    return await apiCall({
      url: "/MUser/SearchUserAndGrupIdByName",
      ...params,
    });
  },
  async SearchUserAndGroupNew(params) {
    return await apiCall({
      url: "/MUser/SearchUserAndGroupNew",
      ...params,
    });
  },
  async SearchUserAndGroupMaterial(params) {
    return await apiCall({
      url: "/MUser/SearchUserAndGroupMaterial",
      ...params,
    });
  },
  async popUpUpdateEvent(params) {
    return await apiCall({
      url: "/Event/popUpUpdateEvent",
      ...params,
    });
  },
  async updateEvent(params) {
    return await apiCall({
      url: "/MEvent/updateEvent",
      ...params,
    });
  },
  async updateBPMember(params) {
    return await apiCall({
      url: "/DashboardAdmin/updateBPMember",
      ...params,
    });
  },
  async createBPMember(params) {
    return await apiCall({
      url: "/DashboardAdmin/insertBPMember",
      ...params,
    });
  },
  async downloadMeetingDocument(params) {
    return await apiCall({
      url: "/Event/DownloadMaterialById",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async viewMeetingDocument(params) {
    return await apiCall({
      url: "/Event/PreviewMaterial",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async viewFinalisasiDocument(params) {
    return await apiCall({
      url: "/BPDoc/ViewContentFinalisasi",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async getListSuperEventByRDGByUsername(params) {
    return await apiCall({
      url: "/Content/getListSuperEventByRDGByUsername",
      ...params,
    });
  },
  async getCounterByRDGType(params) {
    return await apiCall({
      url: "/Content/getCounterByRDGType",
      ...params,
    });
  },
  async getContentFilter(params) {
    return await apiCall({
      url: "/Content/getContentFilter",
      ...params,
    });
  },
  async Logout(params) {
    return await apiCall({
      url: "/Login/Logout",
      ...params,
    });
  },
  async CKEditorToken(params) {
    return await apiCall({
      url: "/CKEditor/GetTokenCkEditor",
      ...params,
    });
  },
  async CKBoxToken(params) {
    return await apiCall({
      url: "/CKEditor/GetTokenCkBox",
      ...params,
    });
  },
  async getListBPDocMemberByIdBPDoc(params) {
    return await apiCall({
      url: "/BPDoc/GetListBPDocMemberByIdBPDoc",
      ...params,
    });
  },
  async getListMBPDocMemberTemplateByIdMBPDocTemplate(params) {
    return await apiCall({
      url: "/BPDoc/getListMBPDocMemberTemplateByIdMBPDocTemplate",
      ...params,
    });
  },
  async addBPDocMemberByIdBPDoc(params) {
    return await apiCall({
      url: "/BPDoc/AddBPDocMemberByIdBPDoc",
      ...params,
    });
  },
  async addMBPDocMemberTemplateByIdMBPDocTemplate(params) {
    return await apiCall({
      url: "/BPDoc/addMBPDocMemberTemplateByIdMBPDocTemplate",
      ...params,
    });
  },
  async deleteListBPDocMemberByIdBPDocMember(params) {
    return await apiCall({
      url: "/BPDoc/DeleteListBPDocMemberByIdBPDocMember",
      ...params,
    });
  },
  async deleteListMBPDocMemberTemplateByIdMBPDocMemberTemplate(params) {
    return await apiCall({
      url: "/BPDoc/deleteListMBPDocMemberTemplateByIdMBPDocMemberTemplate",
      ...params,
    });
  },
  async getListEFormMemberByIdEForm(params) {
    return await apiCall({
      url: "/BPDoc/GetListEFormMemberByIdEForm",
      ...params,
    });
  },
  async updateListEFormMemberByIdEForm(params) {
    return await apiCall({
      url: "/BPDoc/UpdateListEFormMemberByIdEForm",
      ...params,
    });
  },
  async addEFormMemberByIdEForm(params) {
    return await apiCall({
      url: "/BPDoc/AddEFormMemberByIdEForm",
      ...params,
    });
  },
  async deleteEFormMemberByIdEForm(params) {
    return await apiCall({
      url: "/BPDoc/DeleteEFormMemberByIdEForm",
      ...params,
    });
  },
  async GetListMEFormMemberByIdMEForm(params) {
    return await apiCall({
      url: "/DashboardAdmin/GetListMEFormMemberByIdMEForm",
      ...params,
    });
  },
  async addMEformMemberTemplate(params) {
    return await apiCall({
      url: "/MEformMemberTemplate/addMEformMemberTemplate",
      ...params,
    });
  },
  async updateListMEFormMemberTemplateByIdMEForm(params) {
    return await apiCall({
      url: "/MEformMemberTemplate/updateListMEFormMemberTemplateByIdMEForm",
      ...params,
    });
  },
  async deleteListMEformMemberTemplateByIdMEFormTemplate(params) {
    return await apiCall({
      url: "/MEformMemberTemplate/deleteListMEFormMemberTemplateByIdMEFormMemberTemplate",
      ...params,
    });
  },
  async getFormDocument(params) {
    return await apiCall({
      url: "/EForm/GetEFormByBPDocAndUsername",
      ...params,
    });
  },
  async previewDocument(params) {
    return await apiCall({
      url: "/EForm/GetViewEFormByBPDocAndUsername",
      ...params,
    });
  },
  async getDocumentMetadata(params) {
    return await apiCall({
      url: "/BPDoc/getViewMetadataEForm",
      ...params,
    });
  },
  async SearchUserAndGrupIdByNameAndSector(params) {
    return await apiCall({
      url: "/MUser/SearchUserAndGrupIdByNameAndSector",
      ...params,
    });
  },
  async SearchUserAndGrupIdByNameAndSectorTemplate(params) {
    return await apiCall({
      url: "/Muser/SearchUserAndGrupIdByNameAndSectorTemplate",
      ...params,
    });
  },
  async GetViewEFormByBPDocAndUsername(params) {
    return await apiCall({
      url: "/EForm/GetViewEFormByBPDocAndUsername",
      ...params,
    });
  },
  async getTop10DocByUser(params) {
    return await apiCall({
      url: "/Event/getTop10DocByUser",
      ...params,
    });
  },
  /* GET LIST RDG TYPE CREATE RDG LAINNYA */
  async getMEventSubTypeList(params) {
    return await apiCall({
      url: "/Event/getMEventSubTypeList",
      ...params,
    });
  },
  /* GET LIST RDG CREATE RDG LAINNYA */
  async getEventSubTypeListByEventId(params) {
    return await apiCall({
      url: "/Event/getEventSubTypeListByEventId",
      ...params,
    });
  },
  /* GET LIST EVENT CREATE RDG LAINNYA */
  async getEventbySubTypeListId(params) {
    return await apiCall({
      url: "/Event/getEventbySubTypeListId",
      ...params,
    });
  },
  /* POST CREATE RDG LAINNYA */
  async addEventOthers(params) {
    return await apiCall({
      url: "/Event/insertEventOthers",
      ...params,
    });
  },
  /* DELETE MEETING RDG LAINNYA */
  async deleteEventById(params) {
    return await apiCall({
      url: "/Event/deleteEventById",
      ...params,
    });
  },
  /* GET LINK BUKU DIGITAL MATERIAL */
  async getLinkMaterial(params) {
    return await apiCall({
      url: "/Event/getLinkMaterial",
      ...params,
    });
  },
  async downloadAllDocument(params) {
    return await apiCall({
      url: "/Event/DownloadSelectedMaterialById",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async downloadDocumentResult(params) {
    return await apiCall({
      url: "/Event/DownloadHasilPembahasanById",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async viewDocumentResult(params) {
    return await apiCall({
      url: "/Event/PreviewHasilPembahasan",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async getContentFromStorage(params) {
    return await apiCall({
      url: "/CKEditor/GetDataContent",
      ...params,
    });
  },
  async downloadAllDocumentResult(params) {
    return await apiCall({
      url: "/Event/DownloadSelectedHasilPembahasanById",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async downloadDocumentApprove(params) {
    return await apiCall({
      url: "/BPDoc/DownloadBPDocumentFinal",
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async getDocConvertionPDFBeforeSend(params) {
    return await apiCall({
      url: "/BPDoc/GetDocConvertionPDFBeforeSend",
      store: store,
      decryptResponse: false,
      responseType: "blob",
      ...params,
    });
  },
  async getDropdownCreate(params) {
    return await apiCall({
      url: "/Event/getDropdownCreate",
      store: store,
      ...params,
    });
  },
  async publishEvent(params) {
    return await apiCall({
      url: "/MEvent/publishEvent",
      store: store,
      ...params,
    });
  },
  async cancelEvent(params) {
    return await apiCall({
      url: "/Event/cancelEvent",
      store: store,
      ...params,
    });
  },
};

export default clientv2;
