import clientv2 from "@/v2/library/ApiClient";

async function fetchData(commit, apiCall, requestData, keyToStore) {
  commit("setLoading", true);
  try {
    const res = await apiCall(requestData);

    const toIgnore = [
      "meetingPlatform",
      "insertEvent",
      "deleteEvent",
      "UpdateEvent",
    ];
    if (toIgnore.includes(keyToStore)) {
      commit("setLoading", false);
      return res;
    }

    const dataToUpdate = {};

    dataToUpdate[keyToStore] = res.responseData;
    switch (res.responseCode) {
      case "011000": //code for success
        commit("setData", dataToUpdate);
        commit("setLoading", false);
        if (res.responseData) {
          return res.responseData;
        } else {
          return true;
        }
      default: // code for empty data
        commit("setData", {});
        commit("setLoading", false);
        return res;
    }
  } catch (err) {
    commit("setError", err);
    commit("setLoading", false);

    if (keyToStore === "updateEvent") {
      return err;
    }
    return {};
  }
}

export default {
  namespaced: true,
  state: {
    count: 0,
    data: new Map(),
    loading: false,
    loadingProgress: 0,
    error: null,
  },
  getters: {
    getData: (state: any) => {
      return state.data;
    },
    getLoading: (state: any) => {
      return state.loading;
    },
  },
  mutations: {
    setData(state: any, newData: any) {
      state.data = newData;
    },
    setLoading(state: any, isLoading: boolean) {
      state.loading = isLoading;
    },
    setError(state: any, error: any) {
      state.error = error;
    },
  },
  actions: {
    async fetchListEventType({ commit }) {
      const reqParams = {};
      return await fetchData(
        commit,
        clientv2.getListEventType,
        reqParams,
        "eventType"
      );
    },
    async fetchListSubEventType({ commit }, id) {
      const reqParams = {
        data: {
          idEventType: id,
        },
      };
      return await fetchData(
        commit,
        clientv2.getEventSubTypeByEventTypeId,
        reqParams,
        "eventSubType"
      );
    },
    async fetchListSubSubEventType({ commit }, id) {
      const reqParams = {
        data: {
          idSubEventType: id,
        },
      };
      return await fetchData(
        commit,
        clientv2.getEventSubTypeListByEventSubTypeId,
        reqParams,
        "eventSubSubType"
      );
    },
    async insertEvent({ commit }, event) {
      const reqParams = {
        data: { ...event },
      };
      const result = await fetchData(
        commit,
        clientv2.insertEvent,
        reqParams,
        "insertEvent"
      );

      if (result.responseCode === "011004") {
        return {
          message: result.responseMessage,
          color: "error",
          timeout: 3000,
        };
      }

      return result;
    },
    async fetchHighlightEvent({ commit }) {
      const result = await fetchData(
        commit,
        clientv2.getTop3EventByUser,
        {},
        "top3Events"
      );
      return result;
    },
    async fetchEditEventData({ commit }, idEvent) {
      const reqParams = {
        data: {
          // idEvent: "77860307-865C-4B13-A9DB-77D4726F179F",
          idEvent: idEvent,
        },
      };
      return await fetchData(
        commit,
        clientv2.getEventDetailByIdEventEdit,
        reqParams,
        "editEventData"
      );
    },
    async fetchListMeetingMethod({ commit }) {
      const reqParams = {};
      return await fetchData(
        commit,
        clientv2.getEventMethod,
        reqParams,
        "eventMethod"
      );
    },
    async fetchListMeetingPlatform({ commit }) {
      const reqParams = {};
      return await fetchData(
        commit,
        clientv2.getMeetingPlatform,
        reqParams,
        "meetingPlatform"
      );
    },
    async popUpUpdateEvent({ commit }, event) {
      const reqParams = {
        data: { ...event },
      };
      const response = await fetchData(
        commit,
        clientv2.popUpUpdateEvent,
        reqParams,
        "popUpUpdateEvent"
      );

      return response;
    },
    async updateEvent({ commit }, event) {
      const reqParams = {
        data: { ...event },
      };
      const response = await fetchData(
        commit,
        clientv2.updateEvent,
        reqParams,
        "updateEvent"
      );

      return response;
    },
    async fetchTop10DocByUser({ commit }) {
      const reqParams = {
        data: {},
      };
      return await fetchData(
        commit,
        clientv2.getTop10DocByUser,
        reqParams,
        "top10Docs"
      );
    },
    /* FETCH LIST RDG TYPE CREATE RDG LAINNYA */
    async fetchMEventSubTypeList({ commit }, req) {
      const reqParams = {
        data: {
          sectorName: req.sectorName,
        },
      };

      return await fetchData(
        commit,
        clientv2.getMEventSubTypeList,
        reqParams,
        "listRDGTypeLainnya"
      );
    },
    /* FETCH LIST RDG CREATE RDG LAINNYA */
    async fetchEventSubTypeListByEventId({ commit }, req) {
      const reqParams = {
        data: {
          rDGType: req.rdgType,
          month: req.month,
          year: req.year,
          BPName: req.BPName,
        },
      };

      return await fetchData(
        commit,
        clientv2.getEventSubTypeListByEventId,
        reqParams,
        "listRDGLainnya"
      );
    },
    /* FETCH LIST EVENT CREATE RDG LAINNYA */
    async fetchEventbySubTypeListId({ commit, rootState }, req) {
      const reqParams = {
        data: {
          username: rootState.username,
          idEvent: req.idEvent,
        },
      };

      return await fetchData(
        commit,
        clientv2.getEventbySubTypeListId,
        reqParams,
        "listEventLainnya"
      );
    },
    /* POST CREATE RDG LAINNYA */
    async insertEventOthers({ commit }, req) {
      const reqParams = {
        data: { ...req },
      };

      const response = await fetchData(
        commit,
        clientv2.addEventOthers,
        reqParams,
        "insertEventOthers"
      );
      return response;
    },
    /* DELETE MEETING RDG LAINNYA */
    async deleteEvent({ commit }, event) {
      const reqParams = {
        data: { idEvent: event.id },
      };

      const response = await fetchData(
        commit,
        clientv2.deleteEventById,
        reqParams,
        "deleteEvent"
      );
      return response;
    },
    /* GET LINK BUKU DIGITAL MATERIAL */
    async getLinkMaterial({ commit }, event) {
      const reqParams = {
        data: { idEvent: event.id },
      };

      const response = await fetchData(
        commit,
        clientv2.getLinkMaterial,
        reqParams,
        "getLinkMaterial"
      );
      return response;
    },
    /* GET DROPDOWN CREATE */
    async getDropdownCreate({ commit }) {
      const reqParams = {};
      return await fetchData(
        commit,
        clientv2.getDropdownCreate,
        reqParams,
        "dropdownCreate"
      );
    },
    /* PUBLISH EVENT */
    async publishEvent({ commit }, event) {
      const reqParams = {
        data: { idEvent: event.id },
      };

      const response = await fetchData(
        commit,
        clientv2.publishEvent,
        reqParams,
        "popUpPublishEvent"
      );
      return response;
    },
    /* CANCEL EVENT */
    async cancelEvent({ commit }, event) {
      const reqParams = {
        data: { idEvent: event.id },
      };

      const response = await fetchData(
        commit,
        clientv2.cancelEvent,
        reqParams,
        "popUpCancelEvent"
      );
      return response;
    },
  },
};
