import client from "@/library/ApiClient";
import store from "@/store/index";
import { useRoute } from "vue-router";

export function mListSatker() {
  return client
    .MSatkerPembuat({
      store: store,
      data: { username: store.state.username },
    })
    .then((response) => {
      return response.plainData.responseData;
    });
}

export function mProsesBisnis() {
  return client
    .MBusinessProcess({
      store: store,
      data: { username: store.state.username },
    })
    .then((response) => {
      return response.plainData.responseData;
    });
}

export function mProgramStrategis() {
  return client
    .MProgramStrategis({
      store: store,
      data: { username: store.state.username },
    })
    .then((response) => {
      return response.plainData.responseData;
    });
}

export function mSifatDokumen() {
  return client
    .MClassification({
      store: store,
      data: { username: store.state.username },
    })
    .then((response) => {
      return response.plainData.responseData;
    });
}

export function mEventName() {
  return client
    .MEvent({
      store: store,
      data: { username: store.state.username },
    })
    .then((response) => {
      return response.plainData;
    });
}

export function mListPenyusun() {
  const route = useRoute();
  return client
    .getListTaskMemberTypeByIdTask({
      store: store,
      data: {
        username: store.state.username,
        idTasks: route.params.taskId,
        memberType: "penyusun",
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          return response.plainData.responseData;
        }
        default: {
          return [{}];
        }
      }
    });
}

export function mDocumentTypeApproval() {
  return client
    .GetDocumentSupportTypeForApproval({
      store: store,
    })
    .then((response) => {
      return response.plainData;
    });
}

export function mListTaskMemberExcludeGroupMember() {
  const route = useRoute();
  return client
    .getListTaskMemberTypeByIdTask({
      store: store,
      data: {
        username: store.state.username,
        idTasks: route.params.taskId,
        memberType: "penyusun",
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          const filter: Array<object> = [];
          response.plainData.responseData.filter((element) => {
            if (element.groupName == "") {
              filter.push(element);
            }
          });
          return filter;
        }
        default: {
          return [{}];
        }
      }
    });
}

export function mGetTaskDocumentSupportEditByIdDocument(_id) {
  return client
    .getTaskDocumentSupportEditByIdDocument({
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
          return [{}];
        }
      }
    });
}

export function mGetDocumentTypeForApproval() {
  return client
    .GetDocumentTypeForApproval({
      store: store,
    })
    .then((response) => {
      return response.plainData;
    });
}

export function mGetDocumentTypeForNonApproval() {
  return client
    .GetAllDocumentType({
      store: store,
    })
    .then((response) => {
      return response.plainData;
    });
}

export function mGetDocumentSupportTypeByIdMethod(_id, _idTaskTemplate) {
  return client
    .GetDocumentSupportTypeByIdMethod({
      store: store,
      data: {
        id: _id,
        idTaskTemplate: _idTaskTemplate,
      },
    })
    .then((response) => {
      return response.plainData;
    });
}

export function mGetDocumentSupportMethod() {
  return client
    .getDocumentSupportMethod({
      store: store,
    })
    .then((response) => {
      return response.plainData;
    });
}
