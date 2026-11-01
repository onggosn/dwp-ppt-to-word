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

export type TSelect = {
  id: string | number;
  value: string | number;
  jabatanSatker?: string;
};

export type TResponseBase<T> = {
  responseCode: string;
  responseData: {
    data: T;
  };
  responseMessage: string;
};

export type TRDGBBulananDetailSummary = {
  title: string;
  value: number;
};

export type TResponseRDGBBulananDetail = TResponseBase<{
  eventName: string;
  summary: TRDGBBulananDetailSummary[];
}>;

export type TTOCSection = {
  idBpSection: string;
  bpSectionName: string;
};

export type TTOCDoc = {
  idBpDocument: string;
  bpDocumentName: string;
  isView: boolean;
  dataSection: TTOCSection[];
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

export type TInfoPage = {
  totalData?: number;
  prevPageNo?: number;
  pageNo: number;
  nextPageNo?: number;
  totalPage?: number;
  entriesPerPage?: number;
};

export type TWorkspaceRDGResponse = {
  infoPage: TInfoPage;
  data: TWorkspaceRDGL[];
};
