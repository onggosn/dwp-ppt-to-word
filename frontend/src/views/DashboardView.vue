<template>
  <v-container>
    <div class="mx-6 my-3">
      <v-row>
        <v-col cols="12">
          <v-card class="card-non-outline">
            <v-card-text>
              <dashboard-summary :typeFilter="tab" :subFilter="subTab" />
            </v-card-text>
          </v-card>
          <v-card class="card-non-outline my-3">
            <v-card-text class="py-2">
              <div class="d-flex justify-space-between align-center">
                <v-tabs v-model="tab" bg-color="white">
                  <v-tab
                    v-for="(item, idx) in listMenu"
                    :key="idx"
                    class="menu-list"
                    slider-color="transparent"
                    :value="item.name"
                    :to="{ name: item.name }"
                  >
                    {{ item.label }}
                  </v-tab>
                </v-tabs>
                <div>
                  <dashboard-search
                    v-if="tab == 'dashboard.assignment'"
                    :typeFilter="tab"
                    :subFilter="subTab"
                    :dataLoading="isDataLoading"
                    @submitFilter="changeSearch"
                  />
                  <dashboard-filter
                    :typeFilter="tab"
                    :subFilter="subTab"
                    :dataLoading="isDataLoading"
                    @submitFilter="changeFilter"
                  />
                </div>
              </div>
            </v-card-text>
          </v-card>
          <router-view
            :filter="filterData"
            @subTabChange="onSubTabChange"
            @dataLoading="onDataLoading"
          >
          </router-view>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import DashboardSummary from "../components/dashboard/DashboardSummary.vue";
import DashboardFilter from "@/components/dashboard/DashboardFilter.vue";
import DashboardSearch from "@/components/dashboard/DashboardSearch.vue";

export default {
  name: "dashboardView",
  components: {
    DashboardSummary,
    DashboardFilter,
    DashboardSearch,
  },
  data() {
    return {
      tab: null,
      subTab: null,
      isDataLoading: false,
      filterData: {
        sort: {
          sortName: null,
          sortType: "ascending",
          sortTime: "descending",
        },
        filter: {},
        searchKeyword: "",
      },

      // name sama dengan name router
      listMenu: [
        {
          name: "dashboard.pengajuan",
          label: "Pengajuan",
        },
        {
          name: "dashboard.persetujuan",
          label: "Persetujuan",
        },
        {
          name: "dashboard.workspace",
          label: "Workspace",
        },
        {
          name: "dashboard.task",
          label: "Task",
        },
        {
          name: "dashboard.document",
          label: "Document",
        },
        {
          name: "dashboard.assignment",
          label: "Assignment",
        },
      ],
    };
  },
  methods: {
    isMenuActive(menu) {
      return this.$route.name == menu;
    },
    changeFilter(param) {
      // debugger;
      this.filterData = {
        ...this.filterData,
        ...param,
      };
    },
    changeSearch(param) {
      this.filterData = {
        ...this.filterData,
        searchKeyword: param,
      };
    },
    onSubTabChange(param) {
      this.resetFilter();
      this.subTab = param;
    },
    onDataLoading(param) {
      this.isDataLoading = param;
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
  },
  watch: {
    tab(newData, oldData) {
      if (oldData && newData != oldData) {
        this.resetFilter();
        this.searchKeyword = "";
      }
    },
  },
};
</script>

<style scoped>
.card-non-outline {
  border-radius: 15px;
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25);
}

.menu-list {
  text-transform: capitalize;
  letter-spacing: -0.2px !important;
  font-style: normal;
  font-weight: 600;
  font-size: 13px;
  color: #267dc2;
  height: 35px;
}

:deep(.v-slide-group__container) {
  align-items: center !important;
  justify-content: space-between !important;
}

:deep(.menu-list.v-tab--selected) {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%);
  color: #fff !important;
  font-weight: 600 !important;
  border-radius: 15px !important;
}
:deep(.v-tab) {
  letter-spacing: 0.1px;
}
.blue-gradient {
  background: linear-gradient(92.09deg, #065695 -46.47%, #267dc2 157.9%);
  color: white !important;
  border-radius: 10px;
}
.text-grey-theme {
  color: rgba(121, 121, 121, 0.9);
}
</style>
