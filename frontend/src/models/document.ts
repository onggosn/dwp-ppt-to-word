import client from "@/library/ApiClient";
import store from "@/store/index";
import { useRoute } from "vue-router";

export class Document {
  constructor(
    private id: string,
    private taskId: string,
    private type: number,
    private name: string,
    private topic: string,
    private size: number = 0,
    private presenter: string,
    private editor: string,
    private keyword: string,
    private ps: string,
    private event: string,
    private satker: string,
    private linkEdit: string,
    private createdBy: string,
    private createdDate: string,
    private linkView: string,
    private status: string,
    private documentSite: string,
    private userApprovals: [],
    private trackingDocument: [],
    private access: [],
    private canDownloadPPt: boolean,
    private typeDocument: string,
    private listPenyusun: any[] | null,
    private isSendDocument: boolean,
    private isLinkedDocument: boolean,
    private linkedDocumentId: string,
    private extension: string,
    private icon: string,
    private isEditDocumentPNIN: boolean
  ) {}
}

class DocumentInfo {
  constructor(
    private entriesPerPage: number = 0,
    private nextPageNo: number = 0,
    private pageNo: number = 0,
    private prevPageNo: number = 0,
    private totalData: number = 0,
    private totalPage: number = 0
  ) {}
}

async function mGetIsOwner(idTask): Promise<boolean> {
  return await client
    .getTasksByIdTask({
      store: store,
      data: {
        id: idTask,
        username: store.state.username,
      },
    })
    .then((response) => {
      return response.plainData[0].isOwner;
    });
}

export async function getDocument(
  _idTask: string,
  _page: number,
  _pageSize: number
): Promise<object> {
  const documentList: Document[] = [];
  let pageInfo: DocumentInfo = {} as DocumentInfo;
  await client
    .getListDocumentPendukung({
      data: {
        username: store.state.username,
        idTask: _idTask,
        page: _page,
        pageSize: _pageSize,
      },
      store: store,
    })
    .then((response): void => {
      switch (response.plainData.responseCode) {
        case "011000": {
          pageInfo = response.plainData.responseData.infoPage;
          for (const item of response.plainData.responseData.data) {
            documentList.push(
              new Document(
                item.id,
                item.taskId,
                item.documentTypeId,
                item.documentNameDisplay,
                item.documentTopic,
                item.sizeDocument,
                item.presenter,
                item.editor,
                item.keyword,
                item.programStrategisName,
                item.mEventName,
                item.satker,
                item.linkEdit,
                item.createdBy,
                item.createdDate,
                item.linkView,
                item.statusDoc,
                item.documentSite,
                item.userApprovals,
                item.trackingDocument,
                item.detilDocumentAccess,
                item.canDownloadPPt,
                item.typeDocument,
                item.listPenyusun,
                item.isSendDocument,
                item.isLinkedDocument,
                item.linkedDocumentId,
                getDocumentExtension(item.documentNameDisplay),
                getDocumentIcon(item.documentNameDisplay, item.isSendDocument),
                item.isEditDocumentPNIN
              )
            );
          }
          break;
        }
        default:
          break;
      }
    });

  return {
    list: documentList,
    info: pageInfo,
    isOwner: await mGetIsOwner(_idTask).then((response) => response),
  };
}

export async function getDocumentUtama(
  _idTask: string,
  _page: number,
  _pageSize: number
): Promise<any> {
  const documentList: Document[] = [];
  let pageInfo: DocumentInfo = {} as DocumentInfo;
  await client
    .getListDocumentUtama({
      data: {
        username: store.state.username,
        idTask: _idTask,
        page: _page,
        pageSize: _pageSize,
      },
      store: store,
    })
    .then((response): void => {
      switch (response.plainData.responseCode) {
        case "011000": {
          pageInfo = response.plainData.responseData.infoPage;
          for (const item of response.plainData.responseData.data) {
            documentList.push(
              new Document(
                item.id,
                item.taskId,
                item.documentTypeId,
                item.documentNameDisplay,
                item.documentTopic,
                item.sizeDocument,
                item.presenter,
                item.editor,
                item.keyword,
                item.programStrategisName,
                item.eventName,
                item.MSatkerName,
                item.linkEdit,
                item.createdBy,
                item.createdDate,
                item.linkView,
                item.statusDoc,
                item.documentSite,
                item.userApprovals,
                item.trackingDocument,
                item.detilDocumentAccess,
                item.canDownloadPPt,
                item.typeDocument,
                item.listPenyusun,
                item.isSendDocument,
                item.isLinkedDocument,
                item.linkedDocumentId,
                getDocumentExtension(item.documentNameDisplay),
                getDocumentIcon(item.documentNameDisplay, item.isSendDocument),
                item.isEditDocumentPNIN
              )
            );
          }
          break;
        }
        default:
          break;
      }
    });

  return {
    list: documentList,
    info: pageInfo,
    isOwner: await mGetIsOwner(_idTask).then((response) => response),
  };
}

export function deleteDocumentPendukung(params): Promise<any> {
  if (params.isLinkedDocument) {
    return client.deleteTaskDocumentSupportGoldenCopyById({
      store: store,
      data: {
        id: params.linkedDocumentId,
      },
    });
  } else {
    return client.deleteTaskDocumentSupportById({
      store: store,
      data: {
        id: params.idDocument,
      },
    });
  }
}

export function deleteDocumentUtama(params): Promise<any> {
  return client.DeleteDocument({
    store: store,
    data: {
      documentName: params,
    },
  });
}

export function getDocumentDetail(_id, _type): Promise<any> {
  if (_type == "utama") {
    return client
      .GetTaskDocumentDetail({
        store: store,
        data: {
          id: _id,
        },
      })
      .then((response) => {
        switch (response.plainData.responseCode) {
          case "011000": {
            return response.plainData.responseData;
          }
          default: {
            return [];
          }
        }
      });
  } else {
    return client
      .GetTaskDocumentSupportDetail({
        store: store,
        data: {
          id: _id,
        },
      })
      .then((response) => {
        switch (response.plainData.responseCode) {
          case "011000": {
            return response.plainData.responseData;
          }
          default: {
            return [];
          }
        }
      });
  }
}

export function getDocumentDetailSupportPreview(_documentId): Promise<any> {
  return client
    .GetTaskDocumentSupportDetail({
      store: store,
      data: {
        id: _documentId,
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          // const filteredOject: Array<object> = [];

          return response.plainData.responseData;
        }
        default: {
          return [];
        }
      }
    });
}

export function getDocumentDetailMainPreview(_documentId): Promise<any> {
  return client
    .GetTaskDocumentDetail({
      store: store,
      data: {
        id: _documentId,
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          // const filteredOject: Array<object> = [];

          return response.plainData.responseData;
        }
        default: {
          return [];
        }
      }
    });
}

export function getDocumentDetailPreview(): Promise<any> {
  const route = useRoute();
  return client
    .GetTaskDocumentDetail({
      store: store,
      data: {
        id: route.params.documentId,
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          return response.plainData.responseData.data;
        }
        default: {
          return [];
        }
      }
    });
}

export function getDocumentAllDetail(_documentId) {
  return client
    .getTaskDocumentSupportViewByDocumentId({
      store: store,
      data: {
        id: _documentId,
      },
    })
    .then((response) => {
      return response.plainData;
    });
}

export function getMainDocumentAllDetail(_documentId) {
  return client
    .GetTaskDocumentByIdDocument({
      store: store,
      data: {
        id: _documentId,
      },
    })
    .then((response) => {
      return response.plainData;
    });
}

export function updateStepProgress(_documentId, _position): Promise<object> {
  return client
    .UpdateTaskDocumentSupportProgress({
      store: store,
      data: {
        id: _documentId,
        idMDocumentSupportStep: _position,
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          return {
            message: response.plainData.responseData.description,
            status: true,
          };
        }
        default: {
          return {
            message: "Something went wrong",
            status: false,
          };
        }
      }
    });
}

function getDocumentIcon(value, isSendDocument): string {
  if (isSendDocument) {
    switch (getDocumentExtension(value)) {
      case "pdf": {
        return "/images/docImage/send-other-wp-pdf.svg";
      }
      case "doc":
      case "docx":
        return "/images/docImage/send-other-wp-doc.svg";
      case "xls":
      case "xlsx":
        return "/images/docImage/send-other-wp-xls.svg";
      case "ppt":
      case "pptx":
        return "/images/docImage/send-other-wp-pptx.svg";
      default:
        return "";
    }
  } else {
    switch (getDocumentExtension(value)) {
      case "pdf": {
        return "/images/docImage/iconPdf.png";
      }
      case "doc":
      case "docx":
        return "/images/docImage/iconDoc.png";
      case "xls":
      case "xlsx":
        return "/images/docImage/iconExcel.png";
      case "ppt":
      case "pptx":
        return "/images/docImage/iconPpt.png";
      default:
        return "";
    }
  }
}
export function getDocumentDetailIkuIck(_documentId): Promise<any> {
  return client
    .GetDetailDocumentIkuIck({
      store: store,
      data: {
        id: _documentId,
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          return response.plainData.responseData;
        }
        default: {
          return [];
        }
      }
    });
}

function getDocumentExtension(value): string {
  const temp = value.split(".");
  return temp[temp.length - 1];
}
