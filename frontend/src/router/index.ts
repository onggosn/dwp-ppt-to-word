import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import store from "../store";
import routerV2 from "@v2/Router";
import { omProRouter } from "@/v2/modules/omPro/Router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "sso",
    redirect: "app/v2/home",
    meta: {
      requiresAuth: true,
    },
  },
  // {
  //   path: "/login",
  //   component: () => import("@/views/LoginView.vue"),
  //   meta: {
  //     guestOnly: true,
  //   },
  // },
  {
    path: "/mobile-preview",
    name: "mobile-preview",
    component: () => import("@/v2/views/MobilePreview.vue"),
    meta: {
      guestOnly: true,
    },
  },
  {
    path: "/app",
    redirect: "/app/v1/home",
    meta: {
      requiresAuth: true,
      showMobileMenu: false,
      hasMobileView: false,
    },
    name: "app",
    children: [
      {
        path: "v1",
        redirect: "app/v1/home",
        name: "app.v1",
        component: () => import("@/views/AppLayout.vue"),
        children: [
          {
            path: "home",
            name: "home",
            component: () => import("@/views/HomeView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "dashboard",
            name: "dashboard",
            redirect: "/app/v1/dashboard/pengajuan",
            component: () => import("@/views/DashboardView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
            children: [
              {
                path: "pengajuan",
                name: "dashboard.pengajuan",
                component: () => import("@/views/dashboard/DhsPengajuan.vue"),
              },
              {
                path: "persetujuan",
                name: "dashboard.persetujuan",
                component: () => import("@/views/dashboard/DhsPersetujuan.vue"),
                children: [
                  {
                    path: "workspace",
                    name: "dashboard.persetujuan.workspace",
                    component: () =>
                      import("@/views/dashboard/DhsPersetujuan.vue"),
                    children: [
                      {
                        path: ":id",
                        name: "dashboard.persetujuan.workspace.id",
                        component: () =>
                          import("@/views/dashboard/DhsPersetujuan.vue"),
                      },
                    ],
                  },
                  {
                    path: "task",
                    name: "dashboard.persetujuan.task",
                    component: () =>
                      import("@/views/dashboard/DhsPersetujuan.vue"),
                    children: [
                      {
                        path: ":id",
                        name: "dashboard.persetujuan.task.id",
                        component: () =>
                          import("@/views/dashboard/DhsPersetujuan.vue"),
                      },
                    ],
                  },
                ],
              },
              {
                path: "workspace",
                name: "dashboard.workspace",
                component: () => import("@/views/dashboard/DhsWorkspace.vue"),
              },
              {
                path: "task",
                name: "dashboard.task",
                component: () => import("@/views/dashboard/DhsTask.vue"),
              },
              {
                path: "document",
                name: "dashboard.document",
                component: () => import("@/views/dashboard/DhsDocument.vue"),
              },
              {
                path: "assignment",
                name: "dashboard.assignment",
                component: () => import("@/views/dashboard/DhsAssignment.vue"),
                children: [
                  {
                    path: "penugasan",
                    name: "dashboard.assignment.penugasan",
                    component: () =>
                      import("@/views/dashboard/DhsAssignment.vue"),
                    children: [
                      {
                        path: ":id",
                        name: "dashboard.assignment.penugasan.id",
                        component: () =>
                          import("@/views/dashboard/DhsAssignment.vue"),
                      },
                    ],
                  },
                  {
                    path: "arahan",
                    name: "dashboard.assignment.arahan",
                    component: () =>
                      import("@/views/dashboard/DhsAssignment.vue"),
                    children: [
                      {
                        path: ":id",
                        name: "dashboard.assignment.arahan.id",
                        component: () =>
                          import("@/views/dashboard/DhsAssignment.vue"),
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            path: "workspace-management",
            name: "workspace-management",
            component: () => import("@/views/WorkspaceView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
            children: [
              {
                path: "workspace-detail/:workspaceId?",
                name: "workspace-detail",
                component: () => import("@/views/WorkspaceDetailView.vue"),
                meta: {
                  showMobileMenu: false,
                  hasMobileView: false,
                },
                children: [
                  {
                    path: "task/:taskId?",
                    name: "task-detail",
                    component: () => import("@/views/DetailTaskView.vue"),
                    children: [
                      {
                        path: "description",
                        name: "task-description",
                        component: () =>
                          import("@/views/TaskDescriptionView.vue"),
                      },
                      {
                        path: "document",
                        name: "task-document",
                        component: () => import("@/views/TaskDocumentView.vue"),
                        children: [
                          {
                            path: "support/:pageId?",
                            name: "support",
                            component: () =>
                              import("@/views/ListDocumentSupportView.vue"),
                            children: [
                              {
                                path: "preview/:documentId?",
                                name: "preview-document-support",
                                component: () =>
                                  import(
                                    "@/views/ApprovalDocumentSupportView.vue"
                                  ),
                              },
                            ],
                          },
                          {
                            path: "main/:pageId?",
                            name: "main",
                            component: () =>
                              import("@/views/ListDocumentView.vue"),
                            children: [
                              {
                                path: "preview/:documentId?",
                                name: "preview-document",
                                component: () =>
                                  import("@/views/ApprovalDocumentView.vue"),
                              },
                            ],
                          },
                        ],
                      },
                      {
                        path: "meeting",
                        name: "task-meeting",
                        component: () => import("@/views/TaskMeetingView.vue"),
                      },
                      {
                        path: "discussion",
                        name: "task-discussion",
                        component: () =>
                          import("@/views/TaskDiscussionView.vue"),
                      },
                    ],
                  },
                ],
              },
            ],
          },
          {
            path: "meeting-management",
            name: "meeting-management",
            component: () => import("@/views/MeetingView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "assignment-management",
            name: "assignment-management",
            component: () => import("@/views/AssignmentView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "document-management",
            name: "document-management",
            component: () => import("@/views/DocumentManagementView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "chartpack/:idChartpack/:searchKeyword",
            name: "chartpack",
            component: () => import("@/views/ChartpackView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "chartpack",
            name: "chartpack",
            component: () => import("@/views/ChartpackView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "profile",
            name: "profile",
            component: () => import("@/views/ProfileView.vue"),
            meta: {
              showMobileMenu: false,
            },
          },
          {
            path: "search-meeting/:idLevel/:searchKeyword",
            name: "search-meeting",
            component: () => import("@/views/SearchMeetingView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "search-chartpack/:searchKeyword",
            name: "search-chartpack",
            component: () => import("@/views/SearchChartpackView.vue"),
          },
          {
            path: "suptechbisma",
            name: "suptechbisma",
            component: () => import("@/views/SuptechView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
            children: [
              {
                path: "sektor/:idSektor",
                name: "suptechbisma.sektor",
                component: () =>
                  import("@/components/suptech/SuptechPbiComponent.vue"),
                meta: {
                  showMobileMenu: true,
                },
              },
            ],
          },
          {
            path: "executive-summary",
            name: "executive-summary",
            component: () =>
              import("@/views/suptech/SuptechExecutiveSummaryView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "liquidity",
            name: "liquidity",
            component: () => import("@/views/suptech/SuptechLiquidityView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "credit",
            name: "credit",
            component: () => import("@/views/suptech/SuptechCreditView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "mydashboard",
            name: "mydashboard",
            component: () => import("@/views/SuptechView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
          },
          {
            path: "adm",
            name: "adm",
            redirect: "/app/v1/adm/workspace",
            component: () => import("@/views/AdministratorView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
            children: [
              {
                path: "workspace",
                name: "administrator.workspace",
                component: () =>
                  import("@/views/administrator/adminWorkspace.vue"),
                redirect: "/app/v1/adm/workspace/predefine",
                children: [
                  {
                    path: "predefine",
                    name: "administrator.workspace.predefine",
                    component: () =>
                      import("@/views/administrator/adminWorkspace.vue"),
                  },
                  {
                    path: "custom",
                    name: "administrator.workspace.custom",
                    component: () =>
                      import("@/views/administrator/adminWorkspace.vue"),
                  },
                ],
              },
              {
                path: "role",
                name: "administrator.role",
                component: () => import("@/views/administrator/adminRole.vue"),
              },
              {
                path: "template",
                name: "administrator.template",
                component: () =>
                  import("@/views/administrator/adminTemplate.vue"),
              },
            ],
          },
          {
            path: "poltech",
            name: "poltech",
            component: () => import("@/views/PoltechView.vue"),
            meta: {
              showMobileMenu: false,
              hasMobileView: false,
            },
            children: [
              {
                path: "sektor/:idSektor",
                name: "poltech.sektor",
                component: () =>
                  import("@/components/poltech/PoltechMenuComponent.vue"),
                children: [
                  {
                    path: "area/:idArea",
                    name: "poltech.sektor.area",
                    component: () =>
                      import("@/components/poltech/PoltechPbiComponent.vue"),
                  },
                ],
              },
            ],
          },
        ],
      },
      {
        path: "v2",
        redirect: "app/v2/home",
        name: "app.v2",
        component: () => import("@/v2/views/AppLayoutV2.vue"),
        meta: {
          hasMobileView: false,
          showMobileMenu: false,
        },
        children: [...routerV2, ...omProRouter],
      },
    ],
  },
  {
    path: "/app/v1/assignment/:id",
    name: "assignment-detail",
    meta: {
      requiresAuth: true,
    },
    component: () => import("@/views/assignment/AssignmentDetail.vue"),
  },
  {
    path: "/app/v2/assignment/:id",
    name: "assignment-detail-new",
    meta: {
      requiresAuth: true,
    },
    component: () =>
      import("@v2/views/assignment-management/AssignmentDetail.vue"),
  },
  {
    path: "/about",
    name: "about",
    component: () => import("../views/AboutView.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    component: () => import("@/components/errPage/PageNotFound.vue"),
  },
  {
    path: "/scripts",
    component: () => import("@/components/errPage/PageNotFound.vue"),
  },
  {
    path: "/privacy-policy-data",
    name: "privacy.policy.data",
    component: () => import("@/views/PrivacyPolicyData.vue"),
    meta: {
      guestOnly: true,
    },
  },
  {
    path: "/app/v2/workspace-management/:typeRDG/:idEvent/preview/:idDoc",
    name: "preview.doc",
    component: () =>
      import("@/v2/components/collaboration/preview/PreviewEditorDecouple.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/app/v2/workspace-management/:typeRDG/:idEvent/version/:idDoc/:versionId",
    name: "version.doc",
    component: () =>
      import("@/v2/components/collaboration/preview/VersionEditor.vue"),
    meta: {
      requiresAuth: true,
    },
  },
];

if (process.env.VUE_APP_MODE === "development") {
  routes.push({
    path: "/ui-documentation",
    component: () => import("@/v2/views/AppLayoutPublicV2.vue"),
    children: [
      {
        path: "",
        name: "public.v2.ui-documentation",
        component: () =>
          import("@/v2/views/ui-documentation/UIDocumentationView.vue"),
      },
    ],
  });
}

/* eslint-disable */
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, top: 16 };
    }
  },
});

router.beforeEach((to, from, next) => {
  if (to.meta.restrictedUsername) {
    const currentUsername = store.state.username.toLowerCase();
    const allowedUsername = to.meta.restrictedUsername;
    if (currentUsername !== allowedUsername) {
      return next({
        name: "v2.home",
      });
    }
  }
  
  if (to.matched.some((route) => route.meta.requiresAuth)) {
      next();
  } else if (
    to.matched.some((route) => route.meta.guestOnly && store.getters.isLoggedIn)
  ) {
    return next({ name: "home" });
  } else {
    if (localStorage.isLoggedIn) {
      if (to.fullPath == "") next({ name: "home" });
      else next();
    }
    next();
  }
});

// Log navigasi di APM
// router.afterEach((to, from) => {
//   apm.setCustomContext({ from, to });
// });

export default router;
