<template>
  <div class="d-flex justify-space-between align-center">
    <p class="font-weight-bold mb-3" style="font-size: 18px; color: #065695">
      List FAQ
    </p>
  </div>

  <!-- Custom skeleton matching FAQ expansion panel layout -->
  <div v-if="isLoading" class="skeleton-list mt-2">
    <div
      v-for="i in 5"
      :key="i"
      class="skeleton-panel"
      :style="{ animationDelay: `${(i - 1) * 0.07}s` }"
    >
      <div class="skeleton-panel-body">
        <div class="sk-block sk-topic"></div>
        <div class="sk-block sk-meta"></div>
        <div class="sk-block sk-chevron"></div>
      </div>
    </div>
  </div>

  <template v-else>
    <list-item
      v-for="(item, idx) in list"
      :key="idx"
      class="mt-5"
      :item="item"
      :delay="`${idx * 0.07}s`"
      @refresh-topic-list="refreshTopicList"
    />
  </template>

  <div class="text-center mt-7">
    <v-pagination
      v-if="list.length && !isLoading"
      rounded="1"
      elevation="2"
      size="small"
      v-model="currentPage"
      :length="pagination.totalPage"
      :total-visible="10"
      @update:model-value="changePage"
    />
  </div>

  <div v-if="!list.length && !isLoading" class="empty-illustration">
    <img
      :src="require('@/v2/assets/empty/no_available_state.svg')"
      class="img-no-available"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, getCurrentInstance } from "vue";
import ListItem from "@/v2/components/admin/faq/ListFAQItem.vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

interface FAQItem {
  [key: string]: unknown;
}

interface FAQFilter {
  dateSince?: string | null;
  dateTo?: string | null;
  topicFilter?: string | null;
}

interface Pagination {
  totalData: number;
  pageNo: number;
  totalPage: number;
  entriesPerPage: number;
}

const store = useStore();
const route = useRoute();
const { root } = getCurrentInstance() as any;

const list = ref<FAQItem[]>([]);
const isLoading = ref(false);
const currentPage = ref(1);
const pagination = ref<Pagination>({
  totalData: 0,
  pageNo: 1,
  totalPage: 1,
  entriesPerPage: 10,
});

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const refreshList = computed(() => store.getters["adminStore/getRefreshList"]);
const filterValue = computed<FAQFilter>(
  () => store.getters["adminStore/getItemsFilter"]
);

function buildPayload() {
  return {
    CategoryFAQFilter: filterValue.value?.topicFilter ?? [],
    faqSearch: searchMode.value ? searchValue.value : "",
    sortBy: searchMode.value
      ? 0
      : parseInt((route.query.eventSort as string) ?? 0),
    startDate: filterValue.value?.dateSince ?? null,
    endDate: filterValue.value?.dateTo ?? null,
    page: pagination.value.pageNo,
    pageSize: pagination.value.entriesPerPage,
  };
}

async function getList() {
  isLoading.value = true;
  try {
    const res = await store.dispatch(
      "adminStore/getListTopics",
      buildPayload()
    );
    const { data, infoPage } = res.responseData;
    list.value = data ?? [];
    pagination.value.totalData = infoPage?.totalData ?? 0;
    pagination.value.totalPage = infoPage?.totalPage ?? 1;
    store.commit("globalStore/setTotalData", infoPage?.totalData);
    store.commit("globalStore/setTotalDataPerPage", data?.length ?? 0);
  } catch {
    root.refs.toast.show({
      message: "Failed to fetch faqs. Please try again later.",
      color: "error",
      timeout: 5000,
    });
  } finally {
    isLoading.value = false;
  }
}

async function refreshTopicList() {
  const res = await store.dispatch("adminStore/getListTopics", buildPayload());
  list.value = res.responseData?.data ?? [];
}

function changePage(page: number) {
  pagination.value.pageNo = page;
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

/* ── Skeleton panels ────────────────────────────── */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-panel {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  padding: 0 16px;
  height: 60px;
  display: flex;
  align-items: center;
  animation: fadeSlideUp 0.4s ease-out both;
}

.skeleton-panel-body {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 12px;
}

/* col-6 topic name */
.sk-topic {
  flex: 1;
  height: 13px;
  border-radius: 6px;
  background: #e8e8e8;
  max-width: 48%;
  position: relative;
  overflow: hidden;
}

/* col-6 metadata (last modified) */
.sk-meta {
  flex: 1;
  height: 12px;
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
}

.sk-chevron {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
  margin-left: auto;
}

/* Shimmer sweep */
.sk-topic::after,
.sk-meta::after,
.sk-chevron::after {
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
.sk-meta::after {
  animation-delay: 0.12s;
}
.sk-chevron::after {
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
