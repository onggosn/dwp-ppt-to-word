<template>
  <template v-if="isLoading">
    <v-row class="pt-6">
      <v-col cols="12" v-for="idx in 5" :key="idx">
        <free-style-shimmer
          :is-loading="true"
          width="100%"
          height="3rem"
          border-radius="10px"
        />
      </v-col>
    </v-row>
  </template>
  <template v-else>
    <div v-if="assignments.list.length === 0">
      <img
        src="/images/assignment/empty-assignment.png"
        style="display: block; margin: 0 auto; width: 400px; margin-top: 80px"
      />
      <div
        class="text-center text-18 fw-600 text-grayTheme-gradien font-italic mt-4"
      >
        No Assignment History Available...
      </div>
    </div>
    <div v-else class="pt-4">
      <v-card class="card-assignment-history ma-1">
        <v-card-title class="heading-label pt-4 pl-4">
          List Assignment
        </v-card-title>
        <v-card-text class="pt-6">
          <template v-for="(item, idx) in assignments.list" :key="idx">
            <dashboard-row-component :item="item" type="default">
              <template #datetime>
                <v-col cols="4">
                  <span class="text-13 font-italic fw-500 text-left">{{
                    item.taskName
                  }}</span>
                </v-col>
              </template>
              <template #label>
                <v-col cols="2">
                  <v-chip
                    rounded
                    :class="`${getStatusColor(item.statusName.toLowerCase())} `"
                  >
                    {{ item.statusName }}
                  </v-chip>
                </v-col>
              </template>
              <history-assignment-detail :id="item.idAssignment" />
            </dashboard-row-component>
          </template>
        </v-card-text>
      </v-card>
    </div>
  </template>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useStore } from "vuex";
import DashboardRowComponent from "@v2/components/dashboard/DashboardRowComponent.vue";
import HistoryAssignmentDetail from "@v2/components/history/HistoryAssignmentDetail.vue";

const store = useStore();
const isLoading = ref(false);
const assignments = reactive<any>({
  list: [],
});

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const getStatusColor = (statusName: string): string => {
  const statusColors: Record<string, string> = {
    done: "btn-status-green", // Completed
    "in progress": "btn-status-orange", // In Progress
    "need for approval": "btn-status-orange", // Pending
  };
  return statusColors[statusName] || "btn-status-default";
};

const fetchAssignments = async () => {
  isLoading.value = true;
  const requestData = {
    idWorkspace: props.id || "",
  };

  try {
    const response = await store.dispatch(
      "historyStore/getListAssignment",
      requestData
    );

    const result = response?.responseData ?? {};
    assignments.list = (result ?? []).map((e: any) => ({
      id: e.idAssignment,
      taskName: e.taskName,
      statusName: e.statusName,
      assignmentTitle: e.assignmentName || "Untitled Assignment",
      ...e,
    }));
  } catch (error) {
    assignments.list = [];
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchAssignments();
});
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

.btn-status-green {
  background-color: #e8f6eb;
  color: #2bc244;
  padding: 18px;
}
.btn-status-orange,
.btn-status-default {
  background-color: rgb(255, 238, 202);
  color: #906e2c;
  padding: 18px;
}
.btn-status-blue {
  background-color: rgb(233, 245, 255);
  color: rgb(34, 121, 189);
  padding: 18px;
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
  background-clip: text !important;
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

:deep(.v-pagination__next),
:deep(.v-pagination__prev) {
  color: #065695;
}
.history-assignment {
  opacity: 0.9;
}
.card-assignment-history {
  border-radius: 15px;
  box-shadow: 0px 4px 18px 0px #c0c0c040;
}
.heading-label {
  font-size: 18px !important;
  font-weight: 800;
  color: #4b4b4b;
}
:deep(.v-expansion-panel) {
  border-left: none !important;
  box-shadow: none !important;
}
:deep(.v-expansion-panel-title__icon) {
  border: 1px solid #065695 !important;
  border-radius: 10px !important;
  padding: 4px !important;
  background-color: white !important;
  color: #065695 !important;
}
:deep(.v-expansion-panel--active .v-expansion-panel-title__icon) {
  border: none !important;
}
:deep(.panel-custom .v-expansion-panel__shadow) {
  box-shadow: 0px 4px 18px 0px #c0c0c040 !important;
}
:deep(
    .panel-custom
      .v-expansion-panel-title.v-expansion-panel-title--active.panel-header
  ) {
  border-bottom: 1px solid #eeeeee !important;
  margin-bottom: 15px !important;
}
</style>
