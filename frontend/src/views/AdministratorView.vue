<template>
  <v-container>
    <v-row class="admin-banner white--text mx-6 my-3">
      <v-col class="pa-6 ml-5">
        <h2 class="fw600 text-white">Welcome to Dashboard Administrator!</h2>
        <p class="fw400 text-13 text-white">
          You can manage your workspace, task and role in this
        </p>
        <p class="fw400 text-13 text-white">page!</p>
      </v-col>
    </v-row>
    <div class="pl-5 pr-5 pt-2 mx-2">
      <v-row>
        <v-col cols="12">
          <v-card class="card-non-outline mb-2">
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
                <div v-if="isUseFilter">
                  <dashboard-searching
                    typeFilter="dashboard.administrator"
                    :subFilter="tab"
                    :dataLoading="isDataLoading"
                    @submitFilter="changeSearch"
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
import DashboardSearching from "@/components/dashboard/DashboardSearching.vue";
export default {
  name: "administratorView",
  components: {
    DashboardSearching,
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
          name: "administrator.workspace",
          label: "Workspace",
        },
        {
          name: "administrator.role",
          label: "Role",
        },
        {
          name: "administrator.template",
          label: "Template",
        },
      ],
    };
  },
  methods: {
    isMenuActive(menu) {
      return this.$route.name == menu;
    },
    changeFilter(param) {
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
  computed: {
    isUseFilter() {
      return ![
        "administrator.template",
        "administrator.workspace.predefine",
        "administrator.workspace",
      ].includes(this.$route.name);
    },
  },
};
</script>

<style scoped>
.admin-banner {
  background-image: url("@/assets/images/banner-admin.png");
  background-size: 100% 100%;
  height: 160px;
  border-radius: 20px;
}
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
