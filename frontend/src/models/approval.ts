import client from "@/library/ApiClient";
import store from "@/store/index";

export async function mGetApprovalButton(_id) {
  return client
    .GetListFlowDetailSupportbyTaskDocumentId({
      store: store,
      data: {
        id: _id,
      },
    })
    .then((response) => {
      return response.plainData;
    });
}

export async function mApproveDocumentSupport(item, documentId) {
  return client
    .ApproveDocumentSupport({
      store: store,
      data: {
        idMDocumentApprovalFlow: item.idMDocumentSupportApprovalFlow,
        idDocumentSupportType: item.idDocumentSupportType,
        username: store.state.username,
        IdDocumentSupportApprovalCurrent: item.IdDocumentSupportApprovalCurrent,
        IdDocumentSupportApprovalNext: item.IdDocumentSupportApprovalNext,
        approvalDocumentSupportId: item.approvalSupportDocumentId,
        description: item.description,
        taskDocumentId: documentId,
        comment: "",
        traceId: "",
      },
    })
    .then((response) => {
      return response.plainData;
    })
    .finally(() => {
      undefined;
    });
}
