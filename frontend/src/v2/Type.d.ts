// global
export type TResponseBase<T> = {
  responseCode: string;
  responseData: {
    data: T;
  };
  responseMessage: string;
};

export type TResponsePromise = TResponseBase<any> & {
  responseData: {
    description: string;
  };
};

export type TFileDragable = {
  name: string;
  sizeString: string;
  sizeNumber: number;
  file: any;
};

export type TListDocument = {
  id: number;
  value: string;
};

type AdgForm = {
  namaAdg: string;
  jabatan: string;
  pangkat: string;
  email: string;
  adgBidang: string;
  listNamaAdg: Array<any>;
  isloadingSearchNamaAdg: boolean;
  username: string;
  searchNamaAdg: string;
};

type DetailADGSave = {
  adgBidang: string;
  email: string;
  jabatan: string;
  namaAdg: any;
  pangkat: string;
  username: any;
};

export type TModalConfirm = {
  title: string;
  message: string;
  width?: number;
  titleClass?: string;
  messageClass?: string;
  btnSubmitLabel?: string;
  btnSubmitColor?: string;
  btnCancelLabel?: string;
  usingTimeOut?: boolean;
  showIcon?: boolean;
  icon?: {
    code?: string;
    color?: string;
    backgrounColor?: string;
    size?: number;
    typeImage?: string;
  };
};

export type TModalWarning = {
  img: { location: string; width: string; height: string };
  title: string;
  description: string;
  btnBackgroundStyle: string;
  textBtn: string;
  textWeight: number;
  textStyle: string;
};

export type TInfoPage = {
  totalData?: number;
  prevPageNo?: number;
  pageNo: number;
  nextPageNo?: number;
  totalPage?: number;
  entriesPerPage?: number;
};

export type TSelect = {
  id: string | number;
  value: string | number;
  jabatanSatker?: string;
};

type TExtension =
  | "xlsx"
  | "docx"
  | "csv"
  | "pdf"
  | "txt"
  | "zip"
  | "png"
  | "jpeg"
  | "json";

// global

// Notification
export type TNotificationItem = {
  ListNotif?: Array<any>;
  activityName: string;
  createdBy: string;
  createdDate: string;
  description: string;
  eventId: string;
  id: string;
  idActivity: string;
  idArea: string;
  idSektor: string;
  idTask: string;
  idWorkspace: string;
  idWorkspaceLevel: number;
  idWorkspaceType: number;
  message: string;
  notificationObject: string;
  notificationTypeId: number;
  notifyFrom: string;
  notifyTo: string;
  pengaju: string;
  penyetuju: string;
  periode: string;
  seenByUser: boolean;
  taskName: string;
  type: string;
  updatedBy: string;
  updatedDate: string;
  userToNotify: string;
  workspaceName: string;
  workspaceStatus: number;
};

export type TNotificationResponse = TResponseBase<TNotificationItem[]>;
// Notification

export type TListOrganizer = {
  name: string;
  grade: string;
};

// MATERIAL
export type THasilPembahasan = {
  idEvent: string;
  traceId: string;
  title: string;
  documentFile: any;
};

export type TFormMaterial = {
  method: number | any;
  idEvent: string;
  traceId: string;
  file: TFileDragable | any;
  dokumenTipe: number | any;
  versi: string | null;
  topikNama: string | null;
  satkerPembuat: number | any;
  ps: number | any;
  event: number | any;
  presenter: string | null;
  keyword: string | null;
  penyusun: any[];
  pengaju: number | any;
  documentType: string | null;
};

export type TMaterialList = {
  id: string;
  initialDocument: string;
  initialDocumentExt: string;
  materialAction: {
    isDelete: boolean;
    isDownload: boolean;
    isRead: boolean;
    isAccess: boolean;
    isMetadata: boolean;
  };
  materialExt: string;
  materialName: string;
  materialSize: number;
  materialURL: string;
  materialListDoc: string;
  timeStamp: string;
  materialListDocId: number;
};

export type TMaterialPreview = {
  id: string | null;
  docExt: string;
  title: string;
  size?: number | string;
};

export type TMaterialMetadata = {
  id: string;
  title: string;
  statusName: string;
  eventName: string;
  docType: string;
  satkerPembuat: string;
  presenter: string;
  listPenyusun: string[];
  pengaju: string;
  penyetuju: string;
  version: string;
  createdDate: string;
  createdByName: string;
  materialListDoc: string;
  materialListDocId: number;
  listApprovals: {
    title: string;
    name: string;
    approvedDate: string;
  }[];
};

export type TLinkMaterialResponse = {
  materialName: string | null;
  idEvent: string | null;
  idBPDocument: string;
  idParent: any;
  idMEventSubTypeList: number;
  rdgType: string;
};
// MATERIAL

interface unitAgenda {
  id: number;
  value: string;
}

export type TAgendaData = {
  id: string;
  date: string;
  agendaName: string;
  agendaOrder: number;
  invited: string[];
  endTime: string;
  listInvitedUnit: unitAgenda[];
  listPresentingUnit: unitAgenda[];
  startTime: string;
  status: number;
  adgBidang: string[];
  adgBidangAttendance: string[];
  agendaPlace: string;
};

export type TAgendaList = {
  id: string;
  agendaName: string;
  presentingUnit: string[];
  invitedUnit: string;
  startTime: string;
  intervalTime: string;
  endTime: string;
  isEdit: boolean;
  isDelete: boolean;
  status: string;
  date: string;
};

/* WORKSPACE MANAGEMENT */
export type TWorkspaceRDG = {
  RDGType: string;
  username: string;
  eventSearching: string;
  pageSize: number;
  page: number;
  eventSubTypeListFilter: number[];
  status: number[];
  dateFilter: any;
};

export type TWorkspaceRDGL = {
  eventName: string;
  eventDate: string;
  eventStatus: string;
};

export type TWorkspaceOG = {
  workspaceID: string;
  workspaceName: string;
  workspaceStatus: string;
};

export type TWorkspaceRDGResponse = {
  infoPage: TInfoPage;
  data: TWorkspaceRDGL[];
};

export type TDetailRDG = {
  asesmen: Array<TDetailRDGItem>;
  rekomendasi: Array<TDetailRDGItem>;
  persetujuan: Array<TDetailRDGItem>;
};

export type TDetailRDGSummary = {
  title: string;
  value: number;
};

export type TDetailRDGItem = {
  stages: string;
  bp: string;
  idBp: string;
  idBpDocument: string;
  bpStatus: string;
  bpValue: number;
  bpLink: string;
  isAllowNext: boolean;
};

export type TResponseRDGBBulananDetail = TResponseBase<{
  eventName: string;
  summary: TRDGBBulananDetailSummary[];
}>;

export type TRDGBBulananDetailSummary = {
  title: string;
  value: number;
};

export type TResponseBPAssesment = TResponseBase<{
  businessProcess: TBPAssesmentDetail[];
}>;

export type TBPAssesmentDetail = {
  title: string;
  value: TDetailRDGItem[];
};

export type TResponseBPRekomendasi = TResponseBase<{
  businessProcess: TBPRekomendasiDetail[];
}>;

export type TBPRekomendasiDetail = {
  title: string;
  value: TDetailRDGItem[];
};

export type TResponseBPPersetujuan = TResponseBase<{
  businessProcess: TBPPersetujuanDetail[];
}>;

export type TBPPersetujuanDetail = {
  title: string;
  value: TDetailRDGItem[];
};

export type TResponseBPOthers = TResponseBase<{
  chartpack: number;
  aiu: TBPOtherItem;
  policyNote: TBPOtherItem;
  issueNote: TBPOtherItem;
}>;

export type TBPOtherItem = {
  bp: string;
  idStages: number;
  bpValue1: number;
  bpValue2: number;
  bpValuePercentage: number;
  idBp: string;
  idBpDocument: string;
  isAllowNext: boolean;
};

export type TDetailRDGResponse = {
  summary: Array<TDetailRDGSummary>;
  detail: TDetailRDGSummary;
};

export type TContentFilterItem = {
  title: string;
  name: string;
  value: { id: number; value: string }[];
};
/* WORKSPACE MANAGEMENT */

/* CALENDAR */
export type TRequestEventCalendar = {
  userName?: string;
  calendarType: string;
  dateFilter: string;
  eventTypeFilter?: number[];
  eventSubTypeListFilter?: number[];
  eventAdgFilter?: number[];
  komite?: number[];
  eventSearching: string;
};

export type TCalendarTypeItem = {
  value: string;
  title: string;
};

export type TCalendarList = {
  id: string;
  title: string;
  startDate: Date;
  endDate: date;
  startTime: string;
  endTime: string;
  method: string;
  meetingPlatform: string;
  eventTypeId: number;
  eventType: string;
  eventSubTypeId: number;
  eventSubType: string;
  isMaterial: boolean;
};
export type TDetailSection = {
  bp: string;
  idStages: number;
  bpValue1: number;
  bpValuePercentage: number;
  bpValue2: number;
  idBp: string;
  idBpDocument: string;
  isAllowNext: boolean;
  value: number;
};

export type TDetailAssign = {
  bp: string;
  bpValue1: number;
  bpValue2: number;
  bpValuePercentage: number;
  idRDGType: number;
  monthRDG: number;
  yearRDG: number;
  isAllowNext: boolean;
};

export type TSectionSummary = {
  chartpack: number;
  aiu: TDetailSection | null;
  policyNote: TDetailSection | null;
  issueNote: TDetailSection | null;
  publikasi: TDetailSection | null;
  assignment: TDetailAssign | null;
  isvisible?: boolean | null;
};
/* CALENDAR */

// create content
export type TRequestCreateAIU = {
  sector: string | any;
  forms: {
    id: string | null;
    name: string | null;
  }[];
};

export type TRequestCreatePN = {
  sector: string | any;
  forms: TRequestFormPN[];
};

export type TRequestFormPN = {
  title: string | null;
  sections: {
    id: string | number | null;
  }[];
};

type TRDGBBulananDetailSummary = {
  assesmen: string;
  rekomendasi: string;
  persetujuan: string;
};

type TRDGBBulananDetailDetail = {
  stage: string;
  bp: string;
  bpStatus: string;
  bpValue: number;
  bpLink: string;
};

export type TResponseRDGBBulananDetail = TResponseBase<
  TRDGBBulananDetailDetail[]
> & {
  responseData: {
    summary: TRDGBBulananDetailSummary;
    detail: TRDGBBulananDetailDetail[];
  };
};

export type TRequestCreateRDGLainnya = {
  _eventType: { id: number; value: string } | any;
  _rdgType: { id: string; value: string } | any;
  _month: { id: number; name: string } | any;
  _year: string | null;
  _rdg:
    | {
        idEvent: string;
        eventName: string;
      }
    | any;
  _event:
    | {
        idEvent: string;
        bPName: string;
      }
    | any;
  _title: string;
  _description: string;
  _method:
    | {
        id: number;
        value: string;
      }
    | any;
  _media:
    | {
        id: number;
        platform: string;
        isGenerate: number;
      }
    | any;
  _mediaBackup:
    | {
        id: number;
        platform: string;
        isGenerate: number;
      }
    | any;
  _linkMeeting: string;
  _linkMeetingBackup: string;
  _place: string;
  _startDate: string | null;
  _endDate: string | null;
  _startTime: string | null;
  _endTime: string | null;
};

export type TRequestCreateAIUPNIN = {
  _eventType: { id: number; value: string } | any;
  _rdgType: { id: string; value: string } | any;
  _month: { id: number; name: string } | any;
  _year: string | null;
  _rdg:
    | {
        idEvent: string;
        eventName: string;
      }
    | any;
};
// toc = table of content
export type TTOCSection = {
  idBpSection: string;
  bpSectionName: string;
};

export type TTOCDoc = {
  idBpDocument: string;
  bpDocumentName: string;
  isView: boolean;
  dataSection: TTOCSection[];
  isRevision?: boolean;
};

export type TTOCSector = {
  sectorName: string;
  dataDocument: TTOCDoc[];
};

export type TTOCContent = {
  bpName: string;
  dataDocument: TTOCDoc[];
};

export type TTOCReference = {
  bpName: string;
  dataSector: TTOCSector[];
};

export type TTOC = {
  content: TTOCContent[];
  reference: TTOCReference[];
  publikasi: TTOCContent[];
};

export type TResponseTOC = TResponseBase<TTOC> & {
  responseData: {
    content: TTOCContent[];
    reference: TTOCReference[];
    publikasi: TTOCContent[];
  };
};

export type TRequestTOC = {
  username?: string;
  idEvent: string;
};

export type TFormMappingSection = {
  bpName: string | null;
  input: string | null;
  section: string | null;
  idEFormSource: string | null;
  idSector: number;
  outputs: [
    {
      contentId: string | null;
      forms: [
        {
          formId: string | null;
          sectionId: string | any;
          subSectionId: string | null;
          nestedList: {
            section: TSelect[];
            subSection: TSelect[];
          };
        }
      ];
      nestedList: {
        doc: TSelect[];
      };
    }
  ];
};

type TUserPenyetuju = {
  id: number;
  isPresent: boolean;
};

type TUserOtherApproval = {
  userApprovalPenyusun: number;
  userApprovalPengaju: number;
  userApprovalPenyetuju: TUserPenyetuju[];
};

export type TRevisionType = "minor" | "substance" | "reject";

type TReasonApproval = {
  value: string;
};

export type TRequestApproval = {
  id: string;
  sendType: TRevisionType;
  idMBPEFormApproval: number;
  idMBPEFormApprovalCurrent: number;
  idMBPEFormApprovalNext: number;
  idMSector: number;
  isRevision: boolean;
  idMBPApprovalFlow: number;
  idMBPApproval: number;
  idMBPApprovalCurrent: number;
  stepNameCurrent: string;
  idMBPApprovalNext: number;
  stepNameNext: string;
  buttonLabel: TButtonLabel;
  needUserApproved: boolean;
  idStatus: number;
  currentStatus: number;
  nextStatus: number;
  userApproval: number;
  documentNo?: string;
  sendType?: string;
  userOtherApproval?: TUserOtherApproval;
  reason: string | TReasonApproval;
  lastApprove: boolean;
  dateRDG: string;
  rubrikYear: string;
};

/* Button Flow Label */
export type TButtonLabel =
  | "Submit"
  | "Send"
  | "Reject"
  | "Approve"
  | "Revision";

// Hak Akses

export type TResponseSearchByName = {
  id: number;
  inputEmail: string;
  isGroup: false;
  organizationName: string;
  value: string;
  username?: string;
};

export type TResponseSearchByDocType = {
  id: string;
  value: string;
  documentName: string;
};

/* HOMEPAGE */
export type TResponseTop10DocByUser = {
  idBP: string;
  idEvent: string;
  bpName: string;
  idBPDocument: string;
  bpDocumentName: string;
  lastApproved: string;
  eventName: string;
  idMEventSubTypeList: number;
  rdgType: string;
};
export type TListVersion = {
  Id: string;
  version: string;
  canClick: boolean;
};
/* HOMEPAGE */

/* ADMIN */
export type TAdminListVersion = {
  rdgType: string;
  idMEventSubType: string | number;
};

export type TAdminListEventSubType = {
  eventSubType: string;
  idMEventSubTypeList: string | number;
};

export type TAdminListSector = {
  sectorName: string;
  idMSector: string | number;
};

export type TTypeFlow2d = {
  hasAccess: boolean;
  idMSector: number;
  idStatus: number;
  sector:
    | "Makroprudensial"
    | "Moneter"
    | "Sistem Pembayaran"
    | "Pelaksanaan Moneter"
    | "Surveilans"
    | "Implementasi Sistem Pembayaran";
  status: string;
};

export type TApprovalPenyetuju = {
  id: number;
  name: string;
  grade: string;
  isPresent: boolean;
  index: number;
};

export type TListSortingType = {
  id: number;
  value: string;
};

export type TRequestAddMeeting = {
  eventType: TEventType | null;
  rdgType: TEventType | null;
  sector: {
    idMSector: number | null;
    sectorName: string | null;
  } | null;
  stage: TEventType | null;
  title: string | null;
  method: number | null;
  media: number | null;
  startDate: number | any;
  prependStartDate: string | null;
};

export type TSelectListCreate = TResponseBase<{
  idBp: string;
  name: string;
}>;

export type TEventType = {
  id: number | null;
  value: string | null;
};

export type TListDownload = {
  id: number | null;
  totalSheet: number | null;
  type: string | null;
  value: string | null;
};

export type TListMemberMeeting = {
  accessType: string | null;
  gradeName: string | null;
  id: number | null;
  name: string | null;
  organizationName: string | null;
};

export type TUserRoleDetail = {
  idMuser: number;
  email: string;
  username: string;
  jabatanId: number;
  jabatanName: string;
  pangkatName: string;
  createdBy: string;
  createdDate: Date;
  updatedBy: string;
  updatedDate: Date;
  isDelete: boolean;
  isAddMember: boolean;
  lastUpdatedBy: string;
  lastUpdatedDate: Date;
};
export type TListMeetingEvent = {
  id: number;
  title: string;
  createdDate: string;
  createdBy: string;
  updatedDate: string | null;
  updatedBy: string;
  lastModified: string;
  modifiedBy: string;
  isDelete: boolean;
  isEdit: boolean;
};

export type TUserInfoAdmin = {
  id: number;
  username: string;
  name: string;
  satker: string;
  lastModifiedBy: string;
  lastModifiedDate: string;
};

export type TSortingData = {
  id: string;
  value: string;
};

//assignment

export type TCheckboxAssignment = {
  workspaceType?: string;
  period?: string;
  status?: string;
  monthPeriod?: string;
  satkerKoordinator?: string;
  yearPeriod?: string;
  dueYear?: string;
};

export type TSortFilter = {
  sortName: string | null;
  sortType: "ascending" | "descending";
  sortTime: "ascending" | "descending";
};

export type TFilterData = {
  sort: TSortFilter;
  filter: TCheckbox;
  searchKeyword?: string;
};

export type RootAssignment = {
  list: ListAssignment[];
  pagination: Pagination;
};

export type ListAssignment = {
  id: string;
  name: string;
  statusName: string;
  listDitugaskanKepada: string;
  isAvailable: boolean;
  listApproval: ListApproval[];
  listSatkerKoordinatorList: any;
  listSatkerPendukungList: any;
  listAdgList: any;
  listAssignmentMemberList: any;
  idTipePenugasan: number;
  idReminderPeriod: number;
  idEvent: string;
  idStatus: number;
  assignmentName: string;
  description: string;
  workDate: any;
  dueDate: string;
  doclibDraft: string;
  folderDraft: any;
  siteDraft: string;
  doclibFinal: any;
  folderFinal: any;
  siteFinal: any;
  createdBy: string;
  createdDate: string;
  updatedBy: string;
  updatedDate: string;
  tipePenugasan: string;
  eventName: string;
  idEventSubTypeList: number;
  eventSubTypeLIst: string;
  assignmentTypeName: string;
  periode: string;
  satkerKoordinatorList: string;
  satkerPendukungList: string;
  adgBidangList: string;
  idWorkspace?: string;
  idTask?: string;
};

export type ListApproval = {
  idAssignment: string;
  idTipePenugasan: number;
  currentStatus?: number;
  nextApproval?: number;
  label: string;
  idPenugasan?: string;
  idArahan?: string;
};

export type Pagination = {
  page: number;
  total: number;
  visible: number | boolean;
};

export type TDetailAssignment = {
  assignmentName: string;
  description: string;
  statusName: string;
  listSatkerKoordinator: string;
  listDitugaskanKepada: string;
  name: string;
  idStatus: number | string;
  isAvailable?: string | boolean;
  satkerKoordinatorList?: string;
};

export type TFileLoading = {
  hasProgress: boolean;
  sizeDocument: number;
  downloadProgress: number;
  bandwithTxt: string;
};

export type TSortData = {
  sortName: string | null;
  sortType: string;
  sortTime: string;
  [key: string]: any;
};

export type TFilterData = {
  sort: TSortData;
  filter: Record<string, any>;
  searchKeyword: string;
};

export type TMenuItem = {
  name: string;
  label: string;
};

export type TSummaryData = {
  title: string;
  value: string;
};

export type TAssignment = {
  id: number;
  taskName: string;
  statusName: string;
  idStatus: number;
  [key: string]: any;
};

export type TDocument = {
  documentName: string;
  workspaceName: string;
  eventName: string;
  status: number;
  idEvent: string;
};

export type TPagination = {
  page: number;
  total: number;
  visible: number;
};

export type TAssignmentsState = {
  list: TAssignment[];
  pagination: TPagination;
};

export type TDocumentsState = {
  list: TDocument[];
  pagination: TPagination;
};

export type TFormEditor = {
  idEForm: string;
  bPEFormLabel: string;
  isLabelVisible: boolean;
  idFormEditor: string;
  idMEFormTemplate: number;
  eFormSource: string;
  isEdit: boolean;
  isView: boolean;
  isMapping: boolean;
  idParentEForm: string;
  isButtonAccess: boolean;
  bundleVersion: string;
};

export interface TDetailSubmit {
  idEformSource: string;
  subSectionTitle: string;
  sectionTitle: string;
  outputMappings: OutputMapping[];
}

export interface TDetailSubmitStp {
  idEformSource: string;
  subSectionTitle: string;
  sectionTitle: string;
  outputMappings: TFormOutputMapping[];
}

export interface TFormInputMapping {
  id: any;
  idEformSource: any;
  idSection: any;
  isEdited: boolean;
  idSubSection: any;
  isDelete: boolean;
  subSectionTitle: any;
  IdEformSourceOriginal: any;
  sectionTitle: any;
  listSection: Array;
  listSubSection: Array;
  isLoadingSection: boolean;
  isLoadingSubSection: boolean;
  outputMappings: TFormOutputMapping[];
}

export interface TFormOutputMapping {
  documentName: any;
  isDelete: boolean;
  idBp: any;
  idBpDocument: any;
  idEformSource: any;
  idBpSection: any;
  idSubSection: any;
  isEdited: boolean;
  listTahapan: Array;
  listContent: Array;
  listSection: Array;
  listSubSection: Array;
  isLoadingContent: boolean;
  isLoadingSection: boolean;
  condisionalSubsection: string;
  isLoadingSubSection: boolean;
  isLoadingTahapan: boolean;
  tahapan: any;
  sectionTitle: any;
  subSectionTitle: any;
  title: any;
}

interface OutputMapping {
  title: string;
  documentName: string;
}

export type TListEForm = {
  isAppend: boolean;
  listIdEform: string[];
};

export type FilterGroup = {
  title: string;
  name: string;
  value: Array<{
    id: number | string;
    value: string;
    isDisable: number;
    isChecked: number;
    idRdgType?: number[];
  }>;
};

export type InputMapping = {
  sections: {
    id: number | null;
    sectionName: string;
    status?: "new" | "updated" | "deleted" | "existing";
    hasDuplicate?: boolean;
  }[];
};
export interface RouteConfig {
  path: string;
  mode: string;
  component: any;
  backRoute: string;
  props?: Record<string, any>;
  backRoutePatterns?: Array<{
    pattern: string;
    backRoute: string;
  }>;
}

export interface FilterConfig {
  keys: string[];
  defaultChecked: Record<string, any[]>;
  dateFields: boolean;
}

export interface FilterItem {
  id: number | string;
  value: string;
  isDisable?: number | boolean;
  isChecked?: number | boolean;
  idRdgType?: number[];
}

export type TAddPresentationMaterial = {
  eventType: TEventType | null;
  rdgType: TEventType | null;
  sector: {
    idMSector: number | null;
    sectorName: string | null;
  } | null;
  stage: TEventType | null;
  event: TEventType | null;
  title: string | null;
  username: string | null;
};

export type TResponseCbAccess = {
  id: number;
  inputEmail: string;
  isGroup: false;
  organizationName: string;
  value: string;
  isEdit: boolean;
  isDownload: boolean;
  isView: boolean;
  isPreview: boolean;
  isMetadata: boolean;
  isDelete: boolean;
  name: string;
  type: string;
};

export type TPresentationDetail = {
  documentName: string;
  isEditPredefineMaterial: boolean;
  isDeletePredefineMaterial: boolean;
  modifiedBy: string;
  lastModified: string;
  idMEventDocPresentationMaterial: number;
};
// EditAccessSection types
export type TEditAccessCheckbox = {
  id: string;
  name: string;
  username: string;
  type: string;
  isEdit: boolean;
  isView: boolean;
  isDownload: boolean;
  isDelete: boolean;
  memberType: number;
  memberTypeName: string;
  idAssignment: string;
};

export type TEditAccessDelete = {
  idBPDocMember: string;
  name: string;
  type: string;
  isDelete: boolean;
};

export type TWorklistItem = {
  id: string;
  title: string;
  status: string;
  type: string;
  fileType?: string;
  linkHelper?: string;
  idEvent?: string;
};

export type PaginationADG = {
  totalData: number;
  prevPageNo: number;
  nextPageNo: number;
  pageNo: number;
  totalPage: number;
  entriesPerPage: number;
};

export type ParamsListADG = {
  username?: string;
  search?: string;
  page: number;
  pageSize: number;
};

export type DetailADGPersonal = {
  namaAdg: string;
  jabatan: string;
  pangkat: string;
  email: string;
  adgBidang: string;
};

export type DetailListADGResponse = {
  bannerEventDetail: string;
  bannerEventDetailExtention: string;
  homepageEventBanner: string;
  homepageEventBannerExtention: string;
  effectiveDate: string;
  status: string;
  detailADG: DetailADGPersonal[];
};

export type DetailListADG = {
  responseCode: string;
  responseMessage: string;
  responseData: DetailListADGResponse;
};

export type ListADG = {
  idFormasi: string;
  name: string;
  effectiveDate: string;
  lastUpdatedDate: Date;
  lastUpdatedBy: string;
  isActive: boolean;
  detailADG?: DetailListADG | null;
};

export type DetailFormADG = {
  username: string;
  namaADG: string;
  jabatan: string;
  pangkat: string;
  email: string;
  adgBidang: string;
};

export type FormADG = {
  bannerEventDetail: string;
  bannerEventDetailExtention: string;
  homepageEventBanner: string;
  homepageEventBannerExtention: string;
  effectiveDate: string;
  status: string;
  detailADG: DetailADG[];
};

export type TDialogError = {
  width: number;
  slideNumber: string;
  message: string;
  sectionName: string;
};

export type DocConfig = {
  language: string;
  orientation: string;
  size: string;
  margins: {
    top: string;
    bottom: string;
    left: string;
    right: string;
  };
};
