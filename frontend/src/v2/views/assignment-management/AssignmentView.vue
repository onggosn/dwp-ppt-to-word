<template>
  <v-container class="w-100">
    <div class="pa-2 mx-5">
      <v-row>
        <v-col cols="12">
          <v-card v-if="!searchMode" class="card-non-outline">
            <v-card-text>
              <assignment-summary ref="assignment_summary" :typeFilter="tab" />
            </v-card-text>
          </v-card>
          <div class="d-flex justify-space-between align-center mt-5">
            <v-btn
              v-if="!searchMode"
              class="btn-create px-5 py-2"
              @click="showCreate()"
            >
              + Create Assignment
            </v-btn>
            <div v-if="!searchMode" class="d-flex">
              <assignment-filter
                typeFilter="assignment-management"
                :subFilter="tab"
                :roundedBtn="true"
              />

              <assignment-sorting
                @update="setSorting"
                :rounded-btn="true"
                :tab="tab"
              />

              <dashboard-search
                typeFilter="assignment-management"
                :subFilter="tab"
                :dataLoading="isDataLoading"
                @submitFilter="changeSearch"
              />
            </div>
          </div>
          <template v-if="isDataLoading">
            <v-row class="mt-3">
              <v-col
                cols="12"
                v-for="idx in assignPenugasan.pagination.visible"
                :key="idx"
              >
                <free-style-shimmer
                  :is-loading="true"
                  width="100%"
                  height="4.3rem"
                  border-radius="10px"
                />
              </v-col>
            </v-row>
          </template>
          <template v-else>
            <v-tabs v-if="!searchMode" v-model="tab" bg-color="transparent">
              <v-tab class="tab-header" value="penugasan"> PENUGASAN </v-tab>
              <v-tab class="tab-header" value="arahan"> ARAHAN </v-tab>
            </v-tabs>
            <v-window v-model="tab" class="mt-3">
              <v-window-item value="penugasan">
                <div v-if="assignPenugasan.list.length == 0">
                  <img
                    src="/images/no_workspace_available.png"
                    style="
                      display: block;
                      margin: 0 auto;
                      width: 300px;
                      margin-top: 80px;
                    "
                  />
                  <div
                    class="text-center text-18 fw-600 text-grayTheme-gradien font-italic ma-2"
                  >
                    No Data Available....
                  </div>
                </div>
                <div>
                  <div v-for="(item, idx) in assignPenugasan.list" :key="idx">
                    <dashboard-row-component :item="item" type="default">
                      <template v-slot:datetime>
                        <v-col class="ellipsis-3 pb-0">
                          {{ item?.eventName }}
                        </v-col>
                      </template>
                      <template v-slot:label>
                        <v-chip
                          rounded
                          class="ml-2 d-sm-none d-md-flex mr-4"
                          :style="getColor(item?.idStatus)"
                        >
                          {{ item?.statusName }}
                        </v-chip>
                      </template>

                      <assign-det-penugasan-component
                        :id="item.id"
                        @reloadPage="reloadPage"
                      />
                    </dashboard-row-component>
                  </div>
                  <div class="text-center">
                    <v-pagination
                      rounded="1"
                      elevation="2"
                      size="small"
                      v-model="assignPenugasan.pagination.page"
                      :length="assignPenugasan.pagination.total"
                      :total-visible="assignPenugasan.pagination.visible"
                      @update:modelValue="getPenugasan()"
                    ></v-pagination>
                  </div>
                </div>
              </v-window-item>
              <v-window-item value="arahan">
                <div v-if="assignArahan.list.length == 0">
                  <img
                    src="/images/no_document_preview.png"
                    style="
                      display: block;
                      margin: 0 auto;
                      width: 300px;
                      margin-top: 80px;
                    "
                  />
                  <div
                    class="text-center text-18 fw-600 text-grayTheme-gradien font-italic ma-2"
                  >
                    No Data Available....
                  </div>
                </div>
                <div v-else>
                  <div v-for="(item, idx) in assignArahan.list" :key="idx">
                    <dashboard-row-component :item="item" type="default">
                      <template v-slot:label>
                        <v-col class="ellipsis-3 pb-0">
                          {{ item?.eventName }}
                        </v-col>
                      </template>

                      <assign-det-arahan-component
                        :id="item.id"
                        @reloadPage="reloadPage"
                      />
                    </dashboard-row-component>
                  </div>
                  <div class="text-center">
                    <v-pagination
                      rounded="1"
                      elevation="2"
                      size="small"
                      v-model="assignArahan.pagination.page"
                      :length="assignArahan.pagination.total"
                      :total-visible="assignArahan.pagination.visible"
                      @update:modelValue="getArahan()"
                    ></v-pagination>
                  </div>
                </div>
              </v-window-item>
            </v-window>
          </template>
        </v-col>
      </v-row>
    </div>
    <create-assignment-dialog ref="create_dialog" @afterInsert="reloadPage" />
  </v-container>
</template>
<script setup lang="ts">
import { useStore } from "vuex";
import { ref, onMounted, watch } from "vue";

import DashboardRowComponent from "@v2/components/dashboard/DashboardRowComponent.vue";
import AssignDetPenugasanComponent from "@v2/components/assignment/AssignDetPenugasanComponent.vue";
import AssignDetArahanComponent from "@v2/components/assignment/AssignDetArahanComponent.vue";
import AssignmentSummary from "@v2/components/assignment/AssignmentSummary.vue";
import DashboardSearch from "@v2/views/assignment-management/DashboardSearch.vue";
import AssignmentFilter from "@/v2/components/assignment/AssignmentFilter.vue";
import AssignmentSorting from "@/v2/components/assignment/AssignmentSorting.vue";
import CreateAssignmentDialog from "@v2/components/assignment/CreateAssignmentDialog.vue";
import {
  TCheckboxAssignment,
  TFilterData,
  TSortFilter,
  RootAssignment,
} from "@v2/Type";
import { useRoute, useRouter } from "vue-router";

const store = useStore();
const create_dialog = ref();
const assignment_summary = ref();
const routeDetail = useRoute();
const router = useRouter();
let searchMode = false;

const tab = ref<string | undefined>(undefined);
const isDataLoading = ref<boolean>(false);
const assignPenugasan = ref<RootAssignment>({
  list: [],
  pagination: {
    page: 1,
    total: 0,
    visible: 10,
  },
});

const assignArahan = ref<RootAssignment>({
  list: [],
  pagination: {
    page: 1,
    total: 0,
    visible: 10,
  },
});

const filterData = ref<TFilterData>({
  sort: {
    sortName: null,
    sortType: "ascending",
    sortTime: "descending",
  },
  filter: {},
  searchKeyword: "",
});

function validateSearch() {
  searchMode = false;
  if (routeDetail.path.includes("assignmentmanagement-new/arahan/search")) {
    searchMode = true;
    tab.value = "arahan";
  } else if (
    routeDetail.path.includes("assignmentmanagement-new/assignment/search")
  ) {
    searchMode = true;
    tab.value = "penugasan";
  }
}

function getPenugasan() {
  validateSearch();
  isDataLoading.value = true;
  let requestData = {};
  let checkbox: TCheckboxAssignment =
    store.getters["assignmentStore/getItemsFilter"] ?? {};
  let sort: TSortFilter = filterData.value.sort ?? {};
  requestData = {
    search: filterData.value.searchKeyword,
    pageNo: assignPenugasan.value.pagination.page,
    entriesPerPage: assignPenugasan.value.pagination.visible,
    workspaceType: checkbox.workspaceType,
    yearPeriod: checkbox.yearPeriod ?? [],
    status: checkbox.status ?? [],
    sortName: sort.sortName,
    sortType: sort.sortType,
    dueYear: checkbox.dueYear ?? [],
    monthPeriod: checkbox.monthPeriod ?? [],
    satkerKoordinator: checkbox.satkerKoordinator ?? [],
  };
  if (searchMode) {
    let formData = {
      search:
        store.getters["assignmentStore/getStatusSearch"]?.searchKeyword || "",
      pageNo: assignPenugasan.value.pagination.page,
      entriesPerPage: assignPenugasan.value.pagination.visible,
    };
    requestData = formData;
  }
  store
    .dispatch("assignmentStore/getPenugasanList", requestData)
    .then((res: any) => {
      let result = res.responseData ?? {};
      assignPenugasan.value.pagination.total = result.info?.totalPage ?? 0;
      let assignPenugasanList = result.data ?? [];
      assignPenugasan.value.list = assignPenugasanList.map((e) => {
        e.name = e.assignmentName;
        return {
          id: e.id,
          name: e.name,
          status: e.status,
          statusName: e.statusName,
          ...e,
        };
      });
    })
    .finally(() => {
      isDataLoading.value = false;
    });
}

function getArahan() {
  validateSearch();
  let requestData = {};
  isDataLoading.value = true;
  let checkbox: TCheckboxAssignment =
    store.getters["assignmentStore/getItemsFilter"] ?? {};
  let sort: TSortFilter = filterData.value.sort ?? {};

  requestData = {
    search: filterData.value.searchKeyword,
    pageNo: assignArahan.value.pagination.page,
    entriesPerPage: assignArahan.value.pagination.visible,
    workspaceType: checkbox.workspaceType,
    yearPeriod: checkbox.yearPeriod ?? [],
    status: checkbox.status ?? [],
    sortName: sort.sortName,
    sortType: sort.sortType,
    dueYear: checkbox.dueYear ?? [],
    monthPeriod: checkbox.monthPeriod ?? [],
    satkerKoordinator: checkbox.satkerKoordinator ?? [],
  };
  if (searchMode) {
    let formData = {
      search:
        store.getters["assignmentStore/getStatusSearch"]?.searchKeyword || "",
      pageNo: assignArahan.value.pagination.page,
      entriesPerPage: assignArahan.value.pagination.visible,
    };
    requestData = formData;
  }

  store
    .dispatch("assignmentStore/getArahanList", requestData)
    .then((res) => {
      let result = res.responseData ?? {};
      assignArahan.value.pagination.total = result.info?.totalPage ?? 0;
      let assignArahanList = result.data ?? [];
      assignArahan.value.list = assignArahanList.map((e) => {
        e.name = e.assignmentName;
        return {
          id: e.idTask,
          name: e.name,
          status: e.idStatus,
          statusName: e.statusName,
          ...e,
        };
      });
    })
    .finally(() => {
      isDataLoading.value = false;
    });
}

function reloadPage() {
  if (tab.value == "penugasan") {
    assignPenugasan.value.pagination.page = 1;
    getPenugasan();
  } else if (tab.value == "arahan") {
    assignArahan.value.pagination.page = 1;
    getArahan();
  }
  assignment_summary.value.load(tab.value);
}

function changeSearch(param: string) {
  filterData.value = {
    ...filterData.value,
    searchKeyword: param,
  };
  store.commit("assignmentStore/setStatusSearch", {
    searchKeyword: param,
  });
  if (
    routeDetail.path.includes("assignmentmanagement-new") &&
    tab.value == "penugasan"
  ) {
    router.push({ name: "assignmentmanagement-new-assignment-search" });
  }
  if (
    routeDetail.path.includes("assignmentmanagement-new") &&
    tab.value == "arahan"
  ) {
    router.push({ name: "assignmentmanagement-new-arahan-search" });
  }
  // reloadPage();
}

function resetFilter() {
  filterData.value = {
    sort: {
      sortName: null,
      sortType: "ascending",
      sortTime: "descending",
    },
    filter: {},
  };
}

function showCreate() {
  create_dialog.value.show();
}

const colorMap = {
  21: { "background-color": "#E8F6EB", color: "#1CA333" },
  default: { "background-color": "#ffeeca", color: "#906e2c" },
};

function getColor(id: number) {
  return colorMap[id as keyof typeof colorMap] || colorMap.default;
}

onMounted(() => {
  getPenugasan();
  getArahan();
  reloadPage();
});

watch(
  () => tab.value,
  () => {
    resetFilter();
  }
);
watch(
  [() => store.getters["assignmentStore/getItemsFilter"]],
  () => {
    reloadPage();
  },
  { deep: true }
);

watch(
  [() => store.getters["assignmentStore/getStatusSearch"]],
  () => {
    reloadPage();
  },
  { deep: true }
);

const setSorting = (value) => {
  filterData.value.sort = {
    sortName: value.sortName,
    sortType: value.sortType,
    sortTime: "ascending",
  };
  reloadPage();
};
</script>

<style scoped>
.v-container {
  max-width: 100%;
}
.btn-create {
  color: #fff;
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  border-radius: 10px;
  letter-spacing: 0.1px;
  font-weight: 900;
}
.card-non-outline {
  border-radius: 15px;
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
}
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
  background-clip: text;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: red !important;
}
:deep(.v-btn.v-tab) {
  font-weight: 600;
  background: -webkit-linear-gradient(#065695, #267dc2);
  background-clip: text;
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
:deep(.v-pagination__next) {
  color: #065695;
}
:deep(.v-pagination__prev) {
  color: #065695;
}
:deep(.bg-info) {
  color: #fff;
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
}
</style>
