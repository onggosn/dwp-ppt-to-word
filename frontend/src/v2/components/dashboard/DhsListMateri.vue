<template>
  <!-- Custom skeleton matching table card layout -->
  <template v-if="isLoading">
    <div class="skeleton-card">
      <!-- header bar -->
      <div class="skeleton-header">
        <div class="sk-block sk-header-title"></div>
      </div>
      <!-- table rows -->
      <div class="skeleton-table">
        <div class="skeleton-thead">
          <div class="sk-th" v-for="c in 6" :key="c"></div>
        </div>
        <div
          v-for="n in 6"
          :key="n"
          class="skeleton-row"
          :style="{ animationDelay: `${(n - 1) * 0.07}s` }"
        >
          <div class="sk-block sk-cell-no"></div>
          <div class="sk-block sk-cell-name"></div>
          <div class="sk-block sk-cell-ws"></div>
          <div class="sk-block sk-cell-event"></div>
          <div class="sk-block sk-cell-status"></div>
          <div class="sk-block sk-cell-action"></div>
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div v-if="documents.list.length === 0">
      <img
        src="/images/assignment/empty-assignment.png"
        style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
      />
      <div
        class="text-center text-18 fw-600 text-grayTheme-gradien font-italic mt-4"
      >
        No Assignment Available...
      </div>
    </div>
    <div v-else>
      <dashboard-row-component-table
        :item="documents.list"
        :page="documents.pagination.page"
        type="default"
      ></dashboard-row-component-table>
      <div class="text-center">
        <v-pagination
          rounded="1"
          elevation="2"
          size="small"
          v-model="documents.pagination.page"
          :length="documents.pagination.total"
          :total-visible="documents.pagination.visible"
          @update:modelValue="fetchDocuments"
        />
      </div>
    </div>
  </template>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { isNotEmptyObject } from "@/v2/helpers/utils";
import { TDocumentsState } from "@/v2/Type";

import DashboardRowComponentTable from "@v2/components/dashboard/DashboardRowComponentTable.vue";

const route = useRoute();
const store = useStore();

const isLoading = ref(false);
const documents = reactive<TDocumentsState>({
  list: [],
  pagination: {
    page: 1,
    total: 0,
    visible: 10,
  },
});

const searchMode = computed(() => store.getters["globalStore/getStatusSearch"]);
const searchValue = computed(() => store.getters["globalStore/getSearch"]);
const filterValue = computed(
  () => store.getters["documentsStore/getItemsFilter"] ?? {}
);
const sorting = computed(() => store.getters["documentsStore/getItemsSort"]);

const fetchDocuments = async () => {
  isLoading.value = true;
  const sort = sorting.value ?? {};

  // Map sort direction to sortBy number
  let sortBy = 0;
  if (sort.sortName === "status") {
    if (sort.sortType === "ascending") {
      sortBy = 2; // Approved - In Progress
    } else if (sort.sortType === "descending") {
      sortBy = 1; // In Progress - Approved
    }
  }

  const requestData = {
    username: store.state.username,
    search: searchMode.value ? searchValue.value : "",
    page: documents.pagination.page,
    pageSize: documents.pagination.visible,
    workspace: filterValue.value.workspaceType ?? [],
    documentTypes: filterValue.value.documentType ?? [],
    year: filterValue.value.year ?? [],
    month: filterValue.value.month ?? [],
    status: filterValue.value.status ?? [],
    sortBy: sortBy,
    events: filterValue.value.event ?? [],
  };

  await store
    .dispatch("documentsStore/getMateriList", requestData)
    .then((resp) => {
      const result = resp?.responseData ?? {};
      documents.pagination.total = result.info?.totalPage ?? 0;
      documents.list = result.data ?? [];
      const totalData = result.info?.totalData;
      const totalDataPerPage = result.data?.length || 0;
      store.commit("globalStore/setTotalData", totalData);
      store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const reloadPage = () => {
  documents.pagination.page = 1;
  fetchDocuments();
};

onMounted(() => {
  fetchDocuments();
});

watch(
  () => sorting.value,
  (val) => {
    if (
      isNotEmptyObject(val) &&
      route.name === "dashboard.document.v2.materi"
    ) {
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
    if (searchMode.value) reloadPage();
  },
  { deep: true }
);
</script>

<style scoped>
.label-status {
  margin-right: 20px;
  border-radius: 10px;
  color: white !important;
  letter-spacing: -0.7px;
  font-weight: 900;
  height: 30px;
  font-size: 13px;
}

.btn-warning {
  background: linear-gradient(
    179.16deg,
    #e2650b 0.79%,
    #fe7411 99.34%
  ) !important;
}

.btn-status-default {
  background-color: #ffeeca;
  color: #906e2c;
}

.btn-status-style-21 {
  background-color: #e8f6eb;
  color: #1ca333;
}

.btn-status-style {
  letter-spacing: -0.1px;
  font-weight: 900;
  height: 30px !important;
  font-size: 12px;
  width: 180px;
}

:deep(.tab-header.v-slide-group-item--active) {
  background: none !important;
  color: red !important;
  border: none !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: red !important;
}

:deep(.v-btn.v-tab) {
  font-weight: 600;
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
}

:deep(.v-pagination__next),
:deep(.v-pagination__prev) {
  color: #065695;
}

/* ── Skeleton card ─────────────────────────────── */
.skeleton-card {
  background: #fff;
  border-radius: 12px;
  border-left: 5px solid rgb(6, 86, 149);
  border-bottom-left-radius: 15px;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  overflow: hidden;
}

.skeleton-header {
  padding: 14px 16px;
  border-bottom: 1px solid #f0f0f0;
}

.sk-header-title {
  height: 18px;
  width: 160px;
  border-radius: 6px;
}

.skeleton-table {
  padding: 8px 12px;
}

.skeleton-thead {
  display: flex;
  gap: 12px;
  padding: 8px 4px;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 4px;
}

.sk-th {
  height: 10px;
  border-radius: 4px;
  background: #e8e8e8;
  flex: 1;
}

.skeleton-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 4px;
  border-bottom: 1px solid #f5f5f5;
  animation: fadeSlideUp 0.38s ease-out both;
}

.skeleton-row:last-child {
  border-bottom: none;
}

/* columns: No | Name | Workspace | Event | Status | Action */
.sk-block {
  background: #eeeeee;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  height: 13px;
}

.sk-cell-no {
  width: 28px;
}
.sk-cell-name {
  flex: 2;
  min-width: 0;
}
.sk-cell-ws {
  flex: 1;
  min-width: 0;
}
.sk-cell-event {
  flex: 1.5;
  min-width: 0;
}
.sk-cell-status {
  width: 80px;
  border-radius: 999px;
  height: 22px;
}
.sk-cell-action {
  width: 24px;
  border-radius: 50%;
  height: 24px;
}

/* Shimmer sweep */
.sk-block::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.75) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSweep 1.4s ease-in-out infinite;
}
.sk-cell-ws::after {
  animation-delay: 0.08s;
}
.sk-cell-event::after {
  animation-delay: 0.16s;
}
.sk-cell-status::after {
  animation-delay: 0.24s;
}
.sk-cell-action::after {
  animation-delay: 0.32s;
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
    translate: 0 12px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
