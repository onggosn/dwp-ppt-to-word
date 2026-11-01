<template>
  <v-sheet class="bg-transparent ml-5 px-7 py-10">
    <v-row>
      <v-col cols="9">
        <v-sheet class="d-flex flex-row align-start bg-transparent">
          <v-btn icon="mdi-arrow-left" elevation="0" @click="back"></v-btn>
          <div style="margin-left: 30px; padding-top: 12px">
            <p
              style="
                color: #3a416f;
                font-size: 32px;
                font-weight: 600;
                line-height: 23px;
              "
            >
              RDGM
            </p>
            <p style="color: #4b4b4b; margin-top: 15px">
              Search results displayed
              {{ list.length }}
              (total relevant results {{ pagination.totalData }})
            </p>
          </div>
        </v-sheet>
      </v-col>
      <v-col cols="3">
        <v-text-field
          v-model="keyword"
          density="compact"
          hide-details="auto"
          clearable
          @click:clear="store.commit('omWorkspaceStore/setSearchRDGM', '')"
          placeholder="Search"
          variant="solo"
          @keyup.enter="getList(keyword)"
          :autofocus="true"
        >
          <template v-slot:prepend-inner>
            <img src="/images/task/searchMagnifier.svg" /></template
        ></v-text-field>
      </v-col>
    </v-row>
    <rdgm-list
      :isLoading="isLoading"
      :items="list"
      class="mt-11"
      @change-page="changePage"
    ></rdgm-list>
    <div class="text-center mt-7">
      <v-pagination
        v-if="list.length > 0"
        rounded="1"
        elevation="2"
        size="small"
        v-model="currentPage"
        :length="pagination.totalPage"
        :total-visible="10"
        @update:model-value="changePage"
      ></v-pagination>
    </div>
    <template v-if="!isLoading && list.length === 0">
      <div class="empty-illustration">
        <img
          :src="require('@/v2/assets/empty/no_available_state.svg')"
          class="img-no-available"
        />
      </div>
    </template>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import {
  TWorkspaceRDG,
  TWorkspaceRDGL,
  TInfoPage,
} from "@/v2/modules/omPro/Type";
import RdgmList from "@/v2/modules/omPro/components/workspace/RDGMList.vue";

const searchRDGM = computed(
  () => store.getters["omWorkspaceStore/getSearchRDGM"]
);

const isLoading = ref<boolean>(false);

const router = useRouter();
const store = useStore();

const keyword = ref<string>(store.getters["omWorkspaceStore/getSearchRDGM"]);

const currentPage = ref<number>(1);
const list = ref<Array<TWorkspaceRDGL>>([]);
const pagination = ref<TInfoPage>({
  totalData: 0,
  prevPageNo: 0,
  pageNo: 1,
  nextPageNo: 2,
  totalPage: 1,
  entriesPerPage: 10,
});

const requestData = ref<TWorkspaceRDG>({
  pageSize: 10,
  page: pagination.value.pageNo,
  RDGType: "rdgm",
  username: store.state.username,
  eventSearching: searchRDGM.value,
  status: [],
  eventSubTypeListFilter: [],
  dateFilter: { year: [], month: [] },
});

function getList(query: string) {
  requestData.value.eventSearching = query ?? "";
  requestData.value.page = pagination.value.pageNo;
  isLoading.value = true;
  store
    .dispatch(
      "omWorkspaceStore/fetchListSuperEventByRDGByUsername",
      requestData.value
    )
    .then((res) => {
      list.value = res.data;
      pagination.value.pageNo = res.infoPage.pageNo;
      pagination.value.totalData = res.infoPage.totalData;
      pagination.value.totalPage = res.infoPage.totalPage;
    })
    .finally(() => {
      isLoading.value = false;
    });
}
function changePage(curr: number) {
  pagination.value.pageNo = curr;
  requestData.value.page = pagination.value.pageNo;
  getList(keyword.value);
}
function back() {
  store.commit("omWorkspaceStore/setSearchRDGM", "");
  const path = `/app/v2/workspace-management/rdgm`;
  router.push(path);
}

onBeforeMount(() => {
  getList(keyword.value);
});
</script>

<style scoped>
.empty-illustration {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
:deep(.v-field) {
  border-radius: 15px;
}
:deep(.v-input--horizontal) {
  display: contents;
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
