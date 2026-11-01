<template>
  <div :style="route.path.includes('history/search') ? { margin: '50px' } : {}">
    <SearchBar @back="handleBack" />
  </div>
  <div class="pb-3 align-center mx-6">
    <div class="mt-5">
      <component :is="currentComponent" v-bind="currentComponentProps" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import SearchBar from "@/v2/components/search/SearchBar.vue";
import ListMeeting from "@/v2/components/admin/meeting/ListMeeting.vue";
import ListContent from "@/v2/components/admin/ContentAdmin.vue";
import ListRole from "@/v2/components/admin/RoleAdmin.vue";
import ListDashboardAssignment from "@v2/views/dashboard/DashboardAssignment.vue";
import ListDashboardDocument from "@v2/views/dashboard/DashboardDocument.vue";
// import ListAssignmentManagement from "@v2/views/assignment-management/AssignmentView.vue";
import ListWorkspaceManagement from "@v2/views/dashboard/DashboardWorkspace.vue";
import ListHistoryContent from "@/v2/views/HistoryView.vue";
import ListUserOperasional from "@/v2/components/admin/operasional/ListUserOperasional.vue";
import ListNotification from "@/v2/components/admin/notification/ListNotification.vue";

import { computed } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import type { RouteConfig } from "@/v2/Type";
import ListFAQ from "@/v2/components/admin/faq/ListFAQ.vue";

const SEARCH_MODES: RouteConfig[] = [
  // Admin Management
  {
    path: "admin-management/content",
    mode: "content-admin",
    component: ListContent,
    backRoute: "content-admin-predefine",
    backRoutePatterns: [
      {
        pattern: "admin-management/content/predefine",
        backRoute: "content-admin-predefine",
      },
      {
        pattern: "admin-management/content/ongoing",
        backRoute: "content-admin-ongoing",
      },
    ],
  },
  {
    path: "admin-management/meeting",
    mode: "meeting-admin",
    component: ListMeeting,
    backRoute: "meeting-admin-meeting",
    backRoutePatterns: [
      {
        pattern: "admin-management/meeting/meeting",
        backRoute: "meeting-admin-meeting",
      },
      {
        pattern: "admin-management/meeting/presentation-material",
        backRoute: "meeting-admin-presentation-material",
      },
    ],
  },
  {
    path: "admin-management/role",
    mode: "role-admin",
    component: ListRole,
    backRoute: "role-admin-role",
    backRoutePatterns: [
      {
        pattern: "admin-management/role/role",
        backRoute: "role-admin-role",
      },
      {
        pattern: "admin-management/role/user",
        backRoute: "role-admin-user",
      },
    ],
  },
  {
    path: "admin-management/faq",
    mode: "faq-admin",
    component: ListFAQ,
    backRoute: "faq-admin",
    backRoutePatterns: [
      {
        pattern: "admin-management/faq",
        backRoute: "faq-admin",
      },
    ],
  },
  {
    path: "operasional/user",
    mode: "operasional-admin-user",
    component: ListUserOperasional,
    backRoute: "operasional-admin-user",
  },
  {
    path: "admin-management/notification",
    mode: "notification-admin",
    component: ListNotification,
    backRoute: "notification-admin",
  },
  // My Dashboard
  {
    path: "mydashboard/assignment",
    mode: "dashboard.assignment.v2.penugasan",
    component: ListDashboardAssignment,
    backRoute: "dashboard.assignment.v2.penugasan",
    backRoutePatterns: [
      {
        pattern: "mydashboard/assignment/penugasan",
        backRoute: "dashboard.assignment.v2.penugasan",
      },
      {
        pattern: "mydashboard/assignment/arahan",
        backRoute: "dashboard.assignment.v2.arahan",
      },
    ],
  },
  {
    path: "mydashboard/document",
    mode: "dashboard.document.v2.materi",
    component: ListDashboardDocument,
    backRoute: "dashboard.document.v2.materi",
    backRoutePatterns: [
      {
        pattern: "mydashboard/document/materi",
        backRoute: "dashboard.document.v2.materi",
      },
      {
        pattern: "mydashboard/document/hasil",
        backRoute: "dashboard.document.v2.hasil",
      },
    ],
  },
  {
    path: "/mydashboard/workspace/search",
    mode: "dashboard.workspace.v2",
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

const store = useStore();
const router = useRouter();
const route = useRoute();

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

function getBackRoute(path: string): string {
  for (const config of SEARCH_MODES) {
    if (config.backRoutePatterns) {
      for (const { pattern, backRoute } of config.backRoutePatterns) {
        if (path.includes(pattern)) {
          return backRoute;
        }
      }
    }
  }

  const config = getCurrentConfig();
  return config?.backRoute || "";
}

function handleBack(): void {
  const backRoute = getBackRoute(route.path);

  if (backRoute) {
    router.push({ name: backRoute });
  }
  store.commit("globalStore/setStatusSearch", false);
}
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
