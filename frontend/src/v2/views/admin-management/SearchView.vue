<template>
  <div :style="route.path.includes('history/search') ? { margin: '50px' } : {}">
    <SearchTop @back="handleBack" />
  </div>
  <div class="pb-3 align-center mx-6">
    <div class="mt-5">
      <component :is="currentComponent" v-bind="currentComponentProps" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import SearchTop from "@/v2/components/admin/SearchTop.vue";
import ListMeeting from "@/v2/components/admin/meeting/ListMeeting.vue";
import ListContent from "@/v2/components/admin/ContentAdmin.vue";
import ListRole from "@/v2/components/admin/role/ListRole.vue";
import ListDashboardAssignment from "@v2/views/dashboard/DashboardAssignment.vue";
import ListDashboardDocument from "@v2/views/dashboard/DashboardDocument.vue";
import ListAssignmentManagement from "@v2/views/assignment-management/AssignmentView.vue";
import ListWorkspaceManagement from "@v2/views/dashboard/DashboardWorkspace.vue";
import ListHistoryContent from "@/v2/views/HistoryView.vue";

import { watch, onMounted, ref, computed } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import type { RouteConfig } from "@/v2/Type";

const SEARCH_MODES: RouteConfig[] = [
  // Admin Management
  {
    path: "admin-management/content",
    mode: "content-admin",
    component: ListContent,
    backRoute: "content-admin-predefine",
  },
  {
    path: "admin-management/meeting",
    mode: "meeting-admin",
    component: ListMeeting,
    backRoute: "meeting-admin-meeting",
  },
  {
    path: "admin-management/meeting/presentation-material/search",
    mode: "meeting-admin-presentation-material-search",
    component: ListMeeting,
    backRoute: "meeting-admin-meeting",
  },
  {
    path: "admin-management/role",
    mode: "role-admin",
    component: ListRole,
    backRoute: "role-admin",
  },
  // My Dashboard
  {
    path: "mydashboard/assignment/search",
    mode: "penugasan-mydashboard",
    component: ListDashboardAssignment,
    backRoute: "dashboard.assignment.v2.penugasan",
    props: { searchMode: true },
  },
  {
    path: "mydashboard/arahan/search",
    mode: "arahan-mydashboard",
    component: ListDashboardAssignment,
    backRoute: "dashboard.assignment.v2.arahan",
    props: { searchMode: true },
  },
  {
    path: "mydashboard/documentmateri/search",
    mode: "materi-mydashboard",
    component: ListDashboardDocument,
    backRoute: "dashboard.document.v2.materi",
    props: { searchMode: true },
  },
  {
    path: "mydashboard/documenthasil/search",
    mode: "hasil-mydashboard",
    component: ListDashboardDocument,
    backRoute: "dashboard.document.v2.hasil",
    props: { searchMode: true },
  },
  // Assignment Management
  {
    path: "/assignmentmanagement-new/assignment/search",
    mode: "penugasan-assignment",
    component: ListAssignmentManagement,
    backRoute: "v2.assignmentmanagement-new",
    props: { searchMode: true },
  },
  {
    path: "/assignmentmanagement-new/arahan/search",
    mode: "arahan-assignment",
    component: ListAssignmentManagement,
    backRoute: "v2.assignmentmanagement-new",
    props: { searchMode: true },
  },
  {
    path: "/mydashboard/workspace/search",
    mode: "workspace-mydashboard",
    component: ListWorkspaceManagement,
    backRoute: "dashboard.workspace.v2",
  },
  // history search
  {
    path: "/history/search",
    mode: "history-search",
    component: ListHistoryContent,
    backRoute: "v2.history",
    props: { searchMode: true },
  },
];

const CONTENT_ADMIN_BACK_ROUTES = {
  "admin-management/content/predefine": "content-admin-predefine",
  "admin-management/content/ongoing": "content-admin-ongoing",
};

const MEETING_ADMIN_BACK_ROUTES = {
  "admin-management/meeting/meeting": "meeting-admin-meeting",
  "admin-management/meeting/presentation-material":
    "meeting-admin-presentation-material",
};

const store = useStore();
const router = useRouter();
const route = useRoute();
const listMode = ref<string>("");

const currentComponent = computed(() => {
  const config = getCurrentConfig();
  return config?.component || null;
});

const currentComponentProps = computed(() => {
  const config = getCurrentConfig();
  return config?.props || {};
});

function getCurrentConfig(): RouteConfig | undefined {
  return SEARCH_MODES.find((config) => route.path.includes(config.path));
}

function validateRoute(path: string): string {
  const config = SEARCH_MODES.find((config) => path.includes(config.path));
  return config?.mode || "";
}

function getBackRoute(path: string): string {
  const meetingAdminRoute = Object.entries(MEETING_ADMIN_BACK_ROUTES).find(
    ([pattern]) => path.includes(pattern)
  );

  const contentAdminRoute = Object.entries(CONTENT_ADMIN_BACK_ROUTES).find(
    ([pattern]) => path.includes(pattern)
  );

  if (meetingAdminRoute) {
    return meetingAdminRoute[1];
  }

  if (contentAdminRoute) {
    return contentAdminRoute[1];
  }

  const config = getCurrentConfig();
  return config?.backRoute || "";
}

function handleBack(): void {
  const backRoute = getBackRoute(route.path);

  if (backRoute) {
    router.push({ name: backRoute });
  }
  store.commit("adminStore/setStatusSearchMode", false);
}

onMounted(() => {
  listMode.value = validateRoute(route.path);
});

watch(
  () => route.path,
  (newPath) => {
    listMode.value = validateRoute(newPath);
  }
);
</script>

<style scoped>
.v-input__control {
  border-radius: 16px;
  height: 10px;
}
.item-card {
  padding: 23px 30px;
  background-color: rgba(255, 255, 255, 1);

  /* Shadow 1 */
  border-radius: 16px;
  box-shadow: 0px 3px 10px 0px rgba(0, 0, 0, 0.12);
}
:deep(.tab-header.v-slide-group-item--active) {
  background-color: #f44336 !important;
  color: #ffff !important;
  border: none !important;
  border-radius: 12px;
  background-clip: border-box;
  -webkit-background-clip: border-box !important;
}
.tab-header {
  color: #065695;
  font-weight: 600;
  max-height: 40px;
}
.btn-add {
  display: flex;
  height: 36px;
  color: #ffff;
  padding: 8px 14px;
  align-items: flex-end;
  justify-content: flex-end;
  border-radius: 8px;
  background: var(
    --Gradient-Blue,
    linear-gradient(180deg, #065695 0%, #267dc2 100%)
  );
}
</style>
