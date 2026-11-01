import { ref } from "vue";
import { useStore } from "vuex";

export function useCreatePNINAPI() {
  const store = useStore();

  // Loading states
  const isLoading = ref(false);
  const loadingList = ref(false);

  // Data lists
  const listEventType = ref([]);
  const listRDGType = ref([]);
  const listRDG = ref([]);
  const sectorList = ref([]);

  // API calls
  const fetchEventTypes = async () => {
    try {
      const data = await store.dispatch("eventStore/fetchListEventType");
      listEventType.value = data;
      return data;
    } catch (error) {
      console.error("Error fetching event types:", error);
      throw error;
    }
  };

  const fetchRDGTypes = async (req: { sectorName: string }) => {
    try {
      const data = await store.dispatch(
        "eventStore/fetchMEventSubTypeList",
        req
      );
      listRDGType.value = data;
      return data;
    } catch (error) {
      console.error("Error fetching RDG types:", error);
      throw error;
    }
  };

  const fetchRDGList = async (payload: {
    rdgType: any;
    month: any;
    year: any;
    BPName: string;
  }) => {
    try {
      listRDG.value = [];
      const data = await store.dispatch(
        "eventStore/fetchEventSubTypeListByEventId",
        payload
      );
      listRDG.value = data;
      return data;
    } catch (error) {
      console.error("Error fetching RDG list:", error);
      throw error;
    }
  };

  const fetchSectorPNINList = async (idBP: any) => {
    try {
      const data = await store.dispatch("contentStore/getSectorPNINList", idBP);
      sectorList.value = data;
      return data;
    } catch (error) {
      console.error("Error fetching sector PNIN list:", error);
      throw error;
    }
  };

  const fetchSectionList = async (req: { idSector: any; idBP: any }) => {
    try {
      loadingList.value = true;
      store.commit("contentStore/setSectionList", []);
      await store.dispatch("contentStore/getSectionList", req);
    } catch (error) {
      console.error("Error fetching section list:", error);
      throw error;
    } finally {
      loadingList.value = false;
    }
  };

  const createPNINCustom = async (req: {
    idBP: any;
    idSector: any;
    listOutput: any[];
  }) => {
    try {
      isLoading.value = true;
      const data = await store.dispatch("contentStore/createPNINCustom", req);
      return data;
    } catch (error) {
      console.error("Error creating PNIN custom:", error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  // Reset function
  const resetAPIData = () => {
    listEventType.value = [];
    listRDGType.value = [];
    listRDG.value = [];
    sectorList.value = [];
  };

  return {
    // Loading states
    isLoading,
    loadingList,

    // Data
    listEventType,
    listRDGType,
    listRDG,
    sectorList,

    // API methods
    fetchEventTypes,
    fetchRDGTypes,
    fetchRDGList,
    fetchSectorPNINList,
    fetchSectionList,
    createPNINCustom,
    resetAPIData,
  };
}
