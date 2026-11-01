<template>
  <!-- Custom skeleton matching DashboardRowComponent layout -->
  <template v-if="isLoading">
    <div class="skeleton-list">
      <div
        v-for="n in 6"
        :key="n"
        class="skeleton-panel"
        :style="{ animationDelay: `${(n - 1) * 0.07}s` }"
      >
        <div class="skeleton-panel-body">
          <div class="sk-block sk-title"></div>
          <div class="sk-block sk-task"></div>
          <div class="sk-block sk-chevron"></div>
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div v-if="assignments.list.length === 0">
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
      <div v-for="(item, idx) in assignments.list" :key="idx">
        <dashboard-row-component :item="item" type="default">
          <template v-slot:label>
            <v-col class="ellipsis-3 text-13">
              {{ item.taskName }}
            </v-col>
          </template>

          <AssignDetArahanComponent
            :id="item.id"
            :is-dashboard="true"
            @reloadPage="reloadPage"
          />
        </dashboard-row-component>
      </div>
      <div class="text-center">
        <v-pagination
          rounded="1"
          elevation="2"
          size="small"
          v-model="assignments.pagination.page"
          :length="assignments.pagination.total"
          :total-visible="assignments.pagination.visible"
          @update:modelValue="fetchAssignments"
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
import { TAssignmentsState } from "@/v2/Type";

import DashboardRowComponent from "@v2/components/dashboard/DashboardRowComponent.vue";
import AssignDetArahanComponent from "@v2/components/assignment/AssignDetArahanComponent.vue";

const route = useRoute();
const store = useStore();

const isLoading = ref(false);
const assignments = reactive<TAssignmentsState>({
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
  () => store.getters["assignmentStore/getItemsFilter"] ?? {}
);
const sorting = computed(() => store.getters["assignmentStore/getItemsSort"]);

const fetchAssignments = async () => {
  isLoading.value = true;
  const sort = sorting.value ?? {};

  const requestData = {
    username: store.state.username,
    search: searchMode.value ? searchValue.value : "",
    pageNo: assignments.pagination.page,
    entriesPerPage: assignments.pagination.visible,
    workspaceType: filterValue.value.workspaceType,
    yearPeriod: filterValue.value.yearPeriod ?? [],
    status: filterValue.value.status ?? [],
    sortName: sort?.sortName,
    sortType: sort?.sortType,
    dueYear: filterValue.value.dueYear ?? [],
    monthPeriod: filterValue.value.monthPeriod ?? [],
    satkerKoordinator: filterValue.value.satkerKoordinator ?? [],
  };

  await store
    .dispatch("assignmentStore/getListAssignmentArahan", requestData)
    .then((resp) => {
      const result = resp?.responseData ?? {};
      assignments.pagination.total = result.info?.totalPage ?? 0;
      assignments.list = (result.data ?? []).map((e: any) => ({
        id: e.id,
        taskName: e.taskName,
        statusName: e.statusName,
        idStatus: e.idStatus,
        ...e,
      }));
      const totalData = resp.responseData.info?.totalData;
      const totalDataPerPage = resp.responseData.data?.length || 0;
      store.commit("globalStore/setTotalData", totalData);
      store.commit("globalStore/setTotalDataPerPage", totalDataPerPage);
    })
    .finally(() => {
      isLoading.value = false;
    });
};

const reloadPage = () => {
  assignments.pagination.page = 1;
  fetchAssignments();
};

onMounted(() => {
  fetchAssignments();
});

watch(
  () => sorting.value,
  (val) => {
    if (
      isNotEmptyObject(val) &&
      route.name === "dashboard.assignment.v2.arahan"
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

/* ── Skeleton panels ────────────────────────────── */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-panel {
  background: #fff;
  border-radius: 15px;
  border-left: 5px solid rgb(6, 86, 149);
  border-bottom-left-radius: 15px;
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
  padding: 0 16px;
  height: 64px;
  display: flex;
  align-items: center;
  animation: fadeSlideUp 0.4s ease-out both;
}

.skeleton-panel-body {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 14px;
}

/* col-6 assignment title */
.sk-title {
  flex: 1.5;
  height: 13px;
  border-radius: 6px;
  background: #e8e8e8;
  position: relative;
  overflow: hidden;
}

/* slot label — task name */
.sk-task {
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
  flex-shrink: 0;
}

/* Shimmer sweep */
.sk-block::after {
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
.sk-task::after {
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
    translate: 0 14px;
  }
  to {
    opacity: 1;
    translate: 0 0;
  }
}
</style>
