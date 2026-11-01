<template>
  <v-container>
    <div class="pa-2 mx-5">
      <v-row>
        <v-col cols="12">
          <v-card class="card-non-outline">
            <v-card-text>
              <assignment-summary :typeFilter="tab" />
            </v-card-text>
          </v-card>
          <div class="d-flex justify-space-between align-center mt-5">
            <v-btn class="btn-create px-5 py-2" @click="showCreate()">
              + Create Assignment
            </v-btn>
            <div>
              <dashboard-search
                typeFilter="dashboard.assignment"
                :subFilter="tab"
                :dataLoading="isDataLoading"
                @submitFilter="changeSearch"
              />
              <dashboard-filter
                typeFilter="dashboard.assignment"
                :subFilter="tab"
                :dataLoading="isDataLoading"
                @submitFilter="changeFilter"
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
            <v-tabs v-model="tab" bg-color="transparent">
              <v-tab class="tab-header" value="penugasan"> PENUGASAN </v-tab>
              <v-tab class="tab-header" value="arahan"> ARAHAN </v-tab>
            </v-tabs>
            <v-window v-model="tab" class="mt-3">
              <v-window-item value="penugasan">
                <div v-if="assignPenugasan.list.length == 0">
                  <v-img
                    src="/images/no_workspace_available.png"
                    style="
                      display: block;
                      margin: 0 auto;
                      width: 450px;
                      margin-top: 80px;
                    "
                  ></v-img>
                  <div
                    class="text-center text-18 fw-600 text-grayTheme-gradien font-italic"
                  >
                    No Data Available....
                  </div>
                </div>
                <div v-else>
                  <div v-for="(item, idx) in assignPenugasan.list" :key="idx">
                    <dashboard-row-component :item="item" type="default">
                      <template v-slot:datetime>
                        <v-col class="ellipsis-3 text-13 pb-0">
                          {{ item.taskName }}
                        </v-col>
                      </template>
                      <template v-slot:label>
                        <v-btn
                          rounded
                          class="ml-3 label-status btn-status-style d-sm-none d-md-flex"
                          :color="getColor(item.idStatus)"
                        >
                          {{ item.statusName }}
                        </v-btn>
                      </template>

                      <assign-det-penugasan-component
                        :idAssignment="item.id"
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
                  <v-img
                    src="/images/no_document_preview.png"
                    style="
                      display: block;
                      margin: 0 auto;
                      width: 450px;
                      margin-top: 80px;
                    "
                  ></v-img>
                  <div
                    class="text-center text-18 fw-600 text-grayTheme-gradien font-italic"
                  >
                    No Data Available....
                  </div>
                </div>
                <div v-else>
                  <div v-for="(item, idx) in assignArahan.list" :key="idx">
                    <dashboard-row-component :item="item" type="default">
                      <template v-slot:label>
                        <v-col class="ellipsis-3 text-13 pb-0">
                          {{ item.taskName }}
                        </v-col>
                      </template>

                      <assign-det-arahan-component
                        :idAssignment="item.id"
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
<script>
import { formatTimeEngToIndNoDays } from "@/helpers/date";
import client from "@/library/ApiClient";
import DashboardRowComponent from "@/components/dashboard/DashboardRowComponent.vue";
import AssignDetPenugasanComponent from "@/components/assignment/AssignDetPenugasanComponent.vue";
import AssignDetArahanComponent from "@/components/assignment/AssignDetArahanComponent.vue";
import AssignmentSummary from "@/components/assignment/AssignmentSummary.vue";
import DashboardFilter from "@/components/dashboard/DashboardFilter.vue";
import DashboardSearch from "@/components/dashboard/DashboardSearch.vue";
import CreateAssignmentDialog from "@/components/assignment/CreateAssignmentDialog.vue";

export default {
  name: "assignmentView",
  props: {
    filter: {
      type: Object,
      default: function () {
        return {};
      },
    },
  },
  components: {
    DashboardRowComponent,
    AssignDetArahanComponent,
    AssignDetPenugasanComponent,
    AssignmentSummary,
    DashboardFilter,
    DashboardSearch,
    CreateAssignmentDialog,
  },
  data() {
    return {
      tab: null,
      isDataLoading: false,
      assignPenugasan: {
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
      },
      assignArahan: {
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
      },
      filterData: {
        sort: {
          sortName: null,
          sortType: "ascending",
          sortTime: "descending",
        },
        filter: {},
        searchKeyword: "",
      },
    };
  },
  methods: {
    formatTimeEngToIndNoDays: formatTimeEngToIndNoDays,
    getPenugasan() {
      this.isDataLoading = true;
      let checkbox = this.filterData.filter ?? {};
      let sort = this.filterData.sort ?? {};
      let requestData = {
        username: this.$store.state.username,
        search: this.filterData.searchKeyword,
        pageNo: this.assignPenugasan.pagination.page,
        entriesPerPage: this.assignPenugasan.pagination.visible,
        workspaceType: checkbox.workspaceType,
        yearPeriod: checkbox.period,
        status: checkbox.status ?? [],
        sortName: sort.sortName,
        sortType: sort.sortType,
        dueYear: checkbox.period,
        monthPeriod: checkbox.monthPeriod ?? [],
        satkerKoordinator: checkbox.satkerKoordinator ?? [],
      };
      client
        .getListAssignmentbyTipePenugasan({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.assignPenugasan.pagination.total = result.info?.totalPage ?? 0;
          let assignPenugasanList = result.data ?? [];
          this.assignPenugasan.list = assignPenugasanList.map((e) => {
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
          this.isDataLoading = false;
        });
    },
    getArahan() {
      this.isDataLoading = true;
      let checkbox = this.filterData.filter ?? {};
      let sort = this.filterData.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        search: this.filterData.searchKeyword,
        pageNo: this.assignArahan.pagination.page,
        entriesPerPage: this.assignArahan.pagination.visible,
        workspaceType: checkbox.workspaceType,
        yearPeriod: checkbox.period,
        status: checkbox.status ?? [],
        sortName: sort.sortName,
        sortType: sort.sortType,
        dueYear: checkbox.period,
        monthPeriod: checkbox.monthPeriod ?? [],
        satkerKoordinator: checkbox.satkerKoordinator ?? [],
      };

      client
        .getListAssignmentbyTipeArahan({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.assignArahan.pagination.total = result.info?.totalPage ?? 0;
          let assignArahanList = result.data ?? [];
          this.assignArahan.list = assignArahanList.map((e) => {
            e.name = e.assignmentName;
            return {
              id: e.idTask,
              name: e.name,
              status: e.statusId,
              statusName: e.statusName,
              ...e,
            };
          });
        })
        .finally(() => {
          this.isDataLoading = false;
        });
    },
    reloadPage() {
      if (this.tab == "penugasan") {
        this.assignPenugasan.pagination.page = 1;
        this.getPenugasan();
      } else if (this.tab == "arahan") {
        this.assignArahan.pagination.page = 1;
        this.getArahan();
      }
    },
    changeFilter(param) {
      this.filterData = {
        ...this.filterData,
        ...param,
      };
      this.reloadPage();
    },
    changeSearch(param) {
      this.filterData = {
        ...this.filterData,
        searchKeyword: param,
      };
      this.reloadPage();
    },
    resetFilter() {
      this.filterData = {
        sort: {
          sortName: null,
          sortType: "ascending",
          sortTime: "descending",
        },
        filter: {},
      };
    },
    showCreate() {
      this.$refs.create_dialog.show();
    },
    getColor(idStatus) {
      let colorStatus = {
        19: "warning",
        20: "info",
        21: "success",
      };
      return colorStatus[idStatus] ?? "danger";
    },
  },
  created() {
    this.getPenugasan();
    this.getArahan();
    this.reloadPage();
  },
  watch: {
    tab() {
      this.resetFilter();
    },
  },
};
</script>

<style scoped>
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
