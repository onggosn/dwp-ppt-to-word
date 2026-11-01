<template>
  <template v-if="isLoading">
    <v-row>
      <v-col cols="12" v-for="idx in workspace.pagination.visible" :key="idx">
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
      <v-tab class="tab-header" value="workspace"> WORKSPACE </v-tab>
      <v-tab class="tab-header" value="task"> TASK </v-tab>
    </v-tabs>
    <v-window v-model="tab" class="mt-3">
      <v-window-item value="workspace">
        <div v-if="workspace.list.length == 0">
          <img
            src="/images/no_workspace_available.png"
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
            No workspace available....
          </div>
        </div>
        <div v-else>
          <div v-for="(item, idx) in workspace.list" :key="idx">
            <!-- <pre>{{ item }}</pre> -->
            <dashboard-row-component :item="item" type="type-1">
              <template v-slot:label>
                <v-btn rounded class="ml-5 label-status btn-warning">
                  {{ item.headerMessage }}
                </v-btn>
              </template>

              <dash-det-workspace-component
                tag="pengajuan"
                :item="item"
                @reloadPage="reloadPage"
              />
            </dashboard-row-component>
          </div>
          <div class="text-center">
            <v-pagination
              rounded="1"
              elevation="2"
              size="small"
              v-model="workspace.pagination.page"
              :length="workspace.pagination.total"
              :total-visible="workspace.pagination.visible"
              @update:modelValue="getWorkspace()"
            ></v-pagination>
          </div>
        </div>
      </v-window-item>
      <v-window-item value="task">
        <div v-if="task.list.length == 0">
          <img
            src="/images/no_document_preview.png"
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
            No Task Available....
          </div>
        </div>

        <div v-else>
          <div v-for="(item, idx) in task.list" :key="idx">
            <dashboard-row-component :item="item" type="type-1">
              <template v-slot:datetime>
                <v-col style="font-size: 0.8rem">
                  <span v-if="item.statusId == 7">
                    {{ !item.startDate ? "-" : item.startDate }}
                  </span>
                  <span v-else>
                    {{
                      !item.startDate && !item.endDate
                        ? "-"
                        : getDateLabel(
                            item.startDate,
                            item.endDate,
                            item.idTaskType
                          )
                    }}
                  </span>
                </v-col>
              </template>
              <template v-slot:label>
                <v-btn
                  rounded
                  class="ml-5 label-status btn-warning btn-status-style"
                >
                  {{ item.headerMessage }}
                </v-btn>
              </template>
              <dash-det-task-component :item="item" @reloadPage="reloadPage" />
            </dashboard-row-component>
          </div>
          <div class="text-center">
            <v-pagination
              rounded="1"
              elevation="2"
              size="small"
              v-model="task.pagination.page"
              :length="task.pagination.total"
              :total-visible="task.pagination.visible"
              @update:modelValue="getTask()"
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
import DashboardRowComponent from "@/components/dashboard/DashboardRowComponent.vue";
import DashDetWorkspaceComponent from "@/components/dashboard/DashDetWorkspaceComponent.vue";
import DashDetTaskComponent from "@/components/dashboard/DashDetTaskComponent.vue";

export default {
  name: "dhsPengajuan",
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
    DashDetTaskComponent,
    DashDetWorkspaceComponent,
  },
  data() {
    return {
      tab: null,
      isLoading: false,
      workspace: {
        list: [],
        pagination: {
          page: 1,
          total: 0,
          visible: 10,
        },
      },
      task: {
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
    getWorkspace() {
      this.isLoading = true;
      this.$emit("dataLoading", true);
      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        search: "",
        pageNo: this.workspace.pagination.page,
        entriesPerPage: this.workspace.pagination.visible,
        workspaceType: checkbox.workspaceType ?? [],
        yearPeriod: checkbox.period ?? [],
        status: checkbox.status ?? [],
        sortName: sort.sortName ?? "",
        sortType: sort.sortType,
        sortTime: sort.sortTime,
      };

      client
        .getListDashboardWorkspaceSubmission({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.workspace.pagination.total = result.info?.totalPage ?? 0;

          let workspaceList = result.listWorkspace ?? [];
          this.workspace.list = workspaceList.map((e) => {
            e.listApproval = [];
            return {
              id: e.id,
              name: e.workspaceName,
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
    getTask() {
      this.isLoading = true;
      this.$emit("dataLoading", true);
      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};

      let requestData = {
        username: this.$store.state.username,
        search: "",
        page: this.workspace.pagination.page,
        pageSize: this.workspace.pagination.visible,
        taskType: checkbox.taskType ?? [],
        statusId: checkbox.status ?? [],
        satker: checkbox.satker ?? [],
        statusName: "",
        sortName: sort.sortName ?? "",
        sortType: sort.sortType,
        sortTime: sort.sortTime,
      };

      client
        .getListDashboardTaskSubmission({
          store: this.$store,
          data: requestData,
        })
        .then((res) => {
          let result = res.plainData.responseData ?? {};
          this.task.pagination.total = result.infoPage?.totalPage ?? 0;

          let taskList = result.data ?? [];
          this.task.list = taskList.map((e) => {
            e.listApproval = [];
            return {
              id: e.idTask,
              name: e.taskName,
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
      if (this.tab == "workspace") {
        this.workspace.pagination.page = 1;
        this.getWorkspace();
      } else if (this.tab == "task") {
        this.task.pagination.page = 1;
        this.getTask();
      }
    },
  },
  created() {
    this.getWorkspace();
    this.getTask();
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
  color: #065695;
}
:deep(.v-pagination__next) {
  color: #065695;
}
:deep(.v-pagination__prev) {
  color: #065695;
}
</style>
