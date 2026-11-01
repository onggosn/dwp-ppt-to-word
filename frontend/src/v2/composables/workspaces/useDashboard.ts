import { ref, computed, reactive, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import { TAssignmentsState } from "@/v2/Type";

const useDashboard = () => {
  const route = useRoute();
  const store = useStore();

  const isLoading = ref(false);
  const isInitialLoad = ref<boolean>(true);
  const workspace = reactive<TAssignmentsState>({
    list: [],
    pagination: {
      page: 1,
      total: 0,
      visible: 10,
    },
  });
  const sorting = computed(() => store.getters["documentsStore/getItemsSort"]);
  const searchMode = computed(
    () => store.getters["globalStore/getStatusSearch"]
  );
  const searchValue = computed(() => store.getters["globalStore/getSearch"]);

  const filterValue = computed(
    () => store.getters["assignmentStore/getItemsFilter"]
  );

  const itemsFilter = computed(
    () => store.getters["assignmentStore/getDashboardItemsSort"]
  );

  const fetchDashboardSort = async () => {
    await store.dispatch("assignmentStore/getDashboardSort");
  };

  const fetchWorkspace = async () => {
    isLoading.value = true;

    const requestData = {
      idStatus: filterValue.value.idStatus ?? [],
      idMeventSubTypeList: filterValue.value.idMeventSubTypeList ?? [],
      sortType: sorting.value.sortType ?? "",
      sortName: sorting.value.sortName ?? "",
      searchEventName: searchMode.value ? searchValue.value : "",
      pageNumber: workspace.pagination.page,
      pageSize: workspace.pagination.visible,
    };

    await store
      .dispatch("documentsStore/GetListWorkspace", requestData)
      .then((resp) => {
        const result = resp?.responseData ?? {};
        workspace.pagination.total = result.infoPage?.totalPage ?? 0;
        workspace.list = (result.data ?? []).map((e: any) => ({
          listId: e.idEvent,
          listName: e.eventName,
          statusName: e.status,
          ...e,
        }));
        const totalData = result.infoPage?.totalData;
        const totalDataPerPage = result.data?.length || 0;
        store.commit("globalStore/setTotalData", totalData);
        store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
      })
      .finally(() => {
        isLoading.value = false;
      });
  };

  const reloadPage = () => {
    workspace.pagination.page = 1;
    fetchWorkspace();
  };

  watch(
    () => sorting.value,
    () => {
      if (route.name === "dashboard.workspace.v2") {
        reloadPage();
      }
    }
  );

  watch(
    () => JSON.stringify(filterValue.value),
    (newValue, oldValue) => {
      if (!searchMode.value && newValue !== oldValue) {
        reloadPage();
      }
    }
  );

  watch(
    () => searchValue.value,
    () => {
      if (searchMode.value) {
        reloadPage();
      }
    },
    { deep: true }
  );

  onMounted(() => {
    fetchWorkspace();
    fetchDashboardSort();
  });

  return {
    isLoading,
    isInitialLoad,
    sorting,
    workspace,
    itemsFilter,
    fetchWorkspace,
    fetchDashboardSort,
    reloadPage,
  };
};

export default useDashboard;
