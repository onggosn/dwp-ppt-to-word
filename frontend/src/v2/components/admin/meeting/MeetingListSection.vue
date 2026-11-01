<template>
  <p
    v-if="!searchMode"
    class="font-weight-bold mb-3 mt-3"
    style="font-size: 18px; color: #065695"
  >
    List Meeting
  </p>

  <div class="">
    <!-- Custom skeleton matching expansion panel layout -->
    <div v-if="isLoading" class="skeleton-list">
      <div
        v-for="i in 5"
        :key="i"
        class="skeleton-panel"
        :style="{ animationDelay: `${(i - 1) * 0.07}s` }"
      >
        <div class="skeleton-panel-body">
          <div class="skeleton-title"></div>
          <div class="skeleton-chip"></div>
          <div class="skeleton-chevron"></div>
        </div>
      </div>
    </div>

    <template v-if="!isLoading">
      <list-item
        v-for="(item, idx) in list"
        :is-loading="isLoading"
        :key="idx"
        class="mt-5"
        :item="item"
        :delay="`${idx * 0.07}s`"
        @on-delete-meeting="getList"
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
  </div>
</template>

<script setup lang="ts">
import { TWorkspaceRDGL, TInfoPage } from "@/v2/Type";
import { ref, onMounted, watch, computed } from "vue";
import ListItem from "@/v2/components/admin/meeting/ListMeetingItem.vue";
import { useStore } from "vuex";
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
    eventSearching: searchMode.value
      ? searchValue.value
        ? searchValue.value
        : ""
      : "",
    sortBy: searchMode.value
      ? 0
      : parseInt((route.query.eventSort as string) ?? 0),
    orderBy: "",
    eventSubTypeListFilter: searchMode.value
      ? [1, 2, 3, 4, 6]
      : filterValue.value.eventSubTypeListFilter || [1, 2, 3, 4, 6],
    bp: searchMode.value ? [] : filterValue.value.bp || [],
    dateSince: searchMode.value
      ? null
      : filterValue.value.dateSince === ""
      ? null
      : filterValue.value.dateSince,
    dateTo: searchMode.value
      ? null
      : filterValue.value.dateTo === ""
      ? null
      : filterValue.value.dateTo,
    pageSize: pagination.value.entriesPerPage,
    page: pagination.value.pageNo ?? 1,
  };

  store
    .dispatch("adminStore/getMeetingList", payload)
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

/* ── Skeleton panels ────────────────────────────── */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.skeleton-panel {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  margin-bottom: 16px;
  padding: 0 16px;
  height: 60px;
  display: flex;
  align-items: center;

  /* staggered fade-in */
  animation: fadeSlideUp 0.4s ease-out both;
}

.skeleton-panel-body {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 12px;
}

.skeleton-title {
  flex: 1;
  height: 13px;
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  max-width: 58%; /* mirrors col-7 */
}

.skeleton-chip {
  width: 90px;
  height: 26px;
  border-radius: 999px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
}

.skeleton-chevron {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  margin-left: auto;
}

/* Sweep shimmer on every skeleton block */
.skeleton-title::after,
.skeleton-chip::after,
.skeleton-chevron::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.7) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}
.skeleton-chip::after {
  animation-delay: 0.12s;
}
.skeleton-chevron::after {
  animation-delay: 0.24s;
}

@keyframes shimmerSweep {
  from {
    background-position: -200% 0;
  }
  to {
    background-position: 200% 0;
  }
}

/* Entrance — uses translate so hover transform is never blocked */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    translate: 0 16px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
