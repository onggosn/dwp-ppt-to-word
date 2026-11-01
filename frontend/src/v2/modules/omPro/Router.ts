import { RouteRecordRaw } from "vue-router";

export const omWorkspaceManagementChildren: RouteRecordRaw[] = [
  {
    path: "rdgm",
    name: "om.workspace-management-rdgm",
    component: () =>
      import("@omPro/views/workspaceManagement/WorkspaceRDGMView.vue"),
  },
];

export const omProRouter: Array<RouteRecordRaw> = [
  //untuk route baru atau turunan dari v2/Route tambahkan disini
  {
    path: "/app/v2/workspace-management/om/:typeRDG/:idEvent",
    name: "om.workspace-management-rdgm-detail",
    component: () =>
      import("@omPro/views/workspaceManagement/WorkspaceRDGMDetailView.vue"),
  },
  {
    path: "/app/v2/workspace-management/om/:typeRDG/:idEvent/doc-view",
    name: "om.rdg-collaboration-all",
    component: () =>
      import("@omPro/views/workspaceManagement/ViewAllDocument.vue"),
  },
  {
    path: "/app/v2/workspace-management/om/:typeRDG/:idEvent/doc/:idDoc",
    name: "om.rdg-collaboration",
    component: () =>
      import("@omPro/views/workspaceManagement/CollaborationView.vue"),
  },
  {
    path: "/app/v2/workspace-management/om/rdgm/search-result",
    name: "om.rdgm-search-result",
    component: () =>
      import("@omPro/views/workspaceManagement/WorkspaceSearchResultRDGM.vue"),
  },
];
