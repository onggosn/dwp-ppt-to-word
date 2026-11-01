<template>
  <template v-if="isLoading">
    <v-row>
      <v-col cols="12" v-for="idx in penugasan.pagination.visible" :key="idx">
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
      <v-tab
        class="tab-header"
        value="penugasan"
        :to="{ name: 'dashboard.assignment.penugasan' }"
      >
        PENUGASAN
      </v-tab>
      <v-tab
        class="tab-header"
        value="arahan"
        :to="{ name: 'dashboard.assignment.arahan' }"
      >
        ARAHAN
      </v-tab>
    </v-tabs>
    <v-window v-model="tab" class="mt-3">
      <v-window-item value="penugasan">
        <div v-if="penugasan.list.length == 0">
          <img
            src="/images/assignment/empty-assignment.png"
            style="
              display: block;
              margin: 0 auto;
              width: 450px;
              margin-top: 80px;
            "
          />
          <div
            class="text-center text-18 fw-600 text-grayTheme-gradien font-italic mt-4"
          >
            No Assignment Available...
          </div>
        </div>
        <div v-else>
          <div v-for="(item, idx) in penugasan.list" :key="idx">
            <dashboard-row-component :item="item" type="default">
              <template v-slot:datetime>
                <v-col class="ellipsis-3 text-13">
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

              <dash-det-penugasan-component
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
              v-model="penugasan.pagination.page"
              :length="penugasan.pagination.total"
              :total-visible="penugasan.pagination.visible"
              @update:modelValue="getPenugasan()"
            ></v-pagination>
          </div>
        </div>
      </v-window-item>
      <v-window-item value="arahan">
        <div v-if="arahan.list.length == 0">
          <img
            src="/images/assignment/empty-assignment.png"
            style="
              display: block;
              margin: 0 auto;
              width: 450px;
              margin-top: 80px;
            "
          />
          <div
            class="text-center text-18 fw-600 text-grayTheme-gradien font-italic mt-4"
          >
            No Assignment Available....
          </div>
        </div>

        <div v-else>
          <div v-for="(item, idx) in arahan.list" :key="idx">
            <dashboard-row-component :item="item" type="default">
              <template v-slot:label>
                <v-col class="ellipsis-3 text-13">
                  {{ item.taskName }}
                </v-col>
              </template>

              <dash-det-arahan-component
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
              v-model="arahan.pagination.page"
              :length="arahan.pagination.total"
              :total-visible="arahan.pagination.visible"
              @update:modelValue="getArahan()"
            ></v-pagination>
          </div>
        </div>
      </v-window-item>
    </v-window>
  </template>
</template>

<script>
import { formatTimeEngToIndNoDays } from "@/helpers/date";
import client from "@/library/ApiClient";
import DashboardRowComponent from "@/components/dashboard/DashboardRowComponent.vue";
import DashDetPenugasanComponent from "@/components/dashboard/DashDetPenugasanComponent.vue";
import DashDetArahanComponent from "@/components/dashboard/DashDetArahanComponent.vue";

export default {
  name: "dhsAssignment",
  emits: ["subTabChange", "dataLoading"],
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
    DashDetArahanComponent,
    DashDetPenugasanComponent,
  },
  data() {
    return {
      tab: null,
      isLoading: false,
      penugasan: {
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
      },
      arahan: {
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
      },
    };
  },
  methods: {
    formatTimeEngToIndNoDays: formatTimeEngToIndNoDays,
    getColor(idStatus) {
      let colorStatus = {
        19: "warning",
        20: "warning",
        21: "success",
      };
      return colorStatus[idStatus] ?? "danger";
    },
    getPenugasan() {
      this.isLoading = true;
      this.$emit("dataLoading", true);
      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        search: this.filter.searchKeyword,
        pageNo: this.penugasan.pagination.page,
        entriesPerPage: this.penugasan.pagination.visible,
        workspaceType: checkbox.workspaceType,
        yearPeriod: checkbox.period,
        status: checkbox.status ?? [],
        sortName: sort.sortName,
        sortType: sort.sortType,
        dueYear: checkbox.period,
        satkerKoordinator: checkbox.satkerKoordinator ?? [],
      };
      client
        .getListAssignmentByTipePenugasanAndAssignmentMember({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.penugasan.pagination.total = result.info?.totalPage ?? 0;
          let penugasanList = result.data ?? [];
          this.penugasan.list = penugasanList.map((e) => {
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
          this.isLoading = false;
          this.$emit("dataLoading", false);
        });
    },
    getArahan() {
      this.isLoading = true;
      this.$emit("dataLoading", true);
      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        search: this.filter.searchKeyword,
        pageNo: this.arahan.pagination.page,
        entriesPerPage: this.penugasan.pagination.visible,
        workspaceType: checkbox.workspaceType,
        yearPeriod: checkbox.period,
        status: checkbox.status ?? [],
        sortName: sort.sortName,
        sortType: sort.sortType,
        dueYear: checkbox.period,
        satkerKoordinator: checkbox.satkerKoordinator ?? [],
      };
      client
        .getListAssignmentbyTipeArahanAndAssignmentMember({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.arahan.pagination.total = result.info?.totalPage ?? 0;
          let arahanList = result.data ?? [];
          this.arahan.list = arahanList.map((e) => {
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
          this.isLoading = false;
          this.$emit("dataLoading", false);
        });
    },
    reloadPage() {
      if (this.tab == "penugasan") {
        this.penugasan.pagination.page = 1;
        this.getPenugasan();
      } else if (this.tab == "arahan") {
        this.arahan.pagination.page = 1;
        this.getArahan();
      }
    },
  },
  created() {
    this.getPenugasan();
    this.getArahan();
    this.$emit("subTabChange", null);
  },
  watch: {
    tab(value) {
      this.$emit("subTabChange", value);
    },
    filter() {
      this.reloadPage();
    },
  },
};
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
</style>
