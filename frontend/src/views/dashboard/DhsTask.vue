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
      src="/images/no_document_preview.png"
      style="display: block; margin: 0 auto; width: 450px; margin-top: 80px"
    />
    <div class="text-center text-18 fw-600 text-grayTheme-gradien font-italic">
      No Task Available....
    </div>
  </div>
  <div v-else>
    <div v-for="(item, idx) in listData" :key="idx">
      <dashboard-row-component :item="item" type="default">
        <template v-slot:datetime>
          <span v-if="item.statusId == 7" class="text-13">
            {{ !item.startDate ? "-" : item.startDate }}
          </span>
          <span v-else class="text-13">
            {{
              !item.startDate && !item.endDate
                ? "-"
                : getDateLabel(item.startDate, item.endDate, item.idTaskType)
            }}
          </span>
        </template>
        <dash-det-task-component :item="item" @reloadPage="getData" />
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
import { getDateLabel } from "@/helpers/date";
import DashboardRowComponent from "@/components/dashboard/DashboardRowComponent.vue";
import DashDetTaskComponent from "@/components/dashboard/DashDetTaskComponent.vue";

export default {
  name: "dhsTask",
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
    getDateLabel: getDateLabel,
    getData() {
      this.isLoading = true;
      this.$emit("dataLoading", true);

      let checkbox = this.filter.filter ?? {};
      let sort = this.filter.sort ?? {};
      let requestData = {
        username: this.$store.state.username,
        pageSize: this.pagination.visible,
        page: this.pagination.page,
        sortType: sort.sortType,
        sortName: sort.sortName ?? "",
        statusId: checkbox.status ?? [],
      };

      client
        .getDashboardTaskList({
          store: this.$store,
          data: requestData,
        })
        .then((response) => {
          let result = response.plainData.responseData ?? {};
          this.pagination.total = result.infoPage.totalPage ?? 0;

          let taskList = result.data ?? [];
          this.listData = taskList.map((e) => {
            if (!e.listApproval) {
              e.listApproval = [];
            }

            if (![1, 15].includes(e.statusId)) {
              // ketika not started go to task hilang
              let newApproval = [{ label: "Go To Task" }].concat(
                e.listApproval
              );
              e.listApproval = newApproval;
            }

            return {
              ...e,
              id: e.idTask,
              name: e.taskName,
              status: e.statusId,
              statusName: e.statusName,
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
