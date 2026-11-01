import { TExtension } from "../Type";

export const monthNames = [
  { id: 1, name: "January" },
  { id: 2, name: "February" },
  { id: 3, name: "March" },
  { id: 4, name: "April" },
  { id: 5, name: "May" },
  { id: 6, name: "June" },
  { id: 7, name: "July" },
  { id: 8, name: "August" },
  { id: 9, name: "September" },
  { id: 10, name: "October" },
  { id: 11, name: "November" },
  { id: 12, name: "December" },
];

export const rdgType = [
  "RDGB Cakupan Bulanan",
  "RDGB Cakupan Triwulanan",
  "RDGB Cakupan Tahunan",
  "RDGTK Cakupan Triwulanan",
  "RDGTK Cakupan Tahunan",
];

export const status = ["Not Started", "In Progress", "Done"];

export const yearRdg = ["2024", "2023", "2022", "2021"];

export const businessStageList = {
  summary: [{ assesmen: 0, rekomendasi: 0, persetujuan: 0, total: 0 }],
  detail: [
    {
      stages: "Assesmen",
      bp: "RSOEM",
      bpStatus: "Not Started",
      bpValue: 100,
      bpLink: "",
    },
    {
      stages: "Assesmen",
      bp: "RSOMA",
      bpStatus: "Not Started",
      bpValue: 0,
      bpLink: "",
    },
    {
      stages: "Assesmen",
      bp: "RSOPS",
      bpStatus: "Not Started",
      bpValue: 50,
      bpLink: "",
    },
    {
      stages: "Assesmen",
      bp: "Rekomendasi Awal BKBI",
      bpStatus: "Not Started",
      bpValue: 0,
      bpLink: "",
    },
    {
      stages: "Assesmen",
      bp: "SOEM",
      bpStatus: "Not Started",
      bpValue: 0,
      bpLink: "",
    },
    {
      stages: "Assesmen",
      bp: "SOMA",
      bpStatus: "Not Started",
      bpValue: 0,
      bpLink: "",
    },
    {
      stages: "Assesmen",
      bp: "SOPS",
      bpStatus: "Not Started",
      bpValue: 0,
      bpLink: "",
    },
  ],
};

export const latestContent = [
  {
    idBP: "faaaaf41-7245-4311-ab0a-b216c17dced2",
    idEvent: "087c1609-6c85-4a43-a64f-bb0325792f36",
    bpName: "AIU",
    idBPDocument: "486e9d3e-38f6-47c6-9b42-8305e4b198a1",
    bpDocumentName: "Risalah Rapat DKEM_RSOEM_Mei 2024",
    lastApproved: "Monday, 06 May 2024",
  },
  {
    idBP: "a8b5b527-fe5a-45fb-9ac1-374edd879542",
    idEvent: "f753f122-fd76-4ec6-b616-871aca667a94",
    bpName: "AIU",
    idBPDocument: "27e1cb8b-fa07-4ad9-99d3-8c8b952cf480",
    bpDocumentName: "DKSP SOPS Maret 2031_02_Velositas_BI-RTGS",
    lastApproved: "Monday, 06 May 2024",
  },
  {
    idBP: "3271d4fe-44a7-42dc-8e61-3f911638ea62",
    idEvent: "36866b9e-c683-483f-b2c9-53884259dbb3",
    bpName: "AIU",
    idBPDocument: "3b044d6c-5943-4e7e-a245-0aafd454b348",
    bpDocumentName: "DKEM_AIU_Mei 2024_03_Pasar Keuangan Global",
    lastApproved: "Friday, 03 May 2024",
  },
  {
    idBP: "3271d4fe-44a7-42dc-8e61-3f911638ea62",
    idEvent: "36866b9e-c683-483f-b2c9-53884259dbb3",
    bpName: "AIU",
    idBPDocument: "4ab4e4a3-9ce7-4228-b6ce-7a9a26a4b8a0",
    bpDocumentName: "DKEM_AIU_Mei 2024_02_Inflasi Global",
    lastApproved: "Friday, 03 May 2024",
  },
  {
    idBP: "3271d4fe-44a7-42dc-8e61-3f911638ea62",
    idEvent: "36866b9e-c683-483f-b2c9-53884259dbb3",
    bpName: "PN",
    idBPDocument: "0e0e8deb-b791-478b-988c-f16bf1901457",
    bpDocumentName: "DKEM_AIU_Mei 2024_01_PDB Global",
    lastApproved: "Friday, 03 May 2024",
  },
  {
    idBP: "5bbe56a9-5200-498b-aa6a-8d669dd82158",
    idEvent: "6982b02f-cfea-4eb0-a449-94aac6650b06",
    bpName: "IN",
    idBPDocument: "ae2c802a-b38e-43fc-a3a2-5f24036985bf",
    bpDocumentName: "Risalah Rapat DKEM_RSOEM_Januari 2031",
    lastApproved: "Tuesday, 30 April 2024",
  },
];

export const mimeTypes: Record<TExtension, string> = {
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  csv: "text/csv",
  pdf: "application/pdf",
  txt: "text/plain",
  zip: "application/zip",
  png: "image/png",
  jpeg: "image/jpeg",
  json: "application/json",
};
