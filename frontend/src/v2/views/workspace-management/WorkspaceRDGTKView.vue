<template>
  <div class="d-flex justify-space-between align-center">
    <p class="font-weight-bold" style="font-size: 32px; color: #3a416f">
      RDGTK
    </p>
    <div class="d-flex flex-row align-center gc-5">
      <workspace-filter @onUpdateFilter="updateFilter"></workspace-filter>
      <workspace-search :type-search="'RDGTK'"></workspace-search>
    </div>
  </div>
  <workspace-list
    :isLoading="isLoading"
    :items="list"
    type="rdgtk"
    class="mt-11"
    @change-page="changePage"
  ></workspace-list>
  <div class="text-center mt-7">
    <v-pagination
      rounded="1"
      elevation="2"
      size="small"
      v-model="currentPage"
      :length="pagination.totalPage"
      :total-visible="10"
      @update:model-value="changePage"
    ></v-pagination>
  </div>
  <div v-if="!isLoading && list.length === 0" class="empty-illustration">
    <img
      :src="require('@/v2/assets/empty/no_available_state.svg')"
      class="img-no-available"
    />
  </div>
</template>

<script setup lang="ts">
import {
  TWorkspaceRDG,
  TWorkspaceRDGL,
  TWorkspaceRDGResponse,
  TInfoPage,
} from "@/v2/Type";
import { useRoute } from "vue-router";
import { ref, onBeforeMount } from "vue";
import { useStore } from "vuex";

import WorkspaceList from "@/v2/components/workspace/WorkspaceList.vue";
import WorkspaceSearch from "@/v2/components/workspace/WorkspaceSearch.vue";
import WorkspaceFilter from "@/v2/components/workspace/WorkspaceFilter.vue";

const route = useRoute();
const store = useStore();
const username = ref<string>(store.state.username);

const list = ref<Array<TWorkspaceRDGL>>([]);
const pagination = ref<TInfoPage>({
  totalData: 0,
  prevPageNo: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});
const isLoading = ref<boolean>(false);
const requestData = ref<TWorkspaceRDG>({
  pageSize: 10,
  page: pagination.value.pageNo,
  RDGType: "RDGTK",
  username: username.value,
  eventSearching: "",
  status: [],
  eventSubTypeListFilter: [],
  dateFilter: { year: [], month: [] },
});
const currentPage = ref<number>(1);

function changePage(curr: number) {
  pagination.value.pageNo = curr;
  requestData.value.page = pagination.value.pageNo;
  getList();
}

function getList() {
  isLoading.value = true;
  store
    .dispatch(
      "workspaceStore/fetchListSuperEventByRDGByUsername",
      requestData.value
    )
    .then((res: TWorkspaceRDGResponse) => {
      list.value = res.data;
      pagination.value.pageNo = res.infoPage.pageNo;
      pagination.value.totalData = res.infoPage.totalData;
      pagination.value.totalPage = res.infoPage.totalPage;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function updateFilter(filter: any) {
  Object.keys(filter).forEach((key) => {
    if (key == "rdg") {
      requestData.value.eventSubTypeListFilter = filter[key];
    } else if (key == "status") {
      requestData.value.status = filter[key];
    } else if (key == "year") {
      requestData.value.dateFilter.year = filter[key];
    } else if (key == "month" || key == "partialMonths") {
      requestData.value.dateFilter.month = filter[key];
    }
  });
  getList();
  store.commit("workspaceStore/setContentFilterCommit", filter);
}

onBeforeMount(() => {
  const filter = store.getters["workspaceStore/getContentFilterCommit"];
  const isUseFilter = parseInt(route.query.useFilter as string) == 1;
  if (isUseFilter && Object.keys(filter).length !== 0) {
    updateFilter(filter);
  } else {
    store.commit("workspaceStore/setContentFilterCommit", {});
    getList();
  }
});
</script>

<style scoped>
.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
:deep(.v-pagination__item--is-active) {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  border-radius: 10px;
}
:deep(.v-pagination .v-btn) {
  border-radius: 10px;
  font-size: 15px;
  font-weight: bold;
}
:deep(.v-pagination__item) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__next) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
:deep(.v-pagination__prev) {
  color: #065695;
  border-radius: 10px;
  background: white;
}
</style>
