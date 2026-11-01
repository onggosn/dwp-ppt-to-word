<template>
  <template v-if="isLoading">
    <v-row class="mt-2">
      <v-col
        cols="12"
        v-for="idx in workspacePredefine.pagination.visible"
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
      <v-tab
        class="tab-header"
        value="predefine"
        :to="{ name: 'administrator.workspace.predefine' }"
      >
        PRE-DEFINE
      </v-tab>
      <v-tab
        class="tab-header"
        value="custom"
        :to="{ name: 'administrator.workspace.custom' }"
      >
        CUSTOM
      </v-tab>
    </v-tabs>
    <v-window v-model="tab" class="mt-3">
      <v-window-item value="predefine">
        <div v-if="workspacePredefine.list.length == 0">
          <v-img
            src="/images/chartpack/emptybox.png"
            style="
              display: block;
              margin: 0 auto;
              width: 450px;
              margin-top: 80px;
            "
          />
          <div
            class="text-center text-18 fw-600 text-grayTheme-gradien font-italic"
          >
            No Data Available
          </div>
        </div>
        <div v-else>
          <div v-for="(item, idx) in workspacePredefine.list" :key="idx">
            <!-- <pre>{{ item }}</pre> -->
            <admin-row-component :item="item" type="default">
              <admin-det-predefine-component
                tag="predefine"
                :item="item"
                @reloadPage="reloadPage"
              />
            </admin-row-component>
          </div>
        </div>
      </v-window-item>
      <v-window-item value="custom">
        <div v-if="workspaceCustom.list.length == 0">
          <v-img
            src="/images/chartpack/emptybox.png"
            style="
              display: block;
              margin: 0 auto;
              width: 450px;
              margin-top: 80px;
            "
          />
          <div
            class="text-center text-18 fw-600 text-grayTheme-gradien font-italic"
          >
            No Data Available
          </div>
        </div>
        <div v-else>
          <div v-for="(item, idx) in workspaceCustom.list" :key="idx">
            <admin-row-component :item="item" type="default">
              <admin-det-custom-component
                :item="item"
                @reloadPage="reloadPage"
              />
            </admin-row-component>
          </div>
          <div class="text-center">
            <v-pagination
              rounded="1"
              elevation="2"
              size="small"
              v-model="workspaceCustom.pagination.page"
              :length="workspaceCustom.pagination.total"
              :total-visible="workspaceCustom.pagination.visible"
              @update:modelValue="getWorkspaceCustom()"
            ></v-pagination>
          </div>
        </div>
      </v-window-item>
    </v-window>
  </template>
</template>

<script>
import { getDateLabel } from "@/helpers/date";
import client from "@/library/ApiClient";
import AdminRowComponent from "@/components/administrator/AdminRowComponent.vue";
import AdminDetPredefineComponent from "@/components/administrator/AdminDetPredefineComponent.vue";
import AdminDetCustomComponent from "@/components/administrator/AdminDetCustomComponent.vue";
import adminMock from "@/mock/Administrator.js";

export default {
  name: "adminWorkspace",
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
    AdminRowComponent,
    AdminDetCustomComponent,
    AdminDetPredefineComponent,
  },
  data() {
    return {
      tab: null,
      isLoading: false,
      workspacePredefine: {
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
      },
      workspaceCustom: {
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
    getDateLabel: getDateLabel,
    getWorkspaceCustom() {
      this.isLoading = true;
      this.$emit("dataLoading", true);
      // let checkbox = this.filter.filter ?? {};
      // let sort = this.filter.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        // search: "",
        pageNo: this.workspaceCustom.pagination.page,
        entriesPerPage: this.workspaceCustom.pagination.visible,
        searchKeyword: this.filter.searchKeyword,
        // workspaceType: checkbox.workspaceType ?? [],
        // yearPeriod: checkbox.period ?? [],
        // status: checkbox.status ?? [],
        // sortName: sort.sortName ?? "",
        // sortType: sort.sortType,
        // sortTime: sort.sortTime,
      };
      client
        .getListWorkspaceCustom({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let MOCK_DATA = false;
          let result = {};
          if (MOCK_DATA) result = adminMock.listWorkspaceCustom.responseData;
          else result = res.plainData.responseData ?? {};

          this.workspaceCustom.pagination.total = result.info?.totalPage ?? 0;
          let workspaceList = result.data ?? [];
          this.workspaceCustom.list = workspaceList.map((e) => {
            return {
              id: e.id,
              name: e.workspaceName,
              status: null,
              statusName: null,
              ...e,
            };
          });
        })
        .catch((err) => {
          if (err.response?.status === 403) {
            this.$root.toast.show({
              message: "tidak memiliki akses ke halaman ini",
              color: "warning",
              timeout: 30000,
            });
            this.$router.push({
              name: "home",
            });
          }
        })
        .finally(() => {
          this.isLoading = false;
          this.$emit("dataLoading", false);
        });
    },
    getWorkspacePredefine() {
      this.isLoading = true;
      this.$emit("dataLoading", true);
      let requestData = {
        username: this.$store.state.username,
      };

      client
        .getListWorkspacePredefine({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          let wpcPredefine = result ?? [];
          this.workspacePredefine.list = wpcPredefine.map((e) => {
            e.listApproval = [];
            return {
              id: e.id,
              name: e.workspaceTypeName,
              ...e,
            };
          });
        })
        .catch((err) => {
          if (err.response?.status === 403) {
            this.$root.toast.show({
              message: "tidak memiliki akses ke halaman ini",
              color: "warning",
              timeout: 30000,
            });
            this.$router.push({
              name: "home",
            });
          }
        })
        .finally(() => {
          this.isLoading = false;
          this.$emit("dataLoading", false);
        });
    },
    reloadPage() {
      if (this.tab == "custom") {
        this.workspaceCustom.pagination.page = 1;
        this.getWorkspaceCustom();
      } else if (this.tab == "predefine") {
        this.workspacePredefine.pagination.page = 1;
        this.getWorkspacePredefine();
      }
    },
  },
  created() {
    // this.getWorkspaceCustom();
    this.getWorkspacePredefine();
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
  /* letter-spacing: -0.7px; */
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
  background: white !important;
  color: #065695;
}
:deep(.v-pagination__next) {
  color: #065695;
}
:deep(.v-pagination__prev) {
  color: #065695;
}
</style>
