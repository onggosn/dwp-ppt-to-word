export default {
  namespaced: true,
  state: {
    formEditor: {} as any,
    eventName: "",
    documentName: "",
    documentTypeId: "",
    documentStatus: "", //not started, in progress, need for review, need for approval
    documentStatusId: "",
    rdgType: "",
    downloadCondition: false,
    documentSubmitCheck: false,
    startEditEForm: false,
    editAccessDocument: false,
    documentFlowCheck: 0,
    listForm: [],
    loading: false,
    loadingProgress: 0,
    error: null,
    loaderChip: 0,
    disableAllForm: false,
    accessStatus: false,
    accessStatusFinal: false,
    isStartDoc: false,
    isPreview: false,
    isPreviewPDF: false,
    disableAllApprovalButton: false,
    sectionActive: "" as string,
    documentVersion: "",
    flagUpdateAiu: false,
    listVersion: [],
    flagButtonVersion: false,
    flagAccessDoc: false,
    flagAlertAiu: false,
    reasonDeleteAiu: "",
    flagAlertCancel: false,
    reasonCancel: "",
    reasonReject: "",
    alartLabelCancel: "",
    idBpdocVersion: "",
    reloadTrackChanges: 0,
    isDocSectoral: "",
    eventKop: {},
    isViewTitle: false,
    title: "",
    isExportWord: false,
    noRisalahRdg: "" as string,
    noRisalahRapat: "" as string,
    dateRisalahRdg: "" as string,
    isImportPPT: false,
    isDisablePPT: false,
    listTabMetadata: [],
    noBkbs: "" as string,
    isEditTitlePNIN: false,
    noRisalahKomiteGabungan: null as string | null,
    dataMaterial: null as string | null,
    isContentMaterial: false,
    isContentFinalisasi: false,
    docConfig: {
      language: "",
      orientation: "",
      size: "",
      margins: {
        top: "",
        right: "",
        bottom: "",
        left: "",
      },
    },
  },
  getters: {
    getEventName: (state: any) => {
      return state.eventName;
    },
    getDocumentName: (state: any) => {
      return state.documentName;
    },
    getDocumentTypeId: (state: any) => {
      return state.documentTypeId;
    },
    getRdgType: (state: any) => {
      return state.rdgType;
    },
    getDocumentSectoral: (state: any) => {
      return state.isDocSectoral;
    },
    getDocumentStatus: (state: any) => {
      return state.documentStatus;
    },
    getDocumentStatusId: (state: any) => {
      return state.documentStatusId;
    },
    getDownloadCondition: (state: any) => {
      return state.downloadCondition;
    },
    getStartEditEForm: (state: any) => {
      return state.startEditEForm;
    },
    getEditAccessDocument: (state: any) => {
      return state.editAccessDocument;
    },
    getListForm: (state: any) => {
      return state.listForm ?? [];
    },
    getDocumentFlowCheck: (state: any) => {
      return state.documentFlowCheck;
    },
    getLoading: (state: any) => {
      return state.loading;
    },
    getLoaderChip: (state: any) => {
      return state.loaderChip;
    },
    getDisableAllForm: (state: any) => {
      return state.disableAllForm;
    },
    getAccessStatus: (state: any) => {
      return state.accessStatus;
    },
    getaccessStatusFinal: (state: any) => {
      return state.accessStatusFinal;
    },
    getStartDoc: (state: any) => {
      return state.isStartDoc;
    },
    getDisableAllApprovalButton: (state: any) => state.disableAllApprovalButton,
    getDocumentSubmitCheck: (state: any) => state.documentSubmitCheck,
    getSectionActive: (state: any) => state.sectionActive,
    getDocumentVersion: (state: any) => {
      return state.documentVersion;
    },
    getListVersion: (state: any) => {
      return state.listVersion;
    },
    getButtonVersion: (state: any) => {
      return state.flagButtonVersion;
    },
    getFlagAccessDoc: (state: any) => state.flagAccessDoc,
    getFlagAlertAiu: (state: any) => state.flagAlertAiu,
    getReasonDeleteAiu: (state: any) => state.reasonDeleteAiu,
    getFlagAlertCancel: (state: any) => state.flagAlertCancel,
    getReasonReject: (state: any) => state.reasonReject,
    getReasonCancel: (state: any) => state.reasonCancel,
    getAlartLabelCancel: (state: any) => state.alartLabelCancel,
    getUpdateAiu: (state: any) => state.flagUpdateAiu,
    getIdBpDocVersion: (state: any) => {
      return state.idBpdocVersion;
    },
    getEventKop: (state: any) => {
      return state.eventKop;
    },
    getPreviewDoc: (state: any) => {
      return state.isPreview;
    },
    getPreviewPDF: (state: any) => {
      return state.isPreviewPDF;
    },
    getViewTitle: (state: any) => state.isViewTitle,
    getTitle: (state: any) => state.title,
    getExportWord: (state: any) => state.isExportWord,
    getNoRisalahRdg: (state: any) => state.noRisalahRdg,
    getNoRisalahRapat: (state: any) => state.noRisalahRapat,
    getDateRisalahRdg: (state: any) => state.dateRisalahRdg,
    getListTabMetadata: (state: any) => {
      return state.listTabMetadata;
    },
    getImportPPT: (state: any) => state.isImportPPT,
    getDisableImportPPT: (state: any) => state.isDisablePPT,
    getNoBkbs: (state: any) => {
      return state.noBkbs;
    },
    getIsEditTitlePNIN: (state: any) => state.isEditTitlePNIN,
    getNoRisalahKomiteGabungan: (state: any): string | null =>
      state.noRisalahKomiteGabungan,
    getDataMaterial: (state: any) => state.dataMaterial,
    getIsContentMaterial: (state: any) => state.isContentMaterial,
    getIsContentFinalisasi: (state: any) => state.isContentFinalisasi,
    getDocConfig: (state: any) => state.docConfig,
  },
  mutations: {
    setFormEditor(state: any, payload: any) {
      state.formEditor = payload;
    },
    setEventName(state, newName) {
      state.eventName = newName;
    },
    setDocumentName(state, newName) {
      state.documentName = newName;
    },
    setDocumentTypeId(state, newTypeId) {
      state.documentTypeId = newTypeId;
    },
    setRdgType(state, newRdgType) {
      state.rdgType = newRdgType;
    },
    setDocSectoral(state, newTypeId) {
      state.isDocSectoral = newTypeId;
    },
    setDocumentStatus(state, newStatus) {
      state.documentStatus = newStatus;
    },
    setDocumentStatusId(state, newStatusId) {
      state.documentStatusId = newStatusId;
    },
    setDownloadCondition(state, newStatus) {
      state.downloadCondition = newStatus;
    },
    setStartEditEForm(state, newValue) {
      state.startEditEForm = newValue;
    },
    setEditAccessDocument(state, newValue) {
      state.editAccessDocument = newValue;
    },
    setListForm(state, newList) {
      state.listForm = newList;
    },
    setDocumentFlowCheck(state, newValue) {
      state.documentFlowCheck = newValue;
    },
    setLoading(state: any, isLoading: boolean) {
      state.loading = isLoading;
    },
    setError(state: any, error: any) {
      state.error = error;
    },
    setLoaderChip(state, newValue) {
      state.loaderChip = newValue;
    },
    setDisableAllForm(state, newValue) {
      state.disableAllForm = newValue;
    },
    setAccessStatus(state, newValue) {
      state.accessStatus = newValue;
    },
    setaccessStatusFinal(state: any, newValue: boolean) {
      state.accessStatusFinal = newValue;
    },
    setStartDoc(state: any, newValue: boolean) {
      state.isStartDoc = newValue;
    },
    setDisableAllApprovalButton(state: any, newValue: boolean) {
      state.disableAllApprovalButton = newValue;
    },
    setdocumentSubmitCheck(state, newValue) {
      state.documentSubmitCheck = newValue;
    },
    setSectionActive(state: any, payload: string) {
      state.sectionActive = payload;
    },
    setDocumentVersion(state, newValue) {
      state.documentVersion = newValue;
    },
    setListVersion(state, newList) {
      state.listVersion = newList;
    },
    setButtonVersion(state, newValue) {
      state.flagButtonVersion = newValue;
    },
    setFlagAccessDoc(state: any, newValue: boolean) {
      state.flagAccessDoc = newValue;
    },
    setFlagAlertAiu(state: any, newValue: boolean) {
      state.flagAlertAiu = newValue;
    },
    setreasonReject(state: any, newValue: boolean) {
      state.reasonReject = newValue;
    },
    setReasonDeleteAiu(state, newValue) {
      state.reasonDeleteAiu = newValue;
    },
    setFlagAlertCencel(state: any, newValue: boolean) {
      state.flagAlertCancel = newValue;
    },
    setReasonCencel(state, newValue) {
      state.reasonCancel = newValue;
    },
    setAlartLabelCancel(state, newValue) {
      state.alartLabelCancel = newValue;
    },
    setUpdateAiu(state, newValue) {
      state.flagUpdateAiu = newValue;
    },
    setIdBpDocVersion(state, newValue) {
      state.idBpdocVersion = newValue;
    },
    setEventKop(state, newValue) {
      state.eventKop = newValue;
    },
    increstReloadTrackChanges(state) {
      state.reloadTrackChanges++;
    },
    setPreviewDoc(state, newValue) {
      state.isPreview = newValue;
    },
    setPreviewPDF(state, newValue) {
      state.isPreviewPDF = newValue;
    },
    setViewTitle(state, newValue) {
      state.isViewTitle = newValue;
    },
    setTitle(state, newValue) {
      state.title = newValue;
    },
    setExportWord(state, newValue) {
      state.isExportWord = newValue;
    },
    setNoRisalahRdg(state, newValue) {
      state.noRisalahRdg = newValue;
    },
    setNoRisalahRapat(state, newValue) {
      state.noRisalahRapat = newValue;
    },
    setDateRisalahRdg(state, newValue) {
      state.dateRisalahRdg = newValue;
    },
    setListTabMetadata(state, newValue) {
      state.listTabMetadata = newValue;
    },
    setImportPPT(state, newValue) {
      state.isImportPPT = newValue;
    },
    setDisableImportPPT(state, newValue) {
      state.isDisablePPT = newValue;
    },
    setNoBkbs(state, newValue) {
      state.noBkbs = newValue;
    },
    setIsEditTitlePNIN(state, newValue) {
      state.isEditTitlePNIN = newValue;
    },
    setNoRisalahKomiteGabungan(state, newValue) {
      state.noRisalahKomiteGabungan = newValue;
    },
    setDataMaterial(state, newValue) {
      state.dataMaterial = newValue;
    },
    setIsContentMaterial(state, newValue) {
      state.isContentMaterial = newValue;
    },
    setIsContentFinalisasi(state, newValue) {
      state.isContentFinalisasi = newValue;
    },
    setDocConfig(state, newValue) {
      state.docConfig = newValue;
    },
  },
  actions: {},
};
