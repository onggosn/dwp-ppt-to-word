<template>
  <template v-if="isLoading">
    <v-row>
      <v-col cols="12" v-for="idx in pagination.visible" :key="idx">
        <free-style-shimmer
          :is-loading="true"
          width="100%"
          height="4.3rem"
          border-radius="10px"
        />
      </v-col>
    </v-row>
  </template>
  <div v-else-if="listData.length == 0">
    <img
      src="/images/no_workspace_available.png"
      style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
    />
    <div class="text-center text-18 fw-600 text-grayTheme-gradien font-italic">
      No Workspace Available....
    </div>
  </div>
  <div v-else>
    <div v-for="(item, idx) in listData" :key="idx">
      <dashboard-row-component :item="item" type="default">
        <dash-det-workspace-component
          tag="workspace"
          :item="item"
          @reloadPage="getData"
        />
      </dashboard-row-component>
    </div>
    <div class="text-center">
      <v-pagination
        v-model="pagination.page"
        rounded="1"
        elevation="2"
        size="small"
        :length="pagination.total"
        :total-visible="pagination.visible"
        @update:modelValue="getData()"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import client from "@/library/ApiClient";
import DashboardRowComponent from "@/components/dashboard/DashboardRowComponent.vue";
import DashDetWorkspaceComponent from "@/components/dashboard/DashDetWorkspaceComponent.vue";

export default {
  name: "dhsWorkspace",
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
    DashDetWorkspaceComponent,
  },
  data() {
    return {
      isLoading: false,
      listData: [],
      pagination: {
        visible: 10,
        page: 1,
        total: 0,
      },
    };
  },
  methods: {
    getData() {
      this.isLoading = true;
      this.$emit("dataLoading", true);

      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        pageNo: this.pagination.page,
        entriesPerPage: this.pagination.visible,
        workspaceType: checkbox.workspaceType ?? [],
        yearPeriod: checkbox.period ?? [],
        status: checkbox.status ?? [],
        sortName: sort.sortName ?? "",
        sortType: sort.sortType,
      };

      client
        .getListWorkspaceByUserName({
          store: this.$store,
          data: requestData,
        })
        .then((response) => {
          let result = response.plainData.responseData ?? {};
          this.pagination.total = result.info.totalPage ?? 0;

          let workspaceList = result.listWorkspace ?? [];
          this.listData = workspaceList.map((e) => {
            if (!e.listApproval) {
              e.listApproval = [];
            }
            let newApproval = [{ label: "Go To Workspace" }].concat(
              e.listApproval
            );

            e.listApproval = newApproval;
            return {
              id: e.id,
              name: e.workspaceName,
              status: e.status,
              statusName: e.statusName,
              ...e,
            };
          });
        })
        .catch(() => {
          this.listData = [];
          this.pagination.total = 0;
        })
        .finally(() => {
          this.isLoading = false;
          this.$emit("dataLoading", false);
        });
    },
  },
  watch: {
    filter() {
      this.pagination.page = 1;
      this.getData();
    },
  },
  created() {
    this.getData();
    this.$emit("subTabChange", null);
  },
};
</script>

<style scoped>
:deep(.v-icon) {
  color: #065695;
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
