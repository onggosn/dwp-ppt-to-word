<template>
  <v-sheet class="mx-10 bg-transparent">
    <v-row
      v-if="!searchMode"
      class="home-banner mt-4 ml-5 mr-5 white--text"
      style="border-radius: 15px; position: relative"
    >
      <!-- Red gradient overlay -->
      <div class="banner-overlay"></div>

      <v-col
        cols="12"
        class="pa-1 ml-8 pa-md-4 ml-md-5"
        style="position: relative; z-index: 2"
      >
        <p class="text-h5 fw600 text-md-h5 mt-md-2 mt-5">History</p>
        <p class="text-subtitle-sm-1 mr-4 mr-md-0">
          You can view your workspace, task and document old dwp in this page!
        </p>
      </v-col>
    </v-row>

    <div v-if="!searchMode" class="d-flex justify-end mr-5 mt-5">
      <DownloadButton>Download</DownloadButton>

      <FilterButton @update="updateFilter"></FilterButton>
      <SortingButton
        class="mt-4 mr-3 rounded-lg"
        :items="sortType"
        @update="updateSort"
      />

      <SearchButton class="rounded-lg" @update="handleSearch" />
    </div>
    <div class="mx-5">
      <p v-if="!searchMode" class="text-gradient-blue text-18">
        List Workspace
      </p>
      <div v-if="!list?.length && !isLoading" class="empty-illustration">
        <img
          :src="require('@/v2/assets/empty/no_available_state.svg')"
          class="img-no-available"
        />
      </div>
      <template v-else>
        <list-item :list="list" :loading="isLoading" />

        <div class="text-center">
          <v-pagination
            v-model="page"
            :length="pagination.totalPage"
            :total-visible="10"
            @update:modelValue="changePage()"
          ></v-pagination>
        </div>
      </template>
    </div>
  </v-sheet>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref, nextTick, computed, watch } from "vue";
import { assign } from "lodash";
import ListItem from "@/v2/components/history/ListHistoryContent.vue";
import SortingButton from "@/v2/components/admin/sort/SortingButton.vue";
import FilterButton from "@/v2/components/admin/FilterButton.vue";
import DownloadButton from "@/v2/components/history/download/ButtonDownload.vue";
import { TListSortingType } from "@/v2/Type";
import SearchButton from "@/v2/components/search/SearchButton.vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { TInfoPage } from "@/v2/Type";

const store = useStore();

const page = ref(1);
const list = ref([]);
const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);

const isLoading = ref(false);
const pagination = ref<TInfoPage>({
  totalData: 0,
  prevPageNo: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});

const router = useRouter();
const route = useRoute();
const itemFilter = computed(() => store.getters["historyStore/getItemsFilter"]);

watch([() => store.getters["globalStore/getSearch"]], () => {
  pagination.value.pageNo = 1;
  getList();
});

const changePage = () => {
  getList(page.value);
};

watch(
  [() => itemFilter],
  () => {
    getList();
  },
  { deep: true }
);

const getList = (pageNumber = 1) => {
  isLoading.value = true;
  const payload = {
    pageSize: 10,
    page: pageNumber,
    search: searchMode.value
      ? searchValue.value == null
        ? ""
        : searchValue.value
      : "",
    workspaceType: itemFilter.value?.workspaceType ?? [],
    monthPeriod: itemFilter.value?.monthPeriod ?? [],
    yearPeriod: itemFilter.value?.yearPeriod ?? [],
    status: itemFilter.value?.status ?? [],
    sortBy: Number(route.query.eventSort) ?? 1,
  };

  store
    .dispatch("historyStore/getHistoryList", payload)
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
};

const sortType = reactive<TListSortingType[]>([
  {
    id: 0,
    value: "Newest - Oldest",
  },
  {
    id: 1,
    value: "Oldest - Newest",
  },
]);

async function updateSort(sortId: number) {
  await router.replace({
    query: assign({}, route.query, {
      eventSort: String(sortId),
    }),
  });

  nextTick(() => {
    page.value = 1;
    getList();
  });
}
function updateFilter(item) {
  store.commit("historyStore/setItemsFilter", item);
}

function handleSearch(item: boolean) {
  router.push({ name: "v2-history-search" });
  store.commit("globalStore/setStatusSearch", item);
}

onMounted(() => {
  if (route.path.includes("search")) {
    store.commit("globalStore/setStatusSearch", true);
  } else {
    store.commit("globalStore/setSearch", "");
    store.commit("globalStore/setStatusSearch", false);
  }
  getList();
});
</script>

<style scoped>
.home-banner {
  max-width: 100%;
  background-image: url("@/v2/assets/batik/pola-batik.png");
  background-repeat: repeat;
  background-size: contain;
  height: 100px;
  border-radius: 20px;
}

.banner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.9;
  background-image: url("@/v2/assets/batik/bg-gradient-history.jpg");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  border-radius: 15px;
  z-index: 1;
}

.white--text {
  color: white;
}
.fw600 {
  color: white;
  font-weight: 600;
  margin-top: 10px;
  letter-spacing: 1px;
}
.select-empty {
  cursor: pointer;
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
  width: 40px;
  height: 40px;
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

:deep(.v-tab .v-btn__content) {
  font-size: 13px;
  font-weight: 900;
  background: -webkit-linear-gradient(#065695, #267dc2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

:deep(.v-tab--selected .v-btn__content) {
  background: -webkit-linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

:deep(.v-tab__slider) {
  background: #ff000d;
}

:deep(.btn-dropdown) {
  margin-top: 16px;
  margin-right: 10px;
}

.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
</style>
