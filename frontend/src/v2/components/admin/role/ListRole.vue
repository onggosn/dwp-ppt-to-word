<template>
  <div class="d-flex justify-space-between align-center">
    <p
      v-if="!searchMode"
      class="font-weight-bold mb-3"
      style="font-size: 18px; color: #065695"
    >
      List Role
    </p>
  </div>

  <v-row v-if="isLoading">
    <v-col v-for="i in 7" :key="i" cols="12">
      <free-style-shimmer
        width="100%"
        height="40px"
        border-radius="10px"
        color="#d3d3d3"
      />
    </v-col>
  </v-row>

  <template v-if="!isLoading">
    <list-item
      v-for="(item, idx) in list"
      :is-loading="isLoading"
      :key="idx"
      class="mt-5"
      :item="item"
    ></list-item>
  </template>

  <div class="text-center mt-7">
    <v-pagination
      v-if="list?.length && !isLoading"
      rounded="1"
      elevation="2"
      size="small"
      v-model="currentPage"
      :length="pagination.totalPage"
      :total-visible="10"
      @update:model-value="changePage"
    />
  </div>

  <div v-if="!list?.length && !isLoading" class="empty-illustration">
    <img
      :src="require('@/v2/assets/empty/no_available_state.svg')"
      class="img-no-available"
    />
  </div>
</template>

<script setup lang="ts">
import { TWorkspaceRDGL, TInfoPage } from "@/v2/Type";
import { ref, onMounted, watch, computed } from "vue";
import { useStore } from "vuex";
import ListItem from "@/v2/components/admin/role/ListRoleMeeting.vue";
import { useRoute } from "vue-router";

const store = useStore();
const route = useRoute();

const list = ref<TWorkspaceRDGL[]>([]);
const pagination = ref<TInfoPage>({
  totalData: 0,
  prevPageNo: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});
const isLoading = ref<boolean>(false);
const currentPage = ref<number>(1);
const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const filterValue = computed(() => store.getters["adminStore/getItemsFilter"]);
const refreshList = computed(() => store.getters["adminStore/getRefreshList"]);

function getList() {
  store.commit("documentStore/setOnLoadingButtonState", true);
  isLoading.value = true;
  let payload = {
    roleSearching: searchMode.value
      ? searchValue.value == null
        ? ""
        : searchValue.value
      : "",
    sortBy: searchMode.value
      ? 0
      : parseInt((route.query.eventSort as string) ?? 0),
    satkerFilter: searchMode.value ? [] : filterValue.value.satkerFilter || [],
    gradeFilter: searchMode.value ? [] : filterValue.value.gradeFilter || [],
    pageSize: pagination.value.entriesPerPage,
    pageNumber: pagination.value.pageNo,
  };

  store
    .dispatch("adminStore/getRoleList", payload)
    .then((res: any) => {
      list.value = res.responseData?.data;
      pagination.value.pageNo = res.responseData.infoPage?.pageNo ?? 1;
      pagination.value.totalData = res.responseData.infoPage?.totalData ?? 10;
      pagination.value.totalPage = res.responseData.infoPage?.totalPage ?? 10;
      const totalData = res.responseData.infoPage?.totalData;
      const totalDataPerPage = res.responseData.data?.length || 0;
      store.commit("globalStore/setTotalData", totalData);
      store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function changePage(curr: number) {
  pagination.value.pageNo = curr;
  getList();
}

watch([route, refreshList], () => {
  getList();
});

watch(
  () => JSON.stringify(filterValue.value),
  (newValue, oldValue) => {
    if (!searchMode.value && newValue !== oldValue) {
      pagination.value.pageNo = 1;
      currentPage.value = 1;
      getList();
    }
  }
);

watch(
  () => searchValue.value,
  () => {
    if (searchMode.value) {
      pagination.value.pageNo = 1;
      currentPage.value = 1;
      getList();
    }
  },
  { deep: true }
);

onMounted(() => {
  getList();
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
