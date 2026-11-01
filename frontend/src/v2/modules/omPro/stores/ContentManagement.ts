/* eslint-disable */
import client from "@/v2/modules/omPro/library/Api";
import {
  TSelect,
  TResponseRDGBBulananDetail,
  TTOC,
  TRequestTOC,
  TTOCDoc,
  TTOCContent,
  TFormMappingSection,
  TDetailRDGItem,
} from "@/v2/modules/omPro/Type";

export default {
  namespaced: true,
  state: {
    sectorList: [] as TSelect[],
    sectorPninList: [] as TSelect[],
    formList: [] as TSelect[],
    sectionList: [] as TSelect[],
    bpList: [] as TSelect[],
    bpDocMapping: [] as TSelect[],
    bpDocSectionMapping: [],
    bpDocSubSectionMapping: [],
    RDGBBulananDetail: {} as TResponseRDGBBulananDetail,
    asesmenList: [] as TDetailRDGItem[],
    rekomendasiList: [] as TDetailRDGItem[],
    persetujuanList: [] as TDetailRDGItem[],
    othersData: {} as any,
    tableOfContent: {} as TTOC,
    formMapping: {} as TFormMappingSection,
    idBP: "",
    isAIU: false,
    reloadToc: 0,
  },
  mutations: {
    setSectorList(state: any, payload: TSelect[]) {
      state.sectorList = payload;
    },
    setSectorPninList(state: any, payload: TSelect[]) {
      state.sectorPninList = payload;
    },
    setFormList(state: any, payload: TSelect[]) {
      state.formList = payload;
    },
    setSectionList(state: any, payload: TSelect[]) {
      state.sectionList = payload;
    },
    setBpList(state: any, payload: TSelect[]) {
      state.bpList = payload;
    },
    setBpDocMappingList(state: any, payload: TSelect[]) {
      state.bpDocMapping = payload;
    },
    setBpDocSectionMappingList(state: any, payload: TSelect[]) {
      state.bpDocSectionMapping = payload;
    },
    setBpDocSubSectionMappingList(state: any, payload: TSelect[]) {
      state.bpDocSectionMapping = payload;
    },
    setRDGBBulananDetail(state: any, payload: TResponseRDGBBulananDetail) {
      state.RDGBBulananDetail = payload;
    },
    setAsesmenList(state: any, payload: TDetailRDGItem[]) {
      state.asesmenList = payload;
    },
    setRekomendasiList(state: any, payload: TDetailRDGItem[]) {
      state.rekomendasiList = payload;
    },
    setPersetujuanList(state: any, payload: TDetailRDGItem[]) {
      state.persetujuanList = payload;
    },
    setOthersData(state: any, payload: any) {
      state.othersData = payload;
    },
    setTableOfContent(state: any, payload: TTOC) {
      state.tableOfContent = payload;
    },
    setFormMapping(state: any, payload: TFormMappingSection) {
      state.formMapping = payload;
    },
    setIdBP(state: any, payload: string) {
      state.idBP = payload;
    },
    setIsAIU(state: any, newVal: boolean) {
      state.isAIU = newVal;
    },
    setReloadToc: (state: any, newVal: any) => {
      state.reloadToc = newVal;
    },
  },
  actions: {
    async getSectorList({ commit }) {
      return client({})
        .post("/EForm/GetSectorList", {})
        .then((response: any) => {
          commit("setSectorList", response.responseData.data);
          return new Promise((resolve) => {
            resolve(response.responseData.data);
          });
        });
    },
    async getSectorPNINList({ commit }) {
      return client({})
        .post("/EForm/GetSectorListPNIN", {})
        .then((response: any) => {
          commit("setSectorPninList", response.responseData.data);
          return new Promise((resolve) => {
            resolve(response.responseData.data);
          });
        });
    },
    async getFormList({ commit }, request: any) {
      return client({})
        .post("/EForm/GetBPDocList", request)
        .then((response: any) => {
          const data = response.responseData?.data ?? [];
          commit("setFormList", data);
          return new Promise((resolve) => resolve(data));
        });
    },
    async getSectionList({ commit }, request: any) {
      return client({})
        .post("/EForm/GetBPSectionListPNIN", request)
        .then((response: any) => {
          const data = response.responseData ?? [];
          commit("setSectionList", data);
          return new Promise((resolve) => resolve(data));
        });
    },
    async getBpList({ commit }, request: any) {
      return client({})
        .post("/EForm/GetBPList", request)
        .then((response: any) => {
          const data = response.responseData ?? [];
          commit("setBpList", data);
          return new Promise((resolve) => resolve(data));
        });
    },
    async getBpDocMappingList({ commit }, request: any) {
      return client({})
        .post("/EForm/GetBPDocListMapping", request)
        .then((response: any) => {
          const data = response.responseData ?? [];
          commit("setBpDocMappingList", data);
          return new Promise((resolve) => resolve(data));
        });
    },
    async getBpDocSectionMappingList({ commit }, request: any) {
      return client({})
        .post("/EForm/GetBPSectionList", request)
        .then((response: any) => {
          const data = response.responseData ?? [];
          commit("setBpDocSectionMappingList", data);
          return new Promise((resolve) => resolve(data));
        });
    },
    async getBpDocSubSectionMappingList({ commit }, request: any) {
      return client({})
        .post("/EForm/GetBPSubSectionList", request)
        .then((response: any) => {
          const data = response.responseData ?? [];
          commit("setBpDocSubSectionMappingList", data);
          return new Promise((resolve) => resolve(data));
        });
    },
    async getDataByEventIdAnalysisRDGM({ commit }, idEvent: string) {
      return client({})
        .post("/DashboardExec/GetDataByEventIdAnalysisRDGM", { idEvent })
        .then((response: any) => {
          commit("setRDGBBulananDetail", response.responseData);
          return response.responseData;
        });
    },

    async getDataByEventIdBPAssesmentRekomendasi({ commit }, idEvent: string) {
      return client({})
        .post("/DashboardExec/GetDataByEventIdBPAssesmentRekomendasi", { idEvent })
        .then((response: any) => {
          commit(
            "setAsesmenList",
            response.responseData.businessProcess[0].value
          );
          return response.responseData.businessProcess[0].value;
        });
    },

    async getDataByEventIdBPRekomendasi({ commit }, idEvent: string) {
      return client({})
        .post("/DashboardExec/GetDataByEventIdBPRekomendasi", { idEvent })
        .then((response: any) => {
          commit(
            "setRekomendasiList",
            response.responseData.businessProcess[0].value
          );
          return response.responseData.businessProcess[0].value;
        });
    },

    async getDataByEventIdBPPersetujuan({ commit }, idEvent: string) {
      return client({})
        .post("/DashboardExec/GetDataByEventIdBPPersetujuan", { idEvent })
        .then((response: any) => {
          commit(
            "setPersetujuanList",
            response.responseData.businessProcess[0].value
          );
          return response.responseData.businessProcess[0].value;
        });
    },

    async getDataByEventIdBPOthers({ commit }, idEvent: string) {
      return client({})
        .post("/DashboardExec/GetDataByEventIdBPOthers", { idEvent })
        .then((response: any) => {
          commit("setOthersData", response.responseData);
          return response.responseData;
        });
    },
    async getTableOfContent({ commit }, payload: TRequestTOC) {
      const request = {
        ...payload,
      };
      return await client({})
        .post(`/EForm/GetContentByUsernameIdEventAndIdBP`, request)
        .then((response: any) => {
          const { isAIUDoc, ...toc } = response.responseData;
          commit("setTableOfContent", toc);
          commit("setIsAIU", isAIUDoc);
          return new Promise((resolve) => {
            resolve(response.responseData);
          });
        });
    },
    async createAIUCustom({ commit }, payload: any) {
      return client({}).post(`/EForm/InsertEFormReference`, payload);
    },
    async createPNINCustom({ rootState }, payload: any) {
      payload.username = rootState.username;
      return client({}).post(`/EForm/InsertEFormPNINReference`, payload);
    },
    async getMappingSection({ commit }, payload: any) {
      return await client({})
        .post(`/EForm/GetEFormMapping`, payload)
        .then((response: any) => {
          // groupping dilakukan karna BE (andreas) tidak mau lakukan grouping
          const data = response.responseData;
          let outputs = (data.Content ?? []).reduce(function (rv, x) {
            (rv[x["IdBP"]] = rv[x["IdBP"]] || []).push(x);
            return rv;
          }, {});
          outputs = Object.entries(outputs).map((entry: any) => {
            const key = entry[0];
            const value = entry[1];
            return {
              contentId: key,
              forms: value.map((form: any) => {
                const section = form?.Form?.Section ?? {};
                const res = {
                  formId: form.Form.IdBPDoc as string,
                  sectionId: {
                    IdEForm: section.IdEForm,
                    IdSection: section.IdBPSection,
                    Value: section.BPSectionName,
                  },
                  subSectionId: section?.SubSection?.IdEForm,
                  nestedList: {
                    section: [],
                    subSection: [],
                  },
                };
                return res;
              }),
              nestedList: {
                doc: [],
              },
            };
          });

          if (outputs.length == 0) {
            outputs.push({
              contentId: null,
              forms: [
                {
                  formId: null,
                  sectionId: null,
                  subSectionId: null,
                  nestedList: {
                    section: [] as TSelect[],
                    subSection: [] as TSelect[],
                  },
                },
              ],
              nestedList: {
                doc: [] as TSelect[],
              },
            });
          }

          const result = {
            bpName: data.BPName,
            idSector: data.IdSector,
            idEFormSource: data.IdEFormSource,
            input: data.FormInput,
            section: data.FormSection,
            outputs: outputs,
          };
          commit("setFormMapping", result);
          return new Promise((resolve) => {
            resolve(result);
          });
        });
    },
    async deleteMappingSection({ rootState }, payload: any) {
      return client({}).post(`/EForm/DeleteEFormMapping`, payload);
    },
    async mappingSection({ rootState }, payload: any) {
      payload.createdBy = rootState.username;
      return client({}).post(`/EForm/InsertEFormMapping`, payload);
    },
  },
  getters: {
    getIdBP: (state: any) => {
      return state.idBP;
    },
    getTOC: (state: any) => state.tableOfContent,
    getTOCDoc: (state: { tableOfContent: TTOC }) => {
      const contentDocList =
        state.tableOfContent?.content.reduce(
          (list: TTOCDoc[], curr: TTOCContent) => {
            return [...list, ...(curr.dataDocument ?? [])];
          },
          []
        ) ?? [];
      /* eslint-disable */
      const referenceDocList = [].concat.apply(
        [],
        [].concat
          .apply(
            [],
            state.tableOfContent?.reference.map(
              (reff) => reff.dataSector
            ) as Array<any>
          )
          .map((sector: any) => sector.dataDocument)
      );
      return [...contentDocList, ...referenceDocList];
    },
    getDocumentProgress: (state: any) => {
      return state.RDGBBulananDetail?.isFinish;
    },
    getIsAIU: (state: any) => state.isAIU,
    getReloadToc: (state: any) => {
      return state.reloadToc;
    },
  },
};
